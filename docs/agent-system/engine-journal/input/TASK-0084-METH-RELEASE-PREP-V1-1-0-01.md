# TASK-0084: METH-RELEASE-PREP-V1-1-0-01

Статус: ready for review; PR #231 open.

Связанный RESULT file: `docs/agent-system/engine-journal/output/RESULT-0084-METH-RELEASE-PREP-V1-1-0-01.md`

## Задача

Подготовить release-prep для v1.1.0 после merge PR #230 и с учётом канона `accepted terminal fold`.

## Режим

- Роль: docs-maintainer.
- Base branch: `developer`.
- Work branch: `work/docs-maintainer-01/release-prep-v1-1-0-01`.
- Release target: `developer` -> `main`.
- Release PR не мержить.
- Tag и GitHub Release не создавать.

## Preflight

- Синхронизировать `developer` с `origin/developer`.
- Проверить, что `HEAD == origin/developer`.
- Проверить `main`/`origin/main`.
- Проверить PR #227 и PR #230 через `gh pr view`.
- Проверить journal gate с новым правилом `accepted terminal fold`.
- Выполнить `gen_file_map.py --check` и `gen_cloud_bundle.py --check`.

## Accepted Terminal Fold

Не считать blocker:

- `terminal-fold accepted`;
- `terminal-fold accepted pending own PR merge`;
- lifecycle-only terminal entries, где PR URL authoritative и явно указано `not release/reviewer blocker`.

STOP только если есть substantive entry в состоянии `open`, `ready`, `closure pending`, `stamp at merge`, неaccepted terminal fold, stale final-state surfaces вне accepted terminal fold, failed generated checks или release payload с runtime/secrets/private downstream data.

## Allowed Files

- `docs/agent-system/CURRENT_STATE.md`
- `docs/agent-system/NEXT_STEPS.md`
- `docs/agent-system/RELEASE_READINESS.md`
- `docs/agent-system/engine-journal/input/TASK-0084-METH-RELEASE-PREP-V1-1-0-01.md`
- `docs/agent-system/engine-journal/output/RESULT-0084-METH-RELEASE-PREP-V1-1-0-01.md`
- `docs/agent-system/engine-journal/INDEX.md`
- `docs/agent-system/cloud/**`

## Проверки

- `python docs/agent-system/tools/gen_file_map.py --check`
- `python docs/agent-system/tools/gen_cloud_bundle.py --check`
- `git diff --check`
- filename-only/count-only forbidden/sensitive scan release payload
- branch guard

## execution_started_at

Measured: `2026-06-24T15:15:30.0330580+07:00`
