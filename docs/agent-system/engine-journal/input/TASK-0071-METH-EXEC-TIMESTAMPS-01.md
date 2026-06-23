# Задача для docs-maintainer: METH-EXEC-TIMESTAMPS-01

Рекомендуемый режим исполнения:

Роль: docs-maintainer
Исполнитель: на усмотрение архитектора
Reasoning effort: высокий
Запуск: Local only
Режим: Agent
Почему: задача меняет канон TASK/RESULT и несколько reusable-шаблонов; нужен branch-guard и точная семантика measured/reported времени.
Время начала выполнения (execution_started_at) [measured/engine]: 2026-06-23T15:44:39.0659334+07:00
Время оркестрации, по факту (orchestration_time_reported) [reported/human, опционально]: не сообщалось

## Цель

Добавить в методологию явные поля времени выполнения:

- measured/engine: фиксируется engine по факту собственного запуска/завершения;
- reported/human: сообщается человеком или оркестратором, опционально и может быть пустым.

## Scope

Обновить:

- `docs/agent-system/templates/TASK_HEADER_COMMON.md`;
- `docs/agent-system/ENGINE_JOURNAL_CONTRACT.md`;
- существующие TASK/RESULT/closure/report templates, где явно дублируются header или RESULT-поля;
- journal entry 0071;
- `docs/agent-system/cloud/**` через штатный `gen_cloud_bundle.py`.

Не менять:

- append-only history старых TASK/RESULT;
- merge-time semantics (`merged_at` остается в closure-stamp);
- manifest, file-map, generators, `.gitattributes`, runtime/CI/secrets;
- `main`/`developer` напрямую.

## Требования к канону

TASK:

```text
Время начала выполнения (execution_started_at) [measured/engine]: <ISO-8601 timestamp with timezone>
Время оркестрации, по факту (orchestration_time_reported) [reported/human, опционально]: <свободное значение или пусто>
```

RESULT:

```text
Время начала выполнения (execution_started_at) [measured/engine]: <ISO-8601 timestamp with timezone>
Время окончания выполнения (execution_finished_at) [measured/engine]: <ISO-8601 timestamp with timezone>
Длительность выполнения (execution_duration) [measured/engine, опционально]: <duration>
Время человека, по факту (human_time_reported) [reported/human, опционально]: <свободное значение или пусто>
```

Reviewer учитывается как отдельный engine-run со своим TASK/RESULT. Отдельного reviewer-time поля внутри work-записи не добавлять. Merge-время не дублировать: авторитетное поле остается `merged_at` в closure-stamp.

## Проверки

- `python docs/agent-system/tools/gen_file_map.py --check`;
- `python docs/agent-system/tools/gen_cloud_bundle.py --check`;
- активный internal link-check: broken links = 0;
- `rg -n "execution_started_at|execution_finished_at|human_time_reported|orchestration_time_reported" docs/agent-system/templates/TASK_HEADER_COMMON.md docs/agent-system/ENGINE_JOURNAL_CONTRACT.md`;
- `git diff --check`;
- branch-guard.

## Final report requirements

Вернуть:

- что добавлено в `TASK_HEADER_COMMON.md`;
- что добавлено в `ENGINE_JOURNAL_CONTRACT.md`;
- точный список обновленных templates;
- подтверждение dogfood execution-полей в TASK/RESULT 0071;
- результаты проверок;
- Source Delta;
- Source-reminder;
- context handoff по numbered cloud filenames;
- передача следующему исполнителю.

## STOP

- HEAD не `work/docs-maintainer-01/exec-timestamps-01`;
- правка вне allowed files;
- попытка ретрофитить старую history;
- новый hard release blocker по execution-полям;
- дублирование merge-time вне closure-stamp;
- generator/manifest/file-map changes без явного разрешения.
