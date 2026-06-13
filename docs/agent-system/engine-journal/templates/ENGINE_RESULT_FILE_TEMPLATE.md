# ENGINE_RESULT_FILE_TEMPLATE

Файл результата:

Связанный TASK file:

Режим источника задачи:

Task source commit SHA:

Task file blob SHA:

TASK file verified:

Engine block/TASK was self-contained:

Recommended Engine Mode present:

Verified baseline present or explicitly not applicable:

No required execution context was taken only from surrounding chat:

Идентификатор задачи:

Номер sequence:

Engine:

Агент:

Начато:

Завершено:

Branch:

Commit SHA:

PR URL:

Статус финализации:

RESULT finalized:

INDEX finalized:

No journal placeholders:

Follow-up finalization commit SHA:

Placeholder check:

PR created at:

Final commit SHA:

Final PR URL:

Ready for review:

Статус PR после review (`PR status after review`):

Merge commit SHA после merge:

Время merge (`merged_at`):

Release PR URL:

Статус release PR:

Merge commit SHA release PR:

Sync PR URL:

Статус sync PR:

Merge commit SHA sync PR:

RESULT закрыт после merge:

INDEX закрыт после merge:

Проверка Post-merge Journal Closure:

Измененные файлы:

- `<changed path>`

Выполненные проверки:

- `<check command>`

Невыполненные проверки и причина:

Результат проверки запрещенных файлов:

Результат проверки sensitive/private markers:

Результат language policy:

Принятые решения:

Риски:

Blockers:

Следующий рекомендуемый шаг:

Methodology feedback:

Примечание по финализации journal:

- placeholders допустимы только до PR creation;
- перед ready-for-review все placeholders должны быть заменены фактическими значениями;
- после merge `RESULT` и `INDEX` должны фиксировать PR status `merged`, merge commit SHA, release/sync PR данные при наличии, `RESULT closed after merge: yes`, `INDEX closed after merge: yes` и `No journal placeholders: yes`;
- после merge недопустимы final states `PR open`, `ready for review`, `draft open`, `pending at file materialization` и `see Engine final report`;
- user-facing labels/descriptions в RESULT и INDEX должны быть на русском языке, кроме technical identifiers и literal external names.
