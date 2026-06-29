# SEMANTIC_COMPLETENESS_GATES

## Назначение

Semantic completeness gates - это обязательный pre-PR слой проверки, который закрывает разрыв между зелёными техническими проверками и фактической согласованностью методологических артефактов. Gate не заменяет reviewer pass и не является полноценным semantic parser: engine выполняет checklist, фиксирует результат в RESULT, а reviewer классифицирует найденные расхождения как `machine-verifiable`, `semantic` или `mixed`.

## Когда применять

Применять перед push/PR для задач, которые меняют TASK/RESULT/INDEX, PR body, state docs, acceptance spec, blocker matrix, fixture plan, boundary docs, templates, review handoff или generated context bundle.

Для read-only review gate применяется как checklist review scope. Для docs-only задач semantic gate проверяет, что diff не включает tests/tools/code/runtime. Для tooling задач semantic gate проверяет, что RESULT/PR body не обещают поведение шире фактического diff и выполненных smoke/checks.

## Universal semantic checks

- Downstream feedback items должны ссылаться на `docs/agent-system/DOWNSTREAM_FEEDBACK_LOOP.md` и проходить sanitization checkpoint по `docs/agent-system/DOWNSTREAM_FEEDBACK_SANITIZATION_POLICY.md` до попадания в backlog, TASK, RESULT или PR body.
- RESULT не должен обещать checks, которые не запускались.
- RESULT не должен содержать deferred placeholders или обещания дописать факты позже.
- PR body не должен утверждать, что создано поведение, которого нет в diff.
- NEXT_STEPS не должен писать, что следующая задача уже начата, если она только кандидат.
- State docs должны различать `implemented`, `in progress`, `candidate` и `future`.
- Если задача docs-only, diff не должен включать tests/tools/code/runtime.
- Если production generator не создавался, PR body, RESULT и docs не должны описывать production implementation как созданную.
- Если smoke/check был временным, временный файл должен быть удалён до commit, а smoke value не должен попасть в commit.

## Cross-document consistency checks

- Acceptance spec, blocker matrix и fixture plan должны согласовывать `scenario_id`, `blocker_code`, `expected_status` и `fixture_id`.
- Boundary docs не должны противоречить state docs: если boundary говорит "только план", CURRENT_STATE/NEXT_STEPS не должны описывать production-ready implementation.
- BACKLOG и NEXT_STEPS должны совпадать по статусу будущих задач: future candidate не становится active без отдельной task entry.
- DECISION_LOG должен фиксировать только принятое решение текущей задачи и не переписывать старые journal entries.
- Manifest/source map/cloud bundle должны включать новые reusable docs только через штатную генерацию.

## PR body consistency checks

- PR body перечисляет только фактически изменённые файлы и созданные capabilities.
- PR body не обещает tests/fixtures/generator/runtime, если они не входят в diff.
- PR body отделяет implemented scope от future follow-up.
- PR body содержит honest checks section: skipped checks объяснены, failed checks не скрыты, smoke results не расширены до полноценной валидации.
- PR body не содержит private target details, real data, credentials, `.env` или downstream-specific identifiers.

## RESULT consistency checks

- RESULT фиксирует фактический branch, PR URL, head SHA, reviewed head SHA или явно объясняет, почему поле не применимо.
- RESULT не обещает checks, которые не запускались.
- RESULT не содержит deferred placeholders.
- RESULT указывает ordinary terminal state (`architect_ready` / `human_merge_allowed`) без требования post-merge closure PR для ordinary PR.
- RESULT содержит Source Delta и context handoff по `docs/agent-system/templates/TASK_HEADER_COMMON.md`.
- RESULT описывает temporary smoke как targeted smoke, а не как full validation.

## Review handoff consistency checks

- Reviewer feedback использует blocker IDs и class `machine-verifiable | semantic | mixed`.
- Для `semantic` и `mixed` blockers требуется reviewer re-review по changed blocker scope.
- Machine-verifiable closure допустим только если команда полностью покрывает blocker и scope не расширился.
- Review handoff не должен создавать новую implementation task без решения архитектора.
- Fix-pass RESULT закрывает конкретные blocker IDs и не заявляет закрытие wider audit scope.

## Machine-verifiable vs semantic checks

`machine-verifiable`:

- `git diff --check`;
- `validate_task_contract.py`;
- `check_task_ready.py`;
- generated parity checks;
- count-only / filename-only safety scans;
- smoke, который проверяет конкретный blocker.

`semantic`:

- соответствие PR body фактическому diff;
- корректность статусов в CURRENT_STATE/NEXT_STEPS;
- отсутствие преждевременного заявления "started/implemented";
- согласованность intent между docs, RESULT и reviewer handoff.

`mixed`:

- acceptance spec / blocker matrix / fixture plan consistency;
- docs-only boundary, где path scope проверяется машинно, а claims проверяются semantic review;
- journal finalization, где tool ловит placeholder category, а reviewer проверяет смысл финального RESULT/INDEX.

## STOP conditions

- Downstream feedback содержит target-specific/private details или утверждает target adoption до `main`/tag release.
STOP и не открывать ready-for-review PR, если:

- RESULT обещает checks, которые не запускались;
- RESULT содержит deferred placeholders;
- PR body утверждает изменения, которых нет в diff;
- docs-only task включает tests/tools/code/runtime;
- acceptance spec, blocker matrix и fixture plan расходятся по scenario/blocker/fixture/status mapping;
- boundary docs противоречат state docs;
- temporary smoke file попал в commit;
- smoke value попал в commit;
- private target data, credentials, `.env` или real data попали в diff;
- generated/cloud/source map drift не объяснён и не исправлен.

## Examples

Good:

- "Создан acceptance spec и blocker matrix; fixture plan описан как future plan; production generator не создавался."
- "Targeted smoke подтвердил blocker category; временный файл удалён до commit."
- "Следующий возможный шаг: отдельная задача `VERIFY-PROTOCOL-GENERATOR-CONTRACT-TESTS-01` после merge."

Bad:

- "Generator implemented", если создан только fixture plan.
- "All checks passed", если запускался только targeted smoke.
- "Next task started", если есть только backlog candidate.
- "Docs-only PR", если diff содержит `tests/**` или production code.
