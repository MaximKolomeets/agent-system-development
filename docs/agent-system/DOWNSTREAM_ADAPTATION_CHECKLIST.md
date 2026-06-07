# DOWNSTREAM_ADAPTATION_CHECKLIST

## Repository identity

- [ ] Repository name заменен на имя target repository.
- [ ] Repository visibility подтверждена отдельно от methodology repository.
- [ ] Project purpose переписан под target repository.
- [ ] Public/private publication constraints зафиксированы.
- [ ] Private data не переносится в public methodology repository.

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
