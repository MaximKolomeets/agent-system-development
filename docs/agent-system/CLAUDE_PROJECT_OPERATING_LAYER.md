# CLAUDE_PROJECT_OPERATING_LAYER

## Назначение

Этот документ описывает нейтральный operating layer для случая, когда команда
ведёт работу по конкретному target implementation repository внутри отдельного
Claude Project (изолированного проектного контекста ассистента).

Документ методологический и не зависит от конкретного downstream-проекта. Он
описывает контракт «один Claude Project на один target repository», шаблон
project custom-instructions и состав knowledge base. Реальные имена проектов,
клиентов, приватные URL и данные сюда не добавляются (канон нейтральности —
`AGENTS.md` и `docs/agent-system/PUBLICATION_POLICY.md`).

Этот слой стоит рядом с `CHATGPT_OPERATING_CONTRACT.md`: оба описывают, как
ассистент-продукт обслуживает проектный чат. Здесь зафиксирован вариант для
Claude Project как control surface поверх repo governance.

## Место в трёхслойной модели

1. **Repo governance** — каноны в `docs/agent-system/*` target repository
   (источник истины: ветки, PR, journal, решения).
2. **Claude Project operating layer** — этот документ: изолированный проектный
   контекст, ролевой контракт, knowledge base и правило свежести.
3. **Cross-project consolidation (Cowork lane)** — `CROSS_PROJECT_CONSOLIDATION_CONTRACT.md`:
   read-only advisory консолидация поверх нескольких проектов.

Operating layer не заменяет repo governance. При конфликте побеждает repo
governance target repository, а operating layer останавливается (`STOP`).

## Правило «один Claude Project на target repository»

- Один Claude Project обслуживает ровно один target implementation repository.
- Контексты проектов изолированы: знания, инструкции и knowledge base одного
  проекта не перетекают в другой. Кросс-проектные обзоры — только через
  отдельный consolidation lane (см. `CROSS_PROJECT_CONSOLIDATION_CONTRACT.md`).
- Если нужно вести два target repository, заводятся два отдельных Claude Project.
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

## Состав knowledge base («Source»)

Project knowledge base («Source») собирается из target repository и держится в
синхронизации с его `developer`. Минимальный нейтральный состав:

| Источник (в target repository) | Зачем в knowledge base |
|---|---|
| `docs/agent-system/CURRENT_STATE.md` | фактическое состояние после последних PR |
| `docs/agent-system/DECISION_LOG.md` | принятые решения, причины, последствия |
| `docs/agent-system/NEXT_STEPS.md` | ближайший план |
| `PROJECT_CONSTITUTION.md` | mission, success criteria, scope control, authority |
| `docs/agent-system/engine-journal/INDEX.md` | карта task → result → PR |
| `docs/agent-system/source/` | справочные source-материалы проекта |

Правила knowledge base:

- только нейтральные/публично-допустимые материалы; секреты, приватные данные и
  реальные клиентские имена не загружаются;
- knowledge base — это слепок (snapshot), а не «живой» repository; источником
  истины остаётся target repository на GitHub;
- если материал в knowledge base противоречит target repository, истиной
  считается target repository.

## Правило свежести (asof + developer HEAD SHA)

Каждый слепок knowledge base несёт метку свежести:

```text
asof: <ISO-8601 timestamp>
developer_head_sha: <commit-sha origin/developer на момент слепка>
```

Проверка актуальности в начале каждого проектного чата:

1. Зафиксировать `developer_head_sha` из knowledge base.
2. Сверить с текущим `origin/developer` target repository (через доступный
   git/connector).
3. Если SHA совпадают — knowledge base актуален, можно работать.
4. Если SHA расходятся — knowledge base устарел: пометить как stale, не
   принимать решения по устаревшему слепку и предложить обновить «Source» до
   текущего `developer` перед содержательной работой.
5. Если проверить актуальность невозможно — честно сказать об этом и работать в
   режиме повышенной осторожности (сверяться с repository перед write-action
   рекомендациями).

Это правило согласовано с каноном `source_snapshot` (`docs/agent-system/source/README.md`):
нельзя менять состояние repository по устаревшему snapshot.

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

- `docs/agent-system/CHATGPT_OPERATING_CONTRACT.md` — аналогичный operating
  contract для другого ассистент-продукта.
- `docs/agent-system/CROSS_PROJECT_CONSOLIDATION_CONTRACT.md` — слой кросс-
  проектной консолидации (Cowork lane).
- `docs/agent-system/source/README.md` — канон `source_snapshot` и запрет
  действий по устаревшему слепку.
- `docs/agent-system/ENGINE_ENTRYPOINT.md` — канон `methodology_reference` и
  порядок работы engine.
