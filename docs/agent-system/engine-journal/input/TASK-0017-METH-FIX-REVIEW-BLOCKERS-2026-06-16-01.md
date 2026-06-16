# TASK-0017-METH-FIX-REVIEW-BLOCKERS-2026-06-16-01

## Задача

Исправить merge-blocker findings из `METH-REVIEW-2026-06-16-01` после merge PR #136.

## Режим

- Агент: `docs-maintainer-01`
- Engine: Codex
- Запуск: Local only
- Reasoning: High
- Режим: Agent
- Scope: docs-only methodology fix и engine-journal artifacts

## Baseline

- Repository: `MaximKolomeets/agent-system-development`
- Base branch: `developer`
- Starting SHA: `f27165472c721ca3171c2cb49b5aea4cfa80aa27`
- Working branch: `work/docs-maintainer-01/meth-fix-review-blockers-2026-06-16-01`
- PR #136 должен быть merged до начала edits.

## Цель

1. Закрыть journal closure для 0014/0015 после release/sync PR #134/#135.
2. Закрыть journal entry 0016 после merge PR #136.
3. Согласовать review-only behavior: `Journal trace: always` независимо от `Report delivery`.
4. Добавить `Repository sync / checkout guard`.
5. Уточнить перенос engine-journal scaffold/templates без operational history methodology repository.
6. Обновить `CURRENT_STATE.md` и `NEXT_STEPS.md`.

## Разрешенные файлы

- `AGENTS.md`
- `docs/agent-system/CURRENT_STATE.md`
- `docs/agent-system/NEXT_STEPS.md`
- `docs/agent-system/WORKFLOW.md`
- `docs/agent-system/BRANCH_POLICY.md`
- `docs/agent-system/ROLE_MODEL.md`
- `docs/agent-system/CODE_REVIEW_WORKFLOW.md`
- `docs/agent-system/ENGINE_ENTRYPOINT.md`
- `docs/agent-system/ENGINE_JOURNAL_CONTRACT.md`
- `docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml`
- `docs/agent-system/templates/CODE_REVIEW_TASK_TEMPLATE.md`
- `docs/agent-system/templates/TASK_HEADER_COMMON.md`
- `docs/agent-system/engine-journal/INDEX.md`
- `docs/agent-system/engine-journal/input/TASK-0017-METH-FIX-REVIEW-BLOCKERS-2026-06-16-01.md`
- `docs/agent-system/engine-journal/output/RESULT-0017-METH-FIX-REVIEW-BLOCKERS-2026-06-16-01.md`
- `docs/agent-system/engine-journal/output/RESULT-0014-METH-GOVERNANCE-BOUNDARIES-branch-main-rules.md`
- `docs/agent-system/engine-journal/output/RESULT-0015-METH-BRANCH-GUARD-precommit-rule.md`
- `docs/agent-system/engine-journal/output/RESULT-0016-METH-REVIEW-2026-06-16-01-methodology-review.md`

## Запреты

- Не читать `.env` / `.env.*`.
- Не менять runtime, Docker, CI, scripts или production code.
- Не менять `main`/`developer` напрямую.
- Не использовать force push.
- Не печатать sensitive grep matching lines.
- Не добавлять private downstream data, credentials, tokens, passwords или private repository URLs.

## Обязательные checks

- `git status --short`
- `git branch --show-current`
- `git diff --check`
- `git diff --name-only developer...HEAD`
- forbidden tracked paths scan
- sensitive marker scan filename-only
- stale closure placeholder scans for 0014/0015/0016 and `INDEX.md`
- review-only wording consistency scan
- sync/checkout guard wording scan

## Финализация

Создать PR в `developer`, затем обновить RESULT/INDEX фактическими PR URL/status/checks. Не пытаться записывать self-referential SHA текущего commit внутрь самого commit.
