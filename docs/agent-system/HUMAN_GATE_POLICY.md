# HUMAN_GATE_POLICY

## Назначение

Human Gate Policy перечисляет действия, которые агент не выполняет сам даже при
наличии технических прав. Агент может анализировать, готовить PR, писать
checklist, собирать evidence и предлагать команды, но финальное действие делает
человек.

Канон: если действие ниже требуется для завершения задачи, агент пишет `STOP`
или переводит PR/RESULT в состояние `automation:stopped-human-required` до
решения человека.

## Human-only actions

| Действие | Почему human-only | Что может сделать агент |
| --- | --- | --- |
| Merge в `main` | `main` является stable release surface. | Подготовить release PR, checks, release notes и risk summary. |
| Merge release/sync PR после release | Release/sync меняет published branch graph. | Подготовить PR, проверить diff и после merge сверить GitHub metadata. |
| Создание annotated release tag | Tag является публичным release pointer. | Предложить tag name и target commit, проверить tag после создания. |
| GitHub Release / public publication | Publication меняет внешний release surface. | Подготовить текст, artifacts checklist и publish instructions. |
| Branch protection/rulesets | Ошибка может открыть protected branch или сломать workflow. | Провести read-only audit и описать desired settings. |
| Изменения CI/CD, deployment или production automation | Может повлиять на supply chain и production delivery. | Подготовить PR только при явном task scope и отметить approval need. |
| Доступ, просмотр или изменение production secrets | Секреты нельзя раскрывать агенту или печатать в журнал. | Указать, какие secret slots/permissions нужны, без значений. |
| Изменение mission, strategy, roadmap direction или Level 3/4 governance | Это изменение смысла проекта, а не implementation detail. | Сформулировать варианты и последствия для решения человека. |
| Удаление данных или destructive irreversible action | Потеря данных может быть необратимой. | Подготовить backup/impact checklist и безопасный dry-run, если разрешено. |
| Финансовые решения | Деньги, подписки и обязательства вне agent authority. | Дать оценку стоимости и варианты, без покупки/подписки. |
| Rollback/hotfix final decision | Rollback влияет на пользователей и release history. | Собрать incident facts, предложить rollback plan и PR/commands по `HOTFIX_AND_ROLLBACK_POLICY.md`. |

## Human gate protocol

1. Agent определяет, что задача требует human-only action.
2. Agent завершает всё безопасное preparation work в task scope.
3. Agent фиксирует в final report и `RESULT`:
   - какое действие human-only;
   - почему оно blocked by human gate;
   - какие checks/evidence уже готовы;
   - что именно должен сделать человек.
4. После действия человека agent может выполнить read-only verification и
   journal reconciliation, если это отдельно входит в scope.

## Связь с task_contract

Для задач, где возможны human-only действия, `task_contract.stop_conditions`
должен включать соответствующий gate, например:

```yaml
stop_conditions:
  - human_gate_required
  - branch_protection_change_needed
  - release_publish_action_needed
  - rollback_decision_needed
```

Если `task_contract` разрешает file changes, это не означает разрешение на
human-only actions. Разрешение на подготовку PR не является разрешением на merge,
tag, publish, ruleset change, secret access, destructive action или rollback.

## Evidence policy

Human-only action после выполнения человеком подтверждается безопасным evidence:

- GitHub PR URL и merge commit SHA;
- tag name и target/tag SHA;
- GitHub Release URL или release page reference;
- ruleset/protection status summary без secret values;
- human report с timestamp, если API evidence недоступно.

Evidence не должен содержать credentials, tokens, cookies, secret values,
private downstream repository names или private operational details.

## Передача

Следующий: human architect — принять решение по human-only action или вернуть
задачу агенту для дополнительной подготовки evidence.
