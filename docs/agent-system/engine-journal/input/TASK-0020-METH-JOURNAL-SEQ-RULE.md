# TASK-0020-METH-JOURNAL-SEQ-RULE

Дословная копия входной задачи METH-JOURNAL-SEQ-RULE.

---

# Задача для docs-maintainer-01: METH-JOURNAL-SEQ-RULE (кодификация F-05)
Запуск: Local only. Engine: Claude Code. Модель: Claude Sonnet 4.6. Effort: Low.
Режим: Agent, строгий whitelist. Каталог: C:\neural\repos\agent-system-development

## Цель
Закрепить правило: следующий sequence-номер журнала берётся ИЗ INDEX на момент выполнения, а не предугадывается в task-блоке (класс инцидента F-05).

## Ветки: base developer; work work/docs-maintainer-01/journal-seq-rule

## Preflight (ПОСЛЕ merge #143)
git fetch --all --prune
git switch developer && git pull --ff-only origin developer
git rev-parse developer && git rev-parse origin/developer
git switch -c work/docs-maintainer-01/journal-seq-rule
git rev-parse --abbrev-ref HEAD     # == work/docs-maintainer-01/journal-seq-rule, иначе STOP

## Allowed files
docs/agent-system/ENGINE_JOURNAL_CONTRACT.md
+ журнал: input/TASK-0020-*, output/RESULT-0020-*, INDEX.md (строка 0020, next по INDEX)

## Изменение (рядом с существующим правилом нумерации, НЕ дублировать прозой)
Добавить в ENGINE_JOURNAL_CONTRACT короткое правило:
«Нумерация sequence — append-only. Следующий номер engine вычисляет ИЗ INDEX на момент выполнения задачи (последний seq + 1) и ИГНОРИРУЕТ любой номер, предсказанный в task-блоке. Нельзя предугадывать, переиспользовать или пропускать seq. Обоснование: параллельная работа может занять предсказанный номер (журнал 0018: блок предписывал 0016, но 0016/0017 были заняты → запись корректно ушла в 0018).»
Согласовать формулировку с уже имеющимся разделом про последовательную нумерацию; если правило о нумерации уже есть — дополнить его этим уточнением, а не заводить второй параграф.

## Проверки / Commit / DoD / STOP
git diff --name-only   # только ENGINE_JOURNAL_CONTRACT + журнал
git diff --check
Перед commit: git rev-parse --abbrev-ref HEAD == work-ветка (правило 3).
commit: docs(agent-system): derive journal seq from INDEX, never predict (F-05)
git push -u origin work/docs-maintainer-01/journal-seq-rule ; gh pr create base=developer.
DoD: правило добавлено каноном (без дубля прозой); только whitelist+журнал; 0020 без placeholders; diff чист; PR через gh; Russian-first.
STOP: HEAD не work-ветка; правка вне whitelist; противоречие с существующим правилом нумерации; push требует credentials.
