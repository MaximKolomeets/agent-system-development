# RELEASE_READINESS

Дата проверки: 2026-07-04

Назначение: release-prep snapshot для кандидатного релиза `v1.5.3`.
Базовый опубликованный release: `v1.5.2`. Следующий release candidate:
`v1.5.3`.

## Release Status

- Status: `candidate_ready_for_release_pr_after_prep_review`.
- Source branch: `developer`.
- Target branch: `main`.
- `origin/main`: `1859a0034b14eed11e9842c4589fdeddb295cc6d`.
- `origin/developer`: `f10a06e2690bc8ff5c5cdb9afff893c39bee0dfe`.
- Latest release tag: `v1.5.2` -> `1859a0034b14eed11e9842c4589fdeddb295cc6d`.
- Previous release tag: `v1.5.1` -> `2467edd8488a51d74483e8095e4887c0f512dfcd`.
- Target release tag: `v1.5.3` -> `absent at preflight`.
- Next planned methodology release: `v1.5.3`.
- Candidate SHA: `f10a06e2690bc8ff5c5cdb9afff893c39bee0dfe`.
- Release base: `v1.5.2` / `origin/main`.
- Release payload range: `v1.5.2..origin/developer`.

`v1.5.2` уже опубликован: remote tag `v1.5.2^{}` и `origin/main` указывают на
`1859a0034b14eed11e9842c4589fdeddb295cc6d`. Этот файл больше не описывает
`v1.5.2` как будущий candidate.

Release PR `developer -> main`, merge в `main`, annotated tag `v1.5.3`,
GitHub Release publication и sync `main -> developer` остаются human-only
действиями по `RELEASE_AUTHORITY_POLICY.md` и `HUMAN_GATE_POLICY.md`. Этот файл
готовит evidence для release PR, но не выполняет release action.

## Boundary Facts

Merge facts verified from GitHub metadata and remote tag state:

- Target release tag `v1.5.3`: absent in `refs/tags/v1.5.3` at preflight.
- Release base `v1.5.2`: peeled tag target
  `1859a0034b14eed11e9842c4589fdeddb295cc6d`.
- Previous release `v1.5.1`: peeled tag target
  `2467edd8488a51d74483e8095e4887c0f512dfcd`.
- Candidate `origin/developer`: `f10a06e2690bc8ff5c5cdb9afff893c39bee0dfe`.
- `origin/main`: `1859a0034b14eed11e9842c4589fdeddb295cc6d`.
- PR #326: `MERGED` at `2026-07-03T16:16:07Z`, merge commit
  `e7f1b01582f209ff689ff199bd3597c3e5f8321f`.
- PR #327: `MERGED` at `2026-07-03T16:37:37Z`, merge commit
  `48560317211e9e81e5d2345a3115a886659062d7`.
- PR #328: `MERGED` at `2026-07-04T09:00:34Z`, merge commit
  `f10a06e2690bc8ff5c5cdb9afff893c39bee0dfe`.

## Journal Gate

- Rows 0155-0157 входят в payload `v1.5.3` поверх `v1.5.2`.
- Row 0155: PR #326 self-enforcement hardening, RESULT/INDEX финализированы.
- Row 0156: PR #327 target commit-language enforcement, RESULT/INDEX
  финализированы.
- Row 0157: PR #328 canonical commit-language tool reconcile, RESULT/INDEX
  финализированы.
- Row 0158: this release-prep task.
- Исторические `RESULT` rows 0155-0157 являются append-only; этот release-prep
  не переписывает их тело.
- Exact status remains authoritative in `docs/agent-system/engine-journal/INDEX.md`
  and corresponding `RESULT-*` files.

## Generated Gates

Required for this release-prep PR:

- `python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-METH-RELEASE-PREP-V1-5-3-01.md --json`.
- `python docs/agent-system/tools/check_task_ready.py --base origin/developer`.
- `python docs/agent-system/tools/validate_commit_message.py --base origin/developer`.
- `python docs/agent-system/tools/validate_policy_invariants.py`.
- `python docs/agent-system/tools/gen_file_map.py --check`.
- `python docs/agent-system/tools/gen_cloud_bundle.py --check`.
- `git diff --check origin/developer...HEAD`.

Required after this PR is merged into `developer`, before release PR approval:

- `python docs/agent-system/tools/check_task_ready.py --base origin/main --release-boundary`.
- Human UAT / Business Acceptance verdict or explicit `not_applicable` reason.
- Human-only release PR merge `developer -> main`.
- Human-only annotated tag `v1.5.3` on the release merge commit.
- Human-only publication/sync decision.
- Release/sync/boundary `RESULT` records actor, action and evidence for
  merge/tag/publish/sync actions without secret values.

## Release Payload Summary

Payload `v1.5.3` includes the post-`v1.5.2` methodology hardening delta:

| Journal row | Task | GitHub PR | Merge facts | Payload |
| --- | --- | --- | --- | --- |
| 0155 | `METH-SELF-ENFORCEMENT-HARDENING-01` | #326 | merged `2026-07-03T16:16:07Z`, merge `e7f1b01582f209ff689ff199bd3597c3e5f8321f` | methodology self-enforcement: pre-emit self-review, CI workflow, commit-language and journal append-only checks, manifest annotations |
| 0156 | `METH-TARGET-COMMIT-LANGUAGE-ENFORCEMENT-01` | #327 | merged `2026-07-03T16:37:37Z`, merge `48560317211e9e81e5d2345a3115a886659062d7` | target adoption commit-language enforcement guidance with Russian-first metadata guardrail |
| 0157 | `METH-COMMIT-LANGUAGE-TOOL-RECONCILE-01` | #328 | merged `2026-07-04T09:00:34Z`, merge `f10a06e2690bc8ff5c5cdb9afff893c39bee0dfe` | canonical `validate_commit_message.py` gate with body Russian-first check and retired duplicate tool removed |

## Safety Scans

- Sensitive filename scan remains filename-only/count-only; secret lines must not
  be printed.
- Strict added-line secret scan must remain value-safe.
- `.env` must not be read.
- Target repositories remain outside this release-prep scope.
- Public methodology repository must not include private downstream names, client
  data, credentials or production/runtime data.

## Release Recommendation

After this release-prep PR is reviewed and human-merged into `developer`, create
release PR `developer -> main` for `v1.5.3`. Do not merge the release PR, create
tag `v1.5.3`, publish GitHub Release or sync back to `developer` by automation;
those are human-only release authority actions.

Until `v1.5.3` is published, downstream tasks continue to use stable pointer
`origin/main` or tag `v1.5.2`.

## Передача

Следующий: methodology-reviewer-01 - scoped review release-prep v1.5.3; затем
архитектор - human merge этого PR в `developer`; затем release-manager - подготовить
human-controlled release PR `developer -> main` для `v1.5.3`.
