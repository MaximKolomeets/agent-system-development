# DOWNSTREAM_ADAPTATION_CHECKLIST

Этот файл — отдельный pre-merge gate (чеклист) для docs-only adoption и review. Он не дублирует правила прозой, а проверяет их пунктами. Канон самих правил:

- режимы adoption, transfer manifest, branch-flow (`developer`/`develop`/`main-only flow`), minimal first PR, пошаговый existing-repo adoption — `docs/agent-system/ADOPTION_GUIDE.md`;
- `methodology_reference` — `docs/agent-system/ENGINE_ENTRYPOINT.md` → раздел «Methodology reference»;
- source snapshot drift — `docs/agent-system/source/README.md`;
- feedback и его sanitization — `docs/agent-system/METHODOLOGY_FEEDBACK_LOOP.md`;
- governance pack и project constitution — `docs/agent-system/TARGET_PROJECT_GOVERNANCE_PACK.md`, `docs/agent-system/PROJECT_CONSTITUTION_FRAMEWORK.md`.

Пункты ниже сохранены полностью как проверяемый список.

## Идентичность repository

- [ ] Repository name заменен на имя target repository.
- [ ] Repository visibility подтверждена отдельно от methodology repository.
- [ ] Project purpose переписан под target repository.
- [ ] Public/private publication constraints зафиксированы.
- [ ] Private data не переносится в public methodology repository.
- [ ] `agent-system-development` описан как methodology/template repository, а не как центральный repository управления target repository.

## Шапка задачи исполнителя (engine)

- [ ] Задачи для `engine` формулируются на русском языке.
- [ ] Шапка использует формат `Задача для <роль>: <task-id>`.
- [ ] `<роль>` является vendor-neutral ролью назначенного исполнителя.
- [ ] `<task-id>` связан с GitHub issue, Pull Request, task id или внутренним номером работы проекта.
- [ ] Шапка содержит запуск, модель, reasoning, режим работы и причину выбора режима.

## Модель веток (branch model)

- [ ] Определен lifecycle mode: `new empty bootstrap` или `existing adoption`.
- [ ] Определена selected branch model.
- [ ] Фактические branches target repository проверены.
- [ ] Выбрана модель `developer`, `develop`, `main`-only flow или другая.
- [ ] Для `standard developer workflow` подтвержден `developer`.
- [ ] Если `developer` отсутствовал, bootstrap creation явно разрешен и зафиксирован.
- [ ] `Fallback-to-main` запрещен для `standard developer workflow`.
- [ ] `BRANCH_POLICY.md` адаптирован под target repository.
- [ ] `WORKFLOW.md` и `PR_WORKFLOW.md` адаптированы.
- [ ] Task templates используют реальные branch names.
- [ ] GitHub Actions branch filters проверены.

## Документы состояния (state documents)

- [ ] `CURRENT_STATE.md` переписан по фактам target repository.
- [ ] `NEXT_STEPS.md` переписан по текущему плану target repository.
- [ ] `DECISION_LOG.md` содержит только решения target repository.
- [ ] Template repository state не скопирован verbatim.
- [ ] Worktree paths заменены на target repository paths.

## Набор governance для проекта (project governance pack)

- [ ] `PROJECT_CONSTITUTION.md` создан по фактам target repository.
- [ ] Mission и success criteria зафиксированы.
- [ ] Current strategic goal ровно одна и актуальна.
- [ ] Out-of-scope явно запрещает новые продукты, платформы, сервисы и направления без approval.
- [ ] Decision Authority содержит Level 1 Implementation, Level 2 Subsystem, Level 3 Architecture и Level 4 Project Strategy.
- [ ] Level 3+ требует explicit user approval.
- [ ] Scope Expansion Control содержит No scope expansion, Minor scope expansion и Major scope expansion.
- [ ] Major scope expansion требует остановки и решения пользователя.
- [ ] `PROJECT_DASHBOARD.md` создан или адаптирован.
- [ ] `ROADMAP.md` создан или адаптирован.
- [ ] `BACKLOG.md` создан.
- [ ] `CURRENT_STATE.md` переписан по фактам target repository.
- [ ] `NEXT_STEPS.md` отражает текущий план.
- [ ] `DECISION_LOG.md` не скопирован verbatim.
- [ ] `PROJECT_GUARDRAILS.md` фиксирует goal, non-goals и forbidden scope.
- [ ] `ENGINE_REGISTRY.md` отделяет agent roles от engines.
- [ ] `ENGINE_REGISTRY.md` содержит Agent Authority Matrix: allowed scope, forbidden scope и approval required.
- [ ] Branch pattern не содержит vendor/tool names.
- [ ] После PR обновляются state docs.

## Чеклист governance-review (governance review checklist)

- [ ] Изменение соответствует mission.
- [ ] Изменение соответствует current strategic goal.
- [ ] Изменение не нарушает out-of-scope.
- [ ] Изменение не меняет architecture level без approval.
- [ ] Требуется ли explicit user approval проверено.

## Включение external/code review

- [ ] Selected reviewer role defined: `code-reviewer-01`, `qa-reviewer-01` или `security-reviewer-01`.
- [ ] Имя исполнителя (engine) отделено от role name.
- [ ] Branch namespace is `work/<role>/*`.
- [ ] Report path is target-local.
- [ ] Review-only scope confirmed.
- [ ] Fixes split into separate implementation PRs.
- [ ] No vendor-specific branches/reports.
- [ ] Sensitive grep result is filename-only.
- [ ] Report uses Critical, Important, Optional findings categories.

## Языковая согласованность

- [ ] Governance docs use one primary human language.
- [ ] For Russian-language projects, governance docs are in Russian.
- [ ] Prompts исполнителя (engine) и agent reports написаны на русском.
- [ ] English is preserved for paths, commands, code identifiers, config keys, package names, API names, vendor/tool names.
- [ ] Mixed-language sections are either justified or normalized.

## Согласованность комментариев

- [ ] New or changed scripts contain Russian comments for non-obvious and safety-critical lines/blocks.
- [ ] Git, branch, push, merge, deletion, remote and security-check commands are commented.
- [ ] Workflow/config files use comments where the format supports comments.
- [ ] Formats that do not support comments use adjacent documentation or schema descriptions.
- [ ] Comments explain what the line/block does and why it exists.
- [ ] Comments do not include secrets, private data or downstream project names.

## Свежесть методологии

- [ ] Оркестратор проверил актуальный `agent-system-development` перед подготовкой engine task.
- [ ] Исполнитель (engine) синхронизировал или свежо прочитал `agent-system-development` перед применением methodology.
- [ ] If sync/check was impossible, the limitation is stated in the report.
- [ ] Methodology feedback is neutral and does not reveal private data.

## Согласованность transfer manifest

- [ ] Transfer manifest не содержит противоречий между reusable templates и target-adapted files.
- [ ] Reusable source templates отделены от materialized target files.

## Безопасность (security)

- [ ] `.env` не читался и не переносился.
- [ ] `.env.*` не переносились, кроме безопасного `.env.example`.
- [ ] `.venv/`, `data/`, `runtime/`, `dist/`, `backups/`, `exports/` не коммитятся.
- [ ] Реальные credentials, tokens, passwords и API keys отсутствуют.
- [ ] Sensitive grep выполнялся только filename-only.
- [ ] Matching lines sensitive grep не печатались.

## Режим adoption (adoption mode)

- [ ] Выбран режим `audit-only`, `docs-only adoption` или `runtime adoption`.
- [ ] Для первого dry run выбран `audit-only`, если пользователь не решил иначе.
- [ ] Minimal first PR создает только `docs/agent-system/ADOPTION_AUDIT.md`.
- [ ] Docs-only adoption не содержит runtime changes.
- [ ] Runtime adoption имеет отдельное архитектурное решение, ветку и PR.

## Проверка (review)

- [ ] `ADOPTION_TRANSFER_MANIFEST.yml` применен как transfer map.
- [ ] Local `AGENTS.md` target repository имеет приоритет.
- [ ] Ссылки на methodology repository не раскрывают private data.
- [ ] Final report содержит Methodology feedback.
- [ ] Methodology feedback сформулирован нейтрально.
- [ ] Проверено отсутствие verbatim copy template state.
