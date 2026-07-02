# AGENT_PROPOSAL_TEMPLATE

Шаблон инициативного предложения агента. Использовать для раздела
`## Unprompted Project Proposals` в RESULT/final report или как основу для
backlog/MIR triage.

## Сводка

- Идентификатор: `proposal-YYYY-NNN`
- Источник: `engine_result` / `review` / `target_dry_run` / `operator_feedback`
- Роль-источник: `methodology-architect-01` / `code-reviewer-01` / `qa-reviewer-01` / `security-reviewer-01` / другая роль
- Статус: `proposed`

## Паттерн проблемы

Описать повторяемый pattern проблемы без private/project-specific деталей.

## Почему вне scope

Объяснить, почему это не должно чиниться внутри текущей задачи.

## Рекомендуемый outcome

- Тип: `backlog_candidate` / `MIR_candidate` / `separate_review` / `separate_implementation_task`
- Рекомендуемая роль-владелец: `orchestrator` / `methodology-architect-01` / `docs-maintainer-01` / `reviewer`
- Затронутая поверхность: docs/templates/tools/policy

## Evidence

Указать безопасное evidence: filenames, policy names, public docs или aggregate
counts. Не вставлять secret values, private URLs, customer data, raw logs или
target source snippets.

## Acceptance Criteria

- Критерий 1.
- Критерий 2.
- Критерий 3.

## Safety And Privacy

- Private data удалены: `yes` / `no` / `not_applicable`.
- Public methodology repository безопасен: `yes` / `no`.
- Human decision требуется: `yes` / `no`.

## Backlog Or MIR Routing

- Рекомендуемый route: `BACKLOG.md` / `METHODOLOGY_IMPROVEMENT_LEDGER.md` / `не добавлять`.
- Причина route.

## Передача

Следующий: orchestrator/architect — принять disposition и при необходимости
создать отдельную scoped task.
