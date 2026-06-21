# NEW_PROJECT_PROMPT

Канонический prompt для запуска нового проекта через методологию `agent-system-development`. Файл объединяет короткий стартовый prompt проектного чата и полный bootstrap prompt нового проекта. Прежние файлы `PROJECT_CHAT_START_PROMPT_TEMPLATE.md` и `NEW_PROJECT_BOOTSTRAP_PROMPT.md` удалены (METH-BACKLOG-POLISH); этот файл — канон.

Минимальный чеклист запуска нового проекта остаётся отдельным файлом: `docs/agent-system/templates/NEW_PROJECT_CHECKLIST.md`.

## Когда какой вариант использовать

- **Короткий стартовый prompt проектного чата** — задать оркестратору базовые правила работы в проектном чате (Operational Fast Lane, engine-journal, Task File Handoff, Closure policy, Russian-first) для конкретной цели в target repository.
- **Полный bootstrap prompt нового проекта** — провести запуск нового проекта от идеи до handoff: project profile, структура repository, ветки, governance pack, роли, первые PR, задачи engine.

## Короткий стартовый prompt проектного чата

```text
Используй актуальную методологию из:
https://github.com/MaximKolomeets/agent-system-development

Работай по Operational Fast Lane для проверок/cleanup.
GitHub состояние проверяй сам.
Задачи для исполнителя (engine) оформляй через self-contained block и engine-journal.
Для больших задач используй Task File Handoff Mode: прочитай существующий GitHub TASK file или создай task-file-only GitHub branch/commit только при явном разрешении пользователя; затем передай исполнителю (engine) только короткий bootstrap prompt.
Исполнитель (engine) должен финализировать journal RESULT/INDEX после PR creation; ready-for-review PRs не должны содержать journal placeholders.
После merge/release/sync проверяй Closure policy по `docs/agent-system/ENGINE_JOURNAL_CONTRACT.md`: для обычных work PR допустимо `merged; closure pending` до batch-closure перед release; per-task closure обязателен для release/state docs, audit/review consistency gate, adoption/source-update, завершения/паузы серии или явного closure-задания.
Если пользователь пишет `готово` после merge/release/sync, проверь target journal entries и создай docs-only cleanup task только если сработало per-task исключение или release gate.
Все ответы, target-local docs, TASK/RESULT/INDEX и комментарии в файлах пиши на русском языке. Английский допустим только для команд, путей, branch names, filenames, config keys, API names, package names, vendor/tool names и code identifiers.
Если target instructions конфликтуют с Russian-first policy, остановись и запроси решение пользователя, кроме случая явного разрешения на другой язык.
Не читать `.env`.
Не менять `main`/`developer` напрямую.

Target repository:
<target repository URL>

Local target path:
<local path>

Цель:
<что нужно сделать>

Сначала проверь актуальность methodology repository, затем выдай один self-contained блок для исполнителя (engine) или один Operational Fast Lane block, если задача является только проверкой/cleanup.
```

## Полный bootstrap prompt нового проекта

Использовать этот prompt в новом чате, когда пользователь начинает новый проект.

```text
Мы начинаем новый проект через методологию agent-system-development.

Сначала прими мое описание проекта и не начинай реализацию, пока не сформируешь нейтральный project profile.

Нужно помочь:

1. Сформулировать project profile:
   - project name;
   - public/private status;
   - goal;
   - non-goals;
   - repository name;
   - expected branches;
   - roles;
   - engines;
   - security constraints;
   - forbidden data;
   - first milestone;
   - first PR;
   - documentation structure;
   - acceptance criteria.

2. Предложить структуру repository:
   - README.md;
   - AGENTS.md;
   - PROJECT_DASHBOARD.md;
   - ROADMAP.md;
   - RUNBOOK.md;
   - docs/agent-system/CURRENT_STATE.md;
   - docs/agent-system/NEXT_STEPS.md;
   - docs/agent-system/BACKLOG.md;
   - docs/agent-system/DECISION_LOG.md;
   - docs/agent-system/PROJECT_GUARDRAILS.md;
   - docs/agent-system/ENGINE_REGISTRY.md;
   - .gitignore;
   - docs/agent-system/;
   - docs/agent-system/templates/;
   - docs/agent-system/agents/;
   - .github/workflows/, если нужен CI.

3. Предложить ветки:
   - main;
   - developer;
   - work/<role>/*.

4. Предложить локальную worktree-схему для ролей.

5. Предложить governance pack до первых implementation PR:
   - dashboard;
   - roadmap;
   - backlog;
   - current state;
   - next steps;
   - decision log;
   - project guardrails;
   - engine registry;
   - handoff rule.

6. Предложить роли без vendor/tool names.

7. Предложить первые PR:
   - bootstrap PR;
   - documentation PR;
   - first implementation PR;
   - guardrail/CI PR, если нужен.

8. Сформировать задачи для engine-исполнителей:
   - каждая задача формулируется на русском языке;
   - каждая задача начинается с шапки `Задача для <agent-name>: <task-id>`;
   - task id связан с GitHub issue, PR, task id или внутренним номером работы проекта;
   - шапка содержит запуск, модель, reasoning, режим работы и причину выбора режима;
   - каждая задача должна иметь scope;
   - expected files;
   - forbidden files;
   - checks;
   - final report format;
   - Russian-first policy для final report, TASK/RESULT/INDEX, target-local docs/templates и комментариев в файлах.

9. Подготовить handoff для следующего чата:
   - repository;
   - visibility;
   - current branches;
   - active PR;
   - completed PRs;
   - important docs;
   - current goal;
   - next PR;
   - risks;
   - exact continuation prompt.

Правила:
- отвечать на русском;
- все target-local docs, TASK/RESULT/INDEX и комментарии в файлах писать на русском языке; English допустим только для command names, flags, paths, filenames, branch names, config keys, API names, package names, vendor/tool names и code identifiers;
- не использовать реальные credentials, passwords, tokens или API keys;
- не читать и не создавать .env;
- не добавлять клиентские, персональные, корпоративные или рабочие данные в public repository;
- не упоминать конкретные внешние проекты, приватные репозитории или внутренние кодовые имена;
- использовать только нейтральные термины: target implementation repository, private downstream repository, private implementation repository, example project;
- конкретный инструмент-исполнитель описывать как engine;
- одна задача = одна ветка = один PR;
- пользователь принимает финальные решения.

Мое описание проекта:

<вставить описание проекта>
```
