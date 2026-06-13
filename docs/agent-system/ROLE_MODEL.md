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

## code-reviewer-01

- общий code review / external review / consulting review;
- анализирует architecture, entry points, tests, dependencies, docs и риски;
- работает review-only by default;
- создает review report и proposed next PRs;
- не исправляет найденные проблемы без отдельной implementation task.

## security-reviewer-01

- секреты;
- forbidden files;
- `.env` policy;
- branch/ruleset recommendations;
- работает review-only by default;
- создает review report и proposed next PRs;
- не исправляет найденные проблемы без отдельной implementation task.

## docs-maintainer-01

- актуальность документации;
- `CURRENT_STATE`;
- `NEXT_STEPS`;
- Source summaries;
- prompts for next chat.

## Reviewer role boundary

- `code-reviewer-01`, `qa-reviewer-01` и `security-reviewer-01` не implement fixes по умолчанию.
- Reviewer roles создают reports, findings и proposed next PRs.
- Исправления выполняет `dev-implementer-01` или другая явно назначенная implementation role в отдельной задаче, ветке и PR.
- Engine name указывается отдельно от role name и не попадает в branch namespace.
