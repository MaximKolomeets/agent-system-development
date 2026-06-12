# TARGET_REPOSITORY_ADOPTION_CHAT_PROMPT

## Назначение

Этот prompt пользователь копирует из methodology repository и вставляет в новый чат, открытый в контексте target repository.

Prompt не запускает полный перенос шаблона. Он просит ChatGPT подготовить первую безопасную задачу для engine в режиме audit-only.

## Copy/paste prompt

```text
Продолжаем внедрение агентской методологии в этот проект.

Целевой репозиторий:

<ВСТАВИТЬ_URL_TARGET_REPOSITORY>

Шаблонный methodology repository:

https://github.com/MaximKolomeets/agent-system-development

Твоя задача в этом чате:

1. Изучи target repository.
2. Изучи актуальный `agent-system-development` как reusable methodology/template repository.
3. Не вноси изменения в файлы сам.
4. Сначала подготовь задачу для engine.
5. Задача должна быть на русском языке и начинаться с обязательной шапки:
6. Все ответы, target-local docs, TASK/RESULT/INDEX и комментарии в файлах должны быть на русском языке. Английский допустим только для команд, путей, branch names, filenames, config keys, API names, package names, vendor/tool names и code identifiers.
7. Если target instructions конфликтуют с Russian-first policy, включи в Engine-задачу STOP-условие и требование запросить решение пользователя.

Задача для <agent-name>: <task-id>

Рекомендуемый режим <engine-name>:

Запуск: <Local only | Cloud allowed | Hybrid>
Модель: <model recommendation>
Reasoning: <Low | Medium | High>
Режим: <Agent | Ask | Manual review>
Почему: <краткое обоснование выбора режима>

Перед формированием задачи:

1. Обратись к актуальному `agent-system-development`.
2. Проверь, что используется текущая версия methodology repository.
3. Если GitHub, connector или локальная синхронизация недоступны, явно напиши это пользователю.
4. Включи в задачу engine preflight для проверки и синхронизации methodology repository.

Формат ответа ChatGPT:

1. Все данные для engine выведи в одном самодостаточном блоке `Блок для Engine — копировать целиком`.
2. Не выноси из Engine-блока команды, allowed files, forbidden files, проверки, STOP-условия и формат отчета.
3. Ручные terminal-шаги выводи отдельно только если они предназначены пользователю, а не engine.
4. Не смешивай engine prompt и manual commands.
5. Если нужна доработка `agent-system-development`, выведи отдельный самодостаточный copy/paste-блок для engine-разработчика methodology repository.

Главная цель:

Применить в target repository обновленную методологию из `agent-system-development`, но безопасно и поэтапно.

Важно:

`agent-system-development` - это reusable methodology/template repository, а не центральный репозиторий управления downstream-проектом.

Все project-specific ветки, отчеты, PR, state docs, governance docs и рабочее состояние должны создаваться только в target repository.

Private data, secrets, `.env`, client data, private repository URL и internal code names нельзя переносить обратно в public methodology repository.

Сначала нужен не полный перенос шаблона, а безопасная первая задача engine в режиме `audit-only`.

Нужно подготовить задачу engine, которая:

1. Проверит target repository.
2. Выполнит repository self-discovery.
3. Прочитает локальные инструкции target repository.
4. Проверит branch model.
5. Проверит наличие или отсутствие `docs/agent-system/`.
6. Проверит наличие root governance docs:
   - `README.md`
   - `AGENTS.md`
   - `PROJECT_CONSTITUTION.md`
   - `PROJECT_DASHBOARD.md`
   - `ROADMAP.md`
   - `RUNBOOK.md`
   - `DECISIONS.md`
7. Проверит готовность к governance pack:
   - `CURRENT_STATE.md`
   - `NEXT_STEPS.md`
   - `BACKLOG.md`
   - `DECISION_LOG.md`
   - `PROJECT_GUARDRAILS.md`
   - `ENGINE_REGISTRY.md`
8. Проверит готовность к Project Constitution Framework:
   - Project Mission
   - Success Criteria
   - Out Of Scope
   - Architectural Principles
   - Current Strategic Goal
   - Agent Authority Matrix
   - Decision Authority Levels
   - Scope Expansion Control
   - Governance Review Checklist
9. Проверит language consistency governance docs target repository.
10. Проверит Russian-first policy в target `AGENTS.md` или эквивалентных target instructions.
11. Проверит, есть ли в target repository скрипты, workflow или templates без достаточных русских комментариев для нужных строк/блоков.
12. После audit порекомендует привести target docs/templates к Russian-first policy.
13. Создаст только audit artifacts:

docs/agent-system/ADOPTION_AUDIT.md
docs/agent-system/engine-journal/

Engine journal scaffold/templates могут быть созданы или обновлены для target repository, но methodology repository operational history нельзя копировать. Первый audit создает target-specific task/result files и target-specific INDEX entry.

Если `docs/agent-system/` еще нет, engine может создать только минимальную папку, файл audit и engine journal artifacts для этой audit-задачи.

Запрещено в первой задаче:

- переносить весь template repository;
- менять runtime-код;
- менять Docker;
- менять CI;
- менять services/workers/orchestrator/API;
- менять architecture docs без отдельного решения;
- читать `.env`;
- коммитить `.env`;
- коммитить `.venv/`, `data/`, `runtime/`, `dist/`, `backups/`, `exports/`;
- менять production data;
- добавлять secrets;
- добавлять private data;
- делать full docs-only adoption без audit.
- удалять или перезаписывать task/result files engine journal без решения пользователя.

Задача engine должна использовать branch model:

1. Проверить наличие `developer`.
2. Если `developer` существует - стартовать от `developer`.
3. Если `developer` отсутствует - стартовать от `main` и явно указать это в отчете.
4. Рабочая ветка должна быть:

work/docs-maintainer-01/<task-id>-adoption-audit

Task id придумай по правилам target repository. Если в проекте нет своей нумерации, предложи нейтральный id вроде:

PR-agent-1a

В задаче engine обязательно указать проверки:

- `git rev-parse --show-toplevel`
- `git remote -v`
- `git branch --show-current`
- `git status --short`
- `git ls-files`
- forbidden tracked paths check
- sensitive grep только filename-only, без вывода matching lines:

git grep -I -l -i -E "token|password|secret|api_key|apikey|credential|пароль|токен" --

Финальный отчет engine должен содержать:

- repository root;
- remote summary;
- current branch;
- выбранная base branch;
- working branch;
- local instructions found;
- existing governance docs;
- missing governance docs;
- existing agent-system docs;
- branch model observation;
- forbidden tracked paths result;
- sensitive grep result без matching lines;
- Project Constitution readiness;
- Governance Pack readiness;
- Engine Registry readiness;
- language consistency result;
- commenting consistency result;
- Russian-first policy result;
- engine journal task/result files;
- recommended docs-only adoption scope;
- stop conditions, если есть;
- Methodology feedback;
- Methodology repository improvement request, если нужна доработка `agent-system-development`;
- next recommended PR.

После анализа target repository выведи мне готовую задачу для engine целиком, чтобы я мог скопировать ее и вставить в окно engine.

В создаваемых или изменяемых скриптах, workflow, config-like files, templates и технических файлах требуй русские комментарии для нужных строк/блоков: что делает строка/блок и зачем он нужен.

Не начинай с полного внедрения. Сначала сформируй только задачу на audit-only adoption.
```

## Как использовать

1. Открыть новый чат в контексте target repository.
2. Скопировать prompt из блока `Copy/paste prompt`.
3. Заменить `<ВСТАВИТЬ_URL_TARGET_REPOSITORY>` на URL target repository.
4. Вставить prompt в чат.
5. Получить задачу для engine.
6. Запустить engine вручную.
