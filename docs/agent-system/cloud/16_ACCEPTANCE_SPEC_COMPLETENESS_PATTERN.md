# ACCEPTANCE_SPEC_COMPLETENESS_PATTERN

## Назначение

Acceptance spec completeness pattern задаёт единый каркас для задач, которые создают acceptance spec, blocker matrix, fixture plan, contract tests или generator scaffold. Pattern нужен, чтобы документы не расходились по scenario IDs, blocker codes, fixture IDs и expected statuses.

## Обязательная связь

Каждая строка acceptance surface должна сводиться к цепочке:

```text
scenario_id -> blocker_code -> fixture_id -> expected_status -> expected_blocker
```

Минимальные поля:

- `scenario_id` - стабильный идентификатор сценария acceptance spec;
- `blocker_code` - код blocker для сценариев со статусом `BLOCKED`;
- `fixture_id` - стабильный идентификатор fixture или future fixture plan entry;
- `expected_status` - ожидаемый статус обработки (`PASS`, `FAIL`, `BLOCKED`);
- `expected_blocker` - ожидаемый blocker для `BLOCKED` fixtures.

## Правила сценариев

- Каждый `BLOCKED` scenario должен иметь `blocker_code`.
- Каждый `blocker_code` должен иметь хотя бы один scenario или быть явно помечен как reserved.
- `PASS` и `FAIL` scenarios не должны требовать `blocker_code`.
- Active source может вести к `PASS` или `FAIL`, но сам по себе не является `BLOCKED`.
- `source_status: unknown`, `superseded` или `conflict` должен вести к blocker, если сценарий не может быть безопасно принят.
- Real data boundary должен быть явным: fixtures используют synthetic/minimal examples, а real/private data запрещены.

## Правила fixtures

- Каждый `fixture_id` ссылается на существующий `scenario_id`.
- `PASS` и `FAIL` fixtures не должны требовать `blocker_code`.
- `BLOCKED` fixtures должны иметь `expected_blocker`.
- `expected_blocker` должен совпадать с `blocker_code` сценария или быть объяснён как derived blocker.
- Fixture plan может быть future plan, но тогда PR/RESULT не должны утверждать, что fixture files или tests созданы.

## Правила blocker matrix

- Matrix перечисляет все active blocker codes или явно помечает reserved codes.
- Matrix указывает, какие scenarios покрывает blocker.
- Matrix не должна вводить blocker codes, которых нет в acceptance spec или reserved list.
- Matrix должна различать semantic blockers и machine-verifiable blockers.

## Правила generator scaffold

- Generator scaffold не считается production generator, если он не создаёт production output и не подключён к runtime/CI.
- Если scaffold только planned, RESULT и PR body пишут "fixture plan" или "contract plan", а не "generator implemented".
- Contract tests создаются отдельной задачей, если текущий scope docs-only или plan-only.

## Review checklist

- Есть mapping `scenario_id -> blocker_code -> fixture_id -> expected_status -> expected_blocker`.
- Все `BLOCKED` scenarios имеют blocker.
- Все blockers имеют scenario coverage или reserved status.
- Все fixtures ссылаются на scenarios.
- `PASS`/`FAIL` fixtures не требуют blocker.
- `BLOCKED` fixtures имеют expected blocker.
- Real data boundary явно запрещает private/real data.
- PR body и RESULT не обещают tests/fixtures/generator, если они не созданы в diff.
