# CONTROL_MATRIX_PATTERN

## Назначение

Паттерн control matrix связывает инварианты политик с кодом, тестами,
CI-gates, этапами и владельцами. Цель - чтобы политики не оставались
декларацией: каждый hard-инвариант имеет проверяемую реализацию. Матрица -
единая точка истины "что считается сделанным".

## Когда применять

- В target repository с несколькими политиками (`security`, `CI`, architecture),
  где инварианты дублируются и рискуют рассинхронизироваться.
- Рекомендуется как часть `TARGET_PROJECT_GOVERNANCE_PACK` для Stage 2+ или
  после явного принятия MIR-01 в target repository.

## Минимальные поля строки

`id` - `invariant` - `source` (документ/раздел) - `stage` -
`implementation` (артефакт) - `test` - `ci_gate` - `fail_mode` - `owner` -
опционально `exception_policy`.

## Правила

- Контроль без `test` и `ci_gate` считается невыполненным.
- `id` стабилен как API: смысл существующего `id` не переопределяется,
  добавляются новые строки.
- Матрица согласована с `ACCEPTANCE_SPEC_COMPLETENESS_PATTERN.md`: где у
  инварианта есть acceptance-сценарии, `test`/`ci_gate` ссылаются на цепочку
  `scenario -> blocker -> fixture -> status`.
- Матрица - источник истины "done"; политики ссылаются на ее `id`, а не
  дублируют детали реализации.
- Изменение `stage` или `fail_mode` требует review, потому что меняет
  обязательность контроля.
- Target repository адаптирует матрицу по своим фактам; methodology repository
  хранит только reusable pattern/template.

## Связь с другими документами

- Политики (`SECURITY_POLICY.md`, `CI_POLICY.md`, ADR) отвечают на "что и
  почему"; матрица отвечает на "где это в коде/тестах/CI".
- `ACCEPTANCE_SPEC_COMPLETENESS_PATTERN.md` задает traceability цепочку для
  acceptance/spec controls; control matrix связывает эту цепочку с policy
  invariants и CI-gates.
- `THREAT_MODEL` в target repository, если принят, связывает угрозы с control
  `id` из матрицы.
- `POLICY_STATUS` в target repository, если принят, фиксирует статус политик;
  matrix операционализирует эти статусы.
