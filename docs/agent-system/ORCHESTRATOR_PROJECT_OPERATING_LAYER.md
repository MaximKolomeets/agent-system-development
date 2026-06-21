# ORCHESTRATOR_PROJECT_OPERATING_LAYER

## Назначение

Этот документ описывает нейтральный operating layer для случая, когда команда
ведёт работу по конкретному target implementation repository внутри отдельного
project operating context (изолированного проектного контекста ассистента).

Документ методологический и не зависит от конкретного downstream-проекта. Он
описывает контракт «один project operating context на один target repository», шаблон
project custom-instructions и состав knowledge base. Реальные имена проектов,
клиентов, приватные URL и данные сюда не добавляются (канон нейтральности —
`AGENTS.md` и `docs/agent-system/PUBLICATION_POLICY.md`).

Этот слой стоит рядом с `ORCHESTRATOR_OPERATING_CONTRACT.md`: оба описывают, как
ассистент-продукт обслуживает проектный чат. Здесь зафиксирован вариант для
project operating context как control surface поверх repo governance.

## Место в трёхслойной модели

1. **Repo governance** — каноны в `docs/agent-system/*` target repository
   (источник истины: ветки, PR, journal, решения).
2. **Project operating layer** — этот документ: изолированный проектный
   контекст, ролевой контракт, knowledge base и правило свежести.
3. **Cross-project consolidation (Cowork lane)** — `CROSS_PROJECT_CONSOLIDATION_CONTRACT.md`:
   read-only advisory консолидация поверх нескольких проектов.

Operating layer не заменяет repo governance. При конфликте побеждает repo
governance target repository, а operating layer останавливается (`STOP`).

## Правило «один project operating context на target repository»

- Один project operating context обслуживает ровно один target implementation repository.
- Контексты проектов изолированы: знания, инструкции и knowledge base одного
  проекта не перетекают в другой. Кросс-проектные обзоры — только через
  отдельный consolidation lane (см. `CROSS_PROJECT_CONSOLIDATION_CONTRACT.md`).
- Если нужно вести два target repository, заводятся два отдельных project operating context.
- Project operating layer не хранит секреты, приватные данные и реальные имена
  downstream-проектов; источником истины остаётся target repository.

## Шаблон project custom-instructions (ролевой контракт)

Ниже нейтральный шаблон инструкций проектного ассистента. Подставляются только
нейтральные термины; реальные имена не вставляются.

```text
Роль: orchestrator/review для target implementation repository.

Язык:
- Russian-first. Все ответы, отчёты и предлагаемые artifacts — на русском.
- English только для technical identifiers, команд, путей, branch names,
  filenames, config keys, API names, package names, vendor/tool names и literal
  external names.

Границы (hard):
- Ассистент НЕ коммитит и НЕ мержит. Он готовит план, задачу и diff-описание;
  запись в repository выполняет engine/человек через PR.
- Не менять main/developer напрямую; одна задача = одна ветка = один PR.
- Source of truth — target repository (ветки, PR, journal), а не память чата.

Integrity guardrails:
- Не выдавать официальный/регулируемый результат из demo/training-данных.
- Не смешивать официальный и учебный контуры (контур фиксируется в данных, а не
  в формулировке промта).
- Не вносить секреты, приватные данные, клиентские данные и реальные протоколы
  в repository или в контекст проекта.

Self-contained engine-блоки:
- Любая задача для engine оформляется одним самодостаточным copy/paste-блоком:
  repository, base/working branch, allowed files, forbidden files, проверки,
  STOP-условия, требования к отчёту и journal. Ничего обязательного не
  оставлять за пределами блока.

Поведение:
- При нехватке фактов о состоянии repository — сверяться с knowledge base и
  правилом свежести (ниже), а не угадывать.
- При конфликте с repo governance target repository — STOP и эскалация.
```

## Knowledge base и freshness

Состав context-load bundle и freshness rule не дублируются здесь. Авторитетный
канон: `docs/agent-system/ORCHESTRATOR_OPERATING_CONTRACT.md` → «Architect →
Orchestrator context handoff».

Project operating context использует этот bundle как стартовый «Source» и
добавляет target-specific материалы только если они разрешены governance target
repository. Knowledge base остаётся слепком (snapshot), а источником истины
остаётся target repository на GitHub.

Если загруженный `developer_head_sha` устарел, оркестратор просит архитектора
дозагрузить изменённые файлы по per-task handoff list из последнего final report
или journal `RESULT`. До дозагрузки нельзя принимать решения по устаревшему
слепку.

## Границы и запреты

- Operating layer не делает коммитов, не мержит PR и не меняет
  `main`/`developer`.
- Не хранит и не передаёт секреты, приватные данные, реальные протоколы и
  реальные имена downstream-проектов.
- Не является audit-trail target repository: воспроизводимая история — это
  engine-journal и PR в target repository.
- Реальные имена, матрицы видимости и дайджесты живут в приватном control plane,
  НИКОГДА в этом публичном методологическом репозитории.

## Связь с другими документами

- `docs/agent-system/ORCHESTRATOR_OPERATING_CONTRACT.md` — аналогичный operating
  contract для другого ассистент-продукта.
- `docs/agent-system/CROSS_PROJECT_CONSOLIDATION_CONTRACT.md` — слой кросс-
  проектной консолидации (Cowork lane).
- `docs/agent-system/source/README.md` — канон `source_snapshot` и запрет
  действий по устаревшему слепку.
- `docs/agent-system/ENGINE_ENTRYPOINT.md` — канон `methodology_reference` и
  порядок работы engine.
