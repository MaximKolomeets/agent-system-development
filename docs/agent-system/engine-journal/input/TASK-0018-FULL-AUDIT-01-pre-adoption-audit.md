# TASK-0018-FULL-AUDIT-01-pre-adoption-audit

Дословная копия входной задачи FULL-AUDIT-01.

Примечание о sequence: задача предписывала запись под 0016, но sequence 0016 (METH-REVIEW-2026-06-16-01) и 0017 (METH-FIX-REVIEW-BLOCKERS-2026-06-16-01) уже заняты параллельной работой архитектора. По append-only + уникальности sequence (ENGINE_JOURNAL_CONTRACT.md) эта задача записана под следующий свободный sequence — 0018. См. finding F-05 в RESULT.

---

# Задача для qa-reviewer-01: FULL-AUDIT-01 (read-only, комплексный аудит перед adoption)
Запуск: Local only. Engine: Claude Code. Модель: Claude Opus 4.8. Effort: High.
Режим: Agent, READ-ONLY на контент (запись ТОЛЬКО в журнал).
Каталог: C:\neural\repos\agent-system-development

## Цель
Сплошной аудит методологии: найти всё, что могло проскочить — broken refs, противоречия, осиротевший контент, stale-журнал, несоответствия governance, последствия новых ручных правок. ТОЛЬКО findings, без исправлений.

## Ветки: base developer; work work/qa-reviewer-01/full-audit

## Allowed WRITE (только журнал)
docs/agent-system/engine-journal/input/TASK-0016-FULL-AUDIT-01-*.md
docs/agent-system/engine-journal/output/RESULT-0016-FULL-AUDIT-01-*.md
docs/agent-system/engine-journal/INDEX.md (строка 0016)
READ: весь репозиторий.
Forbidden: любые правки контента/шаблонов/доков — только журнал; .env; main/developer напрямую.

## Preflight
git fetch --all --prune; git switch developer && git pull --ff-only origin developer
git rev-parse developer && git rev-parse origin/developer
git status --short   # uncommitted-изменения → зафиксировать как находку, не трогать
git switch -c work/qa-reviewer-01/full-audit
git rev-parse --abbrev-ref HEAD   # == work/qa-reviewer-01/full-audit, иначе STOP
зафиксировать baseline SHA developer.

## Объём (пройти ВСЁ, по 8 разделам)
1. Инвентаризация/структура: перечислить docs/agent-system/** и templates/**; осиротевшие файлы (нет входящих ссылок) и отсутствующие каноны.
2. Целостность ссылок: просканировать все внутренние ссылки/pointer'ы; отделить ЖИВЫЕ broken refs от исторической прозы (past-tense «удалён/слит») — в находки только живые.
3. Консистентность: reading-list Core(10) == фактические файлы; каноны vs ссылки (governance 1/2/3; methodology_reference=ENGINE_ENTRYPOINT; source_snapshot=source/README; adoption=ADOPTION_PROMPT/ADOPTION_GUIDE); нет правил, продублированных прозой; нет противоречий.
4. Журнал: INDEX 0001–0015 — без дыр в нумерации, все статусы merged/closed, НЕТ stale «open», НЕТ placeholder'ов; у каждой записи RESULT с baseline SHA и merge-фактами; парность input↔output; terminal-closures без собственных записей.
5. Governance: правила 1/2/3 в каноне BRANCH_POLICY + корректные ссылки в ROLE_MODEL/AGENTS; строка branch-guard в TASK_HEADER_COMMON; forbidden-list AGENTS не противоречит канону.
6. Готовность к adoption: ADOPTION_PROMPT, ADOPTION_GUIDE, NEW_PROJECT_PROMPT/CHECKLIST, ADOPTION_TRANSFER_MANIFEST, ENGINE_ENTRYPOINT — связно, без broken refs, scaffold не сломает реальный target, manifest-категории актуальны.
7. Новые ручные правки: git log/diff developer с baseline RESULT-0012 (f76d661) ИЛИ с SHA, который укажет архитектор — перечислить коммиты вне journal-потока, проверить на консистентность/refs/governance; прямые правки архитектора отметить как процессную заметку (не блокер).
8. Остатки: скан TODO/FIXME/placeholder; висячие ссылки на завершённый backlog (PR-C6.1, 6 удалённых заглушек, CHAT_PROMPT); актуальность manifest.

## RESULT-0016 содержит
- таблицу findings: id · severity (blocker/major/minor/nit) · файл · описание · предлагаемое исправление (НЕ выполнять);
- отдельный подраздел «Новые ручные правки» с оценкой;
- общий вердикт: ready / hold-minor / hold-blockers;
- baseline SHA, timestamp ISO-8601, Russian-first, без placeholders.

## Commit / DoD / STOP
Перед commit: git rev-parse --abbrev-ref HEAD == work-ветка (правило 3).
commit: docs(journal): full pre-adoption audit (0016); gh pr create base=developer.
DoD: 8 разделов пройдены; findings с severity; вердикт; изменён только журнал; diff --check чист; PR через gh; Russian-first.
STOP: HEAD не work-ветка; соблазн исправить контент (нельзя — только findings); push требует credentials.
