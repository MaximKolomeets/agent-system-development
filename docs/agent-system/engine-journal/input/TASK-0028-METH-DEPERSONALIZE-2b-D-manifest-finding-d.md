# TASK-0028: METH-DEPERSONALIZE-2b-D (manifest, finding D)

## Режим

Роль: docs-maintainer.
Исполнитель: на усмотрение архитектора.
Reasoning effort: низкий.
Запуск: Local only.
Режим: docs-only, branch-guard.

Batch-closure policy действует: незакрытые прошлые journal-записи являются допустимым промежуточным состоянием внутри phase и не блокируют эту задачу. Closure выполняется batch перед release.

## Цель

Finding D: выровнять `mandatory_engine_task_header` в `ADOPTION_TRANSFER_MANIFEST.yml` под role-agnostic header и зарегистрировать `SOURCE_CONSUMERS.md` в generic-категории manifest.

## Ветки

- Base: `developer`
- Work: `work/docs-maintainer-01/depersonalize-2b-d`

## Allowed files

- `docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml`
- `docs/agent-system/engine-journal/input/TASK-0028-METH-DEPERSONALIZE-2b-D-manifest-finding-d.md`
- `docs/agent-system/engine-journal/output/RESULT-0028-METH-DEPERSONALIZE-2b-D-manifest-finding-d.md`
- `docs/agent-system/engine-journal/INDEX.md`

## Изменения

1. В `mandatory_engine_task_header` заменить привязку к `<agent-name>` и общему "блоку рекомендуемого режима" на role-agnostic формулировку:
   - `Роль`;
   - `Исполнитель: на усмотрение архитектора`;
   - `Reasoning effort`;
   - ссылка на канон `docs/agent-system/templates/TASK_HEADER_COMMON.md`.
2. Добавить `docs/agent-system/SOURCE_CONSUMERS.md` в `categories.generic.files`.
3. Прочие записи manifest не трогать.
4. Открытые прошлые journal-записи не закрывать в рамках этой задачи.

## Проверки

- `rg -i "Модель:|<engine-name>|chatgpt|codex|claude code" docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml`
- `git diff --name-only origin/developer...HEAD`
- `git diff --check`
- branch-guard перед commit

## STOP

- HEAD не `work/docs-maintainer-01/depersonalize-2b-d`.
- Diff выходит за allowed files.
- `SOURCE_CONSUMERS.md` не попал в generic-категорию.
- Manifest rule остаётся с `Модель:` / `<engine-name>` / vendor-tool именами.

## Передача

Следующий: reviewer — review PR; затем архитектор — merge; затем engine — следующий под-PR phase-2b (2b-2); journal closure — batch перед release; release держим до завершения обезличивания и batch-closure.

Обновить Source-снапшот у зарегистрированных потребителей.
