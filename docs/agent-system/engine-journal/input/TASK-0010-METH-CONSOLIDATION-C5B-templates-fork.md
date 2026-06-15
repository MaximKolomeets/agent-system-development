# TASK-0010-METH-CONSOLIDATION-C5B-templates-fork

Дословная копия входной задачи METH-CONSOLIDATION-C5B.

---

# Задача для docs-maintainer-01: METH-CONSOLIDATION-C5B (templates fork-часть: Р4 + Р5)

## Рекомендуемый режим engine
Запуск: Local only. Рекомендуемый engine: Claude Code.
Модель: Claude Opus
Effort (reasoning): High
Режим: Agent, строгий allowed-files whitelist.
Почему: слияние шаблонов с обязательной сохранностью уникального контента — цена ошибки высокая, нужна аккуратность.

## Цель
Реализовать fork-часть PR-C5 по решениям архитектора:
- Р4 = B: общий header `DEVELOPMENT_TASK_TEMPLATE` + `AGENT_RESEARCH_TASK_TEMPLATE` вынести в один канон; тела шаблонов оставить раздельными, оба ссылаются на канон.
- Р5 = умеренная: `NEW_PROJECT_BOOTSTRAP_PROMPT` + `PROJECT_CHAT_START_PROMPT_TEMPLATE` свести в один new-project prompt канон; `NEW_PROJECT_CHECKLIST` оставить отдельным.
Контент не терять.

## Repository / каталог
MaximKolomeets/agent-system-development
C:\neural\repos\agent-system-development

## Ветки
- base: developer
- work: work/docs-maintainer-01/templates-fork

## Авторитетный scope (прочитать первым)
RESULT-0004 §7 (инвентаризация templates), §10 (whitelist C5), §4 (content-preservation), §9 (Р4/Р5 — для сверки контента; решения уже приняты архитектором, см. ниже; при расхождении формулировок приоритет у решений архитектора, зафиксировать).

## Решения архитектора (приоритетны над дефолтами плана)
- Р4 = B (header→канон, тела раздельные).
- Р5 = умеренная: merge двух prompt в один канон; CHECKLIST отдельно.
Оба решения явно отметить в RESULT как «решение архитектора».

## Allowed files
- Р4: `DEVELOPMENT_TASK_TEMPLATE.md`, `AGENT_RESEARCH_TASK_TEMPLATE.md`, новый header-канон (имя по §7, напр. templates/TASK_HEADER_COMMON.md);
- Р5: `NEW_PROJECT_BOOTSTRAP_PROMPT.md`, `PROJECT_CHAT_START_PROMPT_TEMPLATE.md`, новый канон (напр. templates/NEW_PROJECT_PROMPT.md); `NEW_PROJECT_CHECKLIST.md` НЕ трогать;
- файлы с inbound-ссылками на затронутые шаблоны по §8 — подтвердить из плана;
- + журнал: input/TASK-<next>, output/RESULT-<next>, INDEX.md (next по INDEX, ожидаемо 0010).
Whitelist подтвердить из плана и зафиксировать в RESULT перед правками.

## Правила (как в C3/C5A)
- merge переносит весь уникальный контент в канон ДО развязки; бездомный контент → STOP, вернуть как развилку;
- развязка старого файла: удалить только при 0 inbound-ссылок (grep); если ссылка вне whitelist или в append-only истории — redirect-заглушка; broken refs недопустимы;
- append-only историю (journal, DECISION_LOG, agents/*) не переписывать.

## Forbidden
- файлы вне подтверждённого whitelist; `NEW_PROJECT_CHECKLIST.md`; .env; main/developer напрямую; Docker; ввод credentials; редактирование RESULT прошлых задач; broken refs.

## Preflight (после merge C5A + closure 0009)
cd C:\neural\repos\agent-system-development
git status --short --untracked-files=all
git fetch --all --prune
git switch developer && git pull --ff-only origin developer
git rev-parse developer && git rev-parse origin/developer
git switch -c work/docs-maintainer-01/templates-fork

## Journal (обязательно)
TASK-<next>: дословная копия. RESULT-<next>: что вынесено в каноны (Р4 header, Р5 prompt), карта переноса контента, исходы развязок (delete/stub), обновлённые ссылки, подтверждённый whitelist, baseline SHA, timestamp ISO-8601, task-id, ссылки на §7/§9/§4, явная пометка «решения архитектора Р4=B, Р5=умеренная». INDEX: запись <next>. Russian-first, без placeholders, append-only.

## Проверки
git diff --name-only      # только whitelist + журнал
git diff --check
git grep -n "NEW_PROJECT_BOOTSTRAP_PROMPT\|PROJECT_CHAT_START_PROMPT_TEMPLATE" -- docs   # ссылок на старые пути не осталось (или ведут на заглушку)
Вручную: header-канон Р4 содержит общий контент, оба task-шаблона ссылаются; new-project prompt канон содержит контент обоих prompt; CHECKLIST не тронут; broken refs нет.

## Commit / push / PR (контур gh)
commit: docs(agent-system): templates fork part — task header canon + new-project prompt (C5B)
git push -u origin work/docs-maintainer-01/templates-fork
gh доступен → gh pr create base=developer; иначе → URL pull/new пользователю. push требует credentials → STOP.

## Definition of Done
- Р4: общий header в каноне, оба шаблона ссылаются, тела раздельные; Р5: два prompt сведены в канон, CHECKLIST отдельно; уникальный контент не потерян; broken refs нет;
- изменены только подтверждённый whitelist + журнал; diff --check чист;
- TASK/RESULT/INDEX записаны (sequence, timestamp, baseline SHA), без placeholders; решения архитектора зафиксированы;
- ветка запушена; PR создан или переданы URL/команды; RESULT содержит commit SHA и PR URL;
- Russian-first.

## STOP-условия
бездомный контент → STOP; правка вне whitelist (вкл. CHECKLIST); RESULT-0004 недоступен; неизбежны broken refs; push требует credentials; секрет найден (не печатать).
