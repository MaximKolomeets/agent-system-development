# OPERATIONAL_FAST_LANE

## Назначение

Operational Fast Lane - это короткий режим для простых операционных проверок и cleanup. Он нужен, чтобы не превращать безопасные status checks, cleanup и post-engine result checks в длинные methodology/debug cycles.

Operational Fast Lane не заменяет engine task workflow и не применяется к задачам, которые меняют repository files или создают Pull Request.

Operational Fast Lane не должен включать file-changing instructions для `engine`. Если проверка показывает, что нужны изменения файлов, PR body, journal artifacts или branch state через commit/push, Fast Lane заканчивается до выдачи actionable instructions.

Operational Fast Lane не требует Task File Handoff. Task File Handoff используется для больших задач с TASK file, а не для cleanup/status.

Общий стартовый contract для проектного чата описан в:

```text
docs/agent-system/ORCHESTRATOR_OPERATING_CONTRACT.md
```

Если после применения contract задача сводится только к проверке или cleanup, оркестратор использует этот Fast Lane вместо methodology PR.

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

Fast Lane не создаёт post-merge journal closure для ordinary PR.

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
- shortcut-ответов вида "выполни быстрые команды, а потом пусть исполнитель (engine) patch files";
- больших задач, которым нужен Task File Handoff Mode;
- standalone review-задач, где review сам является отдельной задачей: standalone review ≠ fast-lane status-check, всегда журналирует TASK+RESULT (`Journal trace: always` по `docs/agent-system/CODE_REVIEW_WORKFLOW.md` и `docs/agent-system/ENGINE_JOURNAL_CONTRACT.md`) и идёт docs-only PR; Fast Lane — read-only status/cleanup без journal. Простой GitHub PR status check или git status check остаётся Fast Lane, но это не review.
- active work PR review/autoloop не является standalone review-задачей: reviewer не создаёт отдельный PR, не меняет файлы и оставляет feedback только в PR агента; исправления делает engine в той же task branch по `docs/agent-system/REVIEW_AUTOLOOP.md`.
- В active work PR autoloop machine-verifiable blockers закрываются через reviewer `verification_command` и engine fix-pass report; если checks прошли и scope не расширен, full reviewer pass не нужен. Semantic/mixed blockers требуют minimal reviewer re-review по changed blocker scope.
- Перед завершением PR/fix-pass/ready-to-merge engine запускает read-only ready-gate `python docs/agent-system/tools/check_task_ready.py --base origin/developer`; Fast Lane может принимать его passed output как machine-verifiable evidence, но не превращает Fast Lane в write-action task.
- Если Fast Lane/status check видит generated/cloud EOL-only шум, сначала использовать read-only `python docs/agent-system/tools/generated_eol_guard.py --base origin/developer`; content drift остаётся blocker, а EOL/whitespace-only noise не требует полного reviewer pass без других изменений.
- Для downstream/target status checks methodology reference проверяется по stable ref `origin/main` / `main`, release tag или явно заданному snapshot. Dirty `agent-system-development/developer` или `work/*` не является blocker сам по себе. Fast Lane не выполняет `git switch`, `git checkout`, `git pull`, `git reset`, `git clean` или `git stash` в methodology repository ради чтения downstream reference.

## Правила ответа оркестратора

- Один ответ = один командный блок.
- Для пользователя это один блок команд без дополнительных длинных логов.
- GitHub состояние оркестратор проверяет сам через connector, если доступно.
- Пользователь не должен присылать длинные логи, если все чисто.
- Если все чисто, пользователь пишет только `чисто`.
- Если есть ошибка, пользователь присылает только ошибку и 5-10 строк контекста.
- Не предлагать новый methodology PR для простой проверки/cleanup.
- Не предлагать sync `main -> developer` только из-за release merge commit.
- Не зеркалировать release merge commit обратно в `developer`, если содержательные изменения уже в `developer`.
- Если Fast Lane check обнаруживает необходимость file change, PR body update, journal update, branch state change через commit/push или follow-up commit, следующий ответ должен быть либо полным self-contained блоком для исполнителя (engine), либо коротким запросом решения пользователя, если scope/approval отсутствуют.
- Cleanup-only означает cleanup без изменения repository files, если только не используется полный блок для исполнителя (engine).

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

После любого сообщения пользователя о merge/release/sync оркестратор должен различать GitHub PR state, target journal state и контекст closure policy.

Проверить:

- рабочий PR имеет status `merged`;
- рабочий PR имеет merge commit SHA и `merged_at`, если эти данные доступны;
- для ordinary PR GitHub PR metadata является source of truth для merge facts;
- release PR merged, если release в `main` выполнялся;
- release PR имеет URL/status/merge commit SHA/`merged_at`, если release выполнялся;
- `python docs/agent-system/tools/gen_file_map.py --check` проходит перед release readiness verdict;
- sync PR merged, если выполнялся sync `main -> developer`;
- sync PR имеет URL/status/merge commit SHA/`merged_at`, если sync выполнялся;
- stale work branches удалены или явно оставлены по причине;
- ordinary `RESULT` и `INDEX` имеют PR URL, reviewed head SHA и `architect_ready` / `human_merge_allowed` до merge, если проверяется ordinary PR;
- target `RESULT` и `INDEX` закрыты после merge только для release/audit/explicit boundary reconciliation contexts;
- target `RESULT` и `INDEX` фиксируют merge commit SHA только если boundary reconciliation выполняется и SHA доступен;
- target `RESULT` и `INDEX` фиксируют release/sync факты или явно пишут `не применимо` только в boundary/release context;
- target `RESULT` и `INDEX` не содержат `PR open`, `ready for review`, `draft open`, `pending at file materialization` или `see Engine final report` как final state в release/audit/explicit boundary reconciliation context.

Fast Lane может завершиться коротким `чисто` только если:

- work PR merged: yes;
- release/sync merged или явно `не применимо`;
- RESULT/INDEX closed after merge: yes для release/audit/explicit boundary reconciliation contexts; для ordinary PR достаточно PR URL + reviewed head SHA + `architect_ready` / `human_merge_allowed`, а merge facts читаются из GitHub;
- PROJECT_FILE_MAP parity check: clean;
- cloud bundle parity check: clean;
- task ready-gate: clean, если проверяется active work PR или fix-pass;
- No journal placeholders: yes;
- stale pre-merge status check: clean для boundary reconciliation context; для ordinary PR отдельный closure PR не требуется.

Если stale `RESULT` или `INDEX` найдены в release/audit/explicit boundary reconciliation context или противоречат GitHub facts внутри такого scope, оркестратор должен остановить Fast Lane как read-only/cleanup-only путь и создать отдельную docs-only reconciliation task для `engine`. Такая task должна менять только target journal artifacts и безопасные index/status поля, без runtime, Docker, CI, secrets или private data. Для ordinary PR absence of merge SHA/`merged_at` в `RESULT` не требует отдельной closure task.

Запрещено отвечать `все закрыто`, если GitHub PR merged в release/audit/explicit boundary reconciliation context, но target journal entry все еще содержит `open`, `ready for review`, `not merged`, `submitted for review`, `PR open`, `draft open`, `pending at file materialization` или `see Engine final report` как final state. Для ordinary PR отвечать, что цикл закрыт на ordinary terminal state, а post-merge facts находятся в GitHub PR metadata.

## Безопасность

Operational Fast Lane должен оставаться read-only или cleanup-only. Если в ходе проверки появляется необходимость менять файлы, создавать PR, работать с private data, читать `.env` или разбирать sensitive output, нужно остановиться и перейти к обычной задаче с явным scope, разрешенными файлами, запрещенными файлами и проверками.

Нельзя выводить гибридный shortcut, где Fast Lane-команды смешаны с неформальной просьбой к `engine` изменить repository files. Write-action instructions должны находиться внутри полного self-contained блока для исполнителя (engine) по `docs/agent-system/ORCHESTRATOR_RESPONSE_STANDARD.md`.
