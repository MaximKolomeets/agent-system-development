# RATIONALE-0171-METH-JOURNAL-PARALLEL-SEQUENCE-RESERVATION-01

Связанный TASK file: `docs/agent-system/engine-journal/input/TASK-0171-METH-JOURNAL-PARALLEL-SEQUENCE-RESERVATION-01.md`
Связанный RESULT file: `docs/agent-system/engine-journal/output/RESULT-0171-METH-JOURNAL-PARALLEL-SEQUENCE-RESERVATION-01.md`
Номер sequence: 0171
Идентификатор задачи: METH-JOURNAL-PARALLEL-SEQUENCE-RESERVATION-01
authoring_role: methodology-architect
actor_type: agent
Статус обоснования: finalized_for_review
raw_chain_of_thought_stored: no

## Решаемый вопрос

Как выделять sequence без collision, если merged INDEX и открытые PR содержат
разные, одновременно существующие состояния journal.

## Контекст и evidence

Старое правило использовало последний INDEX sequence плюс один, поэтому
открытый PR не был виден. Два агента могли выбрать одинаковое значение. Для
self-bootstrap scan открытых PR не нашёл occupation `0171`; merged max `0170`
и stable tag зафиксированы в TASK.

## Ограничения и инварианты

Сохраняются четырёхзначный формат, triplet, append-only INDEX, запрет rewrite
и provider neutrality. При недоступном обязательном provider snapshot новое
выделение fail-closed. Tokens, provider authorization и private downstream
данные не фиксируются.

## Рассмотренные варианты

1. Ручной номер из prompt.
2. Только provider-specific lock.
3. Append-only ledger с normalized provider snapshot.

## Выбранный путь

Выбран вариант 3: occupied set объединяет INDEX, ledger и valid snapshot;
next равен `max + 1`. GitHub adapter — reference adapter, а не часть
канонической семантики.

## Причины выбора

Ledger даёт audit trail и offline evidence, snapshot видит open PR, а CI
выявляет duplicate task/reservation identity. Закрытый без merge claim не
освобождает номер автоматически, поэтому race не обходится переиспользованием.

## Отклонённые альтернативы

Ручное назначение не имеет machine-verifiable uniqueness. Внешний lock только
одного provider снижает переносимость и не заменяет append-only history.

## Компромиссы, последствия и риски

Граница атомарности — reservation PR, актуальная base и human serial merge,
а не распределённая транзакция. Stale/unavailable snapshot блокирует новую
allocation; это безопаснее ложного свободного sequence.

## Предположения, неопределённости и confidence

Provider adapters GitLab, GitVerse и SourceCraft реализуют тот же schema;
реальные API mapping проверяются отдельной adoption-задачей. Confidence: high
для validator semantics, medium для provider-specific integration без их API.

## Условия пересмотра или rollback triggers

Пересмотр нужен при новой required metadata version или доказанном provider
state, который не представим normalized snapshot. Rollback reservation — только
append-only abandoned tombstone по human decision.

## Что явно не решалось

Не менялись target repositories, branch protection, product/runtime, release,
existing open PR, historical journal artifacts и provider credentials.

## Связь с решениями

Решение уточняет ENGINE_JOURNAL_CONTRACT и фиксируется новой append-only
DECISION_LOG entry; оно сохраняет triplet и append-only gates.

## Изменения после review

На момент initial implementation review ещё не применялся.
