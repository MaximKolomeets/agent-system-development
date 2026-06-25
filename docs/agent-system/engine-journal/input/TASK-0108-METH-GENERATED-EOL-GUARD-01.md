# TASK-0108-METH-GENERATED-EOL-GUARD-01

## Режим

Роль: methodology-architect-01
Исполнитель: на усмотрение архитектора
Reasoning effort: средний
Запуск: Local only
Режим: Agent

## Цель

Добавить read-only guard для generated/cloud EOL/whitespace шума, чтобы engine и reviewer могли отличать содержательный drift generated artifacts от Windows line-ending noise без repo-wide renormalize.

## Контекст

После `gen_cloud_bundle.py` на Windows периодически появляются status/diff артефакты, где содержательно меняются ожидаемые generated files, но Git показывает дополнительные cloud Markdown files как modified из-за EOL. Это создаёт лишний review шум и ручные откаты. Нужен безопасный guard, который:

- не меняет git state;
- не запускает destructive git commands;
- не читает `.env`;
- не печатает secrets;
- классифицирует generated изменения как `content_changed`, `eol_only_changed`, `whitespace_only_changed`, `binary_or_unreadable` или `not_checked`;
- интегрируется в `check_task_ready.py`;
- документируется в autoloop/Fast Lane/orchestrator response canon.

## Scope

Разрешённые изменения:

- `.gitattributes` — узкое LF правило для methodology generated/journal/template/tool text paths.
- `docs/agent-system/tools/generated_eol_guard.py` — новый read-only guard.
- `docs/agent-system/tools/check_task_ready.py` — условный запуск guard при generated/bundle-source diff.
- `docs/agent-system/REVIEW_AUTOLOOP.md`
- `docs/agent-system/OPERATIONAL_FAST_LANE.md`
- `docs/agent-system/ORCHESTRATOR_RESPONSE_STANDARD.md`
- `docs/agent-system/BACKLOG.md`
- `docs/agent-system/CURRENT_STATE.md`
- `docs/agent-system/NEXT_STEPS.md`
- `docs/agent-system/DECISION_LOG.md`
- `docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml`
- `docs/agent-system/PROJECT_FILE_MAP.md`
- `docs/agent-system/cloud/**`
- `docs/agent-system/engine-journal/INDEX.md`
- `docs/agent-system/engine-journal/input/TASK-0108-METH-GENERATED-EOL-GUARD-01.md`
- `docs/agent-system/engine-journal/output/RESULT-0108-METH-GENERATED-EOL-GUARD-01.md`

Запрещено:

- repo-wide renormalize;
- `git add --renormalize`;
- destructive/state-changing git commands внутри guard;
- чтение `.env`;
- вывод secrets;
- прямые изменения `main` или `developer`.

## Проверки

Выполнить:

```text
python docs/agent-system/tools/generated_eol_guard.py --base origin/developer
python docs/agent-system/tools/generated_eol_guard.py --base origin/developer --json
python docs/agent-system/tools/check_task_ready.py --base origin/developer
python docs/agent-system/tools/check_task_ready.py --base origin/developer --json
python docs/agent-system/tools/gen_file_map.py --check
python docs/agent-system/tools/gen_cloud_bundle.py --check
git diff --check origin/developer...HEAD
```

## Передача

Следующий: methodology-reviewer-01 — проверить read-only поведение guard, отсутствие destructive git commands, корректную классификацию generated EOL/content drift, интеграцию с `check_task_ready.py`, parity generated artifacts и journal finalization.

## Execution

- baseline developer: `33b39dddbbc4340735227103f18f103bff5ab5aa`
- execution_started_at: `2026-06-25T23:20:51.4383472+07:00`
