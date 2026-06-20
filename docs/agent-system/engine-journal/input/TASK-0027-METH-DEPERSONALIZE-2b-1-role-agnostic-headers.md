# TASK-0027-METH-DEPERSONALIZE-2b-1

## Метаданные

- Задача: `METH-DEPERSONALIZE-2b-1` (phase-2b-1: role-agnostic шапки, finding A).
- Роль: docs-maintainer.
- Исполнитель: на усмотрение архитектора.
- Reasoning effort: средний.
- Запуск: Local only.
- Base branch: `developer`.
- Work branch: `work/docs-maintainer-01/depersonalize-2b-1`.
- Baseline SHA (`origin/developer`): `983da98a2d435ba91b652b0205f3d0f6f0867a0f`.
- Timestamp (ISO-8601): `2026-06-20T22:01:32+07:00`.

## Дословный текст задачи

# Задача для docs-maintainer-01: METH-DEPERSONALIZE-2b-1 (role-agnostic шапки, finding A)
## Режим
Роль: docs-maintainer. Исполнитель: на усмотрение архитектора.
Reasoning effort: средний — механическая замена, но ~13 файлов, важна консистентность с каноном.
Запуск: Local only. branch-guard.
## Цель
Заменить не-role-agnostic шапки режима на role-agnostic форму по канону TASK_HEADER_COMMON. ТОЛЬКО finding A (actor-текст C — не в этом PR).
## Repo / каталог
MaximKolomeets/agent-system-development / C:\neural\repos\agent-system-development
## Ветки
base developer; work work/docs-maintainer-01/depersonalize-2b-1
(пустую ветку depersonalize-docs-b удалить — она своя, без коммитов: git branch -D + git push origin --delete, чтобы не плодить.)
## Preflight
git fetch --all --prune; git switch developer && git pull --ff-only origin developer
git switch -c work/docs-maintainer-01/depersonalize-2b-1
git rev-parse --abbrev-ref HEAD     # == work-ветка, иначе STOP
подтвердить seq=0027 из INDEX (не предсказывать).
## Allowed files (группа A, ~13)
README.md
docs/agent-system/ENGINE_ENTRYPOINT.md
docs/agent-system/ENGINE_SELF_DISCOVERY_CONTRACT.md
docs/agent-system/NEW_PROJECT_ONBOARDING_GUIDE.md
docs/agent-system/TARGET_PROJECT_GOVERNANCE_PACK.md
docs/agent-system/ADOPTION_GUIDE.md
docs/agent-system/templates/ADOPTION_AUDIT_TASK_TEMPLATE.md
docs/agent-system/templates/ADOPTION_PROMPT.md
docs/agent-system/templates/DOCS_ONLY_ADOPTION_TASK_TEMPLATE.md
docs/agent-system/templates/ENGINE_REGISTRY_TEMPLATE.md
docs/agent-system/templates/ORCHESTRATOR_RESPONSE_TEMPLATE.md
docs/agent-system/templates/TARGET_PROJECT_GOVERNANCE_PACK_TEMPLATE.md
docs/agent-system/templates/TARGET_REPOSITORY_BOOTSTRAP_TASK_TEMPLATE.md
+ журнал: input/TASK-0027, output/RESULT-0027, INDEX.md
## Изменения
- Блок «Рекомендуемый режим <engine-name>» + «Модель: …» → «Роль: <функция> / Исполнитель: на усмотрение архитектора / Reasoning effort: низкий|средний|высокий» по канону TASK_HEADER_COMMON (канон + ссылка, без дублирования прозой).
- ТОЛЬКО заголовочные блоки режима. Actor-упоминания (C) в этом PR НЕ трогать — они в 2b-2/2b-3.
## Проверки
rg "Рекомендуемый режим <engine-name>|^Модель:" в whitelisted → 0;
diff только whitelist; git diff --check; branch-guard перед commit.
## Journal
TASK-0027/RESULT-0027/INDEX (seq из INDEX). RESULT — какие файлы/что заменено, baseline SHA, timestamp ISO-8601.
## Commit / PR
commit: docs(agent-system): role-agnostic task headers (finding A, phase-2b-1)
push; PR в developer.
## Передача
- что сделано + № PR + head SHA;
- «Следующий: reviewer — review PR (шапки role-agnostic; actor-текст C не трогался)»;
- «Обновить Source у зарегистрированных потребителей»;
- остаток: 2b-2 (adapter, generic-пометка), 2b-3 (active-rule), 2b-4 (history консервативно + manifest D).
## DoD / STOP
DoD: 0 старых шапок в whitelisted; role-agnostic по канону; только whitelist+журнал; branch-guard.
STOP: HEAD не work-ветка; правка вне whitelist; соблазн трогать actor-текст C (нельзя в этом PR).
