# RATIONALE-0168-METH-VALIDATOR-LEGACY-CLOSURE-JOURNAL-01

Связанный TASK file: `docs/agent-system/engine-journal/input/TASK-0168-METH-VALIDATOR-LEGACY-CLOSURE-JOURNAL-01.md`
Связанный RESULT file: `docs/agent-system/engine-journal/output/RESULT-0168-METH-VALIDATOR-LEGACY-CLOSURE-JOURNAL-01.md`
Номер sequence: 0168
Идентификатор задачи: METH-VALIDATOR-LEGACY-CLOSURE-JOURNAL-01
authoring_role: methodology-architect-01
actor_type: agent
Статус обоснования: finalized_for_review
raw_chain_of_thought_stored: no

## Решаемый вопрос

Как исправить journal debt: отдельно зафиксировать уже смерженный PR #347 с
validator fix, не переписывая историю PR #346 и sequence 0167.

## Контекст и evidence

PR #346 закрепил terminal execution policy и был смержен в `developer`.
Последующий PR #347 исправил ложную интерпретацию post-merge изменения
существующей journal-тройки как новой sequence и добавил четыре регрессионных
теста. Его содержательный validator fix оказался ошибочно описан в RESULT-0167,
хотя sequence 0167 относится к PR #346.

## Ограничения и инварианты

Journal artifacts append-only: существующие строки RESULT-0167 нельзя удалять
или переписывать. GitHub metadata остаётся источником merge-facts. Validator,
tests, policy и CI находятся вне scope этой документирующей задачи.

## Рассмотренные варианты

1. Удалить относящийся к PR #347 раздел из RESULT-0167.
2. Оставить неверную атрибуцию без новой записи.
3. Создать самостоятельную запись 0168 и добавить к RESULT-0167 явное
   append-only уточнение границы sequence.

## Выбранный путь

Выбран вариант 3: новая полная journal-тройка 0168 документирует PR #347, а
RESULT-0167 получает только добавочное указание на новую authoritative запись.

## Причины выбора

Вариант одновременно сохраняет append-only gate, делает ownership validator fix
проверяемым и не создаёт специального исключения для sequence 0167.

## Отклонённые альтернативы

Удаление строк нарушило бы `check_journal_append_only.py`. Сохранение
неверной атрибуции оставило бы P1 finding promotion PR #348 без устранения.

## Компромиссы, последствия и риски

Исторический текст PR #347 физически остаётся в RESULT-0167, но прямо помечен
как superseded allocation; читатель должен использовать RESULT-0168 для
validator fix и его accounting. Это цена сохранения проверяемой истории.

## Предположения, неопределённости и confidence

Merge SHA и время PR #347 берутся из GitHub metadata; `1h 42m` рассчитано по
зафиксированным timestamps его создания и окончания локальной валидации.
Confidence: high.

## Условия пересмотра или rollback triggers

Пересмотр нужен, если PR #347 окажется не смержен в `developer`, либо если
append-only validator получит канонический механизм переназначения истории.

## Что явно не решалось

Не реализуется новая validator logic, не меняются tests, policy, CI, Docker,
release/version и содержимое PR #346/#347.

## Связь с решениями

Запись применяет каноны append-only journal и GitHub PR metadata как источника
merge-facts; она устраняет debt на release/promotion boundary.

## Изменения после review

нет: задача создаётся как прямое устранение единственного P1 finding promotion
PR #348 и не вносит нового продуктового или методологического решения.
