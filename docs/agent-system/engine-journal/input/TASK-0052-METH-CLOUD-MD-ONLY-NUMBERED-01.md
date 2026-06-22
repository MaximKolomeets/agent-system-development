# TASK-0052: METH-CLOUD-MD-ONLY-NUMBERED-01

## Режим

Роль: tooling-maintainer. Исполнитель: на усмотрение архитектора. Reasoning effort: высокий. Branch-guard обязателен.

Batch-policy: открытые journal-записи не являются blocker; closure не смешивать.

## Цель

Сделать `docs/agent-system/cloud/` uploadable-бандлом для cloud-оркестратора, который принимает только `.md`: все файлы должны быть numbered `.md`, non-md источники заворачиваются в fenced-блок, а `00_README.md` задаёт карту приоритетов.

## Repo / ветки

- Репозиторий: `MaximKolomeets/agent-system-development`
- Каталог: `C:\neural\repos\agent-system-development`
- base: `developer`
- work: `work/tooling-maintainer-01/cloud-md-only-numbered-01`

## Allowed files

- `docs/agent-system/tools/gen_cloud_bundle.py`
- `docs/agent-system/cloud/**`
- `docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml`
- `docs/agent-system/PROJECT_FILE_MAP.md`
- `docs/agent-system/engine-journal/INDEX.md`
- `docs/agent-system/engine-journal/input/TASK-0052-METH-CLOUD-MD-ONLY-NUMBERED-01.md`
- `docs/agent-system/engine-journal/output/RESULT-0052-METH-CLOUD-MD-ONLY-NUMBERED-01.md`

## Требования

1. Cloud-файлы имеют только `.md`.
2. Имя файла: `NN_<FLAT>[_<EXT>].md`.
3. `00_README.md` содержит map table: `priority | cloud filename | source path | category`.
4. `ADOPTION_TRANSFER_MANIFEST.yml` остаётся source-файлом, но в cloud пишется как `08_ADOPTION_TRANSFER_MANIFEST_yml.md` с fenced `yaml`.
5. Генератор `--check` валидирует схему имён, непрерывную нумерацию, content-parity и source existence.
6. Manifest и `PROJECT_FILE_MAP.md` консистентны с новым generated inventory.

## Проверки

- `python docs/agent-system/tools/gen_cloud_bundle.py --check`
- `python docs/agent-system/tools/gen_file_map.py --check`
- в `docs/agent-system/cloud/` нет non-md и ненумерованных файлов
- manifest cloud-пути совпадают с фактическими cloud-файлами
- `git diff --check`
- branch guard

## Передача

Следующий: `reviewer` — review (все cloud `.md` + numbered, нумерация по канон-порядку, non-md -> fenced, manifest/file-map консистентны, оба `--check` 0); затем архитектор — merge; затем engine — Шаг 2 `METH-CLOUD-HANDOFF-NAMES-01` (footer canon ссылается на numbered cloud-имена); journal closure — batch перед release.
