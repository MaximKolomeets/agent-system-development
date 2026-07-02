# NEXT_STEPS

## Machine-readable task contract

Для новых write-action Engine-задач, docs-only PR, tooling task, review/fix-pass с branch changes и release/adoption flow добавлять `task_contract` по `docs/agent-system/TASK_CONTRACT.md`; перед PR по возможности запускать `python docs/agent-system/tools/validate_task_contract.py <task-file>`. Для cloud handoff канон контракта доступен в default bundle как `13_TASK_CONTRACT.md`.

## Постоянный рабочий цикл (Standing Workflow Loop)

Повторяемый цикл methodology maintenance:

1. Сформулировать plan/task с точным scope, allowed files, checks, STOP conditions и branch guard.
2. Применить `docs/agent-system/QUALITY_FIRST_WORKFLOW.md`: Definition of Ready, проверяемые acceptance criteria, self-review before PR, PR body quality check и blocker-ID based fix-pass policy.
3. Выполнить substantive task в основной `work/<role>/<task>` branch; при необходимости использовать внутренние `work/<role>/<task>/*` sub-branches и слить их обратно до PR.
4. Перед push/PR запустить `python docs/agent-system/tools/check_task_ready.py --base origin/developer`, затем открыть один итоговый PR в `developer`, провести review по head SHA и фактическому diff, затем исправить feedback в той же task branch до `ready_for_merge`.
4a. Если feedback требует повторных проходов, использовать review autoloop: blocker IDs/classes, `verification_command`, engine fix-pass в той же branch, machine-check closure для fully passed machine-verifiable blockers, minimal reviewer re-review для semantic/mixed blockers, затем `architect:ready-to-merge` или `automation:stopped-human-required`.
4b. Если surfaced generated/cloud EOL-only шум, использовать `python docs/agent-system/tools/generated_eol_guard.py --base origin/developer`; content drift исправлять регенерацией/source fix, EOL/whitespace-only noise закрывать как machine-verifiable evidence или отдельным scoped EOL task.
5. После merge ordinary PR не создавать отдельный closure PR: GitHub PR metadata является source of truth для merge facts, а journal остается завершённым на `architect_ready` / `human_merge_allowed`.
6. Повторять work/review/merge до завершения текущей серии.
7. Перед release/audit boundary выполнить boundary reconciliation только если нужен boundary snapshot или есть explicit architect request.
8. Выполнить release-gate: `python docs/agent-system/tools/check_task_ready.py --base origin/main --release-boundary` на `developer`, journal closed, `python docs/agent-system/tools/gen_file_map.py --check`, `python docs/agent-system/tools/gen_cloud_bundle.py --check` (content-oriented / EOL-safe), state-refresh для `CURRENT_STATE.md`/`NEXT_STEPS.md` с regenerated `docs/agent-system/cloud/**`.
9. Человек-архитектор мержит release PR `developer -> main`; затем annotated tag ставится на release merge commit в `main` по активной release-инструкции; после release выполняется sync `main -> developer`.
10. Повторить цикл от актуального `developer`.

## Текущий фокус (Current Focus)

Текущий фокус: release-prep `v1.5.1` после merge PR #298-#302. Release-prep PR
обновляет `RELEASE_READINESS.md`, state docs, boundary reconciliation для
journal 0132-0136, journal entry `0137` и generated cloud bundle. После merge
этого PR отдельной задачей создать release PR `developer -> main` для `v1.5.1`;
release PR merge remains human-only, прямой push в `main` запрещён, GitHub
Release не публикуется.

Точные task/PR факты не дублируются здесь как source of truth. Актуальный pointer:
`docs/agent-system/engine-journal/INDEX.md`; latest release перед этим release-prep:
`v1.5.0`; next intended release tag: `v1.5.1`.

После релиза: перейти к methodology-update для target implementation repository
от stable release pointer `v1.5.1`.

## Опциональный backlog (на усмотрение архитектора)

- **Downstream semantic completeness gates**: по результатам sanitized downstream dry-run в target implementation repository добавить future methodology hardening для Pre-PR semantic completeness checks. Цель — снизить количество fixup-циклов, когда технические gates зелёные, но reviewer находит логические несостыковки между RESULT, acceptance spec, matrix, fixture plan и boundary docs.
  - `METH-DOWNSTREAM-FEEDBACK-COMPLETENESS-GATES-01`: реализовано в `METH-SEMANTIC-COMPLETENESS-GATES-01` через reusable semantic completeness gates.
  - `METH-JOURNAL-FINALIZATION-PHRASES-01`: реализовано в `METH-SEMANTIC-COMPLETENESS-GATES-01` через journal finalization policy и ready-gate category.
  - `METH-ACCEPTANCE-SPEC-COMPLETENESS-PATTERN-01`: реализовано в `METH-SEMANTIC-COMPLETENESS-GATES-01` через acceptance/spec completeness pattern.
  - `METH-DOWNSTREAM-FEEDBACK-LOOP-VERIFICATION-01`: закрыто в `METH-DOWNSTREAM-FEEDBACK-LOOP-SANITIZED-01` как sanitized/reusable variant через `DOWNSTREAM_FEEDBACK_LOOP.md` и `DOWNSTREAM_FEEDBACK_SANITIZATION_POLICY.md`; target-specific/private details не переносились.
  - Status: первые три пункта закрыты текущим methodology hardening PR; sanitized feedback report остаётся отдельной future task.
  - Priority: medium-high.
  - Reason: reduces repeated fixup cycles in target repositories.
- **Review journaling polish**: blocker по PR-C6.1 закрыт. `Journal trace: always` и `Report delivery` разведены; future polish допустим только как wording cleanup без blocker status.
- **Чистка redirect-заглушек** — выполнено (METH-BACKLOG-POLISH): 6 history-only заглушек удалены (`SHORT_TARGET_ADOPTION_PROMPT`, `REVIEW_TEMPLATE`, `NEW_PROJECT_BOOTSTRAP_PROMPT`, `PROJECT_CHAT_START_PROMPT_TEMPLATE`, старый `TARGET_REPOSITORY_ADOPTION_GUIDE`, `PROJECT_LIFECYCLE`); `templates/TARGET_REPOSITORY_ADOPTION_CHAT_PROMPT.md` оставлен заглушкой (внешние bookmark); живые ссылки перенаправлены на каноны. Новый `TARGET_REPOSITORY_ADOPTION_GUIDE.md` из `METH-STABLE-MAIN-REFERENCE-RUSSIAN-FIRST-01` является live stable-reference entrypoint, не старой redirect-заглушкой.
- **Optional polish**: отдельно можно рассмотреть vendor/public metadata hygiene и historical English wording там, где это не нарушает Russian-first policy и не требует rewrite history; это не blocker для adoption.
- **Operating layer (`ASD-OPLAYER-001`, journal 0024)**: добавлены нейтральные контракты `ORCHESTRATOR_PROJECT_OPERATING_LAYER.md` и `CROSS_PROJECT_CONSOLIDATION_CONTRACT.md`, governance pack template расширен разделом «Три слоя управления». Опционально: при downstream adoption включать эти контракты в target governance pack как optional-файлы; реальные visibility-matrix и дайджесты держать в приватном control plane, не в публичном репозитории.
- **Future methodology simplification**: lifecycle simplification и remote PR state as authority реализованы в `METH-NO-ORDINARY-POST-MERGE-CLOSURE-01`; context handoff footer enforcement, journal gate automation и adoption feedback loop automation остаются future backlog и не являются blocker.

## Текущие операционные правила

1. Применять обновленный `ORCHESTRATOR_RESPONSE_STANDARD.md` и `ORCHESTRATOR_RESPONSE_TEMPLATE.md` при подготовке новых Engine-блоков.
2. Проверять Fast Lane -> Engine escalation при любой write-action recommendation.
3. Проверять русские пользовательские заголовки и описания в Engine-блоках.
4. Проверять Closure policy после сообщений о merge/release/sync: ordinary PR завершается на `architect_ready` / `human_merge_allowed`, merge facts брать из GitHub PR metadata, отдельный closure PR не создавать; boundary reconciliation нужна только перед release/audit boundary, при explicit architect request или для batch reconciliation.
5. Если journal stale внутри release/audit/explicit boundary reconciliation scope или противоречит GitHub facts в этом scope, создавать docs-only Engine-блок на reconciliation вместо ответа `все закрыто`.
6. Использовать `CODE_REVIEW_TASK_TEMPLATE.md` для первого безопасного review target implementation repository только после проверки, что task явно содержит режим, объект проверки, allowed/forbidden files и правило сохранения отчета. Review-задачи всегда журналируют TASK+RESULT (`Journal trace: always`).
7. При следующем target repository dry run читать methodology repository только из stable reference `origin/main` / `main`, release tag или явно заданного snapshot; dirty `developer`/`work/*` не считать blocker при доступном stable ref.
7a. Перед target adoption/source-update применять `TARGET_ADOPTION_DETECTOR.md`: Variant A/B/C или STOP; dirty target tree, unstable methodology source, private data risk и риск overwrite target-specific journal/history/state означают STOP.
7b. Перед file-changing PR применять `QUALITY_FIRST_WORKFLOW.md`: missing acceptance criteria или failed self-review означают STOP до PR.
8. Перед любым sync/checkout/switch/pull/merge применять `Repository sync / checkout guard`: root, remote, branch и `git status --short`; dirty tree → STOP.
9. При следующем target repository dry run фиксировать methodology feedback без private data и с sanitization checkpoint.
10. Отдельной future task рассмотреть tags/releases для methodology versioning, если commit-based `methodology_reference` окажется недостаточным.
