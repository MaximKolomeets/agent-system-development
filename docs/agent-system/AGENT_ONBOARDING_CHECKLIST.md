# AGENT_ONBOARDING_CHECKLIST

## Назначение

Checklist нужен перед первым запуском новой роли или нового исполнителя
(`engine`) в target repository. Он снижает риск, что агент начнет работу без
понимания project boundary, branch model, journal contract, forbidden data и
human-only actions.

Этот документ не назначает конкретный vendor/tool. Роль описывается функцией, а
исполнитель выбирается архитектором.

## Когда применять

- новый target repository проходит bootstrap или docs-only adoption;
- в существующий проект добавляется новая роль;
- задачу принимает другой исполнитель;
- проект возвращается после паузы;
- меняется branch model, repository visibility, release authority или human
  gate.

## Входные данные

Перед onboarding должны быть известны или явно помечены как blocker:

- target repository и visibility;
- текущая branch model;
- active goal и ближайший PR;
- роль, scope и forbidden files;
- актуальный `AGENTS.md` или equivalent local instructions;
- stable methodology reference для target adoption/update;
- где ведется engine journal;
- какие действия являются human-only.

## Checklist

### 1. Repository boundary

- [ ] Repository root подтвержден.
- [ ] Remote соответствует ожидаемому target repository.
- [ ] Текущая ветка соответствует задаче.
- [ ] `git status --short` проверен до checkout/sync/pull/merge.
- [ ] Если tree dirty, агент пишет `STOP` и не использует `stash`,
  `reset --hard` или `clean` без отдельного решения пользователя.

### 2. Role and authority

- [ ] Role name vendor-neutral и не содержит tool/vendor name.
- [ ] Исполнитель указан отдельно как `engine` или назначается архитектором.
- [ ] Scope задачи описывает ЧТО нужно сделать; HOW выбирается внутри
  утвержденных constraints.
- [ ] Human-only actions прочитаны по `HUMAN_GATE_POLICY.md`.
- [ ] Merge/tag/publish/sync/rollback authority прочитана по
  `RELEASE_AUTHORITY_POLICY.md`.

### 3. Методология и локальные инструкции

- [ ] Локальный `AGENTS.md` или эквивалентные инструкции прочитаны до правок.
- [ ] Если задача применяет методологию к target repository, зафиксирован
  `methodology_reference` со стабильными `source_ref` и `source_commit`.
- [ ] `developer`, `work/*` и грязное локальное дерево методологии не
  используются как stable downstream source.
- [ ] Overlays по trigger выбраны по `README.md` и `METHODOLOGY_MAP.md`,
  инвентарь берется из `ADOPTION_TRANSFER_MANIFEST.yml`.

### 4. Приватность и безопасность

- [ ] `.env`, учетные данные, токены, пароли, приватные URL, клиентские данные,
  персональные данные и внутренние кодовые имена не читаются и не коммитятся.
- [ ] Sensitive grep, если нужен, выполняется filename/count-only.
- [ ] Public repository считается публичным.
- [ ] Target-private facts не переносятся в public methodology repository.

### 5. Journal and reporting

- [ ] Для file-changing task есть TASK, RESULT и INDEX path.
- [ ] TASK содержит branch, allowed files, forbidden files, checks и STOP.
- [ ] RESULT должен быть Russian-first и содержать time/cost accounting,
  `## Methodology feedback`, `## Unprompted Project Proposals` и
  `## Передача`.
- [ ] Ready-for-review PR не оставляет RESULT/INDEX placeholders.

### 6. First task readiness

- [ ] Definition of Ready понятна: цель, non-goals, acceptance criteria,
  allowed files и checks.
- [ ] Если задача слишком большая для prompt, используется Task File Handoff
  Mode.
- [ ] Review boundary задана: кто проверяет, что считается blocker, где
  исправляется feedback.
- [ ] Для UI/API/release-sensitive работ известен UAT или human acceptance gate.

### 7. Handoff

- [ ] Передача фиксирует следующую роль и конкретное действие.
- [ ] Если проект передается в другой chat/thread, используется
  `ARCHITECT_HANDOFF_PACK.md` или target-local handoff template.
- [ ] Если агент заметил вне-scope риск или improvement, он фиксирует proposal,
  но не расширяет текущий scope без решения пользователя.

## STOP conditions

Агент пишет `STOP` и не начинает правки, если:

- repository/remote/branch не совпадают с задачей;
- working tree dirty перед checkout/sync/pull/merge;
- target instructions конфликтуют с Russian-first или safety policy;
- нет allowed files или forbidden files для file-changing task;
- stable methodology source не подтвержден для target adoption/update;
- задача требует human-only action от агента;
- обнаружен риск секрета или private data.

## Передача

Следующий: orchestrator или architect - подтвердить, что новая роль прошла
onboarding checklist перед первой file-changing task.
