# RELEASE_READINESS

Дата проверки: 2026-06-24

Назначение: pre-release snapshot для runway к `v1.2.0` после full audit #238 и fix-серии P0-P4. Это не release approval само по себе: финальный release-gate выполняется после merge P4, batch-closure и reviewer consistency-gate.

## Release Candidate

- Source branch: `developer`
- Target branch: `main`
- `origin/main`: `8c21a45bf189432afcdabfb164f85d175271df74`
- `origin/developer`: `d3a447e16b9cbed6fdd48c973976529a33bd5a61`
- Latest release tag: `v1.1.0` -> `8c21a45bf189432afcdabfb164f85d175271df74`
- Historical tag `v1.0.0`: present -> `123a126afd812255f7d671d98169c077cf33a319`
- Next intended release tag: `v1.2.0`, human-only annotated tag after release PR merge.

Агент не мержит release PR, не пушит в `main`, не создаёт tag и не публикует GitHub Release.

## Independent State Analysis

- PR #238 full audit: `MERGED`.
- PR #239 P0 batch-closure 0086-0088: `MERGED`; rows 0086-0088 are closed with facts in RESULT.
- PR #240 P1 methodology reference tag schema: `MERGED`; `source_tag` / `release_tag` are present as optional fields while `source_commit` remains required.
- PR #241 P2 execution finish field canon: `MERGED`; new measured finish field is `execution_finished_at`.
- PR #242 P3 headings Russian-first batch: `MERGED`; descriptive headings in active adopter-facing docs were aligned.
- P4 state-refresh: this task updates `CURRENT_STATE.md`, `NEXT_STEPS.md`, this snapshot and cloud bundle.
- State-level n-01: live/current vendor/tool literal is not present; the remaining literal is in append-only historical prose and is not a live blocker.

## Journal Gate

Before release `v1.2.0`, run a dedicated batch-closure after P4 merge. Expected substantive merged-but-unclosed entries to include:

- `0089` / PR #238, full audit closure-stamp pending.
- `0091` / PR #240, P1 closure pending.
- `0092` / PR #241, P2 closure pending.
- `0093` / PR #242, P3 closure pending.
- P4 state-refresh entry after its PR is merged.

Lifecycle-only terminal fold `0090` is accepted terminal closure for P0 and is not a substantive blocker by itself. Exact status remains authoritative in `docs/agent-system/engine-journal/INDEX.md` and corresponding `RESULT-*` files.

## Generated Gates

To be re-run after this PR is finalized:

- `python docs/agent-system/tools/gen_file_map.py --check`
- `python docs/agent-system/tools/gen_cloud_bundle.py --check`

## Release Payload Summary

Current diff `origin/main...origin/developer` contains 40 tracked paths before this P4 branch. Payload class remains public methodology docs/templates/journal/cloud generated artifacts; no runtime, secret or private downstream payload is expected.

Key changes since `v1.1.0`:

- P0 closure of post-release 0086-0088 entries.
- P1 optional `source_tag` / `release_tag` in methodology reference.
- P2 `execution_finished_at` canon for new TASK/RESULT.
- P3 Russian-first descriptive headings in active adopter-facing docs.
- P4 state-refresh and cloud bundle regeneration.

## Safety Scans

- Forbidden/runtime/private payload must be checked again in final release-prep.
- Sensitive filename scan must remain filename-only/count-only; secret lines must not be printed.
- `.env` must not be read.

## Release Recommendation

Рекомендация: `NOT READY YET; continue runway`. После merge P4 выполнить batch-closure для merged-but-unclosed substantive entries после 0088, затем reviewer consistency-gate. Если gate clean и оба generated checks проходят, подготовить release PR `developer -> main` для `v1.2.0`; после human merge архитектор ставит annotated tag `v1.2.0`.

## Next Step

1. Review/merge P4 state-refresh PR.
2. Выполнить batch-closure для фактических merged-but-unclosed substantive entries после 0088.
3. Выполнить reviewer consistency-gate.
4. Подготовить release-prep/release PR `developer -> main` для `v1.2.0`.
5. После human merge поставить annotated tag `v1.2.0`, затем sync `main -> developer`.
