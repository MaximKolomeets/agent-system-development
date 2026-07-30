# RATIONALE-0169-METH-AUTONOMOUS-TERMINAL-EXECUTION-PROTOCOL-01

Связанный TASK file: `docs/agent-system/engine-journal/input/TASK-0169-METH-AUTONOMOUS-TERMINAL-EXECUTION-PROTOCOL-01.md`
Связанный RESULT file: `docs/agent-system/engine-journal/output/RESULT-0169-METH-AUTONOMOUS-TERMINAL-EXECUTION-PROTOCOL-01.md`
Номер sequence: 0169
Идентификатор задачи: METH-AUTONOMOUS-TERMINAL-EXECUTION-PROTOCOL-01
authoring_role: dev-implementer-01
actor_type: agent
Статус обоснования: finalized_for_review
raw_chain_of_thought_stored: no

## Решаемый вопрос

Как сделать terminal execution substantive Engine-задач единообразным, не
превращая semantic decision в хрупкий machine validator и не ослабляя уже
действующие continuation, security и human-merge safeguards.

## Контекст и evidence

`EXECUTION_CONTINUATION_POLICY.md` уже различает new task, continuation,
fix-pass и journal finalization. Он не нормирует полный decision fallback,
statuses findings, dependency closure и разделённые iteration budgets. Новый
protocol закрывает этот semantic gap, а related contracts/templates делают его
применимым для последующих задач.

## Ограничения и инварианты

Нельзя менять branch architecture, human-only merge, release/tag authority,
security boundaries или product scope. Machine enforcement допустим только для
устойчиво проверяемых structural facts; semantic diagnosis остаётся explicit
responsibility engine и reviewer.

## Рассмотренные варианты

1. Расширить `EXECUTION_CONTINUATION_POLICY.md` до единого большого канона.
2. Добавить строгий validator для semantic STOP decisions.
3. Создать отдельный terminal-execution protocol и связать его с contracts,
   templates, manifest и existing continuation policy.

## Выбранный путь

Выбран вариант 3. Новый document является authoritative source terminal
outcome, а continuation policy сохраняет узкую ответственность за identity,
dirty scope и bounded continuation. Machine tools не получают semantic
heuristics, способные дать ложный blocker.

## Причины выбора

Разделение делает два слоя понятными: безопасное право продолжать уже начатую
работу и обязанность довести substantive task до PR/STOP. Dependency closure
явно включает manifest, capacity и generated mirrors, поэтому source addition
не оставляет скрытого generated drift.

## Отклонённые альтернативы

Вариант 1 смешал бы two distinct responsibilities в уже используемом policy.
Вариант 2 потребовал бы ненадёжно выводить смысл owner decision из prose и мог
бы заблокировать безопасную работу ложным finding.

## Компромиссы, последствия и риски

Protocol требует от author TASK явно указывать budgets и envelope, что делает
prompt длиннее. Это компенсируется воспроизводимым terminal report и отсутствием
бесконечных retry loops. Residual risk нельзя использовать как замену acceptance
outcome.

## Предположения, неопределённости и confidence

Предполагается, что review feedback остаётся в task PR и действует existing
`REVIEW_AUTOLOOP.md`. Confidence: high, потому что новый canon не меняет
машинные guards, а связывает уже существующие boundaries.

## Условия пересмотра или rollback triggers

Пересмотр требуется, если практика покажет, что конкретный budget либо
dependency closure нуждается в новом machine-readable field. Такое изменение
должно идти отдельной задачей с validator/tests scope.

## Что явно не решалось

Не меняются CI, Docker, runtime, release/version authority, branch model,
tokens или product behavior. Не создаётся semantic auto-validator STOP.

## Связь с решениями

Решение добавлено в `DECISION_LOG.md` и уточняет решение 2026-07-27 о terminal
execution без отмены continuation policy 2026-07-26.

## Изменения после review

На этапе materialization изменений после review нет.
