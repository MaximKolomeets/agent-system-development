# JOURNAL_SEQUENCE_RESERVATION

## Назначение

Этот канон предотвращает collision четырёхзначных sequence в параллельных
engine-journal задачах. Он применяется вместе с
`ENGINE_JOURNAL_CONTRACT.md`, не заменяет `TASK -> RATIONALE -> RESULT`,
append-only `INDEX.md` и не переписывает открытые PR.

## Проблема и варианты

Правило `last INDEX + 1` видит только merged history. Открытый PR с уже
созданной тройкой поэтому невидим второму агенту; два параллельных выбора дают
один номер. Ручной выбор отклонён как неаудируемый. Выбран append-only ledger
и provider-neutral snapshot: они сохраняют offline audit trail и дают CI
проверяемую картину открытых claims.

## Нормативный алгоритм

1. До новой substantive journal-задачи получить complete normalized snapshot
   открытых PR/MR от provider adapter либо approved offline export.
2. Прочитать merged `INDEX.md` и append-only
   `engine-journal/SEQUENCE_RESERVATIONS.json`.
3. `occupied` = sequence из INDEX + `reserved`/`consumed`/`abandoned` ledger
   + valid claims snapshot. Каждая active `reserved` запись ledger, ещё не
   consumed matching merged INDEX, обязана иметь ровно один matching
   machine-readable claim в metadata её PR/MR. Отсутствие, duplicate,
   malformed или identity-mismatch claim — hard failure.
4. `next_sequence = max(occupied) + 1`; формат всегда ровно четыре цифры.
   Агент не угадывает номер и не переиспользует abandoned tombstone.
5. Сначала создать минимальный reservation PR с versioned claim в ledger и
   его PR/MR metadata, затем substantive task. Branch protection должна
   требовать актуальную base либо человек выполняет serial merge. Конкурентный
   add/add ledger conflict или CI duplicate finding является границей
   атомарности.

`consumed` выводится из matching sequence/task id в merged INDEX. Ledger
является потоком append-only событий: первая запись identity имеет состояние
`reserved`; разрешены только `reserved -> abandoned` и
`reserved -> consumed`. Terminal state нельзя вернуть в `reserved` или
перевести в другой terminal state. Закрытый без merge PR не освобождает номер:
он остаётся occupied, пока append-only ledger не получит terminal `abandoned`;
tombstone также никогда не переиспользуется. Rollback — только новый
append-only `abandoned` record после human decision.

## Provider-neutral snapshot

Схема: `schemas/JOURNAL_SEQUENCE_PROVIDER_SNAPSHOT.schema.json`. Требуются
`schema_version`, `provider`, `availability`, `observed_at`, provider PR/MR
`id`, `state`, `head_sha`, `reservation_claims` и для claim:
`metadata_version`, `sequence`, `task_id`, `reservation_id`.

Канонический validator не вызывает provider API. GitHub reference adapter
`tools/github_journal_sequence_snapshot.py` преобразует PR body claim
`<!-- journal-sequence-reservation: {...} -->` в эту схему. GitLab, GitVerse и
SourceCraft должны отдать тот же normalized snapshot: их термины MR/PR и API
не меняют семантику `reserved/consumed/abandoned`. Provider-dependent CI
явно передаёт adapter credential только через environment и задаёт минимальные
read-only permissions. При отсутствии credential adapter не делает
неаутентифицированный запрос и возвращает
`provider_credential_unavailable`; причины включают HTTP access/rate-limit и transport,
некорректный ответ и pagination получают отдельные безопасные коды причины без
token, Authorization, response body, request headers или detail исключения. `.env`
не читается.

Adapter обязан получить все страницы provider API для `state=all` и завершить
snapshot fail-closed при ошибке страницы, timeout, невалидном JSON или
неожиданной структуре. Частичный snapshot никогда не получает
`availability: available`.

Стандартные строки provider `open`, `closed` и `merged` соответствуют schema;
merged PR из ответа `state=all` не является некорректным payload. После записи
snapshot adapter выводит в CI только `provider_snapshot availability=<value>
reason=<normalized-or-none>`; полный snapshot, claim metadata, credentials,
headers, response body и exception detail не выводятся.

Если mandatory live provider source/offline snapshot unavailable или metadata
неполна/неизвестной версии, allocation fail-closed. После adoption offline
работа возможна только по merged ledger, reservation PR, base-update/merge
gate и заранее полученному complete export. Legacy open PR без API/export не
bootstrap-ится автоматически.

## Bootstrap и adoption

Переход с `last + 1` допускается только по human authorization: complete scan
open PR, список sequence/task/reservation identities, доказательство
уникальности, upstream methodology version/commit, регистрация legacy claims
в ledger, RATIONALE/RESULT evidence и включение strict validator для новых
allocation. Нормативный пример: INDEX `0016`, open PR `0017` — следующая
задача получает `0018`; существующий PR не переписывается, второй `0017`
блокируется.

Target adoption переносит этот канон, schema, validator, reference adapter и
пустой target ledger scaffold без methodology operational history. CI вызывает
adapter и strict validator. Первичный self-bootstrap этого механизма —
однократное исключение только при явном human authorization, complete open-PR
scan и записи причины в его TASK/RATIONALE/RESULT.

## Риски и границы

Ledger не является distributed transaction: его атомарность обеспечивается
PR/base-update conflict и human merge gate. Validator сравнивает ledger с
resolved base структурно: каждая прежняя запись должна остаться в том же
порядке и без изменения полей; разрешено только добавление событий в конец.
Stale snapshot, отключённая branch protection или обход reservation PR —
operational risk и blocker, а не повод выбрать номер вручную. История
reservations append-only; provider snapshot — проверяемое evidence, не источник
переписывания historical artifacts.

## Передача

Следующий: methodology reviewer — проверить ledger, provider snapshot и CI
duplicate detection до human merge reservation или substantive PR.
