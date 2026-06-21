# TASK-0034 — METH-DEPERS-COMPLETE-01

## Задача

Задача для docs-maintainer: METH-DEPERS-COMPLETE-01.

Рекомендуемый режим исполнения:

Роль: docs-maintainer.
Исполнитель: на усмотрение архитектора.
Reasoning effort: средний.
Запуск: Local only.
Режим: Agent.
Почему: нужно отличить vendor-остаток от обычного слова «модель» и сохранить branch guard.

## Repository

- Repository: MaximKolomeets/agent-system-development
- Local path: `C:\neural\repos\agent-system-development`
- Base branch: `developer`
- Working branch: `work/docs-maintainer-01/depers-complete-01`
- Baseline SHA: `3fd579ab107387a7e26e7938828c3aa5ddff1273`
- Checked at: `2026-06-21T15:52:11+07:00`

## Scope

Allowed files:

- `docs/agent-system/templates/TASK_HEADER_COMMON.md`
- `docs/agent-system/ENGINE_ENTRYPOINT.md`
- `docs/agent-system/NEW_PROJECT_ONBOARDING_GUIDE.md`
- `AGENTS.md`
- `docs/agent-system/BRANCH_POLICY.md`
- `docs/agent-system/CODE_REVIEW_WORKFLOW.md`
- `docs/agent-system/engine-journal/input/TASK-0034-METH-DEPERS-COMPLETE-01.md`
- `docs/agent-system/engine-journal/output/RESULT-0034-METH-DEPERS-COMPLETE-01.md`
- `docs/agent-system/engine-journal/INDEX.md`

Forbidden:

- любые файлы вне whitelist;
- закрытие или переписывание прошлых journal-записей;
- ослабление prohibition/safety правил;
- чтение `.env`;
- прямые изменения `main` или `developer`.

## Required changes

1. Убрать legacy placeholder имени агента как эквивалент роли: канон в active docs должен быть `Задача для <роль>: <task-id>`.
2. В `ENGINE_ENTRYPOINT.md` и `NEW_PROJECT_ONBOARDING_GUIDE.md` заменить legacy header с именем агента на `Задача для <роль>`.
3. Vendor-примеры в prohibition-строках `AGENTS.md` и `BRANCH_POLICY.md` заменить на neutral placeholder `<vendor-name>`, не ослабляя запрет.
4. В `CODE_REVIEW_WORKFLOW.md` проверить `Модель:`:
   - если это обычное слово «модель», не менять;
   - если это vendor/header label `Модель: <имя исполнителя>`, заменить на `Reasoning effort`;
   - зафиксировать depers-check правило, что bare-слово «модель» без vendor/tool name не является vendor-marker.

## Checks

- grep legacy placeholder имени агента по operational scope должен вернуть 0.
- grep явных vendor-token patterns из задачи по operational scope должен вернуть 0.
- `git diff --name-only developer...HEAD` и working-tree diff должны оставаться в whitelist.
- `git diff --check`.
- `git rev-parse --abbrev-ref HEAD` должен быть `work/docs-maintainer-01/depers-complete-01`.

## STOP

- HEAD не `work/docs-maintainer-01/depers-complete-01`.
- Нужно изменить файл вне whitelist.
- Working tree dirty перед sync/checkout/switch/pull/merge.
- Prohibition/safety правило требует ослабления.

## Передача

Следующий: reviewer — review; затем архитектор — merge; затем engine — METH-MANIFEST-PARITY-01; journal closure — batch перед release.
