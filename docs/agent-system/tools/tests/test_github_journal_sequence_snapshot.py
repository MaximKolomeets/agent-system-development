import json
import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock
from urllib.error import HTTPError, URLError

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import github_journal_sequence_snapshot as snapshot


class Response:
    def __init__(self, payload, link=""):
        self.payload = json.dumps(payload).encode("utf-8")
        self.headers = {"Link": link}

    def read(self):
        return self.payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        return False


def pull(number, body=None, state="open", merged_at=None):
    return {"number": number, "state": state, "merged_at": merged_at, "head": {"sha": f"sha-{number}"}, "body": body}


class GitHubJournalSequenceSnapshotTests(unittest.TestCase):
    def credential_environment(self):
        return mock.patch.dict(snapshot.os.environ, {"GITHUB_TOKEN": "test-token"}, clear=True)

    def test_claim_on_second_page_is_included(self):
        claim = '<!-- journal-sequence-reservation: {"metadata_version":1,"sequence":"0017","task_id":"METH-OPEN-01","reservation_id":"r-0017"} -->'
        responses = [
            Response([pull(1)], '<https://api.github.test/page-2>; rel="next"'),
            Response([pull(2, claim)]),
        ]
        with self.credential_environment(), mock.patch.object(snapshot, "urlopen", side_effect=responses) as opener:
            result = snapshot.fetch_snapshot("owner/repository")
        self.assertEqual("available", result["availability"])
        self.assertEqual(2, len(result["pull_requests"]))
        self.assertEqual("0017", result["pull_requests"][1]["reservation_claims"][0]["sequence"])
        self.assertEqual(2, opener.call_count)

    def test_mixed_open_closed_and_merged_rows_are_available(self):
        claim = '<!-- journal-sequence-reservation: {"metadata_version":1,"sequence":"0018","task_id":"METH-MERGED-01","reservation_id":"r-0018"} -->'
        page = [
            pull(1, state="open"),
            pull(2, state="closed"),
            pull(3, claim, state="closed", merged_at="2026-08-01T10:00:00Z"),
        ]
        with self.credential_environment(), mock.patch.object(snapshot, "urlopen", return_value=Response(page)):
            result = snapshot.fetch_snapshot("owner/repository")
        self.assertEqual("available", result["availability"])
        self.assertEqual(["open", "closed", "merged"], [item["state"] for item in result["pull_requests"]])
        self.assertEqual("0018", result["pull_requests"][2]["reservation_claims"][0]["sequence"])

    def test_normalize_row_preserves_each_schema_state(self):
        cases = [
            (pull(1, state="open"), "open"),
            (pull(2, state="closed"), "closed"),
            (pull(3, state="closed", merged_at="2026-08-01T10:00:00Z"), "merged"),
        ]
        for row, expected_state in cases:
            with self.subTest(state=expected_state):
                normalized = snapshot.normalize_row(row)
                self.assertIsNotNone(normalized)
                self.assertEqual(expected_state, normalized["state"])

    def test_second_page_error_makes_snapshot_unavailable(self):
        responses = [
            Response([pull(1)], '<https://api.github.test/page-2>; rel="next"'),
            URLError("offline"),
        ]
        with self.credential_environment(), mock.patch.object(snapshot, "urlopen", side_effect=responses):
            result = snapshot.fetch_snapshot("owner/repository")
        self.assertEqual("unavailable", result["availability"])
        self.assertEqual("provider_transport_unavailable", result["reason"])
        self.assertEqual([], result["pull_requests"])

    def test_invalid_page_payload_fails_closed(self):
        with self.credential_environment(), mock.patch.object(snapshot, "urlopen", return_value=Response({"unexpected": "object"})):
            result = snapshot.fetch_snapshot("owner/repository")
        self.assertEqual("unavailable", result["availability"])
        self.assertEqual("provider_payload_invalid", result["reason"])

    def test_missing_credential_does_not_call_provider(self):
        with mock.patch.dict(snapshot.os.environ, {}, clear=True), mock.patch.object(snapshot, "urlopen") as opener:
            result = snapshot.fetch_snapshot("owner/repository")
        self.assertEqual("unavailable", result["availability"])
        self.assertEqual("provider_credential_unavailable", result["reason"])
        opener.assert_not_called()

    def test_credential_is_only_in_authorization_header(self):
        captured = []

        def capture(request, timeout):
            captured.append(request)
            return Response([])

        with self.credential_environment(), mock.patch.object(snapshot, "urlopen", side_effect=capture):
            result = snapshot.fetch_snapshot("owner/repository")
        self.assertEqual("available", result["availability"])
        self.assertEqual("B" + "earer test-token", captured[0].get_header("Authorization"))
        self.assertNotIn("test-token", json.dumps(result))

    def test_http_failures_have_safe_normalized_reasons(self):
        cases = {
            401: "provider_authentication_failed",
            403: "provider_access_denied_or_rate_limited",
            429: "provider_rate_limited",
        }
        for status, expected_reason in cases.items():
            with self.subTest(status=status), self.credential_environment(), mock.patch.object(
                snapshot,
                "urlopen",
                side_effect=HTTPError("https://api.github.test", status, "provider detail", {}, None),
            ):
                result = snapshot.fetch_snapshot("owner/repository")
            self.assertEqual("unavailable", result["availability"])
            self.assertEqual(expected_reason, result["reason"])
            self.assertNotIn("provider detail", json.dumps(result))

    def test_workflow_binds_minimal_permissions_and_credential(self):
        workflow = Path(__file__).resolve().parents[4] / ".github" / "workflows" / "methodology-checks.yml"
        content = workflow.read_text(encoding="utf-8")
        self.assertIn("permissions:\n  contents: read\n  pull-requests: read", content)
        step = content.split("- name: Journal sequence reservation", maxsplit=1)[1]
        self.assertIn("GITHUB_TOKEN: ${{ github.token }}", step)
        self.assertIn('--base "${{ steps.base.outputs.base }}"', step)

    def test_diagnostic_output_contains_only_safe_availability_and_reason(self):
        unavailable_snapshot = snapshot.unavailable("provider_transport_unavailable")
        self.assertEqual(
            "provider_snapshot availability=unavailable reason=provider_transport_unavailable",
            snapshot.diagnostic_line(unavailable_snapshot),
        )
        unsafe_snapshot = {
            "availability": "unavailable",
            "reason": "provider detail test-token",
            "headers": {"Authorization": "hidden"},
            "body": "provider response body",
        }
        output = snapshot.diagnostic_line(unsafe_snapshot)
        self.assertEqual("provider_snapshot availability=unavailable reason=none", output)
        self.assertNotIn("test-token", output)
        self.assertNotIn("Authorization", output)
        self.assertNotIn("provider response body", output)

    def test_main_writes_snapshot_and_prints_only_safe_diagnostic(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "snapshot.json"
            stream = io.StringIO()
            with mock.patch.object(snapshot, "fetch_snapshot", return_value=snapshot.unavailable("provider_payload_invalid")), mock.patch(
                "sys.stdout", stream
            ):
                code = snapshot.main(["--repository", "owner/repository", "--output", str(output_path)])
        self.assertEqual(0, code)
        self.assertEqual("provider_snapshot availability=unavailable reason=provider_payload_invalid\n", stream.getvalue())
        self.assertNotIn("test-token", stream.getvalue())


if __name__ == "__main__":
    unittest.main()
