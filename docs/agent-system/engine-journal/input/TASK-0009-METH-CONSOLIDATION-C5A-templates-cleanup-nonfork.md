# TASK-0009-METH-CONSOLIDATION-C5A-templates-cleanup-nonfork

Дословная копия входной задачи METH-CONSOLIDATION-C5A.

---

# Задача для docs-maintainer-01: METH-CONSOLIDATION-C5A (templates cleanup — не-fork часть + вынос развилок)

## Режим
engine: docs-capable (рекомендуемый запуск — Claude Code). Local only. Reasoning: Medium. Agent, строгий allowed-files whitelist.

## Цель
Выполнить НЕ-fork часть PR-C5 (templates cleanup) и вынести fork-часть (Р4, Р5) на решение архитектора, НЕ исполняя её. Контент не терять.

## Repository / каталог
MaximKolomeets/agent-system-development
C:\neural\repos\agent-system-development

## Ветки
- base: developer
- work: work/docs-maintainer-01/templates-cleanup-nonfork

## Авторитетный scope (прочитать первым)
RESULT-0004: §7 (инвентаризация templates: keep/merge/wire), §10 (whitelist C5), §4 (content-preservation), §9 (Р4/Р5 — ТОЛЬКО процитировать варианты, не исполнять).

## Исполнить (не-fork операции)
- merge orphan REVIEW_TEMPLATE → CODE_REVIEW_REPORT_TEMPLATE (уникальный контент перенести, затем развязка по правилу ниже);
- любые прочие НЕ-fork merge дублей templates из §7;
- wire orphan-ов AGENT_REPORT_TEMPLATE и DECISION_TEMPLATE — добавить ссылки на них из docs, указанных в §7/§10, чтобы они перестали быть orphan;
- развязка удаляемого файла: удалить только при 0 inbound-ссылок (проверить grep'ом); если хоть одна ссылка вне whitelist/в append-only истории — оставить redirect-заглушку (как в C3). Broken refs недопустимы.

## НЕ исполнять (fork-часть → вынести)
- Р4: DEVELOPMENT_TASK_TEMPLATE + AGENT_RESEARCH_TASK_TEMPLATE → 1;
- Р5: NEW_PROJECT_BOOTSTRAP_PROMPT консолидация;
- любой иной §7-пункт, помеченный как Р-развилка.
Эти файлы НЕ трогать. В RESULT добавить раздел «Развилки к решению архитектора» и процитировать Р4, Р5 (и прочие C5-развилки) дословно с вариантами из §9.

## Allowed files
- templates и docs, перечисленные для НЕ-fork операций C5 в §7/§10 — подтвердить из плана и зафиксировать в RESULT перед правками; fork-шаблоны (DEVELOPMENT_TASK_TEMPLATE, AGENT_RESEARCH_TASK_TEMPLATE, NEW_PROJECT_BOOTSTRAP_PROMPT) в whitelist НЕ включать;
- + журнал: input/TASK-<next>, output/RESULT-<next>, INDEX.md (next по INDEX, ожидаемо 0009).

## Content-preservation / Fork-guard
- merge переносит уникальный контент ДО удаления/заглушки; бездомный контент → STOP, вернуть как развилку;
- если НЕ-fork пункт оказался fork-зависимым → не исполнять, вынести в раздел развилок.

## Forbidden
- файлы вне подтверждённого whitelist; правка fork-шаблонов; .env; main/developer напрямую; Docker; ввод credentials; редактирование RESULT прошлых задач; broken refs; перезапись append-only истории.

## Preflight (после merge C3 + closure 0008)
cd C:\neural\repos\agent-system-development
git status --short --untracked-files=all
git fetch --all --prune
git switch developer && git pull --ff-only origin developer
git rev-parse developer && git rev-parse origin/developer
git switch -c work/docs-maintainer-01/templates-cleanup-nonfork

## Journal (обязательно)
TASK-<next>: дословная копия. RESULT-<next>: какие templates merged/wired, карта переноса контента, исходы развязок (delete/stub), обновлённые ссылки, подтверждённый whitelist, baseline SHA, timestamp ISO-8601, task-id, ссылки на §7/§10/§4, + раздел «Развилки к решению архитектора» (Р4, Р5 дословно с вариантами). INDEX: запись <next>. Russian-first, без placeholders, append-only.

## Проверки
git diff --name-only      # только whitelist + журнал
git diff --check
git grep -n "REVIEW_TEMPLATE" -- docs   # ссылок на удалённый orphan не осталось (или ведут на заглушку)
Вручную: AGENT_REPORT_TEMPLATE/DECISION_TEMPLATE теперь имеют входящие ссылки; broken refs нет; fork-шаблоны не тронуты.

## Commit / push / PR (контур gh)
commit: docs(agent-system): templates cleanup non-fork part (C5A)
git push -u origin work/docs-maintainer-01/templates-cleanup-nonfork
gh доступен → gh pr create base=developer; иначе → URL pull/new пользователю. push требует credentials → STOP.

## Definition of Done
- не-fork templates merged/wired; уникальный контент не потерян; broken refs нет;
- fork-шаблоны не тронуты; Р4/Р5 процитированы в RESULT с вариантами;
- изменены только подтверждённый whitelist + журнал; diff --check чист;
- TASK/RESULT/INDEX записаны (sequence, timestamp, baseline SHA), без placeholders;
- ветка запушена; PR создан или переданы URL/команды; RESULT содержит commit SHA и PR URL;
- Russian-first.

## STOP-условия
бездомный контент или НЕ-fork пункт оказался fork-зависимым → вынести в развилки; правка вне whitelist; RESULT-0004 недоступен; неизбежны broken refs; push требует credentials; секрет найден (не печатать).
