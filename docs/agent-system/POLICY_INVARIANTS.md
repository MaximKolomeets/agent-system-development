# POLICY_INVARIANTS

## Назначение

Этот документ фиксирует сквозные инварианты методологии: правила, которые не
должны расходиться между policy-документами, templates, manifest и ready-gate.
Инварианты не заменяют сами policy-файлы; они задают компактный контрольный слой
для review и read-only validator `docs/agent-system/tools/validate_policy_invariants.py`.

## Как применять

- Перед PR или release boundary запускать `python docs/agent-system/tools/check_task_ready.py --base origin/developer`.
- Для ручной диагностики запускать `python docs/agent-system/tools/validate_policy_invariants.py`.
- Если validator нашёл contradiction, missing canonical path или broken local link,
  PR не готов: нужно исправить источник противоречия или явно остановиться для
  решения архитектора.
- `validate_policy_invariants.py` дополняет `validate_id_references.py`: ID refs
  остаются в отдельном gate, а H11 self-test проверяет policy markers,
  существование source/template/generated paths и локальные Markdown links.

## Сквозные инварианты

| ID | Инвариант | Канонические источники | Машинная проверка |
| --- | --- | --- | --- |
| `INV-RELEASE-AUTHORITY` | Merge в `main`, annotated release tag, public publication, sync `main -> developer`, branch protection/rulesets, CI/CD/prod secrets, финальный rollback/hotfix decision и destructive data action являются human-only, если отдельный approved automation contract не принят человеком. | `RELEASE_AUTHORITY_POLICY.md`, `HUMAN_GATE_POLICY.md`, `BRANCH_POLICY.md`, `HOTFIX_AND_ROLLBACK_POLICY.md`, `DISASTER_RECOVERY.md` | Наличие authority/human-gate markers и release-sensitive RESULT evidence fields. |
| `INV-BRANCH-MODEL` | `main` обновляется только через release PR `developer -> main`; `developer` принимает изменения через work PR; одна substantive task ведётся в одной основной `work/<role>/<task>` branch; перед commit/sync действует branch/sync guard. | `BRANCH_POLICY.md`, `WORKFLOW.md`, `PR_WORKFLOW.md`, `TASK_HEADER_COMMON.md`, `check_task_ready.py` | Наличие protected-branch markers и work-branch gate в ready-gate. |
| `INV-TIME-COST-ACCOUNTING` | Новые finalized RESULT обязаны иметь accounting fields: `execution_started_at`, `execution_finished_at`, `execution_duration`, `time_spent`, `actor_type`, `human_time_reported`, token/cost fields и calculator summary. При `actor_type: human|hybrid` human time обязателен. | `TIME_ACCOUNTING_POLICY.md`, `COST_TRACKING_POLICY.md`, `ENGINE_JOURNAL_CONTRACT.md`, `TASK_CONTRACT.md`, `check_task_ready.py` | Наличие required accounting fields и hard-gate markers в ready-gate. |
| `INV-SOURCE-REFERENCE` | Target/downstream adoption читает stable methodology reference через `source_ref` (`origin/main`, release tag или published snapshot). `developer`, `work/*`, dirty local tree и open methodology PR branch не являются downstream source of truth. Для задач самой методологии используется отдельный `methodology_development_base`. | `STABLE_METHODOLOGY_REFERENCE_POLICY.md`, `ENGINE_ENTRYPOINT.md`, `TASK_CONTRACT.md`, `ADOPTION_TRANSFER_MANIFEST.yml`, `TARGET_REPOSITORY_ADOPTION_GUIDE.md` | Наличие `source_ref`, `reference_type` и `methodology_development_base` markers; отсутствие requirement использовать `developer` как stable downstream source. |
| `INV-PRIVACY-PUBLICATION` | Public methodology repository не хранит реальные private consumers, private adoption rollout state, private repository names, credentials, customer data, billing accounts или private operational details. В public repo допустимы generic templates и sanitized aggregates/counts/categories. | `PUBLICATION_POLICY.md`, `SECURITY_POLICY.md`, `SOURCE_CONSUMERS.md`, `SOURCE_CONSUMER_REGISTRY_PRIVATE_TEMPLATE.md`, `METHODOLOGY_ADOPTION_MATRIX_PRIVATE_TEMPLATE.md`, `DOWNSTREAM_FEEDBACK_SANITIZATION_POLICY.md` | Наличие private-control/publication markers и запрета на заполненные private registries. |
| `INV-TARGET-ADOPTION` | `ADOPTION_TRANSFER_MANIFEST.yml` является source inventory. `source`, `template`, `scaffold` и `generated` paths должны существовать в methodology checkout; `target_generated` paths не обязаны существовать в source checkout и проверяются через `source_templates`. Target adoption применяет manifest categories и stable reference. | `ADOPTION_TRANSFER_MANIFEST.yml`, `PROJECT_FILE_MAP.md`, `TARGET_ADOPTION_DETECTOR.md`, `ADOPTION_GUIDE.md`, `DOWNSTREAM_ADAPTATION_CHECKLIST.md` | Manifest self-test: source/template/generated/scaffold paths exist; target-generated source templates exist; local Markdown links resolve. |

## Self-test методологии

`validate_policy_invariants.py` выполняет read-only проверки:

1. Все canonical files, перечисленные для H11 инвариантов, существуют.
2. `POLICY_INVARIANTS.md` содержит все `INV-*` identifiers.
3. Policy-документы содержат обязательные markers по полномочиям release/tag,
   branch-модели, учёту времени/стоимости, source reference, privacy и adoption.
4. `ADOPTION_TRANSFER_MANIFEST.yml` не дрейфует: source/template/scaffold/generated
   paths существуют, а `target_generated.source_templates` указывают на существующие
   source/template policy-файлы.
5. Локальные Markdown links в active methodology docs разрешаются в существующие
   файлы. History/journal/cloud/source snapshots не являются входом active self-test.

Вывод validator остаётся безопасным: только `file:line`, issue code и path/detail.
Он не печатает matching lines, secrets, private identifiers или содержимое файлов.

## Границы

- Validator не является semantic NLP-review и не доказывает полноту политики.
- Validator не проверяет private control plane contents, потому что реальные
  consumers не хранятся в public repository.
- Target-generated paths вроде `PROJECT_DASHBOARD.md` или
  `docs/agent-system/POLICY_STATUS.md` не являются missing source files; они
  материализуются в target repository по facts target repository.
- Исторические journal artifacts остаются append-only и не становятся blockers
  для новых инвариантов, если ready-gate явно не проверяет новую finalized запись.

## Передача

Следующий: methodology-reviewer-01 — при review PR проверять, что новые policy
правки не создают contradiction с `INV-*` и проходят `validate_policy_invariants.py`.
