# ERROR_CATALOG (template)

Статус: `draft`. Заполняется в target repository или task-local docs scope.
См. `docs/agent-system/ERROR_CATALOG_PATTERN.md`.

## Rules

- `code` стабилен как API: смысл опубликованного code не переопределяется.
- Blocking code имеет synthetic `test_fixture` или явный `fixture_planned`.
- Сообщения не содержат credentials, secret values, private URLs, client data или
  target-specific sensitive details.
- `blocker_code` из acceptance spec должен ссылаться на этот catalog или на
  reserved code ниже.

## Catalog

| code | severity | user_message | dev_message | retryable | blocks_state | audit_required | test_fixture |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ERR-DOMAIN-001 | blocker | Короткое безопасное сообщение | Техническое объяснение без sensitive values | yes/no | PR/release/adoption/runtime action | yes/no | fixtures/synthetic-case |

## Reserved codes

| code | intended use | owner | activation condition |
| --- | --- | --- | --- |
| ERR-RESERVED-001 | Для будущего known blocker class | role | Когда появится acceptance scenario |

## Deprecated codes

| code | replacement | reason | valid_until |
| --- | --- | --- | --- |
| ERR-OLD-001 | ERR-NEW-001 | Почему больше не использовать | date or release |

## Acceptance/spec mapping

| scenario_id | blocker_code | fixture_id | expected_status | expected_blocker |
| --- | --- | --- | --- | --- |
| SCN-001 | ERR-DOMAIN-001 | FX-001 | BLOCKED | ERR-DOMAIN-001 |
