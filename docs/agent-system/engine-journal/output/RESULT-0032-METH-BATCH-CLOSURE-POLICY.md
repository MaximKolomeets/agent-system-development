# RESULT-0032: METH-BATCH-CLOSURE-POLICY

## Summary

Batch-closure policy закреплена в каноне. Старые открытые записи 0027–0031 не закрывались: это ожидаемое batch-состояние до pre-release closure.

## Baseline

- Repository: `MaximKolomeets/agent-system-development`
- Local path: `C:\neural\repos\agent-system-development`
- Base branch: `developer`
- Working branch: `work/docs-maintainer-01/batch-closure-policy`
- Baseline SHA: `618b68429be7cc788335fa125aecdb789f561caf`
- Timestamp: `2026-06-21T11:49:12.0567039+07:00`

## Изменения по файлам

- `docs/agent-system/ENGINE_JOURNAL_CONTRACT.md`: старый strict post-merge closure заменён на `Closure policy`; default = batch; per-task closure ограничен исключениями; release/audit/explicit closure остаются строгими gates; review blocker-правила стали batch-aware.
- `docs/agent-system/templates/TASK_HEADER_COMMON.md`: добавлены batch-friendly handoff-формулировки и статусная развилка для closure-pending journal.
- `docs/agent-system/templates/CODE_REVIEW_TASK_TEMPLATE.md`: closure wording выровнен с batch policy; final report требует batch-friendly handoff, если применимо.
- `docs/agent-system/templates/CLOSURE_TASK_TEMPLATE.md`: добавлен role-agnostic шаблон per-task closure-only задачи.
- `docs/agent-system/templates/BATCH_CLOSURE_TASK_TEMPLATE.md`: добавлен role-agnostic шаблон pre-release batch-closure задачи.
- `docs/agent-system/BRANCH_POLICY.md`: добавлен release-gate: release `developer -> main` запрещён до полного закрытия journal.
- `docs/agent-system/engine-journal/input/TASK-0032-METH-BATCH-CLOSURE-POLICY.md`: создана входная запись задачи.
- `docs/agent-system/engine-journal/output/RESULT-0032-METH-BATCH-CLOSURE-POLICY.md`: создан RESULT этой задачи.
- `docs/agent-system/engine-journal/INDEX.md`: добавлена строка 0032.

## PR / branch

- Branch: `work/docs-maintainer-01/batch-closure-policy`
- PR URL: `https://github.com/MaximKolomeets/agent-system-development/pull/168`
- PR status: `OPEN`
- Primary commit SHA: `24db5b05df95719362b03a28b247fe7dd28f517c`
- Head SHA at PR creation: `24db5b05df95719362b03a28b247fe7dd28f517c`
- Actual/current PR head SHA after journal finalization push: см. final report; не фиксируется внутри self-referential commit.
- Mergeable at PR creation check: `MERGEABLE`

## Проверки

- `rg -n "Post-merge Journal Closure|закрывается после merge|строго после merge|не должна оставаться в pre-merge" ...`: 0 совпадений.
- `rg -n -i "chatgpt|codex|claude|gpt|gemini|copilot|<engine-name>|Модель:" docs/agent-system/templates/CLOSURE_TASK_TEMPLATE.md docs/agent-system/templates/BATCH_CLOSURE_TASK_TEMPLATE.md`: 0 совпадений.
- `git diff --check`: passed.
- `git diff --name-only` + `git ls-files --others --exclude-standard`: только whitelist.
- branch-guard before commit: `work/docs-maintainer-01/batch-closure-policy`.

## FIX-01: reconcile strict-closure wording

- Review finding: активные шаблоны/контракты вне `engine-journal` всё ещё требовали immediate post-merge closure как общее правило.
- Baseline SHA before fix: `af1730dfd39587da6545aeb674e1da4e6163c111`
- FIX-01 timestamp: `2026-06-21T14:39:40.5452718+07:00`

| Файл | Трактовка | Действие |
| --- | --- | --- |
| `docs/agent-system/ENGINE_JOURNAL_CONTRACT.md` | check-F scope | Добавлена scope-клауза: проверка применяется к operational rules/templates/checklists; append-only journal, decision log, dated state snapshots и sync reports сохраняют historical literals. |
| `docs/agent-system/TASK_FILE_HANDOFF_CONTRACT.md` | batch-развилка | Общий контракт переведён на Closure policy; `merged; closure pending` допустим до batch-closure перед release; per-task closure только для исключений канона. |
| `docs/agent-system/ORCHESTRATOR_RESPONSE_STANDARD.md` | batch-развилка | Общее поведение оркестратора переведено на batch-default vs per-task exceptions; immediate closure больше не универсальное правило. |
| `docs/agent-system/templates/ORCHESTRATOR_RESPONSE_TEMPLATE.md` | batch-развилка | Engine-блоки теперь требуют Closure policy: batch перед release по умолчанию, per-task только для исключений. |
| `docs/agent-system/templates/DEVELOPMENT_TASK_TEMPLATE.md` | batch-развилка | Development-шаблон заменил post-merge closure wording на статус Closure policy (`closed`/`closure pending until batch before release`/`not applicable`). |
| `docs/agent-system/METHODOLOGY_FEEDBACK_LOOP.md` | batch-развилка | Feedback rule различает допустимое `closure pending` и нарушение под release/audit/adoption/series-end/explicit closure gate. |
| `docs/agent-system/MANUAL_REVIEW_CHECKLIST.md` | batch-развилка | Review checklist больше не считает любой merged-but-open journal blocker; blocker только под gates/исключениями. |
| `docs/agent-system/NEXT_STEPS.md` | batch-развилка | Живые операционные правила обновлены на Closure policy; stale cleanup создаётся только при per-task exception или release gate. |
| `docs/agent-system/templates/ADOPTION_PROMPT.md` | per-task исключение | Adoption/source-update явно оформлен как per-task closure exception; обычные work PR остаются batch-default. |
| `docs/agent-system/templates/DOCS_ONLY_ADOPTION_TASK_TEMPLATE.md` | per-task исключение | Docs-only adoption/source-update сохранён как per-task closure exception со ссылкой на Closure policy. |
| `docs/agent-system/templates/ADOPTION_AUDIT_TASK_TEMPLATE.md` | per-task исключение | Adoption audit оформлен как `audit/consistency-gate` и `adoption/source-update` per-task closure exception. |
| `docs/agent-system/templates/TARGET_REPOSITORY_BOOTSTRAP_TASK_TEMPLATE.md` | per-task исключение | Bootstrap/adoption handoff оформлен как per-task closure exception; обычные post-bootstrap work PR — batch-default. |
| `docs/agent-system/templates/NEW_PROJECT_PROMPT.md` | batch-развилка | Project chat prompt переведён на Closure policy: batch-default и per-task exceptions. |
| `docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml` | active rule, batch-развилка | Manifest policy/acceptance/governance строки переведены на Closure policy; release/sync остаются gate для полного closure. |
| `docs/agent-system/CURRENT_STATE.md` | history/state исключён | Не тронут: найденные строки описывают dated state snapshot PR-2x, а не новое действующее правило. |
| `docs/agent-system/DECISION_LOG.md` | history исключён | Не тронут: decision log сохраняет literal прошлого решения по scope-клаузе. |
| `docs/agent-system/agents/docs-maintainer-01/DOC_SYNC_REPORT.md` | history/sync-report исключён | Не тронут: docs-maintainer sync report сохраняет historical literal по scope-клаузе. |

- `INDEX.md`: не менялся; запись 0032 остаётся open по batch-policy и уже финализирована после PR creation.

## Риски

- Нужно проверить reviewer'ом, что новый batch-default не противоречит strict release-gate и audit consistency gate.

## Source-reminder

Обновить Source-снапшот у зарегистрированных потребителей: по `docs/agent-system/SOURCE_CONSUMERS.md`.

## Передача

Следующий: reviewer — review PR; затем архитектор — merge; затем engine — pre-release BATCH-CLOSURE по 0027…0032; затем release dev→main.

## Batch-closure stamp

- Closure mode: pre-release batch-closure.
- Work PR: https://github.com/MaximKolomeets/agent-system-development/pull/168
- Work PR state: `MERGED`
- Work PR mergedAt: `2026-06-21T07:50:48Z`
- Work PR merge commit SHA: `7e8d237f463ebe6eb0b7b56bd5b7cba8cc20437f`
- Final head SHA: `87fe0388765c43346cc9a245f4c1f3a847f2e9da`
- RESULT closed after merge: yes
- INDEX closed after merge: yes
- No journal placeholders: yes
- Closure source: `gh pr view 168 --json number,url,state,mergedAt,mergeCommit,headRefOid`
- Closed by: batch-closure journal 0033.
