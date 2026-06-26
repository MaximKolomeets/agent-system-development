# TASK-0107 — METH-CHECK-TASK-READY-01

execution_started_at: `2026-06-25T22:49:31.8634180+07:00`

## Режим

Роль: methodology-architect-01
Исполнитель: на усмотрение архитектора
Reasoning effort: средний
Режим: Agent, methodology tooling task
Branch: `work/methodology-architect-01/meth-check-task-ready-01`
Base: `developer`

## Цель

Добавить lightweight read-only ready-gate `docs/agent-system/tools/check_task_ready.py`, чтобы engine перед push/PR/fix-pass/review-comment одной командой проверял типовые machine-verifiable blockers: branch guard, changed files summary, whitespace diff, generated parity, sensitive filename/count-only scans, strict added-line secret scan и TASK/RESULT placeholder scan.

## Scope

Разрешённые изменения:

- `docs/agent-system/tools/check_task_ready.py`
- `docs/agent-system/REVIEW_AUTOLOOP.md`
- `docs/agent-system/OPERATIONAL_FAST_LANE.md`
- `docs/agent-system/ORCHESTRATOR_RESPONSE_STANDARD.md`
- `docs/agent-system/BACKLOG.md`
- `docs/agent-system/CURRENT_STATE.md`
- `docs/agent-system/NEXT_STEPS.md`
- `docs/agent-system/DECISION_LOG.md`
- `docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml`
- `docs/agent-system/PROJECT_FILE_MAP.md`
- `docs/agent-system/cloud/**`
- journal artifacts `0107`

Запрещено:

- менять product/runtime repositories, verification repository или private downstream repository;
- читать `.env` или выводить secrets;
- менять runtime/Docker/CI/branch protection;
- создавать release PR, merge, tag или closure PR;
- переписывать старую journal history;
- выполнять destructive git commands внутри нового tool.

## Требования

1. `check_task_ready.py` должен быть read-only и не выполнять `fetch`, `pull`, `switch`, `merge`, `stash`, `reset` или `clean`.
2. CLI: `python docs/agent-system/tools/check_task_ready.py --base origin/developer`; опции `--base`, `--strict`, `--json`.
3. Tool должен выводить human summary и JSON summary без secret values.
4. Tool должен блокировать changed files на `main`/`developer` и changed files вне `work/*`.
5. Tool должен запускать generated checks только при изменении generated/bundle-source файлов.
6. Tool должен считать forbidden paths, sensitive filenames и strict added-line secret patterns без печати matching lines.
7. Tool должен проверять changed TASK/RESULT на unresolved placeholders.
8. Документы autoloop/fast-lane/orchestrator response должны ссылаться на ready-gate как recommended machine-verifiable check.
9. Manifest и PROJECT_FILE_MAP должны зарегистрировать новый source tool.
10. Cloud bundle должен быть regenerated после изменений bundle-source и INDEX.

## Проверки

- `python docs/agent-system/tools/check_task_ready.py --base origin/developer`
- `python docs/agent-system/tools/check_task_ready.py --base origin/developer --json`
- `python docs/agent-system/tools/gen_file_map.py --check`
- `python docs/agent-system/tools/gen_cloud_bundle.py --check`
- `git diff --check origin/developer...HEAD`
- `git diff --name-only origin/developer...HEAD`
- `git diff --stat origin/developer...HEAD`
- `git status --short -uall`
- forbidden/sensitive scans без вывода secret values

## Передача

Следующий: reviewer — проверить read-only характер tool, полноту агрегированных checks, отсутствие secret output, консистентность autoloop/fast-lane/orchestrator docs и generated parity; затем архитектор — human merge в `developer`.
