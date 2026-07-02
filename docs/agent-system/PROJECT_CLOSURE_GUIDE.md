# PROJECT_CLOSURE_GUIDE

## Назначение

Guide описывает безопасное закрытие, паузу или передачу target repository без
потери контекста, ложных release facts и утечки private data.

Closure не означает удаление данных. Удаление repository, веток, артефактов,
секретов, production data или финансовые действия являются human-only и требуют
отдельного решения владельца.

## Когда применять

- milestone завершен и проект переводится в maintenance;
- проект ставится на паузу;
- repository передается другому владельцу;
- target adoption отменяется после audit;
- проект закрывается после release;
- требуется final handoff перед long-term archive.

## Closure modes

| Mode | Когда использовать | Минимальный результат |
| --- | --- | --- |
| `paused` | Работа временно остановлена | current state, next step и resume prompt. |
| `completed` | Цель достигнута | release/tag evidence, final state, handoff. |
| `maintenance` | Активная разработка закончена | правила hotfix/rollback, owners, dependency notes. |
| `transferred` | Проект передан другому owner/team | handoff pack, authority transfer, open risks. |
| `cancelled` | Работа прекращена до результата | причина, сохраненные артефакты, что не делать дальше. |
| `archived` | Repository больше не активен | final state, archive location, access decision. |

## Closure workflow

### 1. Human decision

- [ ] Owner/architect выбрал closure mode.
- [ ] Решение не выполняет агент вместо человека.
- [ ] Если затрагиваются merge/tag/publish/sync/rollback, применены
  `RELEASE_AUTHORITY_POLICY.md` и `HUMAN_GATE_POLICY.md`.
- [ ] Если есть business acceptance, owner/PO подтвердил UAT evidence.

### 2. Repository state

- [ ] Все active PR имеют одно из состояний: merged, closed, superseded или
  explicitly deferred.
- [ ] `developer` стабилизирован или явно помечен как not released.
- [ ] `main` не меняется напрямую агентом.
- [ ] Release tag или rollback target не придумываются; используются только
  проверенные Git/GitHub facts.
- [ ] Branch cleanup выполняется отдельным cleanup scope или human action.

### 3. Journal and evidence

- [ ] TASK/RESULT/INDEX для closure task финализированы.
- [ ] RESULT фиксирует actor, evidence и time/cost accounting.
- [ ] Нет `pending`, `TBD`, unresolved placeholders и противоречивых PR facts.
- [ ] Если closure совпадает с release boundary, применить
  `JOURNAL_ARCHIVING_POLICY.md` отдельной archive task после release.
- [ ] Если факты merge/release недоступны, closure фиксирует blocker, а не
  выдумывает state.

### 4. Governance docs

Обновить target-local docs по фактам target repository:

- `CURRENT_STATE.md`;
- `NEXT_STEPS.md`;
- `DECISION_LOG.md` или `DECISIONS.md`;
- `PROJECT_DASHBOARD.md`;
- `ROADMAP.md`, если closure меняет roadmap;
- `BACKLOG.md`, если остаются deferred items.

State docs из methodology repository не копируются verbatim.

### 5. Privacy and access

- [ ] `.env`, credentials, tokens, client data и private URLs не попали в Git.
- [ ] Если нужно отозвать доступы, это human-only operational action.
- [ ] Реальные consumers, dependency matrix и private rollout notes остаются в
  private control plane.
- [ ] Public closure report не раскрывает private downstream project names.

### 6. Dependencies and consumers

- [ ] Если project является source для других projects, dependency notes
  обновлены в private control plane.
- [ ] Если project потребляет methodology/source release, зафиксирован последний
  stable reference.
- [ ] Breaking closure effect не считается согласованным без owner decision и
  neutral impact note.
- [ ] Cross-project status передается только через redacted digest или private
  control plane.

### 7. Handoff package

Closure handoff должен содержать:

- repository и visibility;
- current `main`/`developer` SHAs или указание, почему они не применимы;
- latest release/tag или `not released`;
- active/open PRs и их решение;
- remaining risks;
- next human action;
- resume prompt, если проект paused/maintenance;
- ссылки на final RESULT/INDEX.

## Чеклист для не-программиста

1. Откройте project dashboard и проверьте, что цель понятна.
2. Убедитесь, что нет незакрытого release/UAT решения.
3. Попросите engine показать статус PR и journal, не меняя файлы.
4. Если нужно закрыть проект, выберите closure mode из таблицы выше.
5. Разрешите отдельную closure task с allowed files и forbidden files.
6. Перед merge closure PR проверьте: что закрыто, что осталось, кто следующий.

## STOP conditions

Closure task останавливается, если:

- owner decision по closure mode отсутствует;
- есть противоречие между GitHub state и journal state;
- нужно удалить данные, revoke access или менять branch protection без human
  decision;
- требуется раскрыть private project names в public methodology repository;
- release/tag/merge facts недоступны;
- dependency impact неизвестен, но closure меняет contract для другого project.

## Передача

Следующий: architect или owner - выбрать closure mode и разрешить отдельную
closure task, если project boundary готов к закрытию или паузе.
