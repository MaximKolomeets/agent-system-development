# RESULT-0015-METH-BRANCH-GUARD-precommit-rule

Файл результата: `docs/agent-system/engine-journal/output/RESULT-0015-METH-BRANCH-GUARD-precommit-rule.md`

Связанный TASK file: `docs/agent-system/engine-journal/input/TASK-0015-METH-BRANCH-GUARD-precommit-rule.md`

Идентификатор задачи: `METH-BRANCH-GUARD`

Номер sequence: `0015`

Агент: `docs-maintainer-01`

Engine: Claude Code

Timestamp (ISO-8601): `2026-06-16T07:46:27+07:00`

Baseline SHA (developer): `5405952a5660ce43f9aad219cddbb2b3c36a5241`

methodology_reference: см. канон в `docs/agent-system/ENGINE_ENTRYPOINT.md` → раздел «Methodology reference»; данные текущей задачи:

```yaml
methodology_reference:
  repository: MaximKolomeets/agent-system-development
  source_branch: developer
  source_commit: 5405952a5660ce43f9aad219cddbb2b3c36a5241
  checked_at: 2026-06-16T07:46:27+07:00
  reference_type: commit
  notes: "Точка после merge METH-GOVERNANCE-BOUNDARIES (#130) и JOURNAL-CLOSE-0013 (#131)."
```

## Подтверждённый whitelist

- `docs/agent-system/BRANCH_POLICY.md` — канон правила 3;
- `docs/agent-system/templates/TASK_HEADER_COMMON.md` — строка-проверка в чеклисте;
- `AGENTS.md` — короткая ссылка на канон;
- журнал: `engine-journal/input/TASK-0015-*.md`, `engine-journal/output/RESULT-0015-*.md`, `engine-journal/INDEX.md`.

## Правило 3 — pre-commit branch guard

**Канон** добавлен в `BRANCH_POLICY.md` → секция «work/<role>/*» → подраздел «Pre-commit branch guard (канон, правило 3)», сразу после правила 2 (изоляция веток):

- перед ЛЮБЫМ `git commit` агент проверяет `git rev-parse --abbrev-ref HEAD`;
- если HEAD не его рабочая ветка `work/<role>/<task>` (особенно `developer`/`main`) → `STOP`, переключиться на правильную work-ветку, затем коммитить;
- прямой коммит в `developer`/`main` запрещён даже локально (не только push); локальный коммит в `developer`/`main` — нарушение, даже если не запушен;
- обоснование: инцидент journal 0013 (resume сессии оставил HEAD на `developer`, коммит сначала лёг туда; remote уцелел только потому, что пушилась work-ветка).

**Ссылки на канон (без дублирования прозой):**

- `templates/TASK_HEADER_COMMON.md` → «Copy/Paste Completeness Check»: добавлен чеклист-пункт «Перед commit: `git rev-parse --abbrev-ref HEAD` == work-ветка задачи; если `developer`/`main` → STOP (канон: BRANCH_POLICY → Pre-commit branch guard)».
- `AGENTS.md`: добавлен bullet (после «Не менять `developer` напрямую») с краткой формулировкой и ссылкой на канон.

## Согласованность с правилами 1/2

- Правило 3 размещено в одном каноне (`BRANCH_POLICY.md`) рядом с правилом 2; формат подраздела «(канон, правило N)» единообразен с правилами 1 и 2.
- Не противоречит: правило 1 (main только через release-PR, мержит человек), правило 2 (изоляция веток), правило 3 (проверка HEAD перед commit, запрет локального коммита в developer/main) — взаимодополняющие.
- Существующие AGENTS-bullets про `main`/`developer`/namespace не дублируются: правило 3 — отдельный аспект (проверка ветки перед commit), добавлен одним bullet со ссылкой.
- `TASK_HEADER_COMMON.md` (канон шапки задач, C5B) теперь содержит branch guard как пункт completeness-чеклиста — попадает во все task-шаблоны, ссылающиеся на канон.

## Измененные файлы (этой задачей)

- `docs/agent-system/BRANCH_POLICY.md`
- `docs/agent-system/templates/TASK_HEADER_COMMON.md`
- `AGENTS.md`
- `docs/agent-system/engine-journal/input/TASK-0015-METH-BRANCH-GUARD-precommit-rule.md`
- `docs/agent-system/engine-journal/output/RESULT-0015-METH-BRANCH-GUARD-precommit-rule.md`
- `docs/agent-system/engine-journal/INDEX.md`

## Выполненные проверки

- Preflight: `git status`, `git fetch --all --prune`, `git switch developer`, `git pull --ff-only` (developer обновлён до `5405952` после merge #130/#131), `git rev-parse developer/origin/developer`, `git switch -c work/docs-maintainer-01/branch-guard`, `git rev-parse --abbrev-ref HEAD` == work-ветка.
- Чтение BRANCH_POLICY (post-#130), TASK_HEADER_COMMON, AGENTS до правок.
- Перед commit: `git rev-parse --abbrev-ref HEAD` == work-ветка (само правило 3 применено к этой задаче).
- `git status --short` — только whitelist + journal; `git diff --check` — чисто.

## Невыполненные проверки и причина

- Markdown lint — documented lint command не подтверждён.
- Docker/production — запрещены scope.

## Результат проверки запрещенных файлов

Файлы вне whitelist не изменялись. Правило не продублировано прозой (канон + ссылки). `.env` не читался.

## Результат проверки sensitive/private markers

Секреты не вводились и не печатались.

## Результат language policy

RESULT Russian-first; English только для technical identifiers, paths, filenames и literal terms.

## Принятые решения

- Канон правила 3 — `BRANCH_POLICY.md`, рядом с правилом 2 (общая тема «work-ветки»).
- В `TASK_HEADER_COMMON.md` правило вошло как пункт «Copy/Paste Completeness Check» (естественное место для pre-commit-проверки в шапке любой задачи).
- В `AGENTS.md` — один новый bullet со ссылкой, без дублирования прозой.

## Риски

- Нет. Документационное усиление, согласовано с правилами 1/2.

## Blockers

Нет.

## Закрытие после merge

Work PR URL: `https://github.com/MaximKolomeets/agent-system-development/pull/132`

Work PR status: `merged`

Work PR merge commit SHA: `d4c527b0541a0b56254e8cf5d654f95ab3b01684`

Work PR merged_at: `2026-06-16T00:49:13Z` (GitHub `mergedAt` через `gh`).

Release PR status: не применимо (перенос в `main` не выполнялся).

Release PR merge commit SHA: не применимо.

Release PR merged_at: не применимо.

Sync PR status: не применимо (sync `main -> developer` не выполнялся).

Sync PR merge commit SHA: не применимо.

Sync PR merged_at: не применимо.

RESULT closed after merge: yes

INDEX closed after merge: yes

No journal placeholders after merge: yes

Stale pre-merge status check: clean.

Closure source: GitHub `gh pr view 132`.

Closure blockers: нет.

## Следующий рекомендуемый шаг

После merge — closure 0015. Также остаётся закрыть journal 0014 (METH-GOVERNANCE-BOUNDARIES, PR #130 уже merged) отдельной closure-задачей. Далее — adoption на реальном target-проекте.

## Methodology feedback

Правило 3 — прямой урок из реального инцидента (0013), закреплённый в каноне и в completeness-чеклисте шапки задач. Это пример работающего methodology feedback loop: операционная ошибка → governance-правило → проверяемый чеклист-пункт, попадающий во все будущие task-шаблоны.
