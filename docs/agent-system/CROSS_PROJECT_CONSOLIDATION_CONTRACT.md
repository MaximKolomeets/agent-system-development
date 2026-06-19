# CROSS_PROJECT_CONSOLIDATION_CONTRACT

## Назначение

Этот документ описывает нейтральный контракт кросс-проектной консолидации: как
безопасно собирать сводную картину поверх НЕСКОЛЬКИХ target implementation
repositories, не нарушая изоляцию проектов и границы данных.

Документ методологический. Реальные имена проектов, клиентов, приватные URL,
дайджесты и матрицы видимости сюда не добавляются. Реальные данные консолидации
живут в приватном control plane (см. раздел «Приватный control plane»).

Термины — только нейтральные: `consumer project` (проект-потребитель сводки),
`source project` (проект-источник статуса), `control plane` (приватный слой
управления видимостью и дайджестами).

## Место в трёхслойной модели

Это третий слой поверх:

1. repo governance (`docs/agent-system/*` в каждом target repository);
2. project operating layer (`CLAUDE_PROJECT_OPERATING_LAYER.md`, по одному на
   target repository).

Консолидация работает поверх слепков, а не вместо repo governance. Источником
истины каждого проекта остаётся его target repository.

## Visibility-matrix (схема)

Видимость между проектами задаётся матрицей «consumer → sees:[source...]».
Схема (без реальных имён):

```text
visibility_matrix:
  <consumer-project>:
    sees:
      - <source-project-A>
      - <source-project-B>
  <another-consumer-project>:
    sees:
      - <source-project-A>
```

Принципы:

- **need-to-know как ГРАНИЦА, не удобство.** Consumer видит source только при
  явной, обоснованной записи в матрице. По умолчанию — не видит.
- видимость направленная: запись `A sees B` не даёт `B sees A`;
- видимость не транзитивна: `A sees B` и `B sees C` не дают `A sees C` без явной
  записи;
- расширение видимости — это решение владельца control plane, фиксируемое в
  приватном control plane, а не в публичном репозитории.

## Формат STATE_DIGEST

`STATE_DIGEST` — компактный, прошедший redaction слепок статуса одного source
project. Нейтральная схема полей:

```text
state_digest:
  project_ref: <нейтральный идентификатор source project>
  asof: <ISO-8601 timestamp>
  developer_head_sha: <commit-sha origin/developer на момент слепка>
  status: <короткий статус: например on-track | blocked | review>
  current_goal: <короткая нейтральная формулировка>
  recent_decisions:
    - <решение/паттерн без приватных деталей>
  open_questions:
    - <вопрос без приватных деталей>
  blockers:
    - <блокер без приватных деталей>
```

`STATE_DIGEST` содержит статус/решения/паттерны, но не содержит секретов,
клиентских данных, реальных протоколов и приватных URL (см. «Redaction»).

## Формат CONSOLIDATED_VIEW

`CONSOLIDATED_VIEW` — сводка для одного consumer project, собранная из
`STATE_DIGEST` тех source projects, которые этот consumer видит по матрице:

```text
consolidated_view:
  consumer_ref: <нейтральный идентификатор consumer project>
  generated_asof: <ISO-8601 timestamp>
  sources:
    - project_ref: <source project>
      asof: <ISO-8601 timestamp>
      developer_head_sha: <commit-sha>
      status: <короткий статус>
      highlights:
        - <статус/решение/паттерн без приватных деталей>
  staleness_notes:
    - <source project>: <fresh | stale: SHA расходится>
```

Правила:

- в `CONSOLIDATED_VIEW` попадают только source projects из строки матрицы для
  этого consumer;
- каждый источник несёт `asof` + `developer_head_sha`; расхождение SHA помечается
  как stale (правило свежести из `CLAUDE_PROJECT_OPERATING_LAYER.md`);
- по устаревшему источнику не выдаются решения, только пометка о необходимости
  обновить дайджест.

## Redaction / boundary

Граница того, что можно и нельзя выносить через консолидацию.

**Можно (после redaction):**

- статус проекта (on-track / blocked / review и т. п.);
- принятые решения и их последствия в нейтральной форме;
- переиспользуемые паттерны и уроки;
- ссылки на публичные/нейтральные artifacts.

**Нельзя (никогда через границу):**

- секреты, токены, credentials, `.env`;
- клиентские и персональные данные;
- реальные протоколы и регулируемые рабочие данные;
- приватные URL и внутренние кодовые имена проектов;
- любые данные, нарушающие изоляцию проекта-источника.

Redaction выполняется на стороне source project ДО попадания в `STATE_DIGEST`.
Если значение нельзя безопасно redact — оно не выносится.

## Cowork lane (read-only advisory)

Кросс-проектная консолидация может выполняться в advisory-режиме ассистента
(Cowork lane). Жёсткие границы этого lane:

- **read-only по репозиторию**: lane читает слепки/дайджесты, но не пишет в
  target repositories;
- **advisory**: выдаёт сводки и рекомендации, не принимает решения за владельца
  проекта;
- **без коммитов в репозиторий**: никаких commit/PR из этого lane;
- **без секретов через границу**: данные за пределами redaction-границы не
  передаются;
- **не для регулируемых данных**: lane не пригоден для юридически/регуляторно
  значимых данных, потому что не даёт воспроизводимого audit-trail; такие данные
  остаются в target repository с journal и PR.

Если задача требует записи, коммита, official/регулируемого результата или
audit-trail — это выходит за пределы Cowork lane, и работа переводится в обычный
engine/PR workflow target repository.

## Приватный control plane (обязательно)

Реальная visibility-matrix, реальные идентификаторы проектов, реальные
`STATE_DIGEST` и `CONSOLIDATED_VIEW` живут в ПРИВАТНОМ control plane.

- Этот публичный методологический репозиторий хранит ТОЛЬКО нейтральные схемы и
  правила (этот документ).
- Реальные имена, матрицы и дайджесты НИКОГДА не коммитятся в этот публичный
  репозиторий и ни в какой публичный репозиторий.
- Control plane отвечает за хранение, доступ и аудит реальной консолидации; его
  устройство и расположение не раскрываются здесь.

## Связь с другими документами

- `docs/agent-system/CLAUDE_PROJECT_OPERATING_LAYER.md` — слой проектного
  operating контекста и правило свежести (asof + developer HEAD SHA).
- `docs/agent-system/PUBLICATION_POLICY.md` — публикационные границы публичного
  репозитория.
- `docs/agent-system/SECURITY_POLICY.md` — правила обращения с секретами и
  чувствительными данными.
- `AGENTS.md` — запрет приватных данных и реальных имён downstream-проектов в
  публичном методологическом репозитории.
