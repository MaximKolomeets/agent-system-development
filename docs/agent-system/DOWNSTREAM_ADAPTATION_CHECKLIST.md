# DOWNSTREAM_ADAPTATION_CHECKLIST

## Repository identity

- [ ] Repository name заменен на имя target repository.
- [ ] Repository visibility подтверждена отдельно от methodology repository.
- [ ] Project purpose переписан под target repository.
- [ ] Public/private publication constraints зафиксированы.
- [ ] Private data не переносится в public methodology repository.
- [ ] `agent-system-development` описан как methodology/template repository, а не как центральный repository управления target repository.

## Engine task header

- [ ] Задачи для `engine` формулируются на русском языке.
- [ ] Шапка использует формат `Задача для <agent-name>: <task-id>`.
- [ ] `<agent-name>` является role-based именем назначенного агента.
- [ ] `<task-id>` связан с GitHub issue, Pull Request, task id или внутренним номером работы проекта.
- [ ] Шапка содержит запуск, модель, reasoning, режим работы и причину выбора режима.

## Branch model

- [ ] Фактические branches target repository проверены.
- [ ] Выбрана модель `developer`, `develop`, `main`-only flow или другая.
- [ ] `BRANCH_POLICY.md` адаптирован под target repository.
- [ ] `WORKFLOW.md` и `PR_WORKFLOW.md` адаптированы.
- [ ] Task templates используют реальные branch names.
- [ ] GitHub Actions branch filters проверены.

## State documents

- [ ] `CURRENT_STATE.md` переписан по фактам target repository.
- [ ] `NEXT_STEPS.md` переписан по текущему плану target repository.
- [ ] `DECISION_LOG.md` содержит только решения target repository.
- [ ] Template repository state не скопирован verbatim.
- [ ] Worktree paths заменены на target repository paths.

## Project governance pack

- [ ] `PROJECT_DASHBOARD.md` создан или адаптирован.
- [ ] `ROADMAP.md` создан или адаптирован.
- [ ] `BACKLOG.md` создан.
- [ ] `CURRENT_STATE.md` переписан по фактам target repository.
- [ ] `NEXT_STEPS.md` отражает текущий план.
- [ ] `DECISION_LOG.md` не скопирован verbatim.
- [ ] `PROJECT_GUARDRAILS.md` фиксирует goal, non-goals и forbidden scope.
- [ ] `ENGINE_REGISTRY.md` отделяет agent roles от engines.
- [ ] Branch pattern не содержит vendor/tool names.
- [ ] После PR обновляются state docs.

## Transfer manifest consistency

- [ ] Transfer manifest не содержит противоречий между reusable templates и target-adapted files.
- [ ] Reusable source templates отделены от materialized target files.

## Security

- [ ] `.env` не читался и не переносился.
- [ ] `.env.*` не переносились, кроме безопасного `.env.example`.
- [ ] `.venv/`, `data/`, `runtime/`, `dist/`, `backups/`, `exports/` не коммитятся.
- [ ] Реальные credentials, tokens, passwords и API keys отсутствуют.
- [ ] Sensitive grep выполнялся только filename-only.
- [ ] Matching lines sensitive grep не печатались.

## Adoption mode

- [ ] Выбран режим `audit-only`, `docs-only adoption` или `runtime adoption`.
- [ ] Для первого dry run выбран `audit-only`, если пользователь не решил иначе.
- [ ] Minimal first PR создает только `docs/agent-system/ADOPTION_AUDIT.md`.
- [ ] Docs-only adoption не содержит runtime changes.
- [ ] Runtime adoption имеет отдельное архитектурное решение, ветку и PR.

## Review

- [ ] `ADOPTION_TRANSFER_MANIFEST.yml` применен как transfer map.
- [ ] Local `AGENTS.md` target repository имеет приоритет.
- [ ] Ссылки на methodology repository не раскрывают private data.
- [ ] Final report содержит Methodology feedback.
- [ ] Methodology feedback сформулирован нейтрально.
- [ ] Проверено отсутствие verbatim copy template state.
