# REVIEW_TEMPLATE

## PR/branch

Указать PR или ветку.

## Scope

Описать границы review.

## Files reviewed

Перечислить просмотренные файлы.

## Checks run

Указать выполненные проверки.

## Findings

Описать найденные проблемы.

## Journal closure

Если PR уже merged, проверить `RESULT` и `INDEX`: PR status `merged`, merge commit SHA, release/sync PR данные при наличии, `RESULT closed after merge: yes`, `INDEX closed after merge: yes`, `No journal placeholders: yes`.

Блокирующие замечания:

- merged PR journal остается `PR open`;
- merged PR journal остается `ready for review`;
- merged PR journal остается `draft open`;
- merged PR journal содержит `pending at file materialization`;
- merged PR journal содержит `see Engine final report`;
- `RESULT` не фиксирует merge commit SHA после merge, когда SHA доступен.

## Required changes

Перечислить обязательные изменения.

## Recommendation

Дать рекомендацию: approve, changes required или hold.
