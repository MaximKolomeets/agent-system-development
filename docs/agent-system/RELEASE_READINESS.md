# RELEASE_READINESS

Дата проверки: 2026-07-02

Назначение: release-prep snapshot для `v1.5.1` после merge PR #298-#302.
Это готовит следующий отдельный release PR `developer -> main`; `main`
обновляется только через human-merged release PR.

## Release Candidate

- Source branch: `developer`
- Target branch: `main`
- `origin/main`: `170ec8e23981f7a379db843ea67314b5cb47ef7c`
- `origin/developer`: `344c347fdf01a4b1e73a40bebb08fc520d0d51e8`
- Latest release tag: `v1.5.0` -> `170ec8e23981f7a379db843ea67314b5cb47ef7c`
- Next intended release tag: `v1.5.1`, annotated tag on the release merge commit
  after release PR merge.

Release PR merge remains human-only. No direct push to `main`; no GitHub Release
publication in this release-prep task.

## Independent State Analysis

- PR #298 MIR-11 configurable commit metadata scopes: `MERGED`.
- PR #299 MIR-10 release-boundary commit-message gate hardening: `MERGED`.
- PR #300 MIR-12 ID reference integrity gate: `MERGED`.
- PR #301 MIR-13 superseded banner standard: `MERGED`.
- PR #302 MIR-14 execution timing discipline: `MERGED`.

Merge facts verified from GitHub metadata:

- PR #298 merged at `2026-07-01T16:36:05Z`, merge commit
  `3aac7a01a1f10c06ff053be39b75168ee7fe7db8`.
- PR #299 merged at `2026-07-01T16:55:46Z`, merge commit
  `cbf57c848d8537b4ace5bc348148ba1b692d2a1b`.
- PR #300 merged at `2026-07-01T17:20:31Z`, merge commit
  `84267fa77214a394b62927ac06d2c4b8389475ef`.
- PR #301 merged at `2026-07-01T17:51:52Z`, merge commit
  `867082c089ab16c4fea094ee697db0e10082f5ca`.
- PR #302 merged at `2026-07-02T01:32:48Z`, merge commit
  `344c347fdf01a4b1e73a40bebb08fc520d0d51e8`.

## Journal Gate

Journal gate for release-prep is clean after this PR's boundary reconciliation:

- INDEX continuity is intact; latest row before this release-prep task is `0136`.
- This release-prep task uses row `0137`.
- Rows 0132-0136 are reconciled to `closed; PR #... merged; facts in RESULT`.
- RESULT 0132-0136 contain closure-stamps with PR state, `merged_at`, merge commit
  and reviewed head SHA.
- Historical `execution_started_at == execution_finished_at` in RESULT 0132/0133
  is not rewritten; it is the motivating defect addressed by MIR-14.
- Row 0131 belongs to the already released v1.5.0 boundary and is not part of the
  `origin/main...origin/developer` payload for v1.5.1.

The current release-prep entry remains open until this PR is reviewed/merged; after merge, release PR creation is the next separate task. Exact status remains authoritative in `docs/agent-system/engine-journal/INDEX.md` and corresponding `RESULT-*` files.

## Generated Gates

- `python docs/agent-system/tools/gen_file_map.py --check`: required for this PR.
- `python docs/agent-system/tools/gen_cloud_bundle.py --check`: required for this PR.
- `python docs/agent-system/tools/generated_eol_guard.py --base origin/developer`:
  required for generated/cloud classification.
- `python docs/agent-system/tools/check_task_ready.py --base origin/developer`:
  required before push/PR.
- `python docs/agent-system/tools/check_task_ready.py --base origin/main --release-boundary`:
  required on `developer`/release boundary before release PR.
- `python docs/agent-system/tools/validate_commit_message.py --base origin/developer`:
  required before push/PR.

## Release Payload Summary

Current diff `origin/main...origin/developer` contains 35 tracked paths before this
release-prep branch. Payload class remains public methodology docs/templates/journal,
read-only tools and generated cloud artifacts; forbidden/runtime/private payload scan
is expected to stay zero.

Key changes since `v1.5.0`:

- MIR-11: configurable commit-message scopes through `LANGUAGE_POLICY.md`
  `commit_metadata.allowed_scopes`; default `[agent-system]` preserved (0132).
- MIR-10: release-boundary commit-message hardening with no-merge range scan,
  cutoff support and release-boundary skip behavior (0133).
- MIR-12: ID reference integrity linter integrated into ready-gate (0134).
- MIR-13: reusable superseded banner template and advisory ready-gate check (0135).
- MIR-14: execution timing discipline and advisory ready-gate finding for
  unreliable execution timing (0136).
- Release-prep boundary reconciliation of 0132-0136 journal facts (0137).

## Safety Scans

- Forbidden/runtime/private payload must be checked again in final release-prep.
- Sensitive filename scan must remain filename-only/count-only; secret lines must not be printed.
- `.env` must not be read.
- Expected forbidden/runtime/private payload count: 0.
- Target repositories are outside this release-prep scope.

## Release Recommendation

Рекомендация: `READY FOR RELEASE PR AFTER MERGE OF THIS RELEASE-PREP PR`.

После merge текущего release-prep PR отдельной задачей создать release PR
`developer -> main` для `v1.5.1`. Release PR merge remains human-only and `main`
is not pushed directly. Annotated tag `v1.5.1` is created on the release merge
commit after release PR merge according to the active release instruction, then
sync `main -> developer` is performed.

## Next Step

1. Review/merge текущий release-prep PR.
2. Отдельной задачей создать release PR `developer -> main` для `v1.5.1`.
3. Человек-архитектор мержит release PR.
4. Создать annotated tag `v1.5.1` на release merge commit в `main`.
5. Выполнить sync `main -> developer`.
6. Перейти к methodology-update для target implementation repository от stable
   release pointer `v1.5.1`.
