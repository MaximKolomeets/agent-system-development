# TASK-0004-METH-CONSOLIDATION-PLAN-01-consolidation-plan

Дословная копия входной задачи METH-CONSOLIDATION-PLAN-01 (plan-only по содержимому, журналируется).

---

# Задача для qa-reviewer-01: METH-CONSOLIDATION-PLAN-01 (plan-only по содержимому, но журналируется)

## Рекомендуемый режим engine
Запуск: Local only. Рекомендуемый engine: Claude Code (или иной docs-capable engine).
Модель: старшая reasoning-модель — нужен широкий охват.
Reasoning: High
Режим: Agent со строгим allowed-files whitelist (писать можно ТОЛЬКО в журнал; содержимое методологии не менять).
Почему: план консолидации требует полного охвата и сохранности контента; результат обязателен к журналированию для воспроизводимости.

## Цель
Подготовить точный план консолидации методологии (finding 5) и записать его в журнал + вернуть в чат. Содержимое методологии (docs/templates вне журнала) НЕ менять, ничего не удалять и не сливать.

## Контекст
~40 docs + ~28 templates, reading-list ~47, дублирование adoption-слоя и methodology_reference. task-id: METH-CONSOLIDATION-PLAN-01.

## Repository
MaximKolomeets/agent-system-development

## Локальный каталог
C:\neural\repos\agent-system-development

## Ветки
- base: developer
- work: work/qa-reviewer-01/consolidation-plan

## Allowed files (запись ТОЛЬКО в журнал)
docs/agent-system/engine-journal/input/TASK-<next>-METH-CONSOLIDATION-PLAN-01-*.md
docs/agent-system/engine-journal/output/RESULT-<next>-METH-CONSOLIDATION-PLAN-01-*.md
docs/agent-system/engine-journal/INDEX.md
<next> — следующий порядковый номер по INDEX (ожидаемо 0004), не переиспользовать.

## Read-only context (читать, НЕ менять)
Весь docs/agent-system/** и templates/**, AGENTS.md, README.md (анализ), и всё прочее содержимое методологии.

## Forbidden
- любая правка/удаление/слияние файлов методологии вне журнала;
- редактирование RESULT прошлых задач;
- .env; main/developer напрямую; Docker; установка зависимостей;
- ввод credentials.

## Preflight
cd C:\neural\repos\agent-system-development
git remote -v
git status --short --untracked-files=all
git fetch --all --prune
git switch developer
git pull --ff-only origin developer
git rev-parse developer && git rev-parse origin/developer
Зафиксировать baseline SHA для воспроизводимости. Если METH-CONSISTENCY-01 ещё не в developer — отметить в RESULT.
Затем: git switch -c work/qa-reviewer-01/consolidation-plan

## Предлагаемая целевая структура (проверить и скорректировать, не вслепую)
1. Reading-list → два уровня: Core mandatory (~8–10: AGENTS, README, ROLE_MODEL, WORKFLOW, BRANCH_POLICY, CODE_REVIEW_WORKFLOW, ENGINE_ENTRYPOINT, CURRENT_STATE, NEXT_STEPS) + Reference (по необходимости).
2. ADOPTION_GUIDE.md — единый канон adoption; вбирает уникальное из TARGET_REPOSITORY_ADOPTION_GUIDE.md, NEW_PROJECT_ONBOARDING_GUIDE.md, DOWNSTREAM_ADAPTATION_CHECKLIST.md.
3. SHORT_TARGET_ADOPTION_PROMPT.md + TARGET_REPOSITORY_ADOPTION_CHAT_PROMPT.md → один templates/ADOPTION_PROMPT.md (короткий + полный внутри).
4. methodology_reference — один канон (ENGINE_SELF_DISCOVERY_CONTRACT.md или ENGINE_ENTRYPOINT.md), остальные ссылаются.
5. ~28 templates — инвентаризация по использованию, слияние дублей.

## Содержание RESULT (он же отчёт в чат) — все разделы, без placeholders
1. Снимок: число docs/templates; размер reading-list; baseline SHA; в developer ли METH-CONSISTENCY-01.
2. Инвентаризация adoption-слоя: по каждому файлу — назначение, уникальный vs пересекающийся контент.
3. Проверка предложенной структуры (п.1–5): по каждому confirm/adjust с обоснованием.
4. Карта content-preservation: для каждого кандидата на delete/merge — его уникальный контент и целевое место; «бездомный» контент — отдельно как развилка.
5. Reading-list: точный Core (~10) и Reference; обоснование границы.
6. methodology_reference: где дублируется (файлы:строки), канон, что заменить ссылками.
7. Templates: инвентаризация по использованию, дубли, merge/delete/keep.
8. Перекрёстные ссылки и манифест: что обновить в README, source index, ADOPTION_TRANSFER_MANIFEST.yml, чтобы не было broken refs и рассинхрона transfer-манифеста.
9. Риски и развилки для архитектора.
10. Предлагаемая разбивка на execution (один или несколько PR): для каждого — scope, allowed files, ожидаемые delete/merge.
11. Включить в план execution-прохода фикс дефолта «review-only = chat-only» → «review журналирует TASK+RESULT всегда».

## Journal (обязательно — core-условие воспроизводимости)
- TASK-<next>: дословная копия этой задачи.
- RESULT-<next>: полный отчёт (разделы 1–11) + baseline SHA + timestamp ISO-8601 + task-id.
- INDEX: добавить запись <next> в хронологическом порядке.
Russian-first, без placeholders, append-only, номера прошлых задач не трогать.

## Commit / push / PR (journal-only, с контуром gh)
1) Один commit: docs(journal): consolidation plan METH-CONSOLIDATION-PLAN-01 (<next>)
2) git push -u origin work/qa-reviewer-01/consolidation-plan
   - если push требует ввода credentials → STOP, не вводить, отдать команды пользователю.
3) PR base=developer:
   - gh доступен → gh pr create;
   - gh недоступен → вернуть пользователю URL pull/new и пометить в RESULT «PR создаёт пользователь». Не ошибка, не зацикливаться.

## Definition of Done
- TASK/RESULT/INDEX записаны (sequence <next>, timestamp, baseline SHA), без placeholders;
- содержимое методологии вне журнала НЕ изменено (git status показывает изменения только в engine-journal);
- для каждого предложенного delete/merge есть целевое место контента либо пометка «бездомный → развилка»;
- раздел 10 даёт основу для execution; раздел 11 присутствует;
- ветка запушена; PR создан (gh) или переданы команды/URL (нет gh);
- отчёт продублирован в чат; Russian-first.

## STOP-условия
- правка потребовала бы изменения файла методологии вне журнала → STOP;
- неоднозначность сверх описанной → зафиксировать как развилку, продолжить;
- push требует credentials → STOP, передать пользователю;
- найден секрет → не печатать.

## Формат финального сообщения engine
Russian. Резюме: сколько файлов к delete/merge/keep, насколько падает обязательный reading-list; sequence номер; commit SHA; PR URL или «PR создаёт пользователь»; подтверждение, что вне журнала ничего не менялось.
