# QUALITY_FIRST_WORKFLOW

## Назначение

`QUALITY_FIRST_WORKFLOW` задаёт обязательный quality bar для новых задач, которые меняют repository files, создают commit/push/PR, ведут journal или запускают review/fix-pass flow.

Цель workflow - чтобы engine до открытия PR доказал, что понял задачу, не расширил scope, закрыл acceptance criteria, сам проверил результат и не переложил на reviewer очевидный операционный шум.

Workflow не заменяет `TASK_CONTRACT`, `REVIEW_AUTOLOOP`, `SEMANTIC_COMPLETENESS_GATES`, `JOURNAL_FINALIZATION_POLICY` и readiness tooling. Он связывает их в pre-PR quality gate.

Workflow также не заменяет `EXTERNAL_REVIEW_LEDGER_PATTERN.md`. Если один
документ или решение проходит много external human review rounds, ledger
консолидирует `applied`/`deferred`/`rejected` предложения и фиксирует anti-loop
/ diminishing-returns stop, чтобы quality-first не превращался в бесконечную
полировку.

## Quality bar перед началом задачи

Перед началом file-changing задачи engine проверяет:

- цель задачи понятна и проверяема;
- non-goals явно отделены от scope;
- allowed files и forbidden files заданы;
- acceptance criteria перечисляют наблюдаемые результаты;
- checks и safety rules заданы;
- expected reviewer mode задан;
- stop conditions заданы;
- expected final report format задан;
- task можно выполнить без контекста, оставленного только в surrounding chat.

Если этих полей нет, engine пишет `STOP` и просит уточнение у архитектора, кроме простых консультационных задач без write-action, PR и journal trace.

## Definition of Ready для task prompt

Task prompt считается ready только если содержит:

- цель;
- non-goals;
- allowed files;
- forbidden files;
- acceptance criteria;
- checks;
- safety rules;
- expected reviewer mode;
- stop conditions;
- expected final report format.

Для задач с `task_contract` prose и contract должны совпадать по mode, scope, checks и STOP. Если conflict найден, engine не выбирает более удобную версию, а пишет `STOP`.

## Definition of Done перед PR

PR можно открывать только если:

- все acceptance criteria проверены и закрыты;
- diff соответствует allowed files;
- forbidden files не менялись;
- state docs согласованы с фактическим diff;
- RESULT и INDEX финализированы настолько, насколько возможно до PR creation;
- generated/cloud artifacts обновлены после source changes;
- required checks прошли или blocker явно зафиксирован;
- safety summary count-only/filename-only, без matching secret/header values;
- next step не противоречит branch, release и closure policy.

Если хотя бы один пункт не выполнен, PR не открывать; либо выполнить bounded fix в рамках scope, либо написать `STOP`.

## Mandatory self-review перед PR

Перед открытием PR engine обязан выполнить self-review:

- перечитать собственный diff;
- сверить diff с allowed files;
- сверить каждый acceptance criterion;
- проверить state docs;
- проверить journal RESULT;
- проверить generated/cloud;
- проверить PR body на control characters, placeholder wording и обещания вне diff;
- проверить, что next step не противоречит branch/release policy.

В RESULT добавить блок:

```markdown
## self_review_before_pr

- acceptance_criteria_checked: yes
- diff_scope_checked: yes
- generated_artifacts_checked: yes
- journal_finalization_checked: yes
- pr_body_quality_checked: yes
- safety_checked: yes
```

Если self-review не прошёл, PR не открывать.

## Reviewer focus после quality-first

После quality-first reviewer не должен заново делать полный аудит всего проекта, если задача scoped.

Reviewer проверяет:

- смысл задачи;
- безопасность scope;
- соответствие acceptance criteria;
- нет ли скрытого расширения;
- нет ли противоречий методологии;
- действительно ли self-review не формальный;
- не появились ли target-specific/private details, если задача публичная methodology task.

Если PR body, RESULT или state docs содержат операционный шум, placeholders, control characters или обещания вне diff, reviewer может классифицировать это как blocker.

## Fix-pass policy

Если reviewer нашёл blocker, engine fix-pass закрывает конкретные blocker IDs, а не делает общий cleanup.

Если замечание пришло из external review ledger и уже имеет disposition
`applied`, `deferred` или `rejected`, оно не должно повторно превращаться в
blocker без новой critical category из `EXTERNAL_REVIEW_LEDGER_PATTERN.md`.

Формат:

```yaml
fix_pass:
  blocker_id: B-01
  status: fixed
  changed_files:
    - ...
  verification:
    - ...
```

Fix-pass не расширяет scope, не добавляет unrelated refactor и не меняет release/tag/merge policy. Если blocker требует architectural decision, private data access, forbidden path или destructive action, engine пишет `STOP`.

## STOP-or-ACT rules

| Situation | Action |
| --- | --- |
| dirty tree before task | STOP |
| file outside allowlist | STOP |
| generated/cloud drift after source change | ACT, regenerate and report |
| EOL-only generated noise | ACT only if safe and bounded |
| unknown private data risk | STOP |
| missing acceptance criteria | STOP |
| reviewer found machine-only blocker | fix-pass with blocker ID |
| reviewer found semantic blocker | fix-pass + explain design decision |

`ACT` означает bounded действие внутри текущего allowed scope с последующим report. `STOP` означает не выполнять изменение и запросить решение архитектора.

## Decision cache

Повторяющиеся решения не спрашивать заново, если они уже зафиксированы в methodology и текущая ситуация совпадает с каноном.

Первые cached decisions:

- no ordinary post-merge closure PR;
- GitHub PR metadata is merge facts source;
- stable methodology source is main/tag;
- dirty tree means STOP;
- target adoption starts with detector recommendation;
- reviewer output should use blocker IDs;
- release/tag are human-only.

Decision cache не разрешает bypass архитектора для risky operations: force-push/rewrite, destructive cleanup, branch protection changes, runtime/Docker/CI changes, private data access, secrets access или target adoption без stable source.

## PR body quality

PR body должен:

- кратко описывать фактический diff;
- не обещать implementation, checks или adoption, которых нет;
- содержать checks summary;
- содержать safety summary;
- не содержать control characters;
- не содержать deferred placeholders;
- не раскрывать private data, secret/header values, private repository identity или target-specific facts вне scope.

Если PR body создавался через shell или временный файл, engine должен перечитать PR body после создания или обновления PR и исправить artifacts вроде BOM, control characters или broken quoting до финального RESULT.

## Examples

Плохо:

```text
Сделать качественно.
```

Хорошо:

```text
- created TARGET_ADOPTION_DETECTOR.md;
- Variant A/B/C/STOP documented;
- dirty target tree leads to STOP;
- adoption from developer/work branch forbidden;
- target-specific journal/history preserved;
- check_task_ready passed.
```

Пример self-review summary:

```markdown
## self_review_before_pr

- acceptance_criteria_checked: yes
- diff_scope_checked: yes
- generated_artifacts_checked: yes
- journal_finalization_checked: yes
- pr_body_quality_checked: yes
- safety_checked: yes
```

## Передача

Следующий: engine - применять quality-first workflow перед открытием каждого file-changing PR; reviewer - проверять смысловые риски и реальность self-review вместо повторной очистки операционного шума.
