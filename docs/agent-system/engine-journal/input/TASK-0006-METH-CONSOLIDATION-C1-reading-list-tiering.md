# TASK-0006-METH-CONSOLIDATION-C1-reading-list-tiering

Дословная копия входной задачи METH-CONSOLIDATION-C1.

---

# Задача для docs-maintainer-01: METH-CONSOLIDATION-C1 (reading-list tiering)

## Режим
engine: docs-capable (рекомендуемый запуск — Claude Code). Local only. Reasoning: Medium. Agent, строгий allowed-files whitelist.

## Цель
Реализовать PR-C1 из плана: разнести reading-list на два уровня — Core (~10) и Reference. Объём и точные списки брать как авторитетные из RESULT-0004 (§10 PR-C1 и §5 reading-list). Контент не терять: ни один пункт не исчезает, только переносится в Core или Reference.

## Repository / каталог
MaximKolomeets/agent-system-development
C:\neural\repos\agent-system-development

## Ветки
- base: developer
- work: work/docs-maintainer-01/reading-list-tiering

## Авторитетный scope (прочитать первым)
docs/agent-system/engine-journal/output/RESULT-0004-*.md — §10 (PR-C1: какие файлы и как меняем) и §5 (точные Core / Reference списки). Исполнять как там определено.

## Allowed files
- Файлы reading-list/навигации, перечисленные для C1 в RESULT-0004 §10 — ТОЛЬКО они. Whitelist подтвердить из плана и зафиксировать в RESULT перед правками.
- + журнал: input/TASK-<next>, output/RESULT-<next>, INDEX.md (next по INDEX, ожидаемо 0006).

## Fork-guard (важно)
Если C1 зависит от нерешённой развилки Р1–Р5 (например, граница Core-списка не зафиксирована, а вынесена как развилка) — НЕ выбирать самостоятельно: STOP и вернуть развилку с вариантами и рекомендацией плана. Решение принимает архитектор.

## Forbidden
- любые файлы вне подтверждённого whitelist;
- удаление любого reading-list пункта (только перенос Core/Reference);
- удаление файлов; изменение смысла документов сверх тиринга;
- .env; main/developer напрямую; Docker; ввод credentials; редактирование RESULT прошлых задач.

## Preflight (после merge C6 + closure 0005)
cd C:\neural\repos\agent-system-development
git status --short --untracked-files=all
git fetch --all --prune
git switch developer && git pull --ff-only origin developer
git rev-parse developer && git rev-parse origin/developer
git switch -c work/docs-maintainer-01/reading-list-tiering

## Journal (обязательно)
TASK-<next>: дословная копия задачи. RESULT-<next>: что перенесено в Core/Reference, подтверждённый whitelist, baseline SHA, timestamp ISO-8601, task-id, ссылка на §10/§5. INDEX: запись <next>. Russian-first, без placeholders, append-only.

## Проверки
git diff --name-only      # только whitelist + журнал
git diff --check
Вручную: Core = список из §5 (~10); каждый прежний пункт reading-list присутствует в Core или Reference (ничего не потеряно); broken refs нет.

## Commit / push / PR (контур gh)
commit: docs(agent-system): tier reading-list into Core + Reference (C1)
git push -u origin work/docs-maintainer-01/reading-list-tiering
gh доступен → gh pr create base=developer; иначе → URL pull/new пользователю, пометка «PR создаёт пользователь». push требует credentials → STOP, не вводить.

## Definition of Done
- reading-list разнесён на Core (~10 по §5) + Reference; ни один пункт не потерян;
- изменены только подтверждённый whitelist + журнал; diff --check чист;
- TASK/RESULT/INDEX записаны (sequence, timestamp, baseline SHA), без placeholders;
- ветка запушена; PR создан или переданы URL/команды; RESULT содержит commit SHA и PR URL;
- Russian-first.
ЛИБО, если сработал fork-guard: ничего не менялось сверх журнала с зафиксированной развилкой, и развилка возвращена архитектору.

## STOP-условия
нерешённая развилка Р1–Р5 → STOP с вариантами; правка вне whitelist; RESULT-0004 недоступен; потеря пункта reading-list неизбежна; push требует credentials; секрет найден (не печатать).
