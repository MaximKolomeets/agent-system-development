# PROJECT_OPERATOR_DASHBOARD

Этот template создает короткий target-local dashboard для управления проектом без
чтения всех policy. Он не заменяет `PROJECT_DASHBOARD.md`; operator dashboard
отвечает на вопрос "можно ли безопасно продолжать сейчас?".

## Snapshot

| Поле | Значение |
| --- | --- |
| Repository | `<repository_full_name>` |
| Updated at | `<ISO-8601 timestamp>` |
| Owner/architect | `<role/person>` |
| Current strategic goal | `<goal>` |
| Active branch | `<branch or none>` |
| Active PR | `<PR URL or none>` |
| Current task | `<task-id or none>` |
| Next safe step | `<one action>` |

## Yes/no gate

Если ответ `нет` или `unknown` в любой строке, следующий шаг — `STOP` или
отдельное решение человека.

| Вопрос | Да/Нет/НП | Evidence |
| --- | --- | --- |
| Ordinary PR можно merge после review? | `<yes/no/not_applicable>` | `<review/checks>` |
| Release boundary можно продолжать? | `<yes/no/not_applicable>` | `<release readiness>` |
| Adoption/source-update можно продолжать? | `<yes/no/not_applicable>` | `<stable reference>` |
| State docs актуальны? | `<yes/no>` | `<CURRENT_STATE/NEXT_STEPS>` |
| Journal blockers отсутствуют? | `<yes/no>` | `<RESULT/INDEX>` |
| Missing time reports отсутствуют или объяснены? | `<yes/no>` | `<time accounting>` |
| Human-only action отделен от automation? | `<yes/no>` | `<HUMAN_GATE_POLICY>` |
| Private data/secrets risk отсутствует? | `<yes/no>` | `<safe scan summary>` |
| Scope expansion отсутствует или approved? | `<yes/no>` | `<constitution/decision>` |
| Rollback/hotfix decision не требуется? | `<yes/no/not_applicable>` | `<policy/evidence>` |

## Blockers

- `<blocker or none>`.

## Risks

- `<risk or none>`.

## Human decisions

- `<decision needed or none>`.

## Last successful checks

| Check | Status | Evidence |
| --- | --- | --- |
| `<command or manual check>` | `<passed/failed/skipped>` | `<safe summary>` |

## Правило обновления

Обновлять после:

- merge значимого PR;
- release/adoption boundary;
- появления blocker;
- смены architect/operator;
- handoff в новый chat/thread;
- incident/hotfix/rollback.

## Передача

Следующий: architect/operator — если все обязательные ответы `yes` или
`not_applicable` с evidence, подтвердить next safe step; иначе вернуть STOP.
