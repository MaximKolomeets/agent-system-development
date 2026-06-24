# TASK-0076 — METH-BWIN-ZERO-MATCH-SCAN-FALLBACK-01

## Режим

Роль: docs-maintainer. Исполнитель: на усмотрение архитектора. Reasoning effort: средний. Docs-only fix, Local only.

Batch-policy: открытые journal-записи не блокируют работу; closure не подмешивать.

## Execution timestamps

- execution_started_at: `2026-06-23T23:27:37.8208017+07:00`
- execution_finished_at: `заполняется в RESULT`
- reported_at: `заполняется в RESULT`

## Baseline

- repository: `MaximKolomeets/agent-system-development`
- base branch: `developer`
- work branch: `work/docs-maintainer-01/bwin-zero-match-scan-fallback-01`
- baseline SHA: `63875b53d6a77ffd14182167bc5125df96ba36d9`
- prerequisite: PR #222 merged into `developer`; local `developer` fast-forwarded to `63875b53d6a77ffd14182167bc5125df96ba36d9`.

## Цель

Закрепить B-WIN fallback для zero-match/no-output scans: если `rg` или wrapper/shell scan на Windows зависает без вывода и без живого полезного процесса, task повторяет scan deterministic sequential способом с явным exit code и фиксирует fallback в RESULT.

## Allowed files

- `docs/agent-system/ORCHESTRATOR_OPERATING_CONTRACT.md`
- `docs/agent-system/ORCHESTRATOR_RESPONSE_STANDARD.md`
- `docs/agent-system/templates/TASK_HEADER_COMMON.md`
- `docs/agent-system/ENGINE_JOURNAL_CONTRACT.md`
- `docs/agent-system/engine-journal/input/TASK-0076-METH-BWIN-ZERO-MATCH-SCAN-FALLBACK-01.md`
- `docs/agent-system/engine-journal/output/RESULT-0076-METH-BWIN-ZERO-MATCH-SCAN-FALLBACK-01.md`
- `docs/agent-system/engine-journal/INDEX.md`
- `docs/agent-system/cloud/**`

## Запрещено

- Не ставить git tag.
- Не создавать GitHub Release.
- Не менять `main`/`developer` напрямую.
- Не читать `.env`.
- Не печатать secrets/matching secret lines.
- Не переписывать append-only history.
- Не расширять scope на runtime tests, новые генераторы или unrelated templates/headings.

## Проверки

- `cmd /c "python docs\agent-system\tools\gen_file_map.py --check"`
- `cmd /c "python docs\agent-system\tools\gen_cloud_bundle.py --check"`
- `git diff --check`
- scan wording по новым fallback-формулировкам
- placeholder scan с deterministic fallback при no-output `rg` hang
- sensitive filename-only/count-only scan без печати matching lines
- branch guard перед commit

## Передача

Следующий: reviewer — review PR по B-WIN zero-match/no-output scan fallback; затем архитектор — merge; затем engine — batch-closure серии 0073..0076 перед release.
