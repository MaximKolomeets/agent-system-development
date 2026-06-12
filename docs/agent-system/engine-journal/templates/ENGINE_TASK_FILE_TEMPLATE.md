# ENGINE_TASK_FILE_TEMPLATE

Файл задачи:

Идентификатор задачи:

Номер sequence:

Создано:

Автор:

Target repository:

Methodology repository:

Агент:

Engine:

Режим источника задачи: `<copy-paste | task-file-handoff>`

Task source commit SHA:

Task file blob SHA:

Ссылка на bootstrap prompt:

Примечание об источнике правды:

Base branch:

Working branch:

Правило языка:

Все ответы, target-local docs, TASK/RESULT/INDEX и комментарии в файлах писать на русском языке. English допускается только для technical identifiers, command names, flags, paths, filenames, branch names, config keys, API names, package names, vendor/tool names и literal external names.

Разрешенные файлы:

- `<allowed path>`

Запрещенные файлы:

- `.env`
- `.venv/`
- `data/`
- `runtime/`
- `dist/`
- `backups/`
- `exports/`
- credentials
- tokens
- private keys
- real passwords
- private repository URLs
- private downstream project names
- client/customer data
- production/runtime data

Цель:

Контекст:

Preflight:

BEGIN POWERSHELL
# Вставить команды preflight для engine.
END POWERSHELL

STOP-условия:

- working tree dirty before changes;
- pull fast-forward impossible;
- forbidden files detected;
- private data or secrets required;
- scope expands beyond allowed files;
- target instructions conflict with Russian-first policy and user did not explicitly allow another language.

Проверки:

BEGIN POWERSHELL
# Вставить команды проверки результата.
END POWERSHELL

Commit policy:

PR policy:

Post-merge journal closure policy:

- после merge рабочего PR зафиксировать PR status `merged`, merge commit SHA и `merged_at`, если доступно;
- если выполнялся release PR в `main`, зафиксировать release PR URL/status/merge commit SHA;
- если выполнялся sync PR `main -> developer`, зафиксировать sync PR URL/status/merge commit SHA;
- после merge `RESULT closed after merge: yes`, `INDEX closed after merge: yes` и `No journal placeholders: yes`;
- не оставлять после merge final states `PR open`, `ready for review`, `draft open`, `pending at file materialization` или `see Engine final report`.

Ожидаемый RESULT file:

Требования к final report:

- branch;
- commit SHA;
- PR URL;
- changed files;
- checks run;
- checks not run and why;
- forbidden files result;
- sensitive/private marker result;
- language policy result;
- risks;
- result file finalized;
- index entry finalized;
- no journal placeholders;
- статус PR после review (`PR status after review`);
- merge commit SHA после merge, если доступен;
- release PR URL/status/merge commit SHA, если release выполнялся;
- sync PR URL/status/merge commit SHA, если sync выполнялся;
- RESULT закрыт после merge;
- INDEX закрыт после merge;
- проверка Post-merge Journal Closure;
- follow-up commit SHA if finalization required;
- next recommended step.
