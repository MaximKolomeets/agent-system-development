# TASK-0075 — METH-V1-1-AUDIT-FINDINGS-FIX-01

## Режим

Роль: docs-maintainer. Исполнитель: на усмотрение архитектора. Reasoning effort: высокий — исправить findings полного аудита без расширения scope и без переписывания истории. Branch-guard обязателен.

Batch-policy: открытые journal-записи не блокируют работу; closure не подмешивать.

## Execution timestamps

- execution_started_at: `2026-06-23T23:06:53.2514820+07:00`
- execution_finished_at: `заполняется в RESULT`
- reported_at: `заполняется в RESULT`

## Baseline

- repository: `MaximKolomeets/agent-system-development`
- base branch: `developer`
- work branch: `work/docs-maintainer-01/v1-1-audit-findings-fix-01`
- baseline SHA: `d4b71327cbbf3bb5aeabccbf9031cd7147a5c23e`
- prerequisite: PR #221 merged into `developer`; local `developer` fast-forwarded to `d4b71327cbbf3bb5aeabccbf9031cd7147a5c23e`.

## Цель

Закрыть findings полного аудита #221:

- F-17: закрепить release-tag шаг как human-only действие после human merge release PR, с проверкой annotated tag на release merge commit `main` и reminder для `v1.0.0`.
- F-18: закрепить Windows sequential fallback для read-only generated `--check`, если wrapper/parallel runner зависает без полезного процесса.
- F-06: привести live state headings к Russian-first с техническим alias в скобках.
- F-10: безопасно нейтрализовать только live/freshness wording; append-only historical literals не переписывать.
- F-LEGACY: классифицировать старые terminal `stamp at merge` строки и не переписывать историю без отдельной journal-only задачи.

## Allowed files

- `docs/agent-system/BRANCH_POLICY.md`
- `docs/agent-system/RELEASE_READINESS.md`
- `docs/agent-system/PR_WORKFLOW.md`
- `docs/agent-system/WORKFLOW.md`
- `docs/agent-system/ORCHESTRATOR_OPERATING_CONTRACT.md`
- `docs/agent-system/ENGINE_JOURNAL_CONTRACT.md`
- `docs/agent-system/ORCHESTRATOR_RESPONSE_STANDARD.md`
- `docs/agent-system/CURRENT_STATE.md`
- `docs/agent-system/NEXT_STEPS.md`
- `docs/agent-system/templates/TASK_HEADER_COMMON.md`
- `docs/agent-system/engine-journal/input/TASK-0075-METH-V1-1-AUDIT-FINDINGS-FIX-01.md`
- `docs/agent-system/engine-journal/output/RESULT-0075-METH-V1-1-AUDIT-FINDINGS-FIX-01.md`
- `docs/agent-system/engine-journal/INDEX.md`
- `docs/agent-system/cloud/**`

## Запрещено

- Не создавать git tag и GitHub Release.
- Не менять `main`/`developer` напрямую.
- Не читать и не выводить `.env`, credentials, private data.
- Не переписывать append-only journal history, кроме новой записи 0075.
- Не исправлять closure rows 0073/0074 в этой задаче: они закрываются отдельным batch-closure.

## Проверки

- `python docs/agent-system/tools/gen_file_map.py --check`
- `python docs/agent-system/tools/gen_cloud_bundle.py --check`
- `git diff --check`
- release/tag wording scan по изменённым release-flow файлам
- generated fallback wording scan по 4 каноническим файлам
- Russian-first heading scan для live state headings
- branch guard: HEAD == `work/docs-maintainer-01/v1-1-audit-findings-fix-01`

## Передача

Следующий: reviewer — review PR по findings F-17/F-18/F-06/F-10/F-LEGACY; затем архитектор — merge; затем engine — batch-closure текущей fix-серии перед release.
