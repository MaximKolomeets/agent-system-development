# TASK-0019-METH-AUDIT-POLISH

Дословная копия входной задачи METH-AUDIT-POLISH.

---

# Задача для docs-maintainer-01: METH-AUDIT-POLISH (закрытие 0018 + полировка findings + journal 0019)
Запуск: Local only. Engine: Claude Code. Модель: Claude Sonnet 4.6. Effort: Medium.
Режим: Agent, строгий whitelist. Каталог: C:\neural\repos\agent-system-development

## Цель
1) Закрыть journal 0018 (audit, PR #141 merged); 2) применить F-01/F-02/F-04; 3) зажурналировать как 0019. F-03 принимаем как историческое — RESULT-0001 НЕ трогаем.

## Ветки: base developer; work work/docs-maintainer-01/audit-polish

## Preflight
git fetch --all --prune; git switch developer && git pull --ff-only origin developer
git rev-parse developer && git rev-parse origin/developer
gh pr view 141 --json number,state,mergedAt,mergeCommit,url   # подтвердить merged + факты
git switch -c work/docs-maintainer-01/audit-polish
git rev-parse --abbrev-ref HEAD   # == work/docs-maintainer-01/audit-polish, иначе STOP

## Allowed files
docs/agent-system/templates/ADOPTION_PROMPT.md      # F-01
AGENTS.md                                           # F-02
docs/agent-system/CODE_REVIEW_WORKFLOW.md           # F-04
docs/agent-system/engine-journal/output/RESULT-0018-*.md   # closure 0018
docs/agent-system/engine-journal/output/RESULT-0019-*.md   # новая запись
docs/agent-system/engine-journal/input/TASK-0019-*.md
docs/agent-system/engine-journal/INDEX.md           # closure-строка 0018 + новая строка 0019

## Изменения
- F-01: в ADOPTION_PROMPT удалить дублирующую строку `ADOPTION_GUIDE.md` в списке «engine должен найти» (оставить одну каноническую); убедиться, что других дублей нет.
- F-02: AGENTS.md review-bullet привести к `Journal trace: always` — консистентно с ROLE_MODEL и CODE_REVIEW_WORKFLOW (ссылка на канон, без дубля прозой).
- F-04: CODE_REVIEW_WORKFLOW.md:~295 «Кандидаты на будущие задачи Codex/Engine» → «… Engine».
- Closure 0018: RESULT-0018 + INDEX-строка 0018 → status merged, merge SHA, merged_at (из gh #141); release/sync не применимо.
- Journal 0019: TASK-0019 (дословно эта задача), RESULT-0019 (что поправлено: F-01/F-02/F-04; F-03 принято как историческое; closure 0018 выполнен; baseline SHA; timestamp ISO-8601), INDEX-строка 0019. Без placeholders, Russian-first.

## Проверки / Commit / DoD / STOP
diff --check; перед commit git rev-parse --abbrev-ref HEAD == work-ветка (правило 3).
commit: docs(agent-system): polish audit findings F-01/02/04 + close journal 0018 (0019)
gh pr create base=developer.
DoD: F-01/02/04 применены; RESULT-0001 не тронут; 0018 закрыт фактами #141; 0019 без placeholders; diff чист; PR через gh; Russian-first.
STOP: HEAD не work-ветка; правка вне whitelist; #141 окажется не merged; противоречие; push требует credentials.
