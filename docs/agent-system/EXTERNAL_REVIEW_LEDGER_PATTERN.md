# EXTERNAL_REVIEW_LEDGER_PATTERN

## Назначение

External review ledger применяется, когда один документ или одно решение
проходит много внешних человеческих review: разные reviewers, разные раунды,
разные предложения. Цель:

- не терять ценные предложения;
- не ходить повторно к reviewers с уже разобранным замечанием;
- не уходить в бесконечную полировку.

## Чем отличается от соседних механизмов

- `REVIEW_AUTOLOOP.md` - ограниченный reviewer/engine цикл по active work PR.
- `METHODOLOGY_FEEDBACK_LOOP.md` - reusable improvements из target repository в
  methodology repository.
- `EXTERNAL_REVIEW_LEDGER_PATTERN.md` - консолидация повторных внешних мнений о
  документе/решении до финализации или утверждения; ledger не обязан быть
  привязан к одному PR.

## Когда применять

- Документ/решение проходит несколько human review rounds.
- Feedback приходит от нескольких external reviewers и начинает повторяться.
- Команда видит риск endless polishing вместо перехода к implementation.

Не применять как обязательный процесс для каждой мелкой task, ordinary PR или
single-review pass. Для active PR feedback использовать `REVIEW_AUTOLOOP.md`.

## Структура ledger

Ledger ведется на один документ или одно решение. Каждое предложение получает
строку со статусом и причиной:

- `applied` - внесено, с указанием revision/PR;
- `deferred` - отложено, с привязкой к будущему stage/PR;
- `rejected` - отклонено, обязательно с причиной.

Минимальные поля строки: `source` (round/reviewer), `proposal`, `disposition`,
`where_recorded`.

Раздел "Отклонено с причинами" особенно ценен: он предотвращает повторное
открытие уже разобранных предложений.

## Анти-loop правило

Новое external remark не блокирует документ и не запускает новый review round,
если:

1. remark уже есть в ledger со статусом `applied`, `deferred` или `rejected`; или
2. remark не относится к critical categories.

Critical categories, методологический минимум:

- correctness результата: расчет, логика, вывод;
- security/privacy и утечка данных;
- legal/compliance significance;
- testability: заявленный control нельзя проверить;
- integrity/boundary mixing, если применимо к project context.

Все остальные remarks получают строку в ledger с привязкой к stage/PR, а команда
двигается дальше.

## Diminishing returns stop

Если подряд `N` rounds external review дают только polishing remarks: нет
critical categories и нет нового substantive feedback, документ объявляется
baseline / ready for approval, и команда переходит к implementation.

Дальнейшие reviews продолжаются как ledger entries, но не как blockers.
Рекомендуемое значение `N`: 2-3; конкретное значение фиксируется в ledger.

## Связь с другими документами

- `QUALITY_FIRST_WORKFLOW.md` закрывает DoR/quality перед PR; ledger закрывает
  множественные external opinions и stop rule для review loop.
- `REVIEW_AUTOLOOP.md` ограничивает active PR fix-pass cycles; ledger ограничивает
  внешние review rounds, не привязанные к одному PR.
- `CONTROL_MATRIX_PATTERN.md`, если принят в target repository, может получить
  applied ledger items как new control IDs.
