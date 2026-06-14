# TASK-0007-METH-CONSOLIDATION-C2-methodology-reference-canon

Дословная копия входной задачи METH-CONSOLIDATION-C2.

---

# Задача для docs-maintainer-01: METH-CONSOLIDATION-C2 (methodology_reference canon)

## Режим
engine: docs-capable (рекомендуемый запуск — Claude Code). Local only. Reasoning: Medium. Agent, строгий allowed-files whitelist.

## Цель
Реализовать PR-C2 из плана: свести дублирование methodology_reference (и source_snapshot, если в scope §10) к одному канону, остальные места заменить ссылкой. Контент не терять: канон сперва вбирает всё уникальное, и только потом дубль убирается из не-канон файлов.

## Repository / каталог
MaximKolomeets/agent-system-development
C:\neural\repos\agent-system-development

## Ветки
- base: developer
- work: work/docs-maintainer-01/methodology-reference-canon

## Авторитетный scope (прочитать первым)
docs/agent-system/engine-journal/output/RESULT-0004-*.md:
- §10 (PR-C2: точный whitelist и подход),
- §6 (где methodology_reference дублируется, какой файл канон, что заменить ссылкой),
- §4 (карта content-preservation),
- §8 (какие перекрёстные ссылки и ADOPTION_TRANSFER_MANIFEST.yml обновить).
Исполнять как там определено. Канон — по §6 (кандидат ENGINE_ENTRYPOINT.md).

## Allowed files
- Только файлы, перечисленные для PR-C2 в RESULT-0004 §10 (4 места methodology_reference + source_snapshot + manifest, если указан). Whitelist подтвердить из плана и зафиксировать в RESULT перед правками.
- + журнал: input/TASK-<next>, output/RESULT-<next>, INDEX.md (next по INDEX, ожидаемо 0007).

## Fork-guard
Если C2 неожиданно упирается в развилку Р1–Р5 — STOP и вернуть её с вариантами. Не выбирать самостоятельно.

## Content-preservation (критично)
- Перед удалением спеки methodology_reference из НЕ-канон файла убедиться, что весь её уникальный контент уже присутствует в каноне.
- «Бездомный» контент (нет чистого места в каноне) → STOP и вернуть как развилку, не удалять.
- В не-канон местах оставить явную ссылку на канон.

## Forbidden
- файлы вне подтверждённого whitelist;
- удаление уникального контента без переноса в канон;
- .env; main/developer напрямую; Docker; ввод credentials; редактирование RESULT прошлых задач.

## Preflight (после merge C1 + closure 0006)
cd C:\neural\repos\agent-system-development
git status --short --untracked-files=all
git fetch --all --prune
git switch developer && git pull --ff-only origin developer
git rev-parse developer && git rev-parse origin/developer
git switch -c work/docs-maintainer-01/methodology-reference-canon

## Journal (обязательно)
TASK-<next>: дословная копия задачи. RESULT-<next>: что стало каноном, что заменено ссылкой, карта переноса контента, обновлённые перекрёстные ссылки/манифест, подтверждённый whitelist, baseline SHA, timestamp ISO-8601, task-id, ссылки на §6/§4/§8. INDEX: запись <next>. Russian-first, без placeholders, append-only.

## Проверки
git diff --name-only      # только whitelist + журнал
git diff --check
git grep -n "methodology_reference" -- docs   # дубли спеки исчезли, ссылки на канон присутствуют
Вручную: канон полон; не-канон места ссылаются; broken refs нет; manifest синхронизирован, если был в scope.

## Commit / push / PR (контур gh)
commit: docs(agent-system): canonicalize methodology_reference (C2)
git push -u origin work/docs-maintainer-01/methodology-reference-canon
gh доступен → gh pr create base=developer; иначе → URL pull/new пользователю. push требует credentials → STOP, не вводить.

## Definition of Done
- methodology_reference определён в одном каноне; остальные места — ссылка; уникальный контент не потерян;
- перекрёстные ссылки/манифест обновлены по §8;
- изменены только подтверждённый whitelist + журнал; diff --check чист;
- TASK/RESULT/INDEX записаны (sequence, timestamp, baseline SHA), без placeholders;
- ветка запушена; PR создан или переданы URL/команды; RESULT содержит commit SHA и PR URL;
- Russian-first.
ЛИБО fork-guard/бездомный контент → ничего сверх журнала не менялось, развилка возвращена.

## STOP-условия
развилка Р1–Р5 или бездомный контент → STOP с вариантами; правка вне whitelist; RESULT-0004 недоступен; push требует credentials; секрет найден (не печатать).
