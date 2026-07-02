# RELEASE_READINESS

Дата проверки: 2026-07-02

Назначение: post-publication snapshot для `v1.5.1`. Этот файл больше не является
инструкцией на будущий release PR `v1.5.1`: release-prep PR #303, release PR #304,
annotated tag `v1.5.1` и sync PR #305 уже выполнены.

## Release Status

- Status: `published/synced`.
- Source branch: `developer`.
- Target branch: `main`.
- `origin/main`: `2467edd8488a51d74483e8095e4887c0f512dfcd`.
- `origin/developer`: `2407cd4950b05fd2bb03583f9ccb1fe84d53eac5`.
- Latest release tag: `v1.5.1` -> `2467edd8488a51d74483e8095e4887c0f512dfcd`.
- Previous release tag: `v1.5.0` -> `170ec8e23981f7a379db843ea67314b5cb47ef7c`.
- Next planned methodology release: `v1.5.2` after H1-H16 hardening PR series.

`main` обновлён human-merged release PR. Прямой push в `main` не выполнялся.
GitHub Release publication не выполнялась в этой серии.

## Publication Facts

Merge facts verified from GitHub metadata and local tag state:

- PR #303 `docs(agent-system): подготовить release v1.5.1`: `MERGED` at
  `2026-07-02T02:11:11Z`, merge commit
  `e3c4210dade210f20b573196ed0d9da64961dc75`.
- PR #304 `release(agent-system): опубликовать методологию v1.5.1`: `MERGED` at
  `2026-07-02T06:46:16Z`, merge commit
  `2467edd8488a51d74483e8095e4887c0f512dfcd`.
- Annotated tag `v1.5.1`: points to
  `2467edd8488a51d74483e8095e4887c0f512dfcd`.
- PR #305 `Sync Merge pull request #304 from MaximKolomeets/developer`: `MERGED`
  at `2026-07-02T06:48:28Z`, merge commit
  `2407cd4950b05fd2bb03583f9ccb1fe84d53eac5`.

## Journal Gate

- Row 0137 (`METH-RELEASE-PREP-V1-5-1-01`) reconciled with PR #303 merge facts,
  release PR #304 facts, tag `v1.5.1` and sync PR #305 facts.
- Row 0138 (`METH-POST-RELEASE-STATE-REFRESH-V1-5-2-PR1-01`) records this H1
  post-release state/status refresh.
- Exact status remains authoritative in `docs/agent-system/engine-journal/INDEX.md`
  and corresponding `RESULT-*` files.

## Generated Gates

For this H1 refresh before PR:

- `python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0138-METH-POST-RELEASE-STATE-REFRESH-V1-5-2-PR1-01.md`.
- `python docs/agent-system/tools/check_task_ready.py --base origin/developer`.
- `python docs/agent-system/tools/generated_eol_guard.py --base origin/developer`.
- `python docs/agent-system/tools/gen_file_map.py --check`.
- `python docs/agent-system/tools/gen_cloud_bundle.py --check`.
- `python docs/agent-system/tools/validate_commit_message.py --base origin/developer`.
- `git diff --check origin/developer...HEAD`.

For the future `v1.5.2` release boundary after PR-1..15:

- `python docs/agent-system/tools/check_task_ready.py --base origin/main --release-boundary`.
- Fresh state refresh for `CURRENT_STATE.md`, `NEXT_STEPS.md`, `RELEASE_READINESS.md`
  and `RULESET_STATUS.md`.
- Regenerated `docs/agent-system/cloud/**`.
- Human-only release PR merge, annotated tag creation, publication decision and
  sync decision by `docs/agent-system/RELEASE_AUTHORITY_POLICY.md` and
  `docs/agent-system/HUMAN_GATE_POLICY.md`.
- Release/sync/boundary `RESULT` records actor, action and evidence for
  merge/tag/publish/sync actions without secret values.

## Release Payload Summary

Key changes published in `v1.5.1`:

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

- Forbidden/runtime/private payload scan for the `v1.5.1` release-prep passed in
  PR #303; future `v1.5.2` release-prep must run fresh scans.
- Sensitive filename scan remains filename-only/count-only; secret lines must not
  be printed.
- `.env` must not be read.
- Target repositories remain outside this H1 refresh scope.

## Release Recommendation

`v1.5.1` is already published and synced. No release PR or tag action remains for
`v1.5.1`.

Next: execute methodology hardening series for `v1.5.2` in separate scoped PRs,
starting with H1 state/status refresh and then H2 journal history scope clarity.
Until `v1.5.2` is published, downstream tasks use stable pointer `origin/main` or
tag `v1.5.1`.

## Передача

Следующий: docs-maintainer-01 — завершить PR-1/H1; затем docs-maintainer-01 —
PR-2/H2 journal history scope clarity.
