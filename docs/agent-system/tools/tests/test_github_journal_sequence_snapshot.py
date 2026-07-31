import json
import sys
import unittest
from pathlib import Path
from unittest import mock
from urllib.error import URLError

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


def pull(number, body=None):
    return {"number": number, "state": "open", "merged_at": None, "head": {"sha": f"sha-{number}"}, "body": body}


class GitHubJournalSequenceSnapshotTests(unittest.TestCase):
    def test_claim_on_second_page_is_included(self):
        claim = '<!-- journal-sequence-reservation: {"metadata_version":1,"sequence":"0017","task_id":"METH-OPEN-01","reservation_id":"r-0017"} -->'
        responses = [
            Response([pull(1)], '<https://api.github.test/page-2>; rel="next"'),
            Response([pull(2, claim)]),
        ]
        with mock.patch.object(snapshot, "urlopen", side_effect=responses) as opener:
            result = snapshot.fetch_snapshot("owner/repository")
        self.assertEqual("available", result["availability"])
        self.assertEqual(2, len(result["pull_requests"]))
        self.assertEqual("0017", result["pull_requests"][1]["reservation_claims"][0]["sequence"])
        self.assertEqual(2, opener.call_count)

    def test_second_page_error_makes_snapshot_unavailable(self):
        responses = [
            Response([pull(1)], '<https://api.github.test/page-2>; rel="next"'),
            URLError("offline"),
        ]
        with mock.patch.object(snapshot, "urlopen", side_effect=responses):
            result = snapshot.fetch_snapshot("owner/repository")
        self.assertEqual("unavailable", result["availability"])
        self.assertEqual("provider_api_unavailable", result["reason"])
        self.assertEqual([], result["pull_requests"])

    def test_invalid_page_payload_fails_closed(self):
        with mock.patch.object(snapshot, "urlopen", return_value=Response({"unexpected": "object"})):
            result = snapshot.fetch_snapshot("owner/repository")
        self.assertEqual("unavailable", result["availability"])
        self.assertEqual("provider_payload_invalid", result["reason"])


if __name__ == "__main__":
    unittest.main()
