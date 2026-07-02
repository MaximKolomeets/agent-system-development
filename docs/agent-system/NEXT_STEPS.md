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

`v1.5.1` опубликован и синхронизирован: release-prep PR #303, release PR #304,
annotated tag `v1.5.1` и sync PR #305 подтверждены. Этот файл больше не ставит
задачу создать release PR для `v1.5.1`.

Ближайший рабочий шаг: завершить PR-1/H1 state/status refresh для `v1.5.2`
hardening series, затем после human merge перейти к PR-2/H2 (`Journal history
scope clarity`). До публикации `v1.5.2` target adoption/source-update задачи
используют stable pointer `origin/main` / tag `v1.5.1`.

Точные task/PR факты остаются в `docs/agent-system/engine-journal/INDEX.md`,
`RESULT-*` closure-stamps и GitHub metadata. Release/status snapshot:
`docs/agent-system/RELEASE_READINESS.md`; ruleset snapshot:
`docs/agent-system/RULESET_STATUS.md`.

## Ближайшая очередь v1.5.2

1. PR-1/H1: post-release state/status refresh, `BACKLOG`/`NEXT_STEPS` split,
   ruleset status, cloud regeneration.
2. PR-2/H2: journal history scope clarity.
3. PR-3/H3: time and cost accounting hard-gate.
4. PR-4/H4: stable-reference schema sync.
5. PR-5/H5: navigation/discovery overlays and checklist tooling.
6. PR-6/H9, PR-7/H13, PR-8/H14: release authority, UAT gate, hotfix/rollback.

Полная future-очередь и менее срочные P2/P3 items живут в `BACKLOG.md`, чтобы
`NEXT_STEPS.md` оставался списком ближайших действий.

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
