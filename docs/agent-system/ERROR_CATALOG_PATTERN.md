# ERROR_CATALOG_PATTERN

## Назначение

Error catalog pattern задает единый стабильный словарь кодов ошибок, blockers и
policy violations. Код ведет себя как API: после публикации его смысл не
переопределяется, а новые случаи добавляются новыми кодами или aliases с явным
deprecation rule.

Pattern нужен, чтобы acceptance specs, fixtures, control matrix, review feedback
и RESULT не называли один и тот же blocker разными словами.

## Когда применять

- Acceptance spec использует `blocker_code`.
- Review feedback или ready-gate должны возвращать стабильные machine-readable
  codes.
- Target repository имеет несколько policy/gate источников, которые должны
  ссылаться на один словарь blockers.
- Нужны synthetic fixtures для blocking categories.

Для мелкой docs-only задачи без повторного использования codes достаточно
локальных reviewer IDs (`B-01`, `M-01`). Error catalog нужен там, где codes
становятся частью reusable contract.

## Минимальные поля кода

| Поле | Назначение |
| --- | --- |
| `code` | Стабильный идентификатор. |
| `severity` | `blocker`, `major`, `minor`, `nit` или target-local шкала. |
| `user_message` | Короткое безопасное сообщение для отчета. |
| `dev_message` | Техническое объяснение без secrets/private values. |
| `retryable` | Можно ли повторить после исправления входных условий. |
| `blocks_state` | Какое состояние блокируется: PR, release, adoption, runtime action. |
| `audit_required` | Требуется ли отдельный audit/review после фикса. |
| `test_fixture` | Synthetic fixture или fixture plan, покрывающий code. |

## Правила стабильности

- `code` не переиспользуется для нового смысла.
- Исправление wording не меняет semantics code.
- Если code устарел, он получает replacement или deprecation note.
- Blocking code должен иметь `test_fixture` или явную причину `fixture_planned`.
- Catalog не хранит реальные credentials, private data, matching secret values
  или target-specific facts.

## Связь с acceptance/spec

`ACCEPTANCE_SPEC_COMPLETENESS_PATTERN.md` использует цепочку:

```text
scenario_id -> blocker_code -> fixture_id -> expected_status -> expected_blocker
```

`blocker_code` в этой цепочке должен ссылаться на code из error catalog или на
явно reserved code. Если acceptance spec вводит новый blocking code без строки
catalog, review должен считать это несогласованностью spec.

## Связь с governance

- `POLICY_STATUS_PATTERN.md` показывает, действует ли policy как blocking source
  на текущей стадии repository.
- `CONTROL_MATRIX_PATTERN.md` связывает policy/control IDs с tests и CI-gates.
- `ERROR_CATALOG_PATTERN.md` описывает, какой stable code возвращается при
  нарушении control или acceptance condition.

## Review checklist

- Все `BLOCKED` acceptance scenarios имеют `blocker_code`.
- Каждый `blocker_code` существует в catalog или явно reserved.
- Blocking codes имеют synthetic fixture или fixture plan.
- User-facing messages безопасны: нет secret values, private URLs, credentials,
  client data или target-specific sensitive details.
- Codes не дублируют reviewer-local IDs без причины.
- Deprecated codes не удалены без migration note.
