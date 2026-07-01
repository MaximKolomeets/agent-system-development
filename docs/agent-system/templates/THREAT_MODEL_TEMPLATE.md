# THREAT_MODEL - <project> (template)

Статус: `draft`. Дополняет `SECURITY_POLICY.md`.

Каждая строка threat model должна иметь test и CI-gate, либо явную пометку
`branch protection / server-side`. Угроза без контроля с тестом считается
открытой.

## 1. Активы

Заполнить по фактам target repository:

- personal/sensitive data;
- secrets/access key material;
- integrity расчета или результата;
- audit history;
- supply chain;
- доступ external users к своим данным;
- иные assets, критичные для target repository.

## 2. Таблица угроз

| Угроза | Контроль | Тест | CI-gate | severity | этап |
| --- | --- | --- | --- | --- | --- |
| Описание угрозы | Контроль; ссылка на `CONTROL_MATRIX` id, если есть | test name/path | ci/gate или `branch protection / server-side` | blocking/critical/high/medium/low | stage |

## 3. Принятые остаточные риски

| Риск | Причина принятия | До какого этапа | Owner |
| --- | --- | --- | --- |
| Описание residual risk | Почему осознанно принято | stage/PR/date | роль |

## 4. Правило

Threat model связана с:

- `SECURITY_POLICY.md`: policy source для security/privacy controls;
- `CONTROL_MATRIX_PATTERN.md`: control id и operational traceability, если
  control matrix принята в target repository;
- `ACCEPTANCE_SPEC_COMPLETENESS_PATTERN.md`: цепочка
  `scenario -> blocker -> fixture -> status` для проверяемых controls.

Threat model не копируется verbatim из methodology repository и заполняется по
target facts. Реальные secrets, private data, client data, private repository URL
и internal code names не включать.
