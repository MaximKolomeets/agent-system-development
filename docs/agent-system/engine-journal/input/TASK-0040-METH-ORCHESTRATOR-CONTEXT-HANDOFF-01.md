# Задача для docs-maintainer-01: METH-ORCHESTRATOR-CONTEXT-HANDOFF-01

## Режим

Роль: docs-maintainer.
Исполнитель: на усмотрение архитектора.
Reasoning effort: высокий.
branch-guard.

Batch-policy: открытые journal-записи не блокируют; closure не подмешивать.

## Цель

Закрепить канон Architect -> Orchestrator context handoff: архитектор должен видеть,
какие файлы загрузить в контекст оркестратора при онбординге нового чата и после
каждой задачи. Оркестратор и со-архитектор без доступа к repo восстанавливают
картину из авторитетного bundle и per-task списка.

## Allowed files

- `docs/agent-system/ORCHESTRATOR_OPERATING_CONTRACT.md`
- `docs/agent-system/ORCHESTRATOR_PROJECT_OPERATING_LAYER.md`
- `docs/agent-system/templates/TASK_HEADER_COMMON.md`
- `docs/agent-system/ORCHESTRATOR_RESPONSE_STANDARD.md`
- `README.md`
- `docs/agent-system/ENGINE_ENTRYPOINT.md`
- `docs/agent-system/engine-journal/INDEX.md`
- `docs/agent-system/engine-journal/input/TASK-0040-METH-ORCHESTRATOR-CONTEXT-HANDOFF-01.md`
- `docs/agent-system/engine-journal/output/RESULT-0040-METH-ORCHESTRATOR-CONTEXT-HANDOFF-01.md`

## Изменения

- В `ORCHESTRATOR_OPERATING_CONTRACT.md` добавить единственный авторитетный раздел
  `Architect → Orchestrator context handoff`: context-load bundle, исключения,
  freshness stamp и stale-поведение.
- В `ORCHESTRATOR_PROJECT_OPERATING_LAYER.md` заменить локальный состав knowledge
  base ссылкой на авторитетный раздел, без дублирования bundle.
- В `TASK_HEADER_COMMON.md` закрепить обязательную per-task строку
  «Архитектору — загрузить в контекст оркестратора: ...» с `asof` и
  `developer_head_sha`.
- В `ORCHESTRATOR_RESPONSE_STANDARD.md` обязать оркестратор ретранслировать
  context handoff и подтверждать `context-handoff present: yes`.
- В `README.md` и `ENGINE_ENTRYPOINT.md` добавить указатель на новый раздел.

## Проверки

- Канон-согласованность: bundle определён один раз в operating contract, остальные
  документы ссылаются.
- `python docs/agent-system/tools/gen_file_map.py --check` -> exit 0.
- `git diff --check` -> clean.
- diff только whitelist.
- branch guard: HEAD == `work/docs-maintainer-01/orchestrator-context-handoff-01`.

## Передача

Следующий: reviewer — review (бандл определён единожды, per-task вывод обязателен,
freshness-штамп, ссылки без дублей); затем архитектор — merge; затем engine —
FIX-3 (adoption-templates sync); journal closure — batch перед release.
