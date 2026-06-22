# Orchestrator Context Cloud Bundle

AUTO-GENERATED — не править руками; регенерировать через `python docs/agent-system/tools/gen_cloud_bundle.py`.

## Freshness

- asof: `2026-06-22T08:27:55+07:00`
- developer_head_sha: `efdcb01cbdac22f9aed4e43e8c84d75b1089063a`
- file_count_including_readme: `12`

## Контракт

- Источник состава: `docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml` → `orchestrator_context_bundle`.
- Каждый файл ниже является flat copy текущего repo content из origin path.
- Проверка drift: `python docs/agent-system/tools/gen_cloud_bundle.py --check`.

## Состав

| origin path | cloud filename |
| --- | --- |
| `docs/agent-system/PROJECT_FILE_MAP.md` | `PROJECT_FILE_MAP.md` |
| `docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml` | `ADOPTION_TRANSFER_MANIFEST.yml` |
| `docs/agent-system/templates/TASK_HEADER_COMMON.md` | `TASK_HEADER_COMMON.md` |
| `docs/agent-system/ORCHESTRATOR_RESPONSE_STANDARD.md` | `ORCHESTRATOR_RESPONSE_STANDARD.md` |
| `docs/agent-system/ORCHESTRATOR_OPERATING_CONTRACT.md` | `ORCHESTRATOR_OPERATING_CONTRACT.md` |
| `docs/agent-system/ENGINE_JOURNAL_CONTRACT.md` | `ENGINE_JOURNAL_CONTRACT.md` |
| `docs/agent-system/BRANCH_POLICY.md` | `BRANCH_POLICY.md` |
| `docs/agent-system/ENGINE_ENTRYPOINT.md` | `ENGINE_ENTRYPOINT.md` |
| `docs/agent-system/engine-journal/INDEX.md` | `ENGINE_JOURNAL_INDEX.md` |
| `docs/agent-system/CURRENT_STATE.md` | `CURRENT_STATE.md` |
| `docs/agent-system/NEXT_STEPS.md` | `NEXT_STEPS.md` |

## Upload how-to

### Chat UI / browser upload

1. Открыть `docs/agent-system/cloud/`.
2. Загрузить все файлы из папки целиком, если интерфейс допускает текущий `file_count_including_readme`.
3. Если нужен incremental refresh, загрузить только изменённые flat-файлы из per-task handoff и этот `README.md`.

### Google Drive for Desktop

1. Архитектор настраивает Google Drive for Desktop в своей пользовательской сессии.
2. Создаёт папку Drive, например `Agent System / orchestrator-context-cloud`.
3. Копирует содержимое `docs/agent-system/cloud/` в эту папку штатными средствами ОС.
4. Проверяет в Drive UI, что количество файлов совпадает с `file_count_including_readme`.

### rclone template

Engine не выполняет авторизацию и не создаёт token files. Команды ниже — шаблон для архитектора после самостоятельной настройки remote:

```text
rclone config
rclone copy docs/agent-system/cloud/ <drive-remote>:orchestrator-context-cloud --dry-run
rclone copy docs/agent-system/cloud/ <drive-remote>:orchestrator-context-cloud
```

`<drive-remote>` — имя remote, созданное архитектором локально. Credentials/tokens не хранить в repository.
