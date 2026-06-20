# TASK-0029: METH-DEPERSONALIZE-2b-2 (orchestrator adapter docs)

## Режим

Роль: docs-maintainer.
Исполнитель: на усмотрение архитектора.
Reasoning effort: средний.
Запуск: Local only.
Режим: docs-only, branch-guard.

Batch-closure policy действует: открытые прошлые journal-записи являются допустимым промежуточным состоянием внутри phase и не блокируют эту задачу. Closure выполняется batch перед release.

## Цель

Обезличить содержимое adapter-документов оркестратора: vendor/tool-имена заменить на роли, а adapter-note сформулировать generic: оркестратор работает через любой chat-интерфейс по выбору архитектора.

## Ветки

- Base: `developer`
- Work: `work/docs-maintainer-01/depersonalize-2b-2`

## Allowed files

- `docs/agent-system/ORCHESTRATOR_RESPONSE_STANDARD.md`
- `docs/agent-system/ORCHESTRATOR_OPERATING_CONTRACT.md`
- `docs/agent-system/templates/ORCHESTRATOR_RESPONSE_TEMPLATE.md`
- `docs/agent-system/engine-journal/input/TASK-0029-METH-DEPERSONALIZE-2b-2-orchestrator-adapter-docs.md`
- `docs/agent-system/engine-journal/output/RESULT-0029-METH-DEPERSONALIZE-2b-2-orchestrator-adapter-docs.md`
- `docs/agent-system/engine-journal/INDEX.md`

## Изменения

1. В `ORCHESTRATOR_RESPONSE_STANDARD.md` заменить vendor/tool actor-text на `оркестратор` и `исполнитель (engine)`.
2. В `ORCHESTRATOR_OPERATING_CONTRACT.md` сделать adapter-note generic: любой chat-интерфейс по выбору архитектора.
3. В `templates/ORCHESTRATOR_RESPONSE_TEMPLATE.md` обезличить actor-text и role/header placeholders.
4. Сохранить запреты и safety/prohibition правила по смыслу.
5. Не переименовывать файлы и не трогать прошлые journal-записи.

## Проверки

- `rg -i "chatgpt|codex|claude code|<engine-name>|Модель:" docs/agent-system/ORCHESTRATOR_RESPONSE_STANDARD.md docs/agent-system/ORCHESTRATOR_OPERATING_CONTRACT.md docs/agent-system/templates/ORCHESTRATOR_RESPONSE_TEMPLATE.md`
- `git diff --name-only origin/developer...HEAD`
- `git diff --check`
- branch-guard перед commit

## STOP

- HEAD не `work/docs-maintainer-01/depersonalize-2b-2`.
- Diff выходит за allowed files.
- Vendor/tool имена остаются в трёх adapter-файлах.
- Prohibition/safety правила удалены вместо обезличивания актора.

## Передача

Следующий: reviewer — review PR; затем архитектор — merge; затем engine — 2b-3 (active-rule actor-scrub); journal closure — batch перед release; release держим до завершения обезличивания и batch-closure.

Обновить Source-снапшот у зарегистрированных потребителей.
