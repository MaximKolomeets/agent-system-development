# RELEASE_READINESS

Дата проверки: 2026-07-03

Назначение: release-prep snapshot для кандидатного релиза `v1.5.2`.
Базовый опубликованный release: `v1.5.1`. Следующий release candidate:
`v1.5.2`.

## Release Status

- Status: `candidate_ready_for_release_pr_after_prep_review`.
- Source branch: `developer`.
- Target branch: `main`.
- `origin/main`: `2467edd8488a51d74483e8095e4887c0f512dfcd`.
- `origin/developer`: `97e874883afbe3ac38ccd815d48f63ca964c5737`.
- Latest release tag: `v1.5.1` -> `2467edd8488a51d74483e8095e4887c0f512dfcd`.
- Previous release tag: `v1.5.0` -> `170ec8e23981f7a379db843ea67314b5cb47ef7c`.
- Next planned methodology release: `v1.5.2`.
- Candidate SHA: `97e874883afbe3ac38ccd815d48f63ca964c5737`.
- Release base: `v1.5.1` / `origin/main`.
- Release payload range: `v1.5.1..origin/developer`.

Release PR `developer -> main`, merge в `main`, annotated tag `v1.5.2`,
GitHub Release publication и sync `main -> developer` остаются human-only
действиями по `RELEASE_AUTHORITY_POLICY.md` и `HUMAN_GATE_POLICY.md`. Этот файл
готовит evidence для release PR, но не выполняет release action.

## Boundary Facts

Merge facts verified from GitHub metadata and local tag state:

- Release base `v1.5.1`: tag target
  `2467edd8488a51d74483e8095e4887c0f512dfcd`.
- Candidate `origin/developer`: `97e874883afbe3ac38ccd815d48f63ca964c5737`.
- `origin/main`: `2467edd8488a51d74483e8095e4887c0f512dfcd`.
- Batch closure PR #322: `MERGED` at `2026-07-02T17:37:05Z`, merge commit
  `97e874883afbe3ac38ccd815d48f63ca964c5737`.

## Journal Gate

- Rows 0138-0141: boundary-reconciled by `METH-RELEASE-PREP-V1-5-2-01` with
  PR #306-#309 merge facts.
- Rows 0142-0152: batch-reconciled by `METH-BATCH-CLOSURE-0142-0152-V1-5-2-01`
  and included in release payload.
- Row 0153: batch-closure PR #322 merge facts reconciled by this release-prep.
- Row 0154: this release-prep task.
- Exact status remains authoritative in `docs/agent-system/engine-journal/INDEX.md`
  and corresponding `RESULT-*` files.

## Generated Gates

Required for this release-prep PR:

- `python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0154-METH-RELEASE-PREP-V1-5-2-01.md`.
- `python docs/agent-system/tools/validate_policy_invariants.py`.
- `python docs/agent-system/tools/russian_first_lint.py`.
- `python docs/agent-system/tools/check_task_ready.py --base origin/developer`.
- `python docs/agent-system/tools/generated_eol_guard.py --base origin/developer`.
- `python docs/agent-system/tools/gen_file_map.py --check`.
- `python docs/agent-system/tools/gen_cloud_bundle.py --check`.
- `python docs/agent-system/tools/validate_commit_message.py --base origin/developer`.
- `git diff --check origin/developer...HEAD`.

Required after this PR is merged into `developer`, before release PR approval:

- `python docs/agent-system/tools/check_task_ready.py --base origin/main --release-boundary`.
- Human UAT / Business Acceptance verdict or explicit `not_applicable` reason.
- Human-only release PR merge `developer -> main`.
- Human-only annotated tag `v1.5.2` on the release merge commit.
- Human-only publication/sync decision.
- Release/sync/boundary `RESULT` records actor, action and evidence for
  merge/tag/publish/sync actions without secret values.

## Release Payload Summary

Payload `v1.5.2` includes the full PR-1..15 / H1..H16 hardening series:

| Methodology PR | Finding block | GitHub PR | Merge facts | Payload |
| --- | --- | --- | --- | --- |
| PR-1 | H1 | #306 | merged `2026-07-02T09:00:28Z`, merge `f993dba56d03682d80f757cf034616fe954f1ea4` | post-release state/status refresh after `v1.5.1`, BACKLOG/NEXT split, release snapshot and ruleset snapshot |
| PR-2 | H2 | #307 | merged `2026-07-02T09:28:36Z`, merge `9fc59150f508f4846fef2b34d9738f49b81e7fb2` | journal history scope clarity |
| PR-3 | H3 | #308 | merged `2026-07-02T10:07:47Z`, merge `85f14f204b8dc77f032af096c417f9130476478c` | time and cost accounting hard-gate |
| PR-4 | H4 | #309 | merged `2026-07-02T10:29:51Z`, merge `4818b553beaa5b426334404696507c48e95d0d22` | stable-reference schema sync |
| PR-5 | H5 | #311 | merged `2026-07-02T11:19:34Z`, merge `aaac1a762a35a00427cbec71be6460c746d3fcda` | navigation and discovery |
| PR-6 | H9 | #312 | merged `2026-07-02T11:40:37Z`, merge `69696842ed93f9a85757b8887012b2c2f2ff5114` | release authority and human-gate policy |
| PR-7 | H13 | #313 | merged `2026-07-02T12:25:37Z`, merge `a669e3d7f7e63b30b56ed0f80e1fe0ea908122b0` | Business Acceptance / UAT gate |
| PR-8 | H14 | #314 | merged `2026-07-02T13:32:49Z`, merge `8db7df25e494e0a28e84ec9e703961fba3ad78e6` | hotfix, rollback and disaster recovery |
| PR-9 | H6 | #315 | merged `2026-07-02T14:02:49Z`, merge `3e6ad6d15aef41db6cec8ff6235a8eb031767d6a` | safe-scan and Russian-first lint |
| PR-10 | H7 | #316 | merged `2026-07-02T14:25:03Z`, merge `d66754023456816fe010e122de7fddb836475258` | management layer for non-technical architect |
| PR-11 | H8+H10 | #317 | merged `2026-07-02T14:50:49Z`, merge `8cde0491069c41029d50f03c5e5cf50bfbdab72a` | private control plane and MIR lifecycle ledger |
| PR-12 | H11 | #318 | merged `2026-07-02T15:23:09Z`, merge `9d74c9d9c329d27ba886915d7d63888c38603c46` | policy invariants and self-test gate |
| PR-13 | H12 | #319 | merged `2026-07-02T15:47:58Z`, merge `25b60ad8d41f42fb3e39daebb0be3757605acfc3` | agent initiative and mandatory feedback |
| PR-14 | H15 | #320 | merged `2026-07-02T16:58:19Z`, merge `da6e6a27a7b8c2129fca8304e133ac2bfe958d4c` | journal archiving and memory hygiene |
| PR-15 | H16 | #321 | merged `2026-07-02T17:17:51Z`, merge `d102590705e404537c8072d6ce6cf6cf5bb5fee2` | lifecycle and cross-project guidance |

Boundary prerequisite:

- PR #322 batch-closes journal rows 0142-0152 before release boundary and was
  merged at `2026-07-02T17:37:05Z`.
- This release-prep reconciles remaining payload rows 0138-0141 and batch row
  0153 with merge facts.

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
release PR `developer -> main` for `v1.5.2`. Do not merge the release PR, create
tag `v1.5.2`, publish GitHub Release or sync back to `developer` by automation;
those are human-only release authority actions.

Until `v1.5.2` is published, downstream tasks continue to use stable pointer
`origin/main` or tag `v1.5.1`.

## Передача

Следующий: methodology-reviewer-01 - scoped review release-prep v1.5.2; затем
архитектор - human merge этого PR в `developer`; затем release-manager - подготовить
human-controlled release PR `developer -> main` для `v1.5.2`.
