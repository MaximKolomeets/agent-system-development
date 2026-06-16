# TASK-0013-METH-BACKLOG-POLISH-stub-cleanup-journaling

Дословная копия входной задачи METH-BACKLOG-POLISH.

---

# Задача для docs-maintainer-01: METH-BACKLOG-POLISH (части A + B)

## Рекомендуемый режим engine
Запуск: Local only. Рекомендуемый engine: Claude Code.
Модель: Claude Sonnet 4.6
Effort (reasoning): Medium
Режим: Agent, строгий allowed-files whitelist.

## Цель
A (пункт 3): чистка накопленных redirect-заглушек + синхрон манифеста.
B (пункт 4, ex-C6.1): согласовать journaling-контракт и fast-lane с новым review-default.

## Repository / каталог
MaximKolomeets/agent-system-development
C:\neural\repos\agent-system-development

## Ветки
- base: developer
- work: work/docs-maintainer-01/backlog-polish

## ЧАСТЬ A — заглушки
1. Для КАЖДОЙ из накопленных redirect-заглушек (REVIEW_TEMPLATE, SHORT_TARGET_ADOPTION_PROMPT, TARGET_REPOSITORY_ADOPTION_CHAT_PROMPT, NEW_PROJECT_BOOTSTRAP_PROMPT, PROJECT_CHAT_START_PROMPT_TEMPLATE, TARGET_REPOSITORY_ADOPTION_GUIDE, PROJECT_LIFECYCLE) собрать актуальную inbound-карту (`git grep`).
2. Правило удаления (политика, одобрена архитектором): broken-ссылки в append-only истории ОТНЫНЕ допустимы (план §8.6). Поэтому:
   - если у заглушки остались ТОЛЬКО ссылки из append-only истории (journal/agents/DECISION_LOG прошлые записи) и она НЕ оправдана внешними bookmark → УДАЛИТЬ файл;
   - если есть ЖИВЫЕ ссылки (вне истории) → НЕ удалять (живые broken refs по-прежнему запрещены); сперва перенаправить живую ссылку на канон, затем по возможности удалить;
   - `TARGET_REPOSITORY_ADOPTION_CHAT_PROMPT` — оставить заглушкой ВСЕГДА (внешние чаты ссылаются на путь, §8.7).
3. `ADOPTION_TRANSFER_MANIFEST.yml`: исключить все redirect-заглушки из категорий target-copy (`categories.*`, `requires_target_adaptation`), чтобы downstream-проекты их не наследовали.
4. `DECISION_LOG.md`: добавить запись о политике «broken-ссылки в append-only истории допустимы; history-only заглушки можно удалять» (append, исторические записи не трогать).

## ЧАСТЬ B — journaling-контракт
5. `ENGINE_JOURNAL_CONTRACT.md` (раздел про review): согласовать с C6 — review всегда пишет TASK+RESULT (journal trace = always), `report delivery` — отдельный параметр (chat | repository).
6. `OPERATIONAL_FAST_LANE.md`: явно зафиксировать, что review ≠ fast-lane status-check (review журналируется, fast-lane — нет).

## Allowed files
7 заглушек (на удаление/правку), ADOPTION_TRANSFER_MANIFEST.yml, DECISION_LOG.md, ENGINE_JOURNAL_CONTRACT.md, OPERATIONAL_FAST_LANE.md
+ файлы с живыми inbound-ссылками на заглушки (по §8, подтвердить из grep)
+ журнал: input/TASK-<next>, output/RESULT-<next>, INDEX.md (ожидаемо 0013)
Whitelist подтвердить и зафиксировать в RESULT перед правками.

## Forbidden
- живые (не-history) broken refs;
- перезапись append-only истории (только append в DECISION_LOG);
- удаление TARGET_REPOSITORY_ADOPTION_CHAT_PROMPT заглушки;
- файлы вне whitelist; .env; main/developer напрямую; ввод credentials; редактирование RESULT прошлых задач.

## Preflight
cd C:\neural\repos\agent-system-development
git status --short --untracked-files=all
git fetch --all --prune
git switch developer && git pull --ff-only origin developer
git rev-parse developer && git rev-parse origin/developer
git switch -c work/docs-maintainer-01/backlog-polish

## Journal
TASK-<next>: дословная копия. RESULT-<next>: по части A — карта inbound на каждую заглушку и решение (delete/keep + почему), изменения манифеста, запись DECISION_LOG; по части B — что согласовано; подтверждённый whitelist, baseline SHA, timestamp ISO-8601. INDEX: запись <next>. Russian-first, без placeholders, append-only.

## Проверки
git diff --name-only
git diff --check
git grep -n "<имя каждой удалённой заглушки>" -- docs README.md   # живых ссылок не осталось (только history)
Вручную: манифест без заглушек; CHAT_PROMPT-заглушка цела; контракт/fast-lane согласованы; DECISION_LOG дополнен.

## Commit / push / PR
commit: docs(agent-system): backlog polish — stub cleanup + journaling contract alignment
git push -u origin work/docs-maintainer-01/backlog-polish
gh доступен → gh pr create base=developer; иначе → URL pull/new. push требует credentials → STOP.

## Definition of Done
- history-only заглушки удалены, живые ссылки перенаправлены, CHAT_PROMPT-заглушка цела, живых broken refs нет;
- манифест без заглушек; DECISION_LOG дополнен; контракт+fast-lane согласованы с review-default;
- только whitelist + журнал; diff --check чист; TASK/RESULT/INDEX без placeholders;
- ветка запушена; PR создан/URL передан; RESULT с commit SHA и PR URL; Russian-first.

## STOP
живой broken ref неизбежен → STOP; правка вне whitelist; нужна перезапись истории; push требует credentials; секрет найден (не печатать).
