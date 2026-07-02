# ENGINE_JOURNAL_CONTRACT

## Назначение

Engine journal фиксирует воспроизводимый журнал задач для `engine` и ответов `engine`.

Английский alias для внешних ссылок: `reproducible engine journal`.

Цель журнала — сделать историю проекта восстановимой по GitHub files: кто
сформулировал задачу, какой `engine` ее выполнил, какая ветка и Pull Request
получились, какие проверки были выполнены и какой следующий шаг рекомендован.

Engine journal не заменяет Git history, Pull Request, commits или
docs-maintainer reports. Он связывает их в одну читаемую цепочку:

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
  archive/
  input/
  output/
  templates/
```

## Область methodology repository и target transfer

`agent-system-development` является reusable methodology/template repository, но
его собственный journal имеет два разных режима.

**Target transfer mode (`journal_transfer_mode: scaffold_only`)**: в target
repository переносится только scaffold journal — `README.md`, структура папок,
шаблоны `templates/**` и пустой/target-specific `INDEX.md` с тем же форматом
таблицы. Operational rows, TASK/RESULT files, PR facts и local closure history из
methodology repository не копируются verbatim.

**Methodology operation mode**: когда задача меняет сам
`agent-system-development` и engine journal явно входит в allowed files/scope,
repository может хранить собственные TASK/RESULT/INDEX entries для
methodology-hardening, release-prep, state-refresh, review-gate и closure tasks.
Такая история является non-transferable operational history: она публична,
append-only, Russian-first, не содержит private downstream data/secrets и не
становится source/template для target repositories.

Reviewer не должен требовать пустые `input/` и `output/` в самом
`agent-system-development`, если существующие entries относятся к
methodology-hardening или release/state/review lifecycle этой methodology.
Правильная проверка — не пустота папок, а допустимый scope записей, отсутствие
private/secrets, Russian-first и запрет копирования operational rows в target.

## Вход и выход

`input/` содержит входные задачи для `engine`.

`output/` содержит ответы `engine` по этим задачам.

`templates/` содержит reusable templates для task/result files.

Task file и result file должны иметь одинаковый sequence number и task id, чтобы
их можно было сопоставить без внешнего контекста.

## Политика Russian-first journal

TASK/RESULT/INDEX files, user-facing labels, descriptions и final report должны быть на русском языке по `docs/agent-system/LANGUAGE_POLICY.md`.

Английский допустим только для technical identifiers, command names, flags, paths, filenames, branch names, config keys, API names, package names, vendor/tool names, SHA values и literal external names.

Commit subject/body и PR title/body также должны быть Russian-first по `docs/agent-system/LANGUAGE_POLICY.md` → «Commit и PR metadata». Перед push/PR `engine` запускает `python docs/agent-system/tools/validate_commit_message.py --base origin/developer` или получает тот же check через ready-gate. Если нарушение commit/PR metadata language случилось и не было безопасно исправлено до push, RESULT обязан зафиксировать нарушение, причину отказа от rewrite/force-push и следующий безопасный шаг. Уже pushed/merged commits не переписываются без отдельного явного решения архитектора.

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

## Journal Epoch и архивирование

Канон архивирования — `docs/agent-system/JOURNAL_ARCHIVING_POLICY.md`.

`Journal Epoch` — release-boundary интервал журнала, закрытый release
`vX.Y.Z`. После release, tag, sync и batch closure старые finalized RESULT могут
быть перемещены отдельным post-release archive PR:

```text
docs/agent-system/engine-journal/output/RESULT-....
docs/agent-system/engine-journal/archive/vX.Y.Z/RESULT-....
```

Это controlled exception к active journal surface, а не удаление истории:

- перенос выполняется только через `git mv`;
- archive RESULT остаются tracked files и доступны через GitHub;
- active `INDEX.md` оставляет epoch summary и ссылки на
  `engine-journal/archive/vX.Y.Z/INDEX.md`;
- open, ready-for-review, closure-pending, blocked или STOP RESULT не
  архивируются;
- archive files не входят в `orchestrator_context_bundle` и не генерируются в
  `docs/agent-system/cloud/**`.

Фактическое архивирование старых RESULT не выполняется обычным feature PR. Оно
делается отдельным post-release archive PR, когда release boundary известен и
архитектор подтвердил, что active journal стал слишком тяжелым для контекста.

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

Если TASK file содержит fenced YAML block `task_contract`, он является source of truth для mode/scope/checks/STOP по `docs/agent-system/TASK_CONTRACT.md`. RESULT должен фиксировать результат `validate_task_contract.py`, если validation запускалась, и результат `validate_commit_message.py` для work PR. Если нарушение task contract или commit/PR metadata language случилось и его нельзя безопасно исправить до push без rewrite/force-push, RESULT фиксирует нарушение, причину и следующий безопасный шаг; уже pushed/merged history не переписывается без отдельного явного решения архитектора.

Для новых file-changing задач RESULT должен включать `self_review_before_pr` по `docs/agent-system/QUALITY_FIRST_WORKFLOW.md`: acceptance criteria, diff scope, generated artifacts, journal finalization, PR body quality и safety checked. Если self-review не прошёл, PR не открывать.

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
- logs с sensitive values.

Sensitive checks в journal result должны фиксировать только безопасный summary:
filenames, counts, categories и status. Matching lines, secret values, headers,
cookies, credentials и другие values нельзя копировать в journal.

## Adoption target repository

При adoption target repository должен получить собственный `docs/agent-system/engine-journal/`.

Target repository journal хранит project-specific task/result history внутри target repository, а не в public methodology repository.

Target adoption использует `journal_transfer_mode: scaffold_only`: переносит
структуру, README, templates и формат `INDEX.md`, но не переносит operational
rows, TASK/RESULT files или archive epochs из methodology repository. Если target
уже содержит свой journal, adoption/update сохраняет target-specific history и
не затирает её историей source methodology.

Первый adoption/audit PR должен создавать или обновлять:

- `docs/agent-system/engine-journal/README.md`;
- `docs/agent-system/engine-journal/INDEX.md`;
- `docs/agent-system/engine-journal/input/`;
- `docs/agent-system/engine-journal/output/`;
- `docs/agent-system/engine-journal/templates/`;
- task file для первой engine-задачи;
- result file для ответа engine.

Если первый шаг adoption остается `audit-only`, task/result files допускаются
как journal artifacts рядом с `docs/agent-system/ADOPTION_AUDIT.md`, потому что
они описывают выполнение audit, а не переносят full methodology state.

Adoption переносит только scaffold/templates и формат `INDEX.md`. Первая target
adoption/audit task создает target-specific task/result files и target-specific
записи `INDEX.md`.

Если `INDEX.md` используется как reusable source, переносится структура таблицы,
заголовки и правила заполнения. Operational rows methodology repository
(`METH-*`, PR history, local closure facts) не копируются verbatim в target
repository.

Methodology repository operational history не переносится.

Archive epochs methodology repository не переносится. Target repository создает
собственные archive epochs только по своей target-specific истории.

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

## Обязательные feedback-разделы RESULT

Новый finalized RESULT обязан содержать два раздела:

```text
## Methodology feedback
## Unprompted Project Proposals
```

Правила:

- если feedback или proposals отсутствуют, раздел остается в RESULT со значением
  `нет`;
- `Methodology feedback` фиксирует, что улучшить в методологии по итогам
  выполнения задачи;
- `Unprompted Project Proposals` фиксирует вне-scope идеи, риски или улучшения,
  которые нельзя выполнять внутри текущей задачи без отдельного allowed scope;
- предложения оформляются по `AGENT_INITIATIVE_PROTOCOL.md` и, при необходимости,
  по `templates/AGENT_PROPOSAL_TEMPLATE.md`;
- предложения из target repository перед переносом в public methodology
  repository проходят sanitization по `DOWNSTREAM_FEEDBACK_SANITIZATION_POLICY.md`;
- proposal не является approval на implementation и попадает в `BACKLOG.md` или
  `METHODOLOGY_IMPROVEMENT_LEDGER.md` только после architect/orchestrator triage.

Ready-gate проверяет наличие этих разделов в новых RESULT. Legacy RESULT до H12
не ретрофитятся и остаются historical/advisory.

### Head SHA без self-reference loop

В finalized RESULT поля `head_sha`, `reviewed_head_sha` и `final_head_sha` допустимы только когда в них записан точный SHA, а не текстовое обещание дописать значение. Если final PR head SHA меняется самим follow-up commit и не может быть встроен в этот же commit, RESULT использует явную source/policy-семантику:

- `pr_head_source: github_pr_metadata`;
- `reviewed_head_source: github_pr_metadata`;
- `final_pr_head_policy: final PR head SHA is not embedded in the same committed RESULT to avoid self-reference loop`;
- `pre_finalization_head_sha: <sha>`, если нужен исторический head до финализации.

Такой формат считается finalized, потому что GitHub PR metadata является источником факта, а RESULT не обещает будущую ручную подстановку SHA.

## Execution timestamps

Новые TASK/RESULT записи фиксируют execution-время и cost accounting по модели
`measured/reported/mixed`:

- `measured/engine` — значения, которые engine фиксирует автоматически или надежно по факту собственного запуска;
- `reported/human` — значения, которые сообщает человек или оркестратор;
- `mixed` — часть значений измерена, часть сообщена человеком.

TASK должен содержать:

- `Время начала выполнения (execution_started_at) [measured/engine]` в формате ISO 8601 с timezone;
- `Время оркестрации, по факту (orchestration_time_reported) [reported/human, опционально]`;
- `actor_type`, `role`, `time_source`, `time_report_confidence` для будущего
  RESULT, если задача создаёт или меняет journal artifacts.

RESULT должен содержать:

- `execution_started_at` в формате ISO 8601 с timezone;
- `execution_finished_at` в формате ISO 8601 с timezone;
- `execution_duration`, вычисленный из start/finish;
- `time_spent` в коротком формате для rollup (`45m`, `2.5h`, `PT2H30M`);
- `actor_type` (`human`, `agent`, `hybrid`);
- `role`;
- `time_source` (`measured`, `reported`, `mixed`);
- `time_report_confidence` (`high`, `medium`, `low`);
- `human_time_reported` (`duration` или `not_applicable`);
- cost-поля по `docs/agent-system/COST_TRACKING_POLICY.md`:
  `input_tokens`, `output_tokens`, `ai_cost_estimate`,
  `human_cost_estimate`, `total_task_cost`, `resource_cost`.

Дисциплина фиксации времени:

- `execution_started_at` фиксируется в начале engine-run до содержательных чтений,
  правок, проверок и repository-mutating действий;
- зафиксированное `execution_started_at` сохраняется в TASK как measured факт и
  при финализации RESULT переносится без пересчета и перезаписи;
- `execution_finished_at` фиксируется в конце выполнения, после финальных
  проверок и перед финальным отчетом;
- `execution_duration` вычисляется из `execution_started_at` и
  `execution_finished_at`, а не вводится как независимое ручное значение;
- если `execution_started_at` равен `execution_finished_at` или длительность
  выглядит нереалистично короткой для задачи с содержательным diff, reviewer или
  ready-gate фиксирует advisory finding `unreliable execution timing`.

Reviewer не получает отдельного поля времени внутри work-записи: review является отдельным engine-run со своим TASK/RESULT и собственными execution/accounting-полями. Merge-время не дублируется в execution-полях. Для ordinary PR source of truth по `merged_at` и merge commit SHA — GitHub PR metadata; closure-stamp в `RESULT` добавляется только при boundary reconciliation или explicit architect request по разделу «GitHub merge facts authority».

Правило не ретрофитится в append-only history: старые TASK/RESULT без
execution/accounting-полей не переписываются. Для новых finalized RESULT
отсутствие required accounting fields является blocker. Для legacy RESULT до H3
это advisory. Если `actor_type` равен `human` или `hybrid`, отсутствие
`human_time_reported` является blocker, кроме STOP/failure с заполненным
`time_report_missing_reason`.

`INDEX.md` содержит колонку `Time`: новые строки заполняют её из `time_spent`,
legacy-строки используют `legacy/advisory`.

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

Search aliases для checks: `PR URL authoritative`; `not a blocker`; `do not create closure solely`.

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
- safe one-line summary на русском языке.

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
- `ADOPTION_TRANSFER_MANIFEST.yml` фиксирует `journal_transfer_mode: scaffold_only`;
- существующие operational rows/TASK/RESULT относятся к methodology-hardening,
  release/state/review lifecycle самой methodology, а не к private downstream
  project history;
- operational rows/TASK/RESULT не содержат private downstream data, credentials,
  tokens, secret values или private repository URLs;
- TASK/RESULT/INDEX являются Russian-first, кроме technical identifiers и literal
  external names;
- reviewer не требует пустые `input/`/`output/` в methodology repository только
  из-за наличия легитимной non-transferable history;
- target adoption/update не копирует operational rows или TASK/RESULT files
  methodology repository verbatim.

### Проверка target repository

Перед merge PR reviewer должен проверить, что:

- task file и result file связаны одним sequence number;
- index обновлен;
- forbidden/private data не добавлены;
- task/result files не противоречат final report;
- RESULT содержит «Source Delta» по канону `docs/agent-system/templates/TASK_HEADER_COMMON.md` и этот блок согласован с фактическим diff;
- RESULT содержит context handoff по канону `docs/agent-system/templates/TASK_HEADER_COMMON.md`: numbered cloud-имена из `docs/agent-system/cloud/00_README.md`, только bundle-файлы, небандловые tooling/source-файлы не перечислены в context-load строке;
- новые finalized RESULT содержат required accounting fields по
  `TIME_ACCOUNTING_POLICY.md` и `COST_TRACKING_POLICY.md`: `execution_*`,
  `time_spent`, `actor_type`, `role`, `time_source`,
  `time_report_confidence`, `human_time_reported`, token/cost fields и
  `resource_cost`; отсутствие этих полей в новом RESULT является blocker,
  legacy-записи остаются advisory; равные start/finish или нереалистично
  короткая длительность при содержательном diff остаются advisory finding
  `unreliable execution timing`;
- новые finalized RESULT содержат `## Methodology feedback` и
  `## Unprompted Project Proposals`; отсутствие разделов является blocker, а
  значение `нет` допустимо;
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
