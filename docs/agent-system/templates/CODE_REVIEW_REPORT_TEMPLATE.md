# <task-id> - code review report

## Summary

Кратко описать scope review, общий вывод и главный риск.

## Repository snapshot

- Repository:
- Local path:
- Remote:
- Base branch:
- Head branch:
- Commit SHA:
- Working tree status:

## Branch model

Указать selected branch model и подтвердить, что reviewer branch создан от разрешенной base branch.

## Project description

Кратко описать назначение repository без private downstream data.

## Architecture overview

Кратко описать основные компоненты, границы и зависимости.

## Entry points

Перечислить основные entry points, команды, workflows или документы, с которых начинается работа.

## Dependency and tooling overview

Кратко описать package managers, runtimes, linters, tests и внешние инструменты, если они обнаружены без чтения forbidden files.

## Tests and quality gates

Описать доступные tests/linters/CI checks и что фактически было выполнено.

## Security and secret-handling observations

Описать observations по forbidden paths, `.env` policy, credentials/tokens/passwords и sensitive grep filename-only result.

## Findings

### Critical

- Нет findings.

### Important

- Нет findings.

### Optional

- Нет findings.

## Recommendations

Перечислить рекомендации без внесения code fixes.

## Proposed next PRs

Для каждого proposed PR указать:

- role:
- branch:
- scope:
- reason:

## Checks executed

Перечислить команды и краткий результат.

## Checks not executed and why

Перечислить tests/linters/checks, которые не запускались, и причину.

## Forbidden paths result

Указать filename-only результат проверки forbidden paths.

## Sensitive grep result

Указать только filenames или `no matches`. Matching lines не печатать.

## Scope boundaries

Подтвердить, что reviewer не менял production code, runtime, Docker, CI, scripts, dependencies и forbidden files.

## Reviewer notes

Дополнительные замечания reviewer.
