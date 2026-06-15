# TASK-0008-METH-CONSOLIDATION-C3-adoption-prompt-merge

Дословная копия входной задачи METH-CONSOLIDATION-C3.

---

# Задача для docs-maintainer-01: METH-CONSOLIDATION-C3 (adoption prompt merge)

## Режим
engine: docs-capable (рекомендуемый запуск — Claude Code). Local only. Reasoning: Medium. Agent, строгий allowed-files whitelist.

## Цель
Реализовать PR-C3 из плана: свести два adoption-prompt (SHORT_TARGET_ADOPTION_PROMPT + TARGET_REPOSITORY_ADOPTION_CHAT_PROMPT) в один канон templates/ADOPTION_PROMPT.md (короткий + полный вариант внутри). Контент не терять. Развязку старых файлов делать по правилу ниже.

## Repository / каталог
MaximKolomeets/agent-system-development
C:\neural\repos\agent-system-development

## Ветки
- base: developer
- work: work/docs-maintainer-01/adoption-prompt-merge

## Авторитетный scope (прочитать первым)
RESULT-0004 §10 (PR-C3 whitelist), §3 (merge двух prompt в один), §8 (inbound-ссылки/манифест к обновлению), §4 (content-preservation). Исполнять как там определено; имя канона templates/ADOPTION_PROMPT.md, если §3 не указывает иное.

## Allowed files
- templates/ADOPTION_PROMPT.md (новый канон);
- два старых prompt-файла (развязка по правилу);
- файлы с inbound-ссылками по §8 (README, source-index, manifest и пр. — подтвердить из плана);
- + журнал: input/TASK-<next>, output/RESULT-<next>, INDEX.md (next по INDEX, ожидаемо 0008).
Whitelist подтвердить из плана и зафиксировать в RESULT перед правками.

## Правило развязки старых файлов (решение архитектора, перекрывает stub-дефолт плана)
1. Перенести оба варианта (short + full) в канон, объединив уникальный контент.
2. Переписать ВСЕ inbound-ссылки (по §8) на канон.
3. Проверить grep'ом, что ссылок на старые пути не осталось.
4. Если ссылок на старый файл 0 → удалить старый файл.
5. Если хоть одну ссылку нельзя чисто перенаправить → НЕ удалять, оставить redirect-заглушку на канон и отметить в RESULT какие ссылки помешали.
Broken refs недопустимы ни при каком исходе.

## Content-preservation / Fork-guard
- Канон вбирает весь уникальный контент обоих prompt ДО удаления/заглушки; бездомный контент → STOP, вернуть как развилку.
- Если §3/§8 оставляют иную нерешённую развилку (Р1–Р5 или прочее) → STOP, вернуть с вариантами.

## Forbidden
- файлы вне подтверждённого whitelist; .env; main/developer напрямую; Docker; ввод credentials; редактирование RESULT прошлых задач; broken refs.

## Preflight (после merge C2 + closure 0007)
cd C:\neural\repos\agent-system-development
git status --short --untracked-files=all
git fetch --all --prune
git switch developer && git pull --ff-only origin developer
git rev-parse developer && git rev-parse origin/developer
git switch -c work/docs-maintainer-01/adoption-prompt-merge

## Journal (обязательно)
TASK-<next>: дословная копия. RESULT-<next>: канон, карта переноса контента, исход развязки (delete или stub + почему), обновлённые ссылки/манифест, подтверждённый whitelist, baseline SHA, timestamp ISO-8601, task-id, ссылки на §3/§8/§4, явная пометка «перекрыт stub-дефолт плана». INDEX: запись <next>. Russian-first, без placeholders, append-only.

## Проверки
git diff --name-only      # только whitelist + журнал
git diff --check
git grep -n "SHORT_TARGET_ADOPTION_PROMPT\|TARGET_REPOSITORY_ADOPTION_CHAT_PROMPT" -- docs   # ссылок на старые пути не осталось (или ведут на заглушку)
Вручную: канон содержит short+full; broken refs нет; manifest синхронизирован.

## Commit / push / PR (контур gh)
commit: docs(agent-system): merge adoption prompts into single canon (C3)
git push -u origin work/docs-maintainer-01/adoption-prompt-merge
gh доступен → gh pr create base=developer; иначе → URL pull/new пользователю. push требует credentials → STOP.

## Definition of Done
- канон templates/ADOPTION_PROMPT.md содержит оба варианта; уникальный контент не потерян;
- старые файлы удалены (если ссылки вычищены) либо оставлены заглушками (если нет) — broken refs нет;
- inbound-ссылки/манифест обновлены по §8;
- изменены только подтверждённый whitelist + журнал; diff --check чист;
- TASK/RESULT/INDEX записаны (sequence, timestamp, baseline SHA), без placeholders;
- ветка запушена; PR создан или переданы URL/команды; RESULT содержит commit SHA, PR URL и исход развязки;
- Russian-first.
ЛИБО fork-guard/бездомный контент → ничего сверх журнала, развилка возвращена.

## STOP-условия
бездомный контент или нерешённая развилка → STOP с вариантами; правка вне whitelist; RESULT-0004 недоступен; неизбежны broken refs; push требует credentials; секрет найден (не печатать).
