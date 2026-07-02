# ARCHITECT_HANDOFF_PACK

## Назначение

`ARCHITECT_HANDOFF_PACK.md` — единый canonical home для передачи проекта другому
архитектору или в новую рабочую сессию.

Этот файл объединяет dossier, protocol и checklist. Не создавать отдельные
`ARCHITECT_HANDOFF_DOSSIER_TEMPLATE.md`, `ARCHITECT_HANDOFF_PROTOCOL.md` и
`ARCHITECT_HANDOFF_CHECKLIST.md`, пока target repository явно не требует
разделения.

## Когда применять

- смена архитектора или owner;
- отпуск, пауза больше одной рабочей недели или потеря контекста;
- release/audit boundary;
- incident, hotfix или rollback;
- передача проекта в новый chat/thread;
- передача target repository другому оператору.

## Handoff pack

Заполняемый блок для передачи:

| Поле | Значение |
| --- | --- |
| Repository | `<repository_full_name>` |
| Visibility | `<public/private/internal>` |
| Stable methodology reference | `<origin/main | tag | snapshot>` |
| Source commit | `<methodology_source_commit>` |
| Source tag/release | `<tag or not_applicable>` |
| Last synced state | `<timestamp + commit/PR>` |
| Current branch | `<branch or none>` |
| Active PR | `<PR URL or none>` |
| Open boundary | `<release/adoption/audit/hotfix/none>` |
| Current strategic goal | `<goal>` |
| Next safe step | `<one action>` |
| Human-only decisions | `<merge/tag/publish/sync/rollback/other>` |
| Risks/blockers | `<short list or none>` |
| Downstream/source consumers to update | `<generic aliases or private registry reference>` |
| Last successful checks | `<commands/status/timestamp>` |
| Missing time reports | `<yes/no/not_applicable>` |
| Journal blockers | `<yes/no/not_applicable>` |

## Dossier: что прочитать за 30 минут

1. `README.md` — вход и trigger overlays.
2. `NON_TECHNICAL_ARCHITECT_GUIDE.md` — если архитектор не программист.
3. `ARCHITECT_COCKPIT.md` — ежедневные/еженедельные вопросы управления.
4. `PROJECT_CONSTITUTION.md` или `PROJECT_CONSTITUTION_FRAMEWORK.md` — mission,
   scope и decision authority.
5. `ROLE_MODEL.md` — кто что делает.
6. `HUMAN_GATE_POLICY.md` и `RELEASE_AUTHORITY_POLICY.md` — что делает только
   человек.
7. `WORKFLOW.md` и `BRANCH_POLICY.md` — как проходят branch/PR/release.
8. `engine-journal/INDEX.md` — последние TASK/RESULT/PR факты.
9. `CURRENT_STATE.md` и `NEXT_STEPS.md` — фактическое состояние и ближайший шаг.
10. `PROJECT_OPERATOR_DASHBOARD.md` или template — yes/no management status.

## Protocol: как передавать

1. Передающий архитектор обновляет handoff pack safe summary.
2. Engine или orchestrator проверяет branch, PR, journal, checks и blockers.
3. Передающий архитектор отмечает human-only решения, которые нельзя выполнять
   автоматически.
4. Принимающий архитектор читает dossier и задает уточняющие вопросы.
5. Принимающий архитектор подтверждает один next safe step.
6. Если есть blocker или unknown critical field, передача завершается статусом
   `STOP: human decision required`, а не молчаливым продолжением.

## Checklist

| Вопрос | Да/Нет/НП | Evidence |
| --- | --- | --- |
| Stable methodology reference указан? | `<yes/no>` | `<ref>` |
| Source commit указан? | `<yes/no>` | `<sha>` |
| Last synced state понятен? | `<yes/no>` | `<timestamp/commit>` |
| Active PR и branch указаны? | `<yes/no/not_applicable>` | `<URL/branch>` |
| Open release/adoption/audit/hotfix boundary понятен? | `<yes/no/not_applicable>` | `<boundary>` |
| Последние 5 решений или ссылка на decision log указаны? | `<yes/no>` | `<link>` |
| Risks/blockers перечислены? | `<yes/no>` | `<summary>` |
| Последние successful checks указаны? | `<yes/no>` | `<commands/status>` |
| Missing time reports проверены? | `<yes/no>` | `<summary>` |
| Human-only actions отделены от automation? | `<yes/no>` | `<policy>` |
| Next safe step сформулирован одним действием? | `<yes/no>` | `<action>` |

## STOP

Передача блокируется, если:

- нет source commit или stable methodology reference;
- active PR неизвестен, но есть незакрытые branch changes;
- есть release/hotfix/rollback decision без human actor;
- обнаружены secrets/private data в handoff;
- next safe step требует Level 3/4 decision без owner approval;
- journal имеет blocker для текущей file-changing task.

## Граница

Handoff pack не заменяет `CURRENT_STATE.md`, `NEXT_STEPS.md`, `DECISION_LOG.md`
или engine journal. Он собирает короткий управленческий snapshot и ссылки на
source-of-truth.

Если target repository хранит private consumer names, private repository URLs
или client data, они остаются в target-local/private control plane и не
попадают в public methodology repository.

## Передача

Следующий: принимающий architect/operator — подтвердить один next safe step или
вернуть `STOP` с недостающим полем handoff pack.
