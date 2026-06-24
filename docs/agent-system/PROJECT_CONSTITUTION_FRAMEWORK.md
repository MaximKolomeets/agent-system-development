# PROJECT_CONSTITUTION_FRAMEWORK

## Назначение

Project Constitution Framework задает обязательный верхнеуровневый документ target repository:

```text
PROJECT_CONSTITUTION.md
```

`PROJECT_CONSTITUTION.md` фиксирует миссию проекта, критерии успеха, out-of-scope, архитектурные принципы, текущую стратегическую цель, authority агентов и уровни решений. Он нужен до первых implementation PR, чтобы `engine` не расширял scope проекта без явного решения пользователя.

`agent-system-development` хранит только reusable framework и template. Конкретный `PROJECT_CONSTITUTION.md` создается и обновляется в target repository по фактам target project.

## Project Constitution в target repository

`PROJECT_CONSTITUTION.md` в target repository должен содержать:

- `Project Mission`;
- `Success Criteria`;
- `Out Of Scope`;
- `Architectural Principles`;
- `Current Strategic Goal`;
- `Agent Authority`;
- `Decision Authority`;
- `Scope Expansion Control`;
- `Governance Review Checklist`.

## Миссия проекта (Project Mission)

Mission описывает, зачем существует проект и какой результат должен быть достигнут. Mission должна быть достаточно короткой, чтобы ее можно было проверять перед каждой задачей и PR.

## Критерии успеха (Success Criteria)

Success Criteria фиксируют измеримые признаки успеха текущего этапа или всего проекта. Критерии должны помогать review отличать завершенную работу от частичной.

## Вне scope (Out Of Scope)

Out Of Scope перечисляет направления, которые проект не делает на текущем этапе.

Универсальные примеры:

- новые продукты;
- новые платформы;
- новые сервисы;
- новые направления бизнеса;
- paid SaaS dependencies;
- production infrastructure;
- large architecture rewrites;
- integrations outside approved roadmap;
- runtime или infrastructure changes вне утвержденного этапа;
- feature work вне текущей strategic goal.

## Архитектурные принципы (Architectural Principles)

Architectural Principles задают ограничения, которые `engine` должен учитывать при планировании и реализации.

Универсальные примеры:

- Local-first;
- docs-first before implementation;
- no microservices before approved stage;
- no Kubernetes before approved stage;
- no paid external dependency without explicit approval;
- no runtime adoption without separate architecture decision.

Principles должны быть адаптированы под target repository. Нельзя копировать project-specific principles из methodology repository или другого target repository.

## Текущая стратегическая цель (Current Strategic Goal)

В target repository должна быть одна активная strategic goal.

Пример нейтральной формулировки:

```text
Complete approved MVP milestone.
```

Если появляется новая strategic goal, старую нужно закрыть, заменить или явно пометить как superseded решением пользователя.

## Полномочия агентов (Agent Authority)

Agent Authority определяет, какие роли агентов могут принимать какие решения и где они должны остановиться.

`PROJECT_CONSTITUTION.md` должен ссылаться на:

```text
docs/agent-system/ENGINE_REGISTRY.md
```

`ENGINE_REGISTRY.md` должен содержать Agent Authority Matrix для каждой роли:

- allowed scope;
- forbidden scope;
- approval required;
- notes или escalation path.

Agent Authority не дает engine права расширять scope задачи, менять strategic goal или обходить local instructions.

## Полномочия принятия решений (Decision Authority)

Decision Authority делится на четыре уровня:

| Level | Название | Что входит | Требование |
|---|---|---|---|
| Level 1 | Implementation | Локальные изменения в рамках утвержденной задачи | Разрешено в task scope |
| Level 2 | Subsystem | Изменения внутри ограниченного subsystem или workflow | Нужна явная связь с task scope и state docs |
| Level 3 | Architecture | Архитектурные решения, меняющие principles, boundaries или runtime model | Требуется explicit user approval |
| Level 4 | Project Strategy | Mission, strategic goal, out-of-scope, roadmap stage или direction change | Требуется explicit user approval |

Level 3+ всегда требует явного approval пользователя до изменений.

## Контроль расширения scope (Scope Expansion Control)

Каждая задача и каждый PR должны классифицировать изменение scope:

| Scope class | Значение | Действие engine |
|---|---|---|
| No scope expansion | Работа полностью остается в task scope | Продолжать после обычных проверок |
| Minor scope expansion | Небольшое уточнение, напрямую нужное для выполнения task scope | Зафиксировать в отчете и docs, если нужно |
| Major scope expansion | Новый subsystem, новая direction, новый runtime/service/platform или изменение strategy | Остановиться и запросить решение пользователя |

Major scope expansion нельзя выполнять без explicit user decision.

## Чеклист governance-review (Governance Review Checklist)

Перед merge значимого PR проверить:

- [ ] Изменение соответствует `Project Mission`.
- [ ] Изменение соответствует `Current Strategic Goal`.
- [ ] Изменение не нарушает `Out Of Scope`.
- [ ] Изменение не меняет `Architectural Principles` без решения.
- [ ] Понятно, какой `Decision Authority` level затронут.
- [ ] Изменение не повышает architecture level без фиксации authority.
- [ ] Если затронуты Level 3+ решения, есть explicit user approval.
- [ ] Обновлены `Roadmap`, `Backlog`, `Current State` или `Decision Log`, если изменение влияет на state.
- [ ] Если есть major scope expansion, engine остановился и запросил решение пользователя.
- [ ] `ENGINE_REGISTRY.md` и Agent Authority Matrix остаются актуальными.

## Связь с governance pack

Project Constitution является законом target repository внутри governance pack.

Минимальная связь:

- `PROJECT_CONSTITUTION.md` - mission, boundaries, authority, scope control и stop conditions;
- `PROJECT_DASHBOARD.md` - краткое состояние;
- `ROADMAP.md` - этапы и milestones;
- `BACKLOG.md` - candidate tasks;
- `CURRENT_STATE.md` - фактическое состояние;
- `NEXT_STEPS.md` - ближайшие действия;
- `DECISION_LOG.md` - принятые решения;
- `PROJECT_GUARDRAILS.md` - практические ограничения;
- `ENGINE_REGISTRY.md` - роли, engines и Agent Authority Matrix.

Governance pack фиксирует состояние и workflow, а Project Constitution фиксирует границы проекта и authority.

## Шаблон и target-specific constitution

`docs/agent-system/templates/PROJECT_CONSTITUTION_TEMPLATE.md` является reusable template.

`PROJECT_CONSTITUTION.md` в target repository является target-specific file. Его нельзя копировать verbatim из methodology repository или другого target repository.

Target-specific constitution должен быть заполнен только по фактам target repository и не должен содержать private repository URL, client data, credentials, tokens, passwords, API keys или internal code names.

## Правила adoption

При adoption target repository создает `PROJECT_CONSTITUTION.md` по template:

```text
docs/agent-system/templates/PROJECT_CONSTITUTION_TEMPLATE.md
```

Файл нельзя копировать как project state из methodology repository или другого target repository. Его нужно заполнить по target facts, без private data, real credentials, private repository URL, client data или internal code names.

До full docs-only adoption target repository должен получить `PROJECT_CONSTITUTION.md` или явно указать, почему constitution отложен.

## STOP-условия

Engine должен остановиться и запросить решение пользователя, если обнаружено:

- major scope expansion;
- конфликт с `Project Mission`;
- конфликт с `Out Of Scope`;
- Level 3+ decision без explicit user approval;
- изменение active strategic goal без решения пользователя;
- риск раскрытия private data или secrets;
- конфликт local instructions с task scope.
