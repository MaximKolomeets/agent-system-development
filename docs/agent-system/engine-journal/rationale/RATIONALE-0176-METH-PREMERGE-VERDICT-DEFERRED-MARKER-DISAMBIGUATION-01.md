# RATIONALE-0176-METH-PREMERGE-VERDICT-DEFERRED-MARKER-DISAMBIGUATION-01

Связанный TASK file: `docs/agent-system/engine-journal/input/TASK-0176-METH-PREMERGE-VERDICT-DEFERRED-MARKER-DISAMBIGUATION-01.md`
Связанный RESULT file: `docs/agent-system/engine-journal/output/RESULT-0176-METH-PREMERGE-VERDICT-DEFERRED-MARKER-DISAMBIGUATION-01.md`
Номер sequence: 0176
Идентификатор задачи: METH-PREMERGE-VERDICT-DEFERRED-MARKER-DISAMBIGUATION-01
authoring_role: dev-implementer
actor_type: agent
Статус обоснования: finalized_for_review
raw_chain_of_thought_stored: no

## Решаемый вопрос

Как отличить завершённый machine-readable pre-merge verdict от настоящего
deferred-finalization marker, не создавая глобальное исключение маркера
незавершённости.

## Контекст и evidence

PR #368 выявил, что прежний scanner реагировал на любой marker
незавершённости и поэтому ошибочно блокировал каноническое значение reviewer gate. Reservation
0176 подтверждена merged PR #370; live provider validator подтвердил
однозначное ownership и allocator `0177`.

## Ограничения и инварианты

Разрешение должно зависеть одновременно от точного имени поля, точного
значения и пути TASK/RESULT. Обычные маркеры, поле с неизвестным значением,
дополнительное обещание и token в свободной фразе не получают исключение.
Сканер выдаёт безопасную reason category, но не печатает совпавшую строку.

## Рассмотренные варианты

1. Удалить marker незавершённости из глобального regex.
2. Переименовать канонический reviewer verdict.
3. Добавить контекстный exact allowlist до общего marker scan.

## Выбранный путь

Выбран вариант 3: классификатор сначала распознаёт единственную полную
строку allowlist в TASK/RESULT, затем отклоняет остальные строки с полем или
token и сохраняет прежние regex для обычных маркеров.

## Причины выбора

Путь не меняет контрактный verdict, не создаёт substring bypass и сохраняет
fail-closed поведение для неизвестных значений. Отдельные unit tests
проверяют каждый отрицательный сценарий и его reason code.

## Отклонённые альтернативы

Глобальное исключение marker незавершённости и неявный substring match отклонены:
оба варианта скрыли бы обычные незавершённые маркеры. Ручное изменение PR #368
также не относится к этой задаче и не устраняет общий defect scanner.

## Компромиссы, последствия и риски

Классификатор знает только явный контрактный field и не является общим
semantic parser. Новому каноническому verdict потребуется отдельное решение,
документация и тест, а не неявное расширение allowlist.

## Предположения, неопределённости и confidence

Каноническое значение подтверждено TASK/RESULT PR #368 и формулировкой
reviewer gate. Confidence high: правило ограничено структурой строки и
проверяется unit tests.

## Условия пересмотра или rollback triggers

Новый verdict, иной contract context или finding о bypass требуют отдельной
методологической задачи. Эта задача не меняет reservation ledger и не
выполняет merge.

## Что явно не решалось

Не изменялись PR #368, его review threads, Human UAT, release PR, tag,
GitHub Release, sync и Issue #369.

## Связь с решениями

Применяются `JOURNAL_FINALIZATION_POLICY.md`, `ENGINE_JOURNAL_CONTRACT.md`,
`POLICY_INVARIANTS.md` и `JOURNAL_SEQUENCE_RESERVATION.md`; новый инвариант
не требуется, потому что безопасное поведение покрывает ready-gate и tests.

## Изменения после review

Methodology review выявил два уточнения. Gap-проверка должна использовать
каноническое множество `occupied`: `reserved`, `consumed` и `abandoned`;
terminal `abandoned` остаётся tombstone, а некорректная поздняя запись ledger
не может освободить ранее занятую sequence. Для pre-merge verdict остаётся
разрешённой только точная строка без backticks. Регрессионные tests проверяют
обе границы и то, что production safety scan добавляет blocker, не раскрывая
содержимое совпавшей строки.

## Передача

Следующий: methodology reviewer — проверить точность allowlist и сохранение
deferred-finalization защиты в implementation PR.
