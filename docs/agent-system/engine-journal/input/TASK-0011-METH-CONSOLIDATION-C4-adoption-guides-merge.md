# TASK-0011-METH-CONSOLIDATION-C4-adoption-guides-merge

Дословная копия входной задачи METH-CONSOLIDATION-C4.

---

# Задача для docs-maintainer-01: METH-CONSOLIDATION-C4 (adoption guides merge, Р1+Р2+Р3)

## Рекомендуемый режим engine
Запуск: Local only. Рекомендуемый engine: Claude Code.
Модель: Claude Opus 4.8
Effort (reasoning): High
Режим: Agent, строгий allowed-files whitelist.
Почему: самый широкий по ссылкам шаг (высокий ref-fan-out), слияние с сохранностью контента и без broken refs — нужна максимальная аккуратность.

## Цель
Реализовать PR-C4: слить adoption-guides по решениям архитектора Р1/Р2/Р3, обновить все ссылки и manifest, не потерять контент, без broken refs.

## Repository / каталог
MaximKolomeets/agent-system-development
C:\neural\repos\agent-system-development

## Ветки
- base: developer
- work: work/docs-maintainer-01/adoption-guides-merge

## Авторитетный scope (прочитать первым)
RESULT-0004: §2 (инвентаризация adoption), §4 (карта content-preservation), §8 (перекрёстные ссылки/манифест), §10 PR-C4 (whitelist).

## Решения архитектора (приоритетны)
- Р1: PROJECT_LIFECYCLE → вводная секция «Жизненный цикл (стадии 1–11)» внутри NEW_PROJECT_ONBOARDING_GUIDE.
- Р2: DOWNSTREAM_ADAPTATION_CHECKLIST — отдельный файл, дедуплицировать (прозовые повторы → ссылки, чеклист-пункты сохранить).
- Р3: канон «developer/develop/main-only flow» = ADOPTION_GUIDE; вариант из TARGET_REPOSITORY_ADOPTION_GUIDE свести туда.
Все три явно отметить в RESULT как «решение архитектора».

## Операции
1. ADOPTION_GUIDE ← перенести уникальные existing-repo шаги из TARGET_REPOSITORY_ADOPTION_GUIDE (новый раздел «Пошаговый existing-repo adoption»); feedback sanitization НЕ дублировать — канон остаётся в METHODOLOGY_FEEDBACK_LOOP, дать ссылку; branch-flow канон (Р3) — здесь.
2. NEW_PROJECT_ONBOARDING_GUIDE ← перенести стадийную модель PROJECT_LIFECYCLE как вводную секцию (Р1).
3. DOWNSTREAM_ADAPTATION_CHECKLIST → дедуп: прозовые повторы правил заменить ссылками на канон, чеклист-пункты оставить (Р2).
4. Развязка слитых файлов: перенести контент в каноны ДО развязки; переписать ВСЕ live-ссылки на каноны; TARGET_REPOSITORY_ADOPTION_GUIDE и PROJECT_LIFECYCLE → redirect-заглушки (т.к. на них ссылается append-only история — удалять нельзя). Broken refs недопустимы.
5. Обновить ссылки (§8): README, ADOPTION_TRANSFER_MANIFEST.yml (в categories/requires_target_adaptation убрать слитые пути, оставить каноны), ENGINE_ENTRYPOINT, STAGE_2_COMPLETION_CHECKLIST, RELEASE_READINESS, source index. Историю (agents/*, прошлые записи DECISION_LOG) НЕ переписывать.

## Allowed files (§10)
docs/agent-system/ADOPTION_GUIDE.md
docs/agent-system/TARGET_REPOSITORY_ADOPTION_GUIDE.md
docs/agent-system/NEW_PROJECT_ONBOARDING_GUIDE.md
docs/agent-system/PROJECT_LIFECYCLE.md
docs/agent-system/DOWNSTREAM_ADAPTATION_CHECKLIST.md
README.md
docs/agent-system/ENGINE_ENTRYPOINT.md
docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml
docs/agent-system/STAGE_2_COMPLETION_CHECKLIST.md
docs/agent-system/RELEASE_READINESS.md
docs/agent-system/source/SOURCE_agent_system_index.md
+ журнал: input/TASK-<next>, output/RESULT-<next>, INDEX.md (next по INDEX, ожидаемо 0011)
Whitelist подтвердить из §10 и зафиксировать в RESULT перед правками.

## Content-preservation / Fork-guard
- весь уникальный контент слитых файлов перенести в каноны ДО развязки; бездомный контент → STOP, вернуть как развилку;
- если §4/§8 вскрывают развилку сверх Р1–Р3 → STOP, вынести.

## Forbidden
- файлы вне whitelist; изменение содержимого METHODOLOGY_FEEDBACK_LOOP (только ссылка); политики (LANGUAGE/SECURITY/PUBLICATION/TOKEN) не трогать; переписывание append-only истории; .env; main/developer напрямую; Docker; ввод credentials; редактирование RESULT прошлых задач; broken refs.

## Preflight (после merge C5B + closure 0010)
cd C:\neural\repos\agent-system-development
git status --short --untracked-files=all
git fetch --all --prune
git switch developer && git pull --ff-only origin developer
git rev-parse developer && git rev-parse origin/developer
git switch -c work/docs-maintainer-01/adoption-guides-merge

## Journal (обязательно)
TASK-<next>: дословная копия. RESULT-<next>: что слито в какие каноны (карты переноса Р1/Р3 контента), дедуп Р2, исходы развязок (stub), обновлённые ссылки/манифест, подтверждённый whitelist, baseline SHA, timestamp ISO-8601, task-id, ссылки на §2/§4/§8, пометка «решения архитектора Р1/Р2/Р3». INDEX: запись <next>. Russian-first, без placeholders, append-only.

## Проверки
git diff --name-only      # только whitelist + журнал
git diff --check
git grep -n "TARGET_REPOSITORY_ADOPTION_GUIDE\|PROJECT_LIFECYCLE" -- docs README.md   # live-ссылки ведут на каноны/заглушки, не битые
git grep -n "methodology_reference:" -- docs   # дубль не вернулся (канон C2 сохранён)
Вручную: ADOPTION_GUIDE содержит existing-repo шаги + branch-flow канон; onboarding содержит lifecycle-секцию; checklist дедуплицирован и цел; manifest синхронизирован; broken refs нет.

## Commit / push / PR (контур gh)
commit: docs(agent-system): merge adoption guides (C4 — Р1/Р2/Р3)
git push -u origin work/docs-maintainer-01/adoption-guides-merge
gh доступен → gh pr create base=developer; иначе → URL pull/new пользователю. push требует credentials → STOP.

## Definition of Done
- ADOPTION_GUIDE ← existing-repo шаги + branch-flow канон (Р3); onboarding ← lifecycle-секция (Р1); checklist дедуплицирован, отдельный (Р2);
- слитые файлы → заглушки; уникальный контент не потерян; broken refs нет; manifest синхронизирован;
- изменены только whitelist + журнал; diff --check чист;
- TASK/RESULT/INDEX записаны (sequence, timestamp, baseline SHA), без placeholders; решения архитектора зафиксированы;
- ветка запушена; PR создан или переданы URL/команды; RESULT содержит commit SHA и PR URL;
- Russian-first.

## STOP-условия
бездомный контент или развилка сверх Р1–Р3 → STOP с вариантами; правка вне whitelist; RESULT-0004 недоступен; неизбежны broken refs; push требует credentials; секрет найден (не печатать).
