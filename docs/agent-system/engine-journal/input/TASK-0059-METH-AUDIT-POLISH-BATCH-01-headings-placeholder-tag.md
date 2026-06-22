# TASK-0059-METH-AUDIT-POLISH-BATCH-01

Задача для docs-maintainer: METH-AUDIT-POLISH-BATCH-01

## Рекомендуемый режим исполнения

Роль: docs-maintainer
Исполнитель: на усмотрение архитектора
Reasoning effort: высокий
Запуск: Local only
Режим: Agent

## Цель

Закрыть оставшуюся полировку перед release:

- H: уточнить семантику placeholder-scan;
- B-doc: разрешить release tag на `main` как дополнительный human-readable anchor рядом с commit SHA в `methodology_reference`;
- A: выполнить узкий RU-headings pass по adopter-facing канонам/гайдам без массового перевода core-контрактов.

Docs-only. Код генераторов и `.gitattributes` не менять.

## Preconditions

- Base branch: `developer`
- Work branch: `work/docs-maintainer-01/audit-polish-batch-01`
- Запуск после merge PR #199..#202; подтвердить через local git + `gh`.
- `docs/agent-system/engine-journal/INDEX.md` содержит seq 0055..0058.
- `python docs/agent-system/tools/gen_file_map.py --check` и `python docs/agent-system/tools/gen_cloud_bundle.py --check` проходят на текущем checkout.

## Разрешённые файлы

- `docs/agent-system/ENGINE_JOURNAL_CONTRACT.md`
- `docs/agent-system/ENGINE_ENTRYPOINT.md`
- adopter-facing docs части A:
  - `docs/agent-system/ADOPTION_GUIDE.md`
  - `docs/agent-system/NEW_PROJECT_ONBOARDING_GUIDE.md`, если есть однозначные descriptive headings
  - `docs/agent-system/templates/ADOPTION_PROMPT.md`, если есть однозначные descriptive headings
  - `docs/agent-system/templates/TARGET_PROJECT_GOVERNANCE_PACK_TEMPLATE.md`
  - `docs/agent-system/templates/PROJECT_CONSTITUTION_TEMPLATE.md`
  - `docs/agent-system/DOWNSTREAM_ADAPTATION_CHECKLIST.md`
- `docs/agent-system/engine-journal/input/TASK-0059-METH-AUDIT-POLISH-BATCH-01-headings-placeholder-tag.md`
- `docs/agent-system/engine-journal/output/RESULT-0059-METH-AUDIT-POLISH-BATCH-01-headings-placeholder-tag.md`
- `docs/agent-system/engine-journal/INDEX.md`
- `docs/agent-system/cloud/**` (регенерация через `gen_cloud_bundle.py`)

## Запрещено

- Менять `gen_file_map.py`, `gen_cloud_bundle.py`, `.gitattributes`.
- Массово переводить headings вне adopter-facing набора.
- Переписывать append-only history.
- Менять `ADOPTION_TRANSFER_MANIFEST.yml` или `PROJECT_FILE_MAP.md`.
- Трогать `main`/`developer` напрямую, runtime/CI/secrets/.env/private downstream data, force push, удалять/перезаписывать TASK/RESULT.

## Проверки

- `python docs/agent-system/tools/gen_file_map.py --check`
- `python docs/agent-system/tools/gen_cloud_bundle.py --check`
- active internal link-check: broken links 0
- `git diff --check`
- Branch guard перед commit.

## Передача

Следующий: reviewer — проверить H/B-doc/A, что placeholder-scan правило не флагует legitimate templates/examples, tag является дополнительным pointer, RU-headings pass узкий и anchors не сломаны; затем архитектор — merge PR; затем engine — batch-closure journal 0055..0059; затем state-refresh + оба `--check`; затем release `developer -> main` (мержит архитектор) + tag; затем sync.
