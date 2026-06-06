# ROLE_MODEL

## dev-implementer-01

- исполнитель задач разработки;
- engine может быть Codex, Claude Code, локальная LLM, человек или другой инструмент;
- не принимает архитектурные решения самостоятельно.

## solution-architect-01

- архитектура;
- декомпозиция крупных задач;
- предложения;
- риски;
- не запускает `dev-implementer-01` напрямую.

## qa-reviewer-01

- проверка качества;
- тесты;
- регрессии;
- review reports;
- не исправляет код без отдельного задания.

## security-reviewer-01

- секреты;
- forbidden files;
- `.env` policy;
- branch/ruleset recommendations.

## docs-maintainer-01

- актуальность документации;
- `CURRENT_STATE`;
- `NEXT_STEPS`;
- Source summaries;
- prompts for next chat.
