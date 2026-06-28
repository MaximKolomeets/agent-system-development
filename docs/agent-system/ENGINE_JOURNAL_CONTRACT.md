# ENGINE_JOURNAL_CONTRACT

## Назначение

Engine journal фиксирует воспроизводимый журнал задач для `engine` и ответов `engine`.

Английский alias: reproducible engine journal.

Цель журнала - сделать историю проекта восстановимой по GitHub files: кто сформулировал задачу, какой `engine` ее выполнил, какая ветка и Pull Request получились, какие проверки были выполнены и какой следующий шаг рекомендован.

Engine journal не заменяет Git history, Pull Request, commits или docs-maintainer reports. Он связывает их в одну читаемую цепочку:

```text
task file -> result file -> branch -> Pull Request -> commit/result
```

## Расположение

Каноническая папка:

```text
docs/agent-system/engine-journal/
```

Обязательная структура:

```text
docs/agent-system/engine-journal/
  README.md
  INDEX.md
  input/
  output/
  templates/
```

## Область template repository

`agent-system-development` is a reusable methodology/template repository.

In this repository, `docs/agent-system/engine-journal/` contains only scaffold,
contract, index, README, and reusable templates. The `input/` and `output/`
folders are intentionally empty except `.gitkeep`.

Real task/result files создаются в target repositories после adoption. Не
сохранять реальную TASK/RESULT history разработки methodology в этом template
repository и не копировать methodology operational history в target
repositories.

Исключение: если пользователь явно назначил methodology-hardening задачу для
самого `agent-system-development` и включил engine journal в allowed files/scope,
эта задача может создать собственные TASK/RESULT/INDEX entries в этом
repository. Такие entries не являются transferable template state и не должны
копироваться в target repositories. Ветка, PR, RESULT и INDEX все равно должны
быть Russian-first, append-only и финализированы после PR creation.

## Вход и выход

`input/` содержит входные задачи для `engine`.

`output/` содержит ответы `engine` по этим задачам.

`templates/` содержит reusable templates для task/result files.

Task file и result file должны иметь одинаковый sequence number и task id, чтобы их можно было сопоставить без внешнего контекста.

## Политика Russian-first journal

TASK/RESULT/INDEX files, user-facing labels, descriptions и final report должны быть на русском языке по `docs/agent-system/LANGUAGE_POLICY.md`.

Английский допустим только для technical identifiers, command names, flags, paths, filenames, branch names, config keys, API names, package names, vendor/tool names, SHA values и literal external names.

Commit subject/body и PR title/body также должны быть Russian-first по `docs/agent-system/LANGUAGE_POLICY.md` → «Commit и PR metadata». Если нарушение commit/PR metadata language случилось и не было безопасно исправлено до push, RESULT обязан зафиксировать нарушение, причину отказа от rewrite/force-push и следующий безопасный шаг. Уже pushed/merged commits не переписываются без отдельного явного решения архитектора.

Если target instructions конфликтуют с Russian-first policy, `engine` должен написать `STOP` и запросить решение пользователя, кроме случая явного разрешения пользователя на другой язык.

## Именование

Рекомендуемое именование:

```text
TASK-0001-PR-2r-engine-journal-contract.md
RESULT-0001-PR-2r-engine-journal-contract.md
```

Где:

- `TASK` - входная задача для `engine`;
- `RESULT` - ответ `engine`;
- `0001` - сквозной номер в журнале;
- `PR-2r` - связанный task/PR id;
- `engine-journal-contract` - короткий slug.

Нумерация sequence — append-only. Следующий номер `engine` вычисляет ИЗ `INDEX.md` на момент выполнения задачи (последний seq + 1) и ИГНОРИРУЕТ любой номер, предсказанный в task-блоке. Нельзя предугадывать, переиспользовать или пропускать seq. Обоснование: параллельная работа нескольких агентов может занять предсказанный номер (journal 0018: task-блок предписывал 0016, но 0016/0017 уже были заняты → запись корректно ушла в 0018).

## Index

`INDEX.md` содержит таблицу:

```text
| Seq | Task id | Input file | Output file | Branch | PR | Status | Notes |
```

Каждая journal entry должна быть добавлена в index отдельной строкой.

## Append-only правило

Engine journal является append-only по умолчанию.

Task/result files нельзя удалять, перезаписывать или переиспользовать для другой задачи без отдельного решения пользователя.

Если задачу нужно уточнить, создается новый task file с новым sequence number или добавляется отдельный follow-up task. Старый task/result остается как historical record.

## Режим Task File Handoff

TASK file может быть создан до выполнения как отдельный task-file-only commit в target repository.

В этом режиме TASK file является source of truth, а short bootstrap prompt только указывает `engine`, какой repository, branch и путь к task file прочитать.

RESULT обязан ссылаться на:

- путь к task file;
- commit SHA task source;
- blob SHA task file, если доступен;
- execution branch;
- execution PR URL;
- final commit SHA.

RESULT обязан включать блок «Source Delta» по канону `docs/agent-system/templates/TASK_HEADER_COMMON.md` → «Source Delta». Этот блок персистится в journal и не заменяется ссылкой на chat/final report.

RESULT обязан включать строку `Архитектору — загрузить в контекст оркестратора: ...` по канону `docs/agent-system/templates/TASK_HEADER_COMMON.md` → «Orchestrator context handoff». В этой строке используются numbered cloud-имена из `docs/agent-system/cloud/00_README.md`, исходные пути пишутся как `src: ...`, а небандловые файлы остаются только в «Source Delta».

Если TASK file, bootstrap prompt, branch или source SHA конфликтуют, `engine` должен написать `STOP` и не выполнять задачу.

Если TASK file содержит fenced YAML block `task_contract`, он является source of truth для mode/scope/checks/STOP по `docs/agent-system/TASK_CONTRACT.md`. RESULT должен фиксировать результат `validate_task_contract.py`, если validation запускалась. Если нарушение task contract или commit/PR metadata language случилось и его нельзя безопасно исправить до push без rewrite/force-push, RESULT фиксирует нарушение, причину и следующий безопасный шаг; уже pushed/merged history не переписывается без отдельного явного решения архитектора.

## Безопасность

Engine journal хранится в GitHub и считается публичным, если repository public.

Запрещено добавлять в journal:

- `.env`;
- credentials;
- tokens;
- private keys;
- real passwords;
- private repository URLs;
- private downstream project names;
- client/customer data;
- production/runtime data;
- secret values;
- logs with sensitive values.

Sensitive checks в journal result должны фиксировать только безопасный summary. Matching lines и secret values нельзя копировать в journal.

## Adoption target repository

При adoption target repository должен получить собственный `docs/agent-system/engine-journal/`.

Target repository journal хранит project-specific task/result history внутри target repository, а не в public methodology repository.

Первый adoption/audit PR должен создавать или обновлять:

- `docs/agent-system/engine-journal/README.md`;
- `docs/agent-system/engine-journal/INDEX.md`;
- `docs/agent-system/engine-journal/input/`;
- `docs/agent-system/engine-journal/output/`;
- `docs/agent-system/engine-journal/templates/`;
- task file для первой engine-задачи;
- result file для ответа engine.

Если первый шаг adoption остается `audit-only`, task/result files допускаются как journal artifacts рядом с `docs/agent-system/ADOPTION_AUDIT.md`, потому что они описывают выполнение audit, а не переносят full methodology state.

Adoption переносит только scaffold/templates и формат `INDEX.md`. Первая target
adoption/audit task создает target-specific task/result files и target-specific
записи `INDEX.md`.

Если `INDEX.md` используется как reusable source, переносится структура таблицы,
заголовки и правила заполнения. Operational rows methodology repository
(`METH-*`, PR history, local closure facts) не копируются verbatim в target
repository.

Methodology repository operational history не переносится.

## Обязательные ссылки

Каждый result file должен ссылаться на:

- связанный task file;
- режим task source;
- commit SHA task source, если TASK file создан заранее;
- blob SHA task file, если доступен;
- task id;
- branch;
- commit SHA, если commit создан;
- PR URL, если PR создан;
- измененные файлы;
- запущенные проверки;
- результат проверки запрещенных файлов;
- результат sensitive/private marker;
- риски;
- следующий рекомендуемый шаг.

## Execution timestamps

Новые TASK/RESULT записи фиксируют execution-время по модели `measured/reported`:

- `measured/engine` — значения, которые engine фиксирует автоматически или надежно по факту собственного запуска;
- `reported/human` — значения, которые сообщает человек или оркестратор; они опциональны и могут оставаться пустыми.

TASK должен содержать:

- `Время начала выполнения (execution_started_at) [measured/engine]` в формате ISO 8601 с timezone;
- `Время оркестрации, по факту (orchestration_time_reported) [reported/human, опционально]`.

RESULT должен содержать:

- `Время начала выполнения (execution_started_at) [measured/engine]` в формате ISO 8601 с timezone;
- `Время окончания выполнения (execution_finished_at) [measured/engine]` в формате ISO 8601 с timezone;
- `Длительность выполнения (execution_duration) [measured/engine, опционально]`;
- `Время человека, по факту (human_time_reported) [reported/human, опционально]`.

Reviewer не получает отдельного поля времени внутри work-записи: review является отдельным engine-run со своим TASK/RESULT и собственными execution-полями. Merge-время не дублируется в execution-полях. Для ordinary PR source of truth по `merged_at` и merge commit SHA — GitHub PR metadata; closure-stamp в `RESULT` добавляется только при boundary reconciliation или explicit architect request по разделу «GitHub merge facts authority».

Правило не ретрофитится в append-only history: старые TASK/RESULT без execution-полей не переписываются. В новых finalized TASK/RESULT отсутствие `execution_started_at` или `execution_finished_at` является minor finding, но не hard blocker, не release blocker и не признак invalid final-state. Отсутствие или пустота `reported/human` полей не является finding.

`execution_finished_at` является единственным каноническим именем measured-поля окончания выполнения. Вариант имени, образованный как `execution_` + `completed_at`, не является допустимым alias для новых записей; если он появляется в новой finalized TASK/RESULT вместо `execution_finished_at`, reviewer фиксирует minor finding. Старые append-only записи с таким drift-именем остаются историей и не ретрофитятся.

## Правило финализации после PR

`RESULT` и `INDEX` могут содержать временные placeholders только до создания PR.

После создания PR `engine` обязан обновить `RESULT` и `INDEX` фактическими значениями:

- финальная branch;
- final commit SHA;
- PR URL;
- PR status;
- запущенные проверки;
- blockers;
- следующий рекомендуемый шаг.

Если PR URL или final commit SHA стали известны только после materialization journal files, `engine` должен сделать follow-up commit в ту же рабочую ветку и push в тот же PR.

Финальный отчет задачи, которая создала PR, была смержена, обновила remote
`developer`/`main` или обнаружила рассинхрон локальной ветки с `origin/*`,
должен содержать конкретный блок `Локальные действия после PR/merge` по
`docs/agent-system/WORKFLOW.md`.

Ready-for-review PR не должен содержать unresolved journal placeholders:

- `created after file materialization`;
- `pending at file materialization`;
- `see Engine final report`;
- `<commit SHA>`;
- `<PR URL>`;
- `<result>`;
- `<check command>`.

Placeholder-scan применяется к finalized `RESULT`/`INDEX` и concrete state/status docs. Легитимные шаблонные поля в templates/examples (`<роль>`, `<task-id>`, `<commit-sha>` и подобные), а также определения forbidden placeholders в тексте политики не являются findings сами по себе. Finding — только unresolved placeholder в finalized или concrete контексте, где уже должно стоять фактическое значение.

Reviewer должен считать такие placeholders blocker.

## Политика PR head SHA без self-reference

Commit не может честно содержать собственный SHA внутри файлов, включенных в этот же commit.

Journal artifacts могут фиксировать:

- `primary/materialization commit SHA`;
- `journal finalization commit SHA`;
- `follow-up materialization commit SHA`, если применимо;
- `latest known PR head SHA before follow-up`, если применимо;
- `actual/current PR head SHA after push`, если он проверен после push и может быть зафиксирован без self-referential loop.

Если запись `actual/current PR head SHA after final push` внутрь `RESULT` или `INDEX` требует бесконечного self-referential commit loop, `engine` не должен выдумывать false value.

В этом случае финальный отчет `engine` и PR body могут быть authoritative place для latest verified PR head SHA after final push.

`RESULT` и `INDEX` должны различать:

- commit SHA, зафиксированный в journal;
- actual/current PR head SHA, проверенный после final push.

Reviewer не должен требовать, чтобы commit содержал собственный SHA.

Unresolved placeholders остаются blockers, но явно отмеченное ограничение self-reference не считается placeholder.

## Closure policy

Default-режим ordinary task PR — **ordinary terminal state**, а не отдельный post-merge closure PR и не обязательный batch debt.

Ordinary terminal state достигается до human merge, когда:

- reviewer дал `reviewer:approved` или approve-equivalent verdict/comment;
- PR переведён в `architect:ready-to-merge` / `human_merge_allowed`;
- `RESULT` и `INDEX` финализированы после PR creation;
- PR URL зафиксирован;
- reviewed head SHA зафиксирован;
- unresolved placeholders отсутствуют.

Допустимые lifecycle/status значения:

- `architect_ready`;
- `human_merge_allowed`;
- `merged_by_github`;
- `boundary_closed`.

`merged_by_github` может быть inferred из GitHub PR metadata без изменения `RESULT` или `INDEX`.

До merge основная task entry может иметь статус `ready_for_merge`, `architect_ready`, `human_merge_allowed` или близкую Russian-first формулировку `готов к human merge`, если `RESULT` и `INDEX` финализированы после PR creation и не содержат unresolved placeholders. После human merge обычного work PR отдельная правка `RESULT/INDEX` не требуется: отсутствие `merged_at` и merge commit SHA в `RESULT` ordinary PR не является blocker. GitHub PR metadata является canonical source для post-merge facts: PR state, `merged_at`, merge commit SHA и PR URL.

Следующий work PR той же фазы не должен останавливаться только из-за того, что предыдущий ordinary PR уже merged в GitHub, но его `RESULT/INDEX` не получили post-merge closure stamp. Executor, reviewer и orchestrator не создают отдельный closure PR после каждого merge и не считают такую запись cleanup debt, если есть PR URL, reviewed head SHA и `architect_ready` / `human_merge_allowed`.

Обычная substantive task завершается на ordinary terminal state. Engine владеет основной task branch до `architect_ready`, исправляет review feedback в той же branch и доводит один итоговый PR до human-merge-ready состояния. Human merge выполняет архитектор; post-merge facts читаются из GitHub PR metadata.

Если task проходит review autoloop, RESULT/final report фиксирует `max_review_cycles`, фактический `review_cycle_count`, последний reviewed head SHA и итоговый статус: `architect:ready-to-merge` или `automation:stopped-human-required`. GitHub PR comments/reviews остаются источником feedback, а journal не создаёт отдельную feedback-запись. Канон: `docs/agent-system/REVIEW_AUTOLOOP.md`.

Перед release/audit boundary допускается boundary reconciliation: плановая сверка GitHub PR metadata и journal surface. Она может batch-обновить старые записи closure-stamp'ами только если архитектор явно запросил reconciliation или boundary gate требует полного исторического snapshot. До такого boundary отсутствие post-merge closure stamp у ordinary PR не является долгом.

Post-merge closure stamp применяется только в случаях:

- release boundary;
- audit boundary;
- explicit architect request;
- batch reconciliation.

Closure-only задача не создаёт новый TASK/RESULT для закрываемой рабочей записи. Если boundary reconciliation или explicit request действительно требуют stamp, задача добавляет closure-stamp с фактами в существующий `RESULT`, обновляет в `INDEX` только status + PR URL и безопасный summary, сохраняя append-only смысл journal entry. Канонический шаблон per-task closure: `docs/agent-system/templates/CLOSURE_TASK_TEMPLATE.md`.

Batch reconciliation проходит по `INDEX.md`, получает факты PR из GitHub и добавляет closure-stamp только для записей, включённых в явный boundary/reconciliation scope. Канонический шаблон batch closure/reconciliation: `docs/agent-system/templates/BATCH_CLOSURE_TASK_TEMPLATE.md`.

### Accepted terminal fold

`terminal-fold accepted` — финальное lifecycle-состояние terminal-записи, а не `open`.

Accepted terminal fold допустим только для lifecycle-only entries: closure, finalstate-fix, reviewer-gate trace, release-prep trace, sync/cleanup trace, если запись не несёт незакрытого содержательного payload.

Правила:

- `terminal-fold accepted` не считается `open`, `ready`, `closure pending` или blocker для reviewer-gate, release-prep и release-gate.
- GitHub PR URL является authority для own merge facts terminal-записи; own merge facts не backfill'ятся рекурсивно отдельной closure-задачей.
- Не создавать новую closure-задачу только ради `terminal-fold accepted`.
- Ordinary substantive entries завершаются на ordinary terminal state; closure-stamp с merge facts нужен только при boundary reconciliation или explicit architect request.
- Если terminal-запись содержит содержательные незакрытые изменения source docs/templates/canons, она не может быть silently accepted и закрывается обычным closure-проходом.

Search aliases for checks: `PR URL authoritative`; `not a blocker`; `do not create closure solely`.

Канонический status в `INDEX`:

```text
terminal-fold accepted; PR URL authoritative; not release/reviewer blocker
```

Для собственной текущей terminal-записи до merge PR допустима формулировка:

```text
terminal-fold accepted pending own PR merge; PR URL authoritative after merge
```

### GitHub merge facts authority

Авторитетный источник post-merge фактов ordinary PR — GitHub PR metadata.

GitHub PR metadata считается source of truth для:

- PR state;
- `merged_at`;
- merge commit SHA;
- PR URL.

Journal хранит task intent, execution result, PR URL, reviewed head SHA и `architect_ready` / `human_merge_allowed` status. Отсутствие `merged_at` или merge commit SHA в `RESULT` ordinary PR после human merge не является blocker.

Closure-stamp в `RESULT-<seq>` является append-only snapshot только для boundary reconciliation или explicit architect request.

Когда closure-stamp нужен, `RESULT-<seq>` фиксирует доступные факты:

- work PR status: `merged`;
- work PR merge commit SHA;
- work PR `merged_at`, если доступно;
- final head SHA;
- work PR URL;
- release PR URL/status/merge commit SHA/`merged_at`, если выполнялся release в `main`, иначе `не применимо`;
- sync PR URL/status/merge commit SHA/`merged_at`, если выполнялся sync `main -> developer`, иначе `не применимо`;
- `RESULT closed after merge: yes`;
- `INDEX closed after merge: yes`;
- `No journal placeholders: yes`;
- next step after closure;
- safe summary of checks.

`INDEX.md` для закрываемой seq фиксирует только:

- final status (`merged; RESULT closed after merge`, `closed`, `closed-at-creation` или другой статус по lifecycle записи);
- PR number/URL;
- optional short mergedAt date, если это помогает навигации;
- safe one-line summary.

`INDEX.md` не является источником полного `mergeCommit` и не должен дублировать полный merge commit SHA. Reviewer сверяет merge facts по GitHub PR metadata; если выполнялся обязательный boundary/explicit closure-pass, дополнительно сверяет `RESULT` closure-stamp и GitHub/local git, но не требует `mergeCommit` в `INDEX`.

Legacy-записи, где old policy уже продублировала merge facts в `INDEX`, остаются как append-only history и не ретрофитятся.

Следующие pre-merge значения являются недопустимыми final states только после обязательного boundary/explicit closure-прохода, если запись не классифицирована как lifecycle-only `terminal-fold accepted`:

- `PR open`;
- `ready for review`;
- `draft open`;
- `pending at file materialization`;
- `see Engine final report`;
- `open; not merged`;
- `merged; closure pending`.

Closure-проход обязан не только зафиксировать факты в closure-stamp `RESULT` и status + PR URL в `INDEX`, но и убрать stale final-state поверхности закрываемой записи внутри заданного boundary scope. Верхний status-marker закрываемого `RESULT` приводится к closed-статусу, согласованному с уже добавленным closure-stamp; terminal lifecycle-only summary в `INDEX` после merge переводится в `terminal-fold accepted`, а не порождает следующий closure PR. Оставшаяся pre-merge поверхность из списка выше после обязательного boundary/explicit closure-прохода является blocker под release/consistency gate, кроме accepted terminal fold по разделу выше.

Если merge commit SHA доступен в GitHub или local git history и boundary/explicit closure-pass выполняется, closure должен зафиксировать его в `RESULT` closure-stamp. Отсутствие merge commit SHA в `RESULT` после обязательного boundary/explicit closure-прохода без явного объяснения считается blocker. Отсутствие merge commit SHA в `RESULT` ordinary PR без closure-pass и отсутствие merge commit SHA в `INDEX` не являются blocker.

Если closure-stamp в `RESULT` или status/PR URL в `INDEX` противоречит GitHub PR state после обязательного boundary/explicit closure-прохода, reviewer должен считать это blocker.

Если release/sync PRs были merged и boundary reconciliation явно выполняется перед release/audit, но journal не фиксирует release/sync facts в заданном boundary scope, reconciliation считается incomplete.

### Scope of closure-policy consistency

Closure-policy consistency check применяется к операционным правилам, active templates, handoff contracts, review checklists и current workflow instructions.

Append-only journal entries, decision log, dated state snapshots и docs-maintainer sync reports сохраняют исторические literals старой политики и не входят в check F. Такие файлы не переписываются ради терминологического scrub, если они описывают прошлое решение/состояние, а не действующее правило.

## Pre-release reviewer consistency-gate

Перед каждым release `developer -> main`, после state-refresh и до human merge, обязателен journaled reviewer consistency-gate по release payload. Это focused delta-review накопленной release-серии, а не повтор полного аудита методологии.

Gate выполняет роль reviewer (`code-reviewer-01` или `qa-reviewer-01`). Режим: read-only по содержанию, `Journal trace: always`, `Report delivery: chat`, ветка `work/<reviewer-role>/<task>`, docs-only journal PR в `developer`. Отдельный новый шаблон не создаётся: reviewer использует существующий pattern `docs/agent-system/templates/CODE_REVIEW_TASK_TEMPLATE.md` + `docs/agent-system/templates/TASK_HEADER_COMMON.md`.

Release payload = накопленный diff `origin/main...origin/developer`, то есть вся серия изменений, которая войдёт в release PR.

Reviewer подтверждает:

- release payload соответствует ровно merged-серии по `INDEX.md`, без посторонних или необъяснённых изменений;
- `python docs/agent-system/tools/gen_file_map.py --check` и `python docs/agent-system/tools/gen_cloud_bundle.py --check` проходят на release-кандидате;
- если на Windows wrapper/parallel runner для read-only generated `--check` завис, reviewer/engine применяет sequential fallback по `ORCHESTRATOR_OPERATING_CONTRACT.md` → «Проверки generated text artifacts: content-oriented / EOL-safe» и записывает команду + exit code в RESULT;
- если на Windows no-output scan (`rg`/wrapper) завис без полезного процесса, reviewer/engine применяет deterministic fallback по тому же B-WIN правилу и записывает fallback-команду, exit code и смысл результата в RESULT;
- journal закрыт сквозняком: closure-stamp есть в `RESULT`, а `INDEX` содержит closed status + PR URL по всем seq серии;
- Source Delta и context handoff согласованы по серии;
- release notes соответствуют фактическому payload;
- unresolved placeholders отсутствуют;
- проверки из раздела «Проверка target repository» применены агрегированно к release payload.

Любой невыполненный пункт блокирует release.

Запись reviewer-gate закрывается per-task в release-prep вместе с остальными pre-release записями, чтобы release PR не включал незакрытый journal.

### Отношение к полному аудиту

Полный сквозной аудит методологии — отдельный baseline-проход по необходимости: перед первой downstream adoption, при крупном изменении методологии или по явному запросу. Он не выполняется на каждый release/PR.

Регулярный release-gate — это focused delta consistency-gate по release payload. Per-PR review внутри batch-серии остаётся review-only и не требует полного аудита методологии.

## Правило review

### Journal trace для review всегда

Любая review-задача (в т.ч. `review-only`) журналирует TASK + RESULT и обновляет `INDEX.md` по этому контракту — `Journal trace: always`. Это согласовано с `docs/agent-system/CODE_REVIEW_WORKFLOW.md`.

`Report delivery` — отдельный независимый параметр, задающий, куда уходит **тело** review report:

- `chat` (дефолт) — тело отчёта возвращается в чат и в repository не сохраняется;
- `repository` / `chat+repository` — тело отчёта дополнительно сохраняется как файл по `Report naming`.

`Report delivery: chat` НЕ отменяет journal trace: TASK/RESULT/INDEX создаются всегда и идут в docs-only PR. «Chat-only» относится только к телу отчёта, а не к отсутствию journal-следа.

### Проверка methodology repository

Для `agent-system-development` reviewer должен проверить, что:

- engine journal scaffold, templates, README и contract присутствуют;
- `input/` and `output/` are intentionally empty except `.gitkeep`;
- `INDEX.md` объясняет, что entries заполняются target repositories;
- real TASK/RESULT operational history не хранится в template repository;
- private downstream data, credentials, tokens или private repository URLs не добавлены.

### Проверка target repository

Перед merge PR reviewer должен проверить, что:

- task file и result file связаны одним sequence number;
- index обновлен;
- forbidden/private data не добавлены;
- task/result files не противоречат final report;
- RESULT содержит «Source Delta» по канону `docs/agent-system/templates/TASK_HEADER_COMMON.md` и этот блок согласован с фактическим diff;
- RESULT содержит context handoff по канону `docs/agent-system/templates/TASK_HEADER_COMMON.md`: numbered cloud-имена из `docs/agent-system/cloud/00_README.md`, только bundle-файлы, небандловые tooling/source-файлы не перечислены в context-load строке;
- новые TASK/RESULT содержат measured execution-поля `execution_started_at`/`execution_finished_at`; отсутствие этих полей в finalized записи является minor finding, но не blocker. `reported/human` поля опциональны и не проверяются как обязательные;
- новые TASK/RESULT не используют неканоническое имя окончания выполнения, образованное как `execution_` + `completed_at`; новое появление такого поля является minor finding, исторические append-only записи не ретрофитятся;
- branch, PR и commit references совпадают с фактическим GitHub state.
- ready-for-review PR не содержит unresolved journal placeholders в `RESULT` или `INDEX`;
- ready-for-review PR соблюдает `docs/agent-system/JOURNAL_FINALIZATION_POLICY.md`: finalized TASK/RESULT/INDEX не содержат deferred finalization markers текущей задачи;
- если это обычный work PR, status `architect_ready` / `human_merge_allowed` допустим как ordinary terminal state; post-merge closure stamp не требуется до boundary reconciliation или explicit architect request;
- TASK/RESULT/INDEX являются Russian-first, кроме technical identifiers и literal external names.

Reviewer не считает blocker тот факт, что ordinary PR после human merge не имеет `merged_at` или merge commit SHA в `RESULT`, если до merge были зафиксированы PR URL, reviewed head SHA и `architect_ready` / `human_merge_allowed`. Reviewer не должен требовать отдельный closure PR для ordinary PR и сверяет post-merge facts по GitHub PR metadata.

Reviewer должен считать blocker, если merged PR journal находится под release boundary, audit boundary, explicit architect request или batch reconciliation scope и при этом:

- остается в статусе `PR open`;
- остается в статусе `ready for review`;
- остается в статусе `draft open`;
- остается в статусе `open; not merged`;
- остается в статусе `merged; closure pending`;
- содержит `pending at file materialization`;
- содержит `see Engine final report`;
- `RESULT` closure-stamp не фиксирует merge commit SHA после merge, когда SHA доступен и closure-stamp входит в boundary/explicit scope;
- не фиксирует `RESULT closed after merge: yes`;
- не фиксирует `INDEX closed after merge: yes`.
