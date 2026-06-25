# Orchestrator Context Cloud Bundle

AUTO-GENERATED — не править руками; регенерировать через `python docs/agent-system/tools/gen_cloud_bundle.py`.

## Freshness

- asof: `2026-06-25T08:32:26+07:00`
- developer_head_sha: `6213ab21bab31a736aee389f6509a2254769fcab`
- file_count_including_readme: `12`

## Контракт

- Источник состава: `docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml` → `orchestrator_context_bundle`.
- Все файлы бандла имеют расширение `.md`, чтобы проходить upload-ограничения cloud-оркестратора.
- Нумерация задаёт приоритет: при лимите ниже полного бандла загружать первые N файлов по имени.
- Non-md источники завернуты в fenced-блок с языком исходного формата.
- Проверка drift: `python docs/agent-system/tools/gen_cloud_bundle.py --check`.

## Приоритетная карта

| priority | cloud filename | source path | category |
| --- | --- | --- | --- |
| `00` | `00_README.md` | generated bundle guide | generated |
| `01` | `01_ORCHESTRATOR_OPERATING_CONTRACT.md` | `docs/agent-system/ORCHESTRATOR_OPERATING_CONTRACT.md` | `source` |
| `02` | `02_ORCHESTRATOR_RESPONSE_STANDARD.md` | `docs/agent-system/ORCHESTRATOR_RESPONSE_STANDARD.md` | `source` |
| `03` | `03_TASK_HEADER_COMMON.md` | `docs/agent-system/templates/TASK_HEADER_COMMON.md` | `template` |
| `04` | `04_BRANCH_POLICY.md` | `docs/agent-system/BRANCH_POLICY.md` | `source` |
| `05` | `05_ENGINE_JOURNAL_CONTRACT.md` | `docs/agent-system/ENGINE_JOURNAL_CONTRACT.md` | `source` |
| `06` | `06_CURRENT_STATE.md` | `docs/agent-system/CURRENT_STATE.md` | `history_state` |
| `07` | `07_ENGINE_JOURNAL_INDEX.md` | `docs/agent-system/engine-journal/INDEX.md` | `journal` |
| `08` | `08_NEXT_STEPS.md` | `docs/agent-system/NEXT_STEPS.md` | `history_state` |
| `09` | `09_ENGINE_ENTRYPOINT.md` | `docs/agent-system/ENGINE_ENTRYPOINT.md` | `source` |
| `10` | `10_PROJECT_FILE_MAP.md` | `docs/agent-system/PROJECT_FILE_MAP.md` | `generated` |
| `11` | `11_ADOPTION_TRANSFER_MANIFEST_yml.md` | `docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml` | `source` |

## Частичная загрузка

Если engine принимает меньше файлов, чем полный бандл, загрузить `00_README.md` и первые N numbered-файлов по лексическому порядку. Двузначный префикс сохраняет правильный порядок при `10+` файлах.

## Upload how-to

### Chat UI / browser upload

1. Открыть `docs/agent-system/cloud/`.
2. Загрузить все `.md` файлы из папки целиком, если интерфейс допускает текущий `file_count_including_readme`.
3. Если нужен incremental refresh, загрузить изменённые numbered-файлы из per-task handoff и этот `00_README.md`.

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
