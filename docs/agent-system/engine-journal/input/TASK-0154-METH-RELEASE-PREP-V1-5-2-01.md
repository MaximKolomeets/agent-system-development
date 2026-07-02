# TASK: METH-RELEASE-PREP-V1-5-2-01

```yaml
task_contract:
  version: 1
  task_id: METH-RELEASE-PREP-V1-5-2-01
  role: methodology-architect-01
  mode: agent
  execution_mode: local_only
  reasoning_effort: high

  repository:
    full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    base_branch: developer
    working_branch: work/methodology-architect-01/meth-release-prep-v1-5-2-01

  methodology_reference:
    repository_full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    source_ref: origin/main
    stable_only: true
    source_commit: 2467edd8488a51d74483e8095e4887c0f512dfcd
    source_tag: v1.5.1
    release_tag: v1.5.1
    reference_type: stable_branch_head
    checked_at: 2026-07-03T00:42:55.0474643+07:00

  methodology_development_base:
    base_branch: developer
    working_branch: work/methodology-architect-01/meth-release-prep-v1-5-2-01
    base_commit: 97e874883afbe3ac38ccd815d48f63ca964c5737
    checked_at: 2026-07-03T00:42:55.0474643+07:00

  scope:
    allowed_files:
      - docs/agent-system/RELEASE_READINESS.md
      - docs/agent-system/CURRENT_STATE.md
      - docs/agent-system/NEXT_STEPS.md
      - docs/agent-system/RULESET_STATUS.md
      - docs/agent-system/PROJECT_FILE_MAP.md
      - docs/agent-system/cloud/**
      - docs/agent-system/engine-journal/INDEX.md
      - docs/agent-system/engine-journal/input/TASK-0154-METH-RELEASE-PREP-V1-5-2-01.md
      - docs/agent-system/engine-journal/output/RESULT-0138-METH-POST-RELEASE-STATE-REFRESH-V1-5-2-PR1-01.md
      - docs/agent-system/engine-journal/output/RESULT-0139-METH-JOURNAL-HISTORY-SCOPE-CLARITY-01.md
      - docs/agent-system/engine-journal/output/RESULT-0140-METH-TIME-COST-ACCOUNTING-HARD-GATE-01.md
      - docs/agent-system/engine-journal/output/RESULT-0141-METH-STABLE-REFERENCE-SCHEMA-SYNC-01.md
      - docs/agent-system/engine-journal/output/RESULT-0153-METH-BATCH-CLOSURE-0142-0152-V1-5-2-01.md
      - docs/agent-system/engine-journal/output/RESULT-0154-METH-RELEASE-PREP-V1-5-2-01.md
    forbidden_files:
      - .env
      - .env.*
      - .venv/**
      - data/**
      - runtime/**
      - dist/**
      - backups/**
      - exports/**
      - credentials
      - tokens
      - access key material
      - real passwords
      - private repository URLs
      - private downstream project names
      - client/customer data
      - production/runtime data
      - main direct changes
      - developer direct changes

  policies:
    journal: required
    cloud_regen: required
    generated_checks: conditional
    review: scoped_semantic
    merge: human_only
    closure_pr: false
    post_merge_closure: boundary_only
    boundary_reconciliation: release_or_audit_only
    language: russian_first

  checks:
    required:
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0154-METH-RELEASE-PREP-V1-5-2-01.md
      - python docs/agent-system/tools/validate_policy_invariants.py
      - python docs/agent-system/tools/russian_first_lint.py
      - python docs/agent-system/tools/check_task_ready.py --base origin/developer
      - python docs/agent-system/tools/generated_eol_guard.py --base origin/developer
      - python docs/agent-system/tools/gen_file_map.py --check
      - python docs/agent-system/tools/gen_cloud_bundle.py --check
      - python docs/agent-system/tools/validate_commit_message.py --base origin/developer
      - git diff --check origin/developer...HEAD

  stop_conditions:
    - dirty_tree_before_start
    - current_branch_is_main_or_developer_with_changes
    - changed_file_outside_allowlist
    - forbidden_path_changed
    - secret_or_env_risk
    - destructive_git_needed
    - branch_protection_change_needed
    - release_pr_or_tag_or_publish_or_sync_needed
```

Файл задачи: `docs/agent-system/engine-journal/input/TASK-0154-METH-RELEASE-PREP-V1-5-2-01.md`

Идентификатор задачи: `METH-RELEASE-PREP-V1-5-2-01`

Номер sequence: `0154`

Создано: `2026-07-03T00:42:55.0474643+07:00`

Время начала выполнения (execution_started_at) [measured/engine]: `2026-07-03T00:42:55.0474643+07:00`

Время оркестрации, по факту (orchestration_time_reported) [reported/human, опционально]: `not_reported`

actor_type: `agent`

role: `methodology-architect-01`

time_source: `measured`

time_report_confidence: `medium`

Автор: пользователь-архитектор

Target repository: `MaximKolomeets/agent-system-development`

Methodology repository: `MaximKolomeets/agent-system-development`

Агент: `methodology-architect-01`

Engine: на усмотрение архитектора

Рекомендуемый режим исполнения:

- launch mode / запуск: task-file-handoff
- model / модель: на усмотрение архитектора
- reasoning: high
- execution mode / режим: docs+tool release-prep
- why this mode is required / почему: release-prep затрагивает release snapshot,
  state docs, generated bundle, journal reconciliation и ready-gate перед
  human-only release PR.

Режим источника задачи: `copy-paste`

Task source commit SHA: `97e874883afbe3ac38ccd815d48f63ca964c5737`

Task file blob SHA: `not_embedded_self_reference_loop`

Ссылка на bootstrap prompt: not_applicable

Примечание об источнике правды: этот TASK file является источником правды для
release-prep v1.5.2; surrounding chat не требуется для выполнения.

Base branch: `developer`

Working branch: `work/methodology-architect-01/meth-release-prep-v1-5-2-01`

Verified Baseline:

- checked repository: `MaximKolomeets/agent-system-development`
- local path, если применимо: `C:\neural\repos\agent-system-development`
- checked base branch: `developer`
- working branch: `work/methodology-architect-01/meth-release-prep-v1-5-2-01`
- checked branch state: clean working tree before changes
- latest relevant PR numbers/statuses, если применимо: PR #306-#309, #311-#322 merged
- latest relevant merged PR, если применимо: PR #322 merged at `2026-07-02T17:37:05Z`
- release PR status, если применимо: not_created_for_v1.5.2
- sync PR status, если применимо: not_applicable_before_release
- latest known merge commit SHA, если доступен: `97e874883afbe3ac38ccd815d48f63ca964c5737`
- open PR state, если relevant: not_applicable_at_task_start
- baseline verification source: `git fetch`, local git refs, `gh pr view`, `gh api rulesets`
- baseline verification date/time: `2026-07-03T00:42:55+07:00`

Проверка полноты copy/paste:

- [x] This TASK/Engine block can be executed without reading surrounding chat text.
- [x] Блок «Рекомендуемый режим исполнения» включён.
- [x] Execution accounting включен: `execution_started_at`, `actor_type`,
  `role`, `time_source`, `time_report_confidence`; `orchestration_time_reported`
  заполнен или оставлен пустым как optional.
- [x] Verified baseline is included or explicitly marked as not applicable.
- [x] Repository/base branch/working branch are included.
- [x] Allowed files are included.
- [x] Forbidden files are included.
- [x] Checks are included.
- [x] STOP conditions are included.
- [x] Final report requirements are included.
- [x] No required execution context exists only in surrounding chat.

Правило языка:

Все ответы, target-local docs, TASK/RESULT/INDEX и комментарии в файлах писать
на русском языке. English допускается только для technical identifiers, command
names, flags, paths, filenames, branch names, config keys, API names, package
names, vendor/tool names и literal external names.

Разрешенные файлы:

- `docs/agent-system/RELEASE_READINESS.md`
- `docs/agent-system/CURRENT_STATE.md`
- `docs/agent-system/NEXT_STEPS.md`
- `docs/agent-system/RULESET_STATUS.md`
- `docs/agent-system/PROJECT_FILE_MAP.md`
- `docs/agent-system/cloud/**`
- `docs/agent-system/engine-journal/INDEX.md`
- `docs/agent-system/engine-journal/input/TASK-0154-METH-RELEASE-PREP-V1-5-2-01.md`
- `docs/agent-system/engine-journal/output/RESULT-0138-METH-POST-RELEASE-STATE-REFRESH-V1-5-2-PR1-01.md`
- `docs/agent-system/engine-journal/output/RESULT-0139-METH-JOURNAL-HISTORY-SCOPE-CLARITY-01.md`
- `docs/agent-system/engine-journal/output/RESULT-0140-METH-TIME-COST-ACCOUNTING-HARD-GATE-01.md`
- `docs/agent-system/engine-journal/output/RESULT-0141-METH-STABLE-REFERENCE-SCHEMA-SYNC-01.md`
- `docs/agent-system/engine-journal/output/RESULT-0153-METH-BATCH-CLOSURE-0142-0152-V1-5-2-01.md`
- `docs/agent-system/engine-journal/output/RESULT-0154-METH-RELEASE-PREP-V1-5-2-01.md`

Запрещенные файлы:

- `.env`
- `.venv/`
- `data/`
- `runtime/`
- `dist/`
- `backups/`
- `exports/`
- credentials
- tokens
- private-key material
- real passwords
- private repository URLs
- private downstream project names
- client/customer data
- production/runtime data
- direct changes to `main`
- direct changes to `developer`

Цель:

Подготовить release-prep v1.5.2 после merge PR #322: обновить
`RELEASE_READINESS.md` на candidate `v1.5.2`, зафиксировать base `v1.5.1`,
candidate SHA, payload PR-1..15 / H1..H16, выполнить state-refresh
`CURRENT_STATE.md`/`NEXT_STEPS.md`/`RULESET_STATUS.md`, закрыть оставшиеся
boundary journal rows 0138-0141 и row 0153, регенерировать cloud bundle и
`PROJECT_FILE_MAP.md`, пройти полный ready-gate.

Контекст:

- `origin/main` и tag `v1.5.1` указывают на
  `2467edd8488a51d74483e8095e4887c0f512dfcd`.
- `origin/developer` после PR #322 указывает на
  `97e874883afbe3ac38ccd815d48f63ca964c5737`.
- Payload `v1.5.2`: PR #306-#309 и #311-#321.
- Batch-closure prerequisite: PR #322 merged at `2026-07-02T17:37:05Z`.
- Release PR `developer -> main`, tag `v1.5.2`, publication и sync являются
  human-only действиями и не входят в эту задачу.

Preflight:

BEGIN POWERSHELL
git rev-parse --show-toplevel
git remote -v
git branch --show-current
git status --short
git rev-parse origin/main
git rev-parse origin/developer
git rev-parse 'v1.5.1^{}'
gh pr view 322 --repo MaximKolomeets/agent-system-development --json number,state,mergedAt,mergeCommit,url,headRefName,baseRefName,title
END POWERSHELL

STOP-условия:

- working tree dirty before changes;
- pull fast-forward impossible;
- PR #322 is not merged;
- `origin/developer` is not `97e874883afbe3ac38ccd815d48f63ca964c5737` at baseline;
- `v1.5.1` tag target differs from `2467edd8488a51d74483e8095e4887c0f512dfcd`;
- forbidden files detected;
- private data or secrets required;
- scope expands beyond allowed files;
- target instructions conflict with Russian-first policy and user did not explicitly allow another language;
- task would require merge/tag/publish/sync/branch-protection changes by agent.

Проверки:

BEGIN POWERSHELL
python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0154-METH-RELEASE-PREP-V1-5-2-01.md
python docs/agent-system/tools/validate_policy_invariants.py
python docs/agent-system/tools/russian_first_lint.py
python docs/agent-system/tools/check_task_ready.py --base origin/developer
python docs/agent-system/tools/generated_eol_guard.py --base origin/developer
python docs/agent-system/tools/gen_file_map.py --check
python docs/agent-system/tools/gen_cloud_bundle.py --check
python docs/agent-system/tools/validate_commit_message.py --base origin/developer
git diff --check origin/developer...HEAD
END POWERSHELL

Commit policy:

- Коммитить только из `work/methodology-architect-01/meth-release-prep-v1-5-2-01`.
- Перед commit проверить `git branch --show-current`.
- Commit message должен соблюдать Russian-first metadata policy и allowed scope.

PR policy:

- Открыть один PR в `developer`.
- PR body должен содержать summary, checks, safety, release authority note,
  Source Delta и next step.
- Не создавать release PR `developer -> main` в рамках этой задачи.

Post-merge journal closure policy:

- после merge рабочего PR зафиксировать PR status `merged`, merge commit SHA и
  `merged_at`, если доступно;
- если выполнялся release PR в `main`, зафиксировать release PR URL/status/merge
  commit SHA/`merged_at`;
- если выполнялся sync PR `main -> developer`, зафиксировать sync PR URL/status/
  merge commit SHA/`merged_at`;
- после merge `RESULT closed after merge: yes`, `INDEX closed after merge: yes`
  и `No journal placeholders: yes`;
- не оставлять после merge final states `PR open`, `ready for review`,
  `draft open`, `file materialization incomplete` или `see Engine final report`.

Post-merge closure checklist:

- [ ] Проверить GitHub/local state work PR.
- [ ] Проверить release PR, если release использовался.
- [ ] Проверить sync PR, если sync использовался.
- [ ] Проверить, что RESULT/INDEX не остались в pre-merge state.
- [ ] Ограничить allowed files минимально: RESULT, INDEX и безопасные state docs.
- [ ] Не менять runtime, Docker, CI, secrets, private data или downstream-specific details.

Ожидаемый RESULT file:

`docs/agent-system/engine-journal/output/RESULT-0154-METH-RELEASE-PREP-V1-5-2-01.md`

Требования к final report:

- branch;
- commit SHA;
- PR URL;
- changed files;
- checks run;
- checks not run and why;
- forbidden files result;
- sensitive/private marker result;
- language policy result;
- risks;
- result file finalized;
- index entry finalized;
- time_spent;
- human_time_reported, если `actor_type` = `human` или `hybrid`;
- token/cost fields;
- no journal placeholders;
- статус PR после review (`PR status after review`);
- merge commit SHA после merge, если доступен;
- `merged_at` date/time, если доступно;
- release PR URL/status/merge commit SHA/`merged_at`, если release выполнялся;
- sync PR URL/status/merge commit SHA/`merged_at`, если sync выполнялся;
- RESULT закрыт после merge;
- INDEX закрыт после merge;
- проверка Post-merge Journal Closure;
- stale pre-merge status check result;
- follow-up commit SHA if finalization required;
- Source Delta;
- next recommended step;
- блок `Передача`.
