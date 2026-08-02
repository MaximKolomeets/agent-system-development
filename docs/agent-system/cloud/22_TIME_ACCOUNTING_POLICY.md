# TIME_ACCOUNTING_POLICY

## Назначение

`TIME_ACCOUNTING_POLICY.md` задаёт единый канон учёта времени для TASK/RESULT,
INDEX и сводных ledger/metrics. Цель — сделать трудозатраты проверяемыми для
ROI, планирования, billing и анализа качества процесса.

Каноническая связка:

- формат TASK/RESULT и lifecycle — `ENGINE_JOURNAL_CONTRACT.md`;
- reusable task header — `templates/TASK_HEADER_COMMON.md`;
- cost-поля — `COST_TRACKING_POLICY.md`;
- сводный шаблон — `templates/TIME_LEDGER_TEMPLATE.md`;
- project/release метрики — `METRICS.md`;
- enforcement — `tools/check_task_ready.py`.

## Обязательные поля RESULT

Новый finalized `RESULT` должен содержать machine-readable строки:

```text
execution_started_at: `<ISO-8601 timestamp with timezone>`
execution_finished_at: `<ISO-8601 timestamp with timezone>`
execution_duration: `<duration>`
time_spent: `<2.5h | 45m | PT2H30M>`
actor_type: `<human | agent | hybrid>`
role: `<methodology role>`
time_source: `<measured | reported | mixed>`
time_report_confidence: `<high | medium | low>`
human_time_reported: `<duration | not_applicable>`
```

`time_spent` — короткое человекочитаемое поле для INDEX/rollup. Оно должно
совпадать по смыслу с `execution_duration`, но допускает округление до удобного
формата (`45m`, `2.5h`, `PT2H30M`).

`execution_duration` вычисляется из `execution_started_at` и
`execution_finished_at`. Не вводить его как независимое ручное число, если
timestamps доступны.

## Участие человека

`actor_type` описывает исполнение конкретного task run:

- `agent` — работу выполнил engine/agent; human merge или обычное решение
  архитектора не превращает task run в `hybrid`;
- `human` — основная работа выполнена человеком;
- `hybrid` — существенная часть выполнения была ручной и существенная часть была
  выполнена agent/engine.

Если `actor_type` равен `human` или `hybrid`, поле `human_time_reported`
обязательно и не может быть `not_applicable`, `unknown` или пустым. Если human
time нельзя получить только потому, что задача остановлена через STOP/failure,
RESULT должен содержать `time_report_missing_reason`.

Для `actor_type: agent` поле `human_time_reported` всё равно рекомендуется
оставлять в RESULT со значением `not_applicable`, чтобы schema была стабильной.

## Источник и доверие

`time_source`:

- `measured` — время получено из timestamps или tool runtime;
- `reported` — время сообщено человеком;
- `mixed` — часть времени измерена, часть сообщена.

`time_report_confidence`:

- `high` — timestamps и duration согласованы, источник надёжен;
- `medium` — есть округление, ручная оценка или неполный tool runtime;
- `low` — задача завершилась частично, есть пропуски или оценка грубая.

## INDEX Time

`engine-journal/INDEX.md` содержит колонку `Time`.

Для новых строк писать краткое значение:

```text
45m
2.5h
hybrid: 1h agent + 30m human
```

Для исторических строк до введения этой политики писать `legacy/advisory`.
Append-only history не ретрофитится и не становится blocker только из-за
отсутствия старых time fields.

## Hard-gate

После введения H3:

- новый finalized `RESULT` без required time fields — blocker;
- новый finalized `RESULT` с `actor_type: human|hybrid` и пустым
  `human_time_reported` — blocker;
- legacy RESULT до policy boundary без этих полей — advisory;
- reviewer не требует переписывать append-only history ради ретрофита времени.

`check_task_ready.py` применяет hard-gate к новым RESULT-файлам в текущем diff.
Изменённые legacy RESULT без accounting fields получают advisory warning, если
они попали в scope проверки.

## Rollup

Rollup делается на трёх уровнях:

- PR: сумма `time_spent` по TASK/RESULT текущего PR;
- release: сумма по merged PR между release boundaries;
- project: недельный/месячный rollup по `TIME_LEDGER_TEMPLATE.md`.

В multi-agent задаче каждый agent/reviewer/human-run фиксирует свой TASK/RESULT
и своё время отдельно. Не складывать время reviewer внутрь work RESULT; review
имеет отдельную journal-запись.
