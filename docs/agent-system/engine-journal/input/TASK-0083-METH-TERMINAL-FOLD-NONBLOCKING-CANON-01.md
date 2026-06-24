# TASK-0083: METH-TERMINAL-FOLD-NONBLOCKING-CANON-01

Задача для docs-maintainer: METH-TERMINAL-FOLD-NONBLOCKING-CANON-01

Рекомендуемый режим исполнения:
Роль: docs-maintainer
Исполнитель: на усмотрение архитектора
Reasoning effort: высокий
Запуск: Local only
Режим: Agent

## Цель

Закрепить `terminal-fold accepted` как допустимое non-blocking lifecycle-состояние, чтобы closure/finalstate задачи не порождали бесконечную цепочку новых closure-задач.

## Verified execution baseline

- Repository: MaximKolomeets/agent-system-development.
- Base branch: `developer`.
- Work branch: `work/docs-maintainer-01/terminal-fold-nonblocking-canon-01`.
- Baseline SHA: `b783216cc3da08333ee7d197e1a6bab7bf544a80`.
- PR #229 precondition: MERGED; merge commit `b783216cc3da08333ee7d197e1a6bab7bf544a80`; mergedAt `2026-06-24T07:50:13Z`.
- Verification source: local git + `gh pr view 229 --json state,mergedAt,mergeCommit,headRefOid,url`.

## Execution timestamps

- Время начала выполнения (execution_started_at) [measured/engine]: 2026-06-24T14:52:34.8924248+07:00
- Время окончания выполнения (execution_finished_at) [measured/engine]: заполнить в RESULT
- Длительность выполнения (execution_duration) [measured/engine, опционально]: заполнить в RESULT
- Время человека, по факту (human_time_reported) [reported/human, опционально]: не отслеживалось

## Allowed files

- `docs/agent-system/ENGINE_JOURNAL_CONTRACT.md`
- `docs/agent-system/templates/BATCH_CLOSURE_TASK_TEMPLATE.md`
- `docs/agent-system/templates/CLOSURE_TASK_TEMPLATE.md`
- `docs/agent-system/templates/TASK_HEADER_COMMON.md`
- `docs/agent-system/ORCHESTRATOR_RESPONSE_STANDARD.md`
- `docs/agent-system/BRANCH_POLICY.md`
- `docs/agent-system/RELEASE_READINESS.md`
- `docs/agent-system/ORCHESTRATOR_OPERATING_CONTRACT.md`
- `docs/agent-system/engine-journal/output/RESULT-0079-*.md`
- `docs/agent-system/engine-journal/output/RESULT-0082-*.md`
- `docs/agent-system/engine-journal/input/TASK-0083-METH-TERMINAL-FOLD-NONBLOCKING-CANON-01.md`
- `docs/agent-system/engine-journal/output/RESULT-0083-METH-TERMINAL-FOLD-NONBLOCKING-CANON-01.md`
- `docs/agent-system/engine-journal/INDEX.md`
- `docs/agent-system/cloud/**`

## Required changes

1. Add authoritative accepted terminal fold canon to `ENGINE_JOURNAL_CONTRACT.md`.
2. Align closure templates, task header, orchestrator response/operating contract and branch release gate.
3. Normalize lifecycle-only terminal rows 0079 and 0082 to `terminal-fold accepted`.
4. Add this TASK/RESULT/INDEX trace as seq 0083 with accepted terminal fold status, not `open`.
5. Regenerate `docs/agent-system/cloud/**`.

## Checks

- `cmd /c "python docs\agent-system\tools\gen_file_map.py --check"` -> exit 0.
- `cmd /c "python docs\agent-system\tools\gen_cloud_bundle.py --check"` -> exit 0.
- `git diff --check origin/developer...HEAD` -> exit 0.
- wording scan for accepted terminal fold terms.
- INDEX continuity / TASK/RESULT pairing.
- stale surface scan excluding accepted terminal fold.
- placeholder scan.
- sensitive filename-only/count-only scan without printing matching lines.

## Передача

Следующий: архитектор — review/merge PR; затем engine — release-prep v1.1.0 без отдельной closure-задачи только ради accepted terminal fold.
