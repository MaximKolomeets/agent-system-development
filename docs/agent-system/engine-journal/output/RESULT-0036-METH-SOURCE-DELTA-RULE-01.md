# RESULT-0036 - METH-SOURCE-DELTA-RULE-01

## Итог

Статус: initial materialization; PR creation pending.

## Baseline

- Repository: MaximKolomeets/agent-system-development
- Local path: `C:\neural\repos\agent-system-development`
- Base branch: `developer`
- Working branch: `work/docs-maintainer-01/source-delta-rule-01`
- Baseline SHA: `e375a27096361483184c593f071df94a97f8b81a`
- Checked at: `2026-06-21T16:26:42+07:00`
- PR: pending
- Head SHA at PR creation: pending

## Что изменено

- `TASK_HEADER_COMMON.md`: добавлен основной канон «Source Delta» с таблицей, категориями из manifest, Source-рекомендациями и STOP-правилом для add/delete/rename inventory-файлов без manifest update.
- `ENGINE_JOURNAL_CONTRACT.md`: RESULT обязан включать «Source Delta» и хранить его в journal; reviewer target-check сверяет блок с фактическим diff.
- `ORCHESTRATOR_RESPONSE_STANDARD.md`: final report engine должен подтверждать `Source Delta present: yes`; оркестратор ретранслирует Source Delta архитектору и запрашивает дополнение, если блока нет.
- `CODE_REVIEW_TASK_TEMPLATE.md`: reviewer сверяет Source Delta с diff и `ADOPTION_TRANSFER_MANIFEST.yml`, включая категории, рекомендации и truthfulness поля `manifest обновлён?`.
- Journal seq 0036 добавлен в TASK/RESULT/INDEX.

## Проверки

- Branch guard: `git rev-parse --abbrev-ref HEAD` -> `work/docs-maintainer-01/source-delta-rule-01`.
- Канон-согласованность: полный формат Source Delta задан в `TASK_HEADER_COMMON`; остальные файлы ссылаются на этот канон и не дублируют таблицу.
- Source Delta dogfood: этот RESULT содержит таблицу по всем затронутым файлам.
- Whitelist diff: pending final check.
- `git diff --check`: pending final check.

## PR

- PR: pending
- Head SHA at PR creation: pending
- PR status after journal finalization: pending

## Source Delta

| путь | действие | категория | Source-рекомендация | manifest обновлён? |
| --- | --- | --- | --- | --- |
| `docs/agent-system/templates/TASK_HEADER_COMMON.md` | modified | template | update | n-a |
| `docs/agent-system/ORCHESTRATOR_RESPONSE_STANDARD.md` | modified | source | update | n-a |
| `docs/agent-system/ENGINE_JOURNAL_CONTRACT.md` | modified | source | update | n-a |
| `docs/agent-system/templates/CODE_REVIEW_TASK_TEMPLATE.md` | modified | template | update | n-a |
| `docs/agent-system/engine-journal/input/TASK-0036-METH-SOURCE-DELTA-RULE-01.md` | added | journal | none | n-a |
| `docs/agent-system/engine-journal/output/RESULT-0036-METH-SOURCE-DELTA-RULE-01.md` | added | journal | none | n-a |
| `docs/agent-system/engine-journal/INDEX.md` | modified | journal | none | n-a |

## Source-reminder

Обновить Source-снапшот у зарегистрированных потребителей: generic-placeholder из scaffold-only `docs/agent-system/SOURCE_CONSUMERS.md`.

## Локальные действия после PR/merge

После merge PR локально синхронизировать `developer` только через guard:

```powershell
git rev-parse --show-toplevel
git remote -v
git branch --show-current
git status --short
git switch developer
git pull --ff-only origin developer
```

`main` не менять напрямую; release/sync выполняются отдельным решением архитектора.

## Риски

- Token separation не проверялся как отдельная инфраструктурная настройка; для solo/operator docs-only режима это operational risk, но не blocker.
- Batch-policy соблюдена: прошлые journal-записи не закрывались.

## Передача

Следующий: reviewer - review; затем архитектор - merge; затем engine - METH-FILE-MAP-GEN-01 (C-2); journal closure - batch перед release.

Обновить Source-снапшот у зарегистрированных потребителей: generic-placeholder из scaffold-only `docs/agent-system/SOURCE_CONSUMERS.md`.
