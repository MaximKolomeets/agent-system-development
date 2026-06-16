# OPERATIONAL_FAST_LANE

## Назначение

Operational Fast Lane - это короткий режим для простых операционных проверок и cleanup. Он нужен, чтобы не превращать безопасные status checks, cleanup и post-engine result checks в длинные methodology/debug cycles.

Operational Fast Lane не заменяет engine task workflow и не применяется к задачам, которые меняют repository files или создают Pull Request.

Operational Fast Lane не должен включать file-changing instructions для `engine`. Если проверка показывает, что нужны изменения файлов, PR body, journal artifacts или branch state через commit/push, Fast Lane заканчивается до выдачи actionable instructions.

Operational Fast Lane не требует Task File Handoff. Task File Handoff используется для больших задач с TASK file, а не для cleanup/status.

Общий стартовый contract для проектного чата описан в:

```text
docs/agent-system/CHATGPT_OPERATING_CONTRACT.md
```

Если после применения contract задача сводится только к проверке или cleanup, ChatGPT использует этот Fast Lane вместо methodology PR.

## Когда применять

Operational Fast Lane применяется для:

- проверка GitHub PR status;
- проверка local git status;
- cleanup branch;
- проверка post-engine result;
- release readiness sanity check;
- post-merge cleanup/status check;
- cleanup remote branch;
- проверка отсутствия open PRs;
- verify work branch is clean.

## Когда не применять

Operational Fast Lane не применяется для:

- изменения архитектуры;
- изменения runtime code;
- adoption bootstrap;
- docs-only governance pack;
- задач, где есть риск secrets/private data;
- задач, которые меняют файлы repository.
- задач, которые обновляют PR body, journal artifacts или branch state через commit/push;
- follow-up commits;
- shortcut-ответов вида "выполни быстрые команды, а потом пусть Engine patch files";
- больших задач, которым нужен Task File Handoff Mode;
- review-задач: review ≠ fast-lane status-check. Review всегда журналирует TASK+RESULT (`Journal trace: always` по `docs/agent-system/CODE_REVIEW_WORKFLOW.md` и `docs/agent-system/ENGINE_JOURNAL_CONTRACT.md`) и идёт docs-only PR; Fast Lane — read-only status/cleanup без journal. Простой GitHub PR status check или git status check остаётся Fast Lane, но это не review.

## Правила ответа ChatGPT

- Один ответ = один командный блок.
- Для пользователя это один блок команд без дополнительных длинных логов.
- GitHub состояние ChatGPT проверяет сам через connector, если доступно.
- Пользователь не должен присылать длинные логи, если все чисто.
- Если все чисто, пользователь пишет только `чисто`.
- Если есть ошибка, пользователь присылает только ошибку и 5-10 строк контекста.
- Не предлагать новый methodology PR для простой проверки/cleanup.
- Не предлагать sync `main -> developer` только из-за release merge commit.
- Не зеркалировать release merge commit обратно в `developer`, если содержательные изменения уже в `developer`.
- Если Fast Lane check обнаруживает необходимость file change, PR body update, journal update, branch state change через commit/push или follow-up commit, следующий ответ должен быть либо полным self-contained Engine-блоком, либо коротким запросом решения пользователя, если scope/approval отсутствуют.
- Cleanup-only означает cleanup без изменения repository files, если только не используется полный Engine-блок.

## Стандартный формат

```text
Тип:
Что вижу:
Выполни один блок:
Ожидаемо:
Следующий шаг:
```

## Проверка и cleanup после merge

Использовать после merge рабочего PR, release PR или sync PR, когда пользователь пишет `готово` или просит закрыть цикл.

После любого сообщения пользователя о merge/release/sync ChatGPT должен различать GitHub PR state и target journal state.

Проверить:

- рабочий PR имеет status `merged`;
- рабочий PR имеет merge commit SHA и `merged_at`, если эти данные доступны;
- release PR merged, если release в `main` выполнялся;
- release PR имеет URL/status/merge commit SHA/`merged_at`, если release выполнялся;
- sync PR merged, если выполнялся sync `main -> developer`;
- sync PR имеет URL/status/merge commit SHA/`merged_at`, если sync выполнялся;
- stale work branches удалены или явно оставлены по причине;
- target `RESULT` и `INDEX` закрыты после merge;
- target `RESULT` и `INDEX` фиксируют merge commit SHA, если он доступен;
- target `RESULT` и `INDEX` фиксируют release/sync факты или явно пишут `не применимо`;
- target `RESULT` и `INDEX` не содержат `PR open`, `ready for review`, `draft open`, `pending at file materialization` или `see Engine final report` как final state.

Fast Lane может завершиться коротким `чисто` только если:

- work PR merged: yes;
- release/sync merged или явно `не применимо`;
- RESULT closed after merge: yes;
- INDEX closed after merge: yes;
- No journal placeholders: yes;
- stale pre-merge status check: clean.

Если stale `RESULT` или `INDEX` найдены, ChatGPT должен остановить Fast Lane как read-only/cleanup-only путь и создать отдельную docs-only journal-closure task для `engine`. Такая task должна менять только target journal artifacts и безопасные index/status поля, без runtime, Docker, CI, secrets или private data.

Запрещено отвечать `все закрыто`, если GitHub PR merged, но target journal entry все еще содержит `open`, `ready for review`, `not merged`, `submitted for review`, `PR open`, `draft open`, `pending at file materialization` или `see Engine final report` как final state.

## Безопасность

Operational Fast Lane должен оставаться read-only или cleanup-only. Если в ходе проверки появляется необходимость менять файлы, создавать PR, работать с private data, читать `.env` или разбирать sensitive output, нужно остановиться и перейти к обычной задаче с явным scope, разрешенными файлами, запрещенными файлами и проверками.

Нельзя выводить гибридный shortcut, где Fast Lane-команды смешаны с неформальной просьбой к `engine` изменить repository files. Write-action instructions должны находиться внутри полного self-contained Engine-блока по `docs/agent-system/CHATGPT_RESPONSE_STANDARD.md`.
