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

Recommended Engine Mode:

- launch mode / запуск:
- model / модель:
- reasoning:
- execution mode / режим:
- why this mode is required / почему:

Режим источника задачи: `<copy-paste | task-file-handoff>`

Task source commit SHA:

Task file blob SHA:

Ссылка на bootstrap prompt:

Примечание об источнике правды:

Base branch:

Working branch:

Verified Baseline:

- checked repository:
- local path, если применимо:
- checked base branch:
- working branch:
- checked branch state:
- latest relevant PR numbers/statuses, если применимо:
- latest relevant merged PR, если применимо:
- release PR status, если применимо:
- sync PR status, если применимо:
- latest known merge commit SHA, если доступен:
- open PR state, если relevant:
- baseline verification source:
- baseline verification date/time:

Copy/Paste Completeness Check:

- [ ] This TASK/Engine block can be executed without reading surrounding chat text.
- [ ] Recommended Engine Mode is included.
- [ ] Verified baseline is included or explicitly marked as not applicable.
- [ ] Repository/base branch/working branch are included.
- [ ] Allowed files are included.
- [ ] Forbidden files are included.
- [ ] Checks are included.
- [ ] STOP conditions are included.
- [ ] Final report requirements are included.
- [ ] No required execution context exists only in surrounding chat.

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
- если выполнялся release PR в `main`, зафиксировать release PR URL/status/merge commit SHA/`merged_at`;
- если выполнялся sync PR `main -> developer`, зафиксировать sync PR URL/status/merge commit SHA/`merged_at`;
- после merge `RESULT closed after merge: yes`, `INDEX closed after merge: yes` и `No journal placeholders: yes`;
- не оставлять после merge final states `PR open`, `ready for review`, `draft open`, `pending at file materialization` или `see Engine final report`.

Post-merge closure checklist:

- [ ] Проверить GitHub/local state work PR.
- [ ] Проверить release PR, если release использовался.
- [ ] Проверить sync PR, если sync использовался.
- [ ] Проверить, что RESULT/INDEX не остались в pre-merge state.
- [ ] Ограничить allowed files минимально: RESULT, INDEX и безопасные state docs.
- [ ] Не менять runtime, Docker, CI, secrets, private data или downstream-specific details.

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
- `merged_at` date/time, если доступно;
- release PR URL/status/merge commit SHA/`merged_at`, если release выполнялся;
- sync PR URL/status/merge commit SHA/`merged_at`, если sync выполнялся;
- RESULT закрыт после merge;
- INDEX закрыт после merge;
- проверка Post-merge Journal Closure;
- stale pre-merge status check result;
- follow-up commit SHA if finalization required;
- next recommended step.
