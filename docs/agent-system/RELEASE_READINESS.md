# RELEASE_READINESS

Дата проверки: 2026-07-01

Назначение: release-prep snapshot для `v1.5.0` после merge PR #286-#294.
Это готовит следующий отдельный release PR `developer -> main`; agent не мержит
release PR, не пушит в `main`, не создаёт tag и не публикует GitHub Release.

## Release Candidate

- Source branch: `developer`
- Target branch: `main`
- `origin/main`: `1cad3af985fa48e7b0ca3358420d2cc5094b7ad6`
- `origin/developer`: `4ed2662b5345798e99197fa14137e8154d946209`
- Latest release tag: `v1.4.1` -> `1cad3af985fa48e7b0ca3358420d2cc5094b7ad6`
- Next intended release tag: `v1.5.0`, human-only annotated tag after release PR merge.

Agent не мержит release PR, не пушит в `main`, не создаёт tag и не публикует GitHub Release.

## Independent State Analysis

- PR #286 EOL normalization: `MERGED`.
- PR #287 target-local xref / reading-list hygiene: `MERGED`.
- PR #288 `METHODOLOGY_MAP` navigator and docs taxonomy: `MERGED`.
- PR #289 CONTROL_MATRIX pattern and template: `MERGED`.
- PR #290 EXTERNAL_REVIEW_LEDGER pattern, template and anti-loop surface: `MERGED`.
- PR #291 THREAT_MODEL template: `MERGED`.
- PR #292 governance patterns: POLICY_STATUS, ERROR_CATALOG, DECISION_NOTE: `MERGED`.
- PR #293 commit metadata enforcement: `MERGED`.
- PR #294 pre-release batch-closure for journal 0122-0129: `MERGED`.

## Journal Gate

Journal gate for release-prep is clean:

- INDEX continuity is intact; latest row before this release-prep task is `0130`.
- Rows 0122-0129 are `closed; PR #... merged; facts in RESULT`.
- RESULT 0122-0129 contain closure-stamps with PR state, `merged_at`, merge commit
  and reviewed head SHA.
- Row 0130 is lifecycle-only terminal fold for PR #294 and is not a release blocker.

The current release-prep entry remains open until this PR is reviewed/merged; after merge, release PR creation is the next separate task. Exact status remains authoritative in `docs/agent-system/engine-journal/INDEX.md` and corresponding `RESULT-*` files.

## Generated Gates

- `python docs/agent-system/tools/gen_file_map.py --check`: required for this PR.
- `python docs/agent-system/tools/gen_cloud_bundle.py --check`: required for this PR.
- `python docs/agent-system/tools/generated_eol_guard.py --base origin/developer`:
  required for generated/cloud classification.
- `python docs/agent-system/tools/check_task_ready.py --base origin/developer`:
  required before push/PR.
- `python docs/agent-system/tools/validate_commit_message.py --base origin/developer`:
  required before push/PR.

## Release Payload Summary

Current diff `origin/main...origin/developer` contains 58 tracked paths before this
release-prep branch. Payload class remains public methodology docs/templates/journal,
read-only tools and generated cloud artifacts; forbidden/runtime/private payload scan
is expected to stay zero.

Key changes since `v1.4.1`:

- EOL-нормализация и `.gitattributes` policy for text source files (0122).
- Target-local xref hygiene and README reading-list path clarity (0123).
- `METHODOLOGY_MAP` navigator and docs taxonomy (0124).
- Reusable CONTROL_MATRIX pattern and template (0125).
- Reusable EXTERNAL_REVIEW_LEDGER pattern/template with anti-loop and
  diminishing-returns stop (0126).
- Target-local THREAT_MODEL template (0127).
- Governance patterns for POLICY_STATUS, ERROR_CATALOG and DECISION_NOTE (0128).
- Commit message format enforcement through `validate_commit_message.py`,
  mandatory ready-gate integration in `check_task_ready.py`, task/orchestrator/review
  surfacing and `ci/commit-message` policy documentation (0129).
- Pre-release batch-closure of 0122-0129 journal facts (0130).

## Safety Scans

- Forbidden/runtime/private payload must be checked again in final release-prep.
- Sensitive filename scan must remain filename-only/count-only; secret lines must not be printed.
- `.env` must not be read.
- Expected forbidden/runtime/private payload count: 0.
- Target repositories are outside this release-prep scope.

## Release Recommendation

Рекомендация: `READY FOR RELEASE PR AFTER MERGE OF THIS RELEASE-PREP PR`.

После merge текущего release-prep PR отдельной задачей создать release PR
`developer -> main` для `v1.5.0`. Agent не мержит release PR, не пушит в `main`, не
создаёт tag и не публикует GitHub Release. После human merge архитектор ставит
annotated tag `v1.5.0` на release merge commit в `main`, затем выполняется sync
`main -> developer`.

## Next Step

1. Review/merge текущий release-prep PR.
2. Отдельной задачей создать release PR `developer -> main` для `v1.5.0`.
3. Человек-архитектор мержит release PR.
4. Человек-архитектор ставит annotated tag `v1.5.0` на release merge commit в `main`.
5. Engine выполняет sync `main -> developer`.
6. Перейти к Блоку B: methodology-update для target implementation repository от
   stable release pointer `v1.5.0`.
