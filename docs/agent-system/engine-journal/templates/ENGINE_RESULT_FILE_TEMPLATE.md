# ENGINE_RESULT_FILE_TEMPLATE

Файл результата:

Связанный TASK file:

Режим источника задачи:

Task source commit SHA:

Task file blob SHA:

TASK file verified:

Engine block/TASK was self-contained:

Рекомендуемый режим исполнения присутствует:

Verified baseline present or explicitly not applicable:

No required execution context was taken only from surrounding chat:

Идентификатор задачи:

Номер sequence:

Engine:

Агент:

Время начала выполнения (execution_started_at) [measured/engine]:

Время окончания выполнения (execution_finished_at) [measured/engine]:

Длительность выполнения (execution_duration) [measured/engine, опционально]:

Время человека, по факту (human_time_reported) [reported/human, опционально]:

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

## Закрытие после merge

Work PR status:

Work PR merge commit SHA:

Work PR merged_at:

Release PR status:

Release PR merge commit SHA:

Release PR merged_at:

Sync PR status:

Sync PR merge commit SHA:

Sync PR merged_at:

RESULT closed after merge:

INDEX closed after merge:

No journal placeholders:

Stale pre-merge status check:

Closure blockers:

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
- после merge `RESULT` и `INDEX` должны фиксировать work PR status `merged`, merge commit SHA, `merged_at`, release/sync PR данные или `не применимо`, `RESULT closed after merge: yes`, `INDEX closed after merge: yes` и `No journal placeholders: yes`;
- после merge недопустимы final states `PR open`, `ready for review`, `draft open`, `pending at file materialization` и `see Engine final report`;
- user-facing labels/descriptions в RESULT и INDEX должны быть на русском языке, кроме technical identifiers и literal external names.
