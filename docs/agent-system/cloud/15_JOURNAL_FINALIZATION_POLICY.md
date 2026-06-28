# JOURNAL_FINALIZATION_POLICY

## Назначение

Journal finalization policy определяет, какие placeholders запрещены в finalized TASK/RESULT/INDEX и как engine завершает journal surface перед ready-for-review PR. Цель - не допускать PR, где RESULT или INDEX обещают дописать head SHA, PR URL, checks или финальные выводы позже.

## Deferred placeholder

Deferred placeholder - это текст, который говорит, что финальное значение, проверка или статус будут заполнены после текущего шага, но PR уже готовится к review. В finalized TASK/RESULT/INDEX такие строки создают ложное состояние: reviewer не может отличить завершённую запись от заготовки.

Запрещённые фразы в finalized TASK/RESULT/INDEX:

- `to be run after final edits`
- `pending`
- `TBD`
- `will be recorded later`
- `after PR creation`
- `after push`
- `pending final head`
- `pending PR URL`
- `pending checks`
- `placeholder`
- `not run yet`
- `to be updated`

Фразы запрещены как literal placeholders. Они допустимы только в явно историческом, backlog или future-plan контексте, где документ описывает правило, прошлый дефект или будущую задачу, а не незаполненное поле текущей записи.

## Где запрещено

- finalized `docs/agent-system/engine-journal/input/TASK-*.md`;
- finalized `docs/agent-system/engine-journal/output/RESULT-*.md`;
- active row текущей задачи в `docs/agent-system/engine-journal/INDEX.md`;
- PR body, если фраза относится к текущему RESULT/check/head/URL;
- final report, если фраза маскирует незавершённый факт.

## Где допустимо

- канонический документ с описанием этой политики;
- BACKLOG или NEXT_STEPS, если фраза явно относится к future candidate;
- историческая append-only запись, если она фиксирует старый дефект и не является active surface текущего PR;
- reviewer finding, где фраза цитируется как запрещённый пример без secret/sensitive value.

## Как исправляет engine

1. Создать TASK/RESULT/INDEX с фактическими полями, которые известны до PR.
2. После создания PR выполнить follow-up commit, если PR URL или final head SHA стали известны только после первого commit.
3. Заменить deferred placeholders фактическими значениями или явным `не применимо` с причиной.
4. Повторить `check_task_ready.py --base origin/developer` plain/json.
5. Убедиться, что output содержит только counts, filenames и category, без matching values.

## Что блокирует reviewer

Reviewer считает blocker:

- Finalized TASK/RESULT/INDEX переносят downstream feedback без sanitization checkpoint по `docs/agent-system/DOWNSTREAM_FEEDBACK_SANITIZATION_POLICY.md`;
- Finalized RESULT утверждает, что target repository уже получил methodology change до `main`, release tag или published snapshot;

- finalized RESULT содержит deferred placeholder текущей задачи;
- INDEX row текущей задачи оставлен как незавершённый pre-review surface;
- PR body обещает обновить checks/head/URL позже;
- RESULT перечисляет checks, которые не запускались;
- ready-gate output печатает matching placeholder values вместо count/filenames/category.

## Как сообщает check_task_ready.py

`check_task_ready.py` выполняет lightweight scan изменённых TASK/RESULT files и выводит категорию `deferred_finalization_placeholder`. Human output и JSON не печатают matching phrase или строку; безопасный формат ограничен count, filenames и category.

Этот gate не является NLP/semantic parser. Он ловит явные deferred finalization markers, а semantic completeness остаётся checklist/reviewer responsibility по `docs/agent-system/SEMANTIC_COMPLETENESS_GATES.md`.
