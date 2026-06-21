# AGENT_RESEARCH_TASK_TEMPLATE

## Общий header

Заполнить общий header по канону `docs/agent-system/templates/TASK_HEADER_COMMON.md`:

- Mandatory header (`Задача для <роль>: <task-id>` + role-agnostic блок рекомендуемого режима исполнения: роль / исполнитель «на усмотрение архитектора» / reasoning effort / запуск / режим / почему);
- Russian-first;
- Рекомендуемый режим исполнения (без имён инструментов/моделей);
- Передача (отчёт заканчивается блоком `Следующий: <роль> — <что делает>`);
- Source-reminder (при изменении методологии/канонов — применить канон `docs/agent-system/templates/TASK_HEADER_COMMON.md` → «Source-reminder»);
- Verified Baseline;
- Проверка полноты copy/paste;
- Project constitution check.

Ниже — секции, специфичные для исследовательской задачи.

## Research ID

Указать идентификатор исследования.

## Hypothesis

Сформулировать проверяемую гипотезу.

## Scope

Описать границы исследования.

## Files to inspect

Перечислить файлы для чтения.

## Forbidden actions

Описать запрещенные действия.

## Expected output

Описать ожидаемый результат исследования.

Отчёт обязан заканчиваться блоком «Передача» по канону `docs/agent-system/templates/TASK_HEADER_COMMON.md` → «Передача» (`Следующий: <роль> — <что делает>`). Если исследование меняло методологию/каноны — применить Source-reminder по канону `docs/agent-system/templates/TASK_HEADER_COMMON.md` → «Source-reminder».
