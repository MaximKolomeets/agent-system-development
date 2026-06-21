# Задача для docs-maintainer-01: METH-ADOPTION-TEMPLATES-SYNC-01

## Режим

Роль: docs-maintainer.
Исполнитель: на усмотрение архитектора.
Reasoning effort: высокий.
branch-guard.

Batch-policy: открытые journal-записи не блокируют; closure не подмешивать.

## Цель

Привести adoption-шаблоны к текущему `ADOPTION_TRANSFER_MANIFEST.yml`:
устаревшие manifest categories убрать из живого adoption scope, а adoption task
templates дополнить явным требованием Source Delta.

## Discovery

- Сначала проверить устаревшие manifest categories в `docs/agent-system`,
  `docs/agent-system/templates` и `README.md`.
- Исторические попадания в `docs/agent-system/engine-journal/**` не редактировать:
  journal append-only.
- Проверить, какие adoption task templates не содержат `Source Delta`.
- Авторитетные текущие categories: `source`, `template`, `target_generated`,
  `history_state`, `journal`, `scaffold`, `generated`.

## Allowed files

- `docs/agent-system/ADOPTION_GUIDE.md`
- `docs/agent-system/templates/ADOPTION_PROMPT.md`
- `docs/agent-system/templates/ADOPTION_AUDIT_TASK_TEMPLATE.md`
- `docs/agent-system/templates/DOCS_ONLY_ADOPTION_TASK_TEMPLATE.md`
- `docs/agent-system/engine-journal/INDEX.md`
- `docs/agent-system/engine-journal/input/TASK-0041-METH-ADOPTION-TEMPLATES-SYNC-01.md`
- `docs/agent-system/engine-journal/output/RESULT-0041-METH-ADOPTION-TEMPLATES-SYNC-01.md`

## Изменения

- Старые adoption category references заменить на текущие manifest categories и
  adoption rules:
  - `target_generated` создаётся в target repository и не ищется как source path;
  - `history_state` не копируется verbatim;
  - `journal` переносится только как scaffold/templates, без operational rows;
  - `generated` регенерируется, не копируется руками;
  - `source` и `template` проверяются на наличие в source checkout.
- В `ADOPTION_AUDIT_TASK_TEMPLATE.md` и `DOCS_ONLY_ADOPTION_TASK_TEMPLATE.md`
  добавить явное требование Source Delta в Copy/Paste checklist, checks и final report/result requirements.

## Проверки

- operational `rg` устаревших categories вне `engine-journal/**` -> 0.
- `rg --files-without-match "Source Delta"` по двум adoption task templates -> 0 files.
- `python docs/agent-system/tools/gen_file_map.py --check` -> exit 0.
- `git diff --check` -> clean.
- diff только whitelist.
- branch guard: HEAD == `work/docs-maintainer-01/adoption-templates-sync-01`.

## Передача

Следующий: reviewer — review (старых категорий 0 в operational scope; Source Delta
в adoption-шаблонах; маппинг old→new по смыслу верен); затем архитектор —
merge; затем engine — FIX-5 (closure-index clarify); journal closure — batch
перед release.
