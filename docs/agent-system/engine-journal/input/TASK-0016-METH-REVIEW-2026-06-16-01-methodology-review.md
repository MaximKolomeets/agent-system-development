# TASK-0016-METH-REVIEW-2026-06-16-01-methodology-review

Файл задачи: `docs/agent-system/engine-journal/input/TASK-0016-METH-REVIEW-2026-06-16-01-methodology-review.md`

Идентификатор задачи: `METH-REVIEW-2026-06-16-01`

Номер sequence: `0016`

Агент: `code-reviewer-01`

Режим: review-only, строгий whitelist, journal trace always.

Report delivery: chat. Полный body review-отчета не сохранять в repository.

Каталог: `C:\neural\repos\agent-system-development`

Base branch: `developer`

Work branch: `work/code-reviewer-01/meth-review-2026-06-16-01`

## Цель

Провести комплексную review-only проверку актуального methodology repository после последних governance, branch-policy, journal и release/sync изменений.

Проверить согласованность обязательных Core/Reference документов, engine-journal, target-adoption инструкций, Russian-first policy, public repository hygiene, branch/release policy и отсутствие stale closure-state.

## Allowed files

- `docs/agent-system/engine-journal/input/TASK-0016-METH-REVIEW-2026-06-16-01-methodology-review.md`
- `docs/agent-system/engine-journal/output/RESULT-0016-METH-REVIEW-2026-06-16-01-methodology-review.md`
- `docs/agent-system/engine-journal/INDEX.md`

Полный review body сохраняется только в chat final report, не в repository.

## Forbidden files / scope

- Не менять production/methodology docs за пределами трех journal-файлов.
- Не читать `.env`.
- Не менять `main`/`developer` напрямую.
- Не коммитить `.env`, `.venv`, `data/`, `runtime/`, `dist/`, `backups/`, `exports/`.
- Не добавлять private downstream project names, credentials или корпоративные данные.
- Не запускать development executor и не исправлять найденные issues в рамках review-only задачи.

## Обязательные preflight checks

- Проверить текущий repository root и remote.
- Синхронизировать `developer` с GitHub.
- Создать work branch от актуального `developer`.
- Перед любым commit выполнить branch guard: `git rev-parse --abbrev-ref HEAD` должен вернуть `work/code-reviewer-01/meth-review-2026-06-16-01`.
- Проверить `git status --short`, changed-file scope и `git diff --check`.

## Обязательное чтение / проверка

Core:

- `AGENTS.md`
- `README.md`
- `docs/agent-system/CURRENT_STATE.md`
- `docs/agent-system/NEXT_STEPS.md`
- `docs/agent-system/ROLE_MODEL.md`
- `docs/agent-system/WORKFLOW.md`
- `docs/agent-system/BRANCH_POLICY.md`
- `docs/agent-system/CODE_REVIEW_WORKFLOW.md`
- `docs/agent-system/ENGINE_ENTRYPOINT.md`
- `docs/agent-system/ENGINE_JOURNAL_CONTRACT.md`

Reference/templates:

- `docs/agent-system/OPERATIONAL_FAST_LANE.md`
- `docs/agent-system/ADOPTION_GUIDE.md`
- `docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml`
- `docs/agent-system/DOWNSTREAM_ADAPTATION_CHECKLIST.md`
- `docs/agent-system/LANGUAGE_POLICY.md`
- `docs/agent-system/METHODOLOGY_FEEDBACK_LOOP.md`
- `docs/agent-system/source/README.md`
- `docs/agent-system/source/SOURCE_agent_system_index.md`
- `docs/agent-system/templates/ADOPTION_PROMPT.md`
- `docs/agent-system/templates/TASK_HEADER_COMMON.md`
- `docs/agent-system/templates/CODE_REVIEW_TASK_TEMPLATE.md`
- `docs/agent-system/templates/CODE_REVIEW_REPORT_TEMPLATE.md`
- `docs/agent-system/templates/TARGET_REPOSITORY_ADOPTION_CHAT_PROMPT.md`

## Review axes

- GitHub/repository state versus local `developer`, `main`, release/sync PR state.
- Engine journal closure correctness, absence of ready-for-review placeholders.
- Review-only workflow consistency: `Journal trace: always`, `Report delivery: chat`.
- Branch policy: `main` through release PR only, `developer` through PR after bootstrap, work branch isolation, pre-commit branch guard.
- Target-adoption safety and Russian-first policy.
- Public repository hygiene: no private downstream names, no credentials, no forbidden runtime/export directories.
- Vendor-neutral naming boundaries.
- Stale state in `CURRENT_STATE.md`, `NEXT_STEPS.md`, source snapshot and manifest/template routing.

## Required final report shape

Финальный chat report должен быть Russian-first и включать:

1. Краткий verdict.
2. Проверенный baseline.
3. GitHub state.
4. Mandatory files coverage.
5. Findings with severity and file/line evidence.
6. Merge blockers.
7. Non-blocking candidates.
8. False positives / intentional historical context.
9. Security/public hygiene.
10. Language consistency.
11. Source snapshot status.
12. Branch/release workflow status.
13. Journal trace status.
14. Проверки/команды.
15. Измененные файлы.
16. PR/journal finalization status.
17. Methodology feedback.

## DoD

- Review выполнен без правок production/methodology docs.
- Созданы TASK/RESULT/INDEX journal artifacts.
- Journal RESULT/INDEX финализированы после PR creation: указаны PR URL/status и commit SHA, без unresolved placeholders.
- Commit сделан только из work branch.
- Branch pushed.
- PR создан в `developer`.
- Финальный полный review report возвращен в chat.
