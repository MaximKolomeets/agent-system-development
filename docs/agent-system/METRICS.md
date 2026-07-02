# METRICS

## Назначение

`METRICS.md` задаёт reusable набор process metrics для methodology/target
repositories. Это не live dashboard конкретного private project; project-specific
значения ведутся в target repository или в явно разрешённом local ledger.

## Базовые метрики

| Metric | Definition | Source | Cadence |
| --- | --- | --- | --- |
| Task time | Сумма `time_spent` по RESULT за период. | `engine-journal/output/RESULT-*`, `INDEX.md` | weekly/monthly/release |
| Human time | Сумма `human_time_reported` для `actor_type: human|hybrid`. | RESULT accounting fields | weekly/monthly/release |
| AI tokens | Сумма `input_tokens` + `output_tokens`, если доступны. | RESULT cost fields | weekly/monthly/release |
| Task cost | Сумма `total_task_cost`, если доступна. | RESULT cost fields | weekly/monthly/release |
| Average task to merge | Время от `execution_started_at` до GitHub `merged_at` по PR. | RESULT + GitHub PR metadata | release/project |
| Review cycles per PR | Количество review/fix-pass циклов на PR. | RESULT, PR comments/reviews | release/project |
| PR without blockers | Доля PR без blocker findings. | review RESULT / PR review | release/project |
| Saved time estimate | Оценка разницы между baseline human-only и фактическим hybrid/agent run. | ledger estimate | monthly/project |

## Минимальный release rollup

Перед release boundary допускается краткая сводка:

```text
Period:
Release:
PR count:
Task count:
Total time:
Human time:
Input tokens:
Output tokens:
AI cost estimate:
Human cost estimate:
Total task cost:
Average task to merge:
Review cycles per PR:
PR without blockers:
Saved time estimate:
Legacy/advisory entries:
```

## Правила качества данных

- Метрика не должна скрывать `not_available`; неизвестные значения считаются
  отдельно.
- Legacy entries до H3 не ретрофитятся и отмечаются как `legacy/advisory`.
- Private billing rates, client names, account ids и internal project names не
  добавляются в public methodology repository.
- Если данные получены из GitHub PR metadata, указать дату/время проверки.
- Если данные оценочные, указать confidence (`high`, `medium`, `low`).
