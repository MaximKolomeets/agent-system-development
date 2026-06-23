# TASK-0062-METH-RELEASE-PREP-DEV-TO-MAIN-01

Роль: docs-maintainer.
Исполнитель: на усмотрение архитектора.
Reasoning effort: высокий.
Запуск: Local only.
Режим: Agent.

## Цель

Выполнить release-prep gate перед human release:

1. Закрыть per-task journal seq `0061` по merge-фактам PR #205.
2. Подтвердить, что journal `0055..0061` закрыт сквозняком, а generated checks проходят.
3. Создать terminal release-prep journal entry `0062`.
4. Открыть closure-PR `work/docs-maintainer-01/release-prep-dev-to-main-01` -> `developer`.
5. Не открывать release PR `developer -> main`, пока closure-PR 0062 не merged в `developer`.

## Baseline

- Repository: `MaximKolomeets/agent-system-development`.
- Base branch: `developer`.
- Work branch: `work/docs-maintainer-01/release-prep-dev-to-main-01`.
- Baseline `developer`: `e8761f7ec206214ab462564edc54d1dc3959abba`.
- Verification source: local git + GitHub PR state.
- Verification timestamp: `2026-06-23T09:00:21+07:00`.
- PR #205: `MERGED`, merge commit `e8761f7ec206214ab462564edc54d1dc3959abba`, merged at `2026-06-23T01:58:50Z`.

## Scope

Allowed files:

- `docs/agent-system/engine-journal/output/RESULT-0061-*.md` (append closure-stamp only)
- `docs/agent-system/engine-journal/INDEX.md`
- `docs/agent-system/engine-journal/input/TASK-0062-METH-RELEASE-PREP-DEV-TO-MAIN-01.md`
- `docs/agent-system/engine-journal/output/RESULT-0062-METH-RELEASE-PREP-DEV-TO-MAIN-01.md`
- `docs/agent-system/cloud/**`

Forbidden:

- Methodology content docs/templates/contracts/generators/manifest/file-map.
- Direct changes to `main` or `developer`.
- Release PR merge, tag creation, force push.
- `.env`, secrets, runtime/CI/private downstream data.

## Checks

- `python docs/agent-system/tools/gen_file_map.py --check`
- `python docs/agent-system/tools/gen_cloud_bundle.py --check`
- `git diff --check`
- INDEX scan: `0055..0061` closed, `0062` present, no pre-merge placeholders.

## Release handoff

Release PR `developer -> main` is intentionally not opened by this branch until closure-PR 0062 is merged. After architect merges closure-PR 0062, engine must pull `developer`, rerun both checks, then open release PR `developer -> main` with release notes. Release PR merge and tag creation are human-only.

## Передача

Следующий: reviewer — consistency-gate closure-PR 0062; затем архитектор — merge closure-PR 0062; затем engine — open release PR `developer -> main` (не мержить); затем архитектор — merge release PR + annotated tag; затем engine — sync `main -> developer`, branch cleanup, downstream adoption on tag.
