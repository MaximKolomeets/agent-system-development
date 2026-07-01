# CONTROL_MATRIX (template)

Статус: `draft`. Заполняется в target repository. См.
`docs/agent-system/CONTROL_MATRIX_PATTERN.md`.

## Hard-инварианты

| id | Инвариант | Источник | Этап | Реализация | Тест | CI-gate | Fail-mode | Владелец |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CTRL-DOMAIN-001 | Что гарантируем | Документ/раздел | Stage 2 | path/module | test name/path | ci/gate | merge blocked / apply blocked | роль |

## Пороговые/процессные контроли

| id | Контроль | Источник | Этап |
| --- | --- | --- | --- |
| CTRL-PROCESS-001 | Что проверяем процессно | Документ/раздел | Stage 2 |

## Правило

Контроль без теста и CI-gate считается невыполненным. `id` стабильны.
Матрица согласована с `ACCEPTANCE_SPEC_COMPLETENESS_PATTERN.md`.
