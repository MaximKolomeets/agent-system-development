# COST_TRACKING_POLICY

## Назначение

`COST_TRACKING_POLICY.md` задаёт минимальный reusable канон стоимости для
agent/human work. Политика нужна для ROI, budget visibility, billing и сравнения
вариантов выполнения.

Каноническая связка:

- time source и actor fields — `TIME_ACCOUNTING_POLICY.md`;
- RESULT/JOURNAL lifecycle — `ENGINE_JOURNAL_CONTRACT.md`;
- rollup ledger — `templates/TIME_LEDGER_TEMPLATE.md`;
- метрики эффективности — `METRICS.md`;
- enforcement/calculator — `tools/check_task_ready.py`.

## Обязательные поля RESULT

Новый finalized `RESULT` должен содержать:

```text
input_tokens: `<integer | not_available | not_applicable>`
output_tokens: `<integer | not_available | not_applicable>`
ai_cost_estimate: `<number | not_available | not_applicable>`
human_cost_estimate: `<number | not_available | not_applicable>`
total_task_cost: `<number | not_available | not_applicable>`
resource_cost: `AI tokens: <...>; Human hours: <...>`
```

Если provider/runtime не отдаёт token usage или стоимость, использовать явное
`not_available`, а не оставлять поле пустым. Если категория не применима,
использовать `not_applicable`.

## Семантика стоимости

- `input_tokens` и `output_tokens` — фактические token counts, если доступны.
- `ai_cost_estimate` — оценка стоимости AI/tool execution.
- `human_cost_estimate` — оценка стоимости human effort, если применимо.
- `total_task_cost` — суммарная оценка task cost.
- `resource_cost` — человекочитаемая строка rollup, например
  `AI tokens: 12000 input / 4000 output; Human hours: not_applicable`.

Если числовые `ai_cost_estimate`, `human_cost_estimate` и `total_task_cost`
заполнены одновременно, `total_task_cost` должен совпадать с суммой AI + human в
пределах округления. Если стоимость resource/runtime учитывается отдельно, это
нужно явно описать в `resource_cost` и RESULT risks.

## Confidence и неизвестные значения

Cost fields могут быть `not_available`, когда среда исполнения не отдаёт
надёжные token/cost facts. Это не blocker, если поле заполнено явно и
`time_report_confidence` отражает качество источника.

Запрещены пустые значения, placeholders и `pending` в finalized RESULT.

## Calculator

`check_task_ready.py` выполняет lightweight calculator по RESULT-файлам текущего
diff:

- суммирует числовые `input_tokens` и `output_tokens`;
- суммирует числовые `ai_cost_estimate`, `human_cost_estimate` и
  `total_task_cost`;
- проверяет арифметику `ai_cost_estimate + human_cost_estimate = total_task_cost`,
  если все три значения числовые;
- не печатает provider secrets, account ids, rate cards или private billing data.

Legacy RESULT без cost fields остаются advisory и не ретрофитятся.

## Rollup

Rollup уровни:

- PR: сумма token/cost полей по RESULT текущего PR;
- release: сумма по PR release payload;
- project: недельный/месячный rollup в ledger/metrics.

Для public methodology repository запрещено добавлять private billing account ids,
client rates, internal project names или confidential rate cards.
