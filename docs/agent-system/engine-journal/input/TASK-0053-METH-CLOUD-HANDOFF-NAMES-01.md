# TASK-0053: METH-CLOUD-HANDOFF-NAMES-01

## Режим

Роль: docs-maintainer. Исполнитель: на усмотрение архитектора. Reasoning effort: высокий. Branch-guard обязателен.

Batch-policy: открытые journal-записи не являются blocker; closure не смешивать.

## Цель

Обновить canon footer-конвенции: строка `Архитектору — загрузить в контекст оркестратора: ...` должна ссылаться на numbered cloud-имена из `docs/agent-system/cloud/00_README.md`, а не только на исходные пути.

## Repo / ветки

- Репозиторий: `MaximKolomeets/agent-system-development`
- Каталог: `C:\neural\repos\agent-system-development`
- base: `developer`
- work: `work/docs-maintainer-01/cloud-handoff-names-01`

## Allowed files

- `docs/agent-system/ORCHESTRATOR_OPERATING_CONTRACT.md`
- `docs/agent-system/templates/TASK_HEADER_COMMON.md`
- `docs/agent-system/ORCHESTRATOR_RESPONSE_STANDARD.md`
- `docs/agent-system/ENGINE_JOURNAL_CONTRACT.md`
- `docs/agent-system/cloud/**`
- `docs/agent-system/engine-journal/INDEX.md`
- `docs/agent-system/engine-journal/input/TASK-0053-METH-CLOUD-HANDOFF-NAMES-01.md`
- `docs/agent-system/engine-journal/output/RESULT-0053-METH-CLOUD-HANDOFF-NAMES-01.md`

## Требования

1. Footer перечисляет только файлы, входящие в `orchestrator_context_bundle`.
2. Каждый bundle-файл указывается cloud-именем из `docs/agent-system/cloud/00_README.md`, а исходный путь пишется как `src: ...`.
3. Небандловые tooling/source-файлы остаются в «Source Delta», но не попадают в context-load строку.
4. Состав базового bundle не дублируется в канон-доках; ссылка на `00_README.md` является авторитетной картой `source path -> cloud filename`.

## Проверки

- все 4 canon-документа содержат numbered cloud naming + only-bundle + ссылку на `docs/agent-system/cloud/00_README.md`;
- `python docs/agent-system/tools/gen_cloud_bundle.py --check`;
- `python docs/agent-system/tools/gen_file_map.py --check`;
- `git diff --check`;
- branch guard.

## Передача

Следующий: `reviewer` — review (footer = numbered cloud-имена + only-bundle во всех 4 доках; пример корректен; оба `--check` 0); затем архитектор — merge; затем engine — pre-release BATCH-CLOSURE 0052…последний; затем state-refresh confirm → release dev→main.
