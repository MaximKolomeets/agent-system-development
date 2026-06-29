# TARGET_ADOPTION_DETECTOR

## Назначение

`TARGET_ADOPTION_DETECTOR` описывает reusable detector для выбора безопасного режима adoption target implementation repository перед переносом methodology layer.

Detector не выполняет adoption сам. Он собирает только безопасные structural facts target repository, классифицирует ситуацию как Variant A/B/C или STOP и выдаёт рекомендацию для следующей engine task.

## Когда применять

Применять перед:

- первым adoption methodology repository в target implementation repository;
- обновлением уже существующего `docs/agent-system/`;
- повторным запуском adoption после interrupted, partial или conflicting setup;
- подготовкой docs-only adoption task из stable source `main`, release tag или published Source/cloud snapshot.

Не применять как shortcut вокруг safety checks: dirty tree, private data risk, unstable methodology source или unclear branch model остаются STOP.

## Inputs

Detector принимает только нейтральные repository facts:

- repository root path;
- remote URL presence, без публикации private URL в public methodology output;
- current branch name;
- working tree status;
- наличие или отсутствие `docs/agent-system/`;
- наличие или отсутствие engine journal scaffold;
- наличие или отсутствие `ADOPTION_TRANSFER_MANIFEST.yml`;
- наличие или отсутствие `CURRENT_STATE.md`, `NEXT_STEPS.md`, `DECISION_LOG.md`;
- выбранный stable methodology source: `main`, release tag или published Source/cloud snapshot.

Detector не читает `.env`, secrets, key material, credentials, real data, customer data, raw logs или target-specific private content.

## Required checks

Минимальные проверки:

- repository root detected;
- remote URL detected;
- current branch detected;
- working tree clean;
- target repository is not main/protected branch with uncommitted changes;
- `docs/agent-system` exists or not;
- engine journal exists or not;
- `ADOPTION_TRANSFER_MANIFEST.yml` exists or not;
- `CURRENT_STATE`/`NEXT_STEPS`/`DECISION_LOG` exist or not;
- `methodology_reference` present and stable;
- branch model present: `main`/`developer`/`work/*` or documented target-specific alternative;
- local target modifications are not overwritten;
- private data / `.env` / secrets are not read;
- target-specific history is preserved;
- generated/cloud files are regenerated only after source changes;
- adoption source is stable `main`/tag/published snapshot, not methodology `developer` or `work/*` branch.

## Adoption modes

Detector выбирает один из режимов:

- Variant A - clean new adoption;
- Variant B - existing methodology layer update;
- Variant C - partial/broken/adversarial adoption;
- STOP - safety or ambiguity blocker before any adoption task.

`STOP` имеет приоритет над A/B/C. Если безопасная классификация невозможна, detector не должен угадывать.

## Variant A: clean new adoption

Условия:

- target repository не содержит `docs/agent-system/`;
- нет engine journal history target repository;
- working tree clean;
- branch model понятна;
- stable methodology source доступен.

Рекомендация:

- подготовить first adoption/audit task;
- начинать с audit-only или minimal docs-only bootstrap;
- создавать target-local state docs по фактам target repository;
- не копировать operational history methodology repository.

## Variant B: existing methodology layer update

Условия:

- target repository уже содержит `docs/agent-system/`;
- есть target-specific journal/history/state;
- working tree clean;
- stable methodology source доступен;
- локальные target-specific files можно сохранить без overwrite.

Рекомендация:

- подготовить scoped source-update task;
- preserve target-specific journal, history, state, decisions and branch facts;
- обновлять reusable methodology files from stable source;
- не перетирать `CURRENT_STATE.md`, `NEXT_STEPS.md`, `DECISION_LOG.md` verbatim из methodology repository.

## Variant C: partial/broken/adversarial adoption

Условия:

- `docs/agent-system/` существует частично;
- journal, manifest или state docs inconsistent;
- working tree dirty;
- branch model unclear;
- stable methodology source недоступен;
- есть риск overwrite target-specific history;
- target instructions конфликтуют с requested adoption mode.

Рекомендация:

- не выполнять adoption/update сразу;
- подготовить audit/fix task;
- зафиксировать blockers без private data;
- восстановить clean baseline, branch model и stable methodology reference до materialization.

## STOP conditions

Detector пишет `STOP`, если:

- working tree dirty и нет явно выбранного clean worktree;
- target repository на protected/main branch с uncommitted changes;
- нужно читать `.env`, secrets, tokens, key material или raw logs;
- нужно раскрыть private repository URL, customer data или project-private details;
- stable methodology source не `main`, release tag или published snapshot;
- adoption пытается использовать methodology `developer`, `work/*`, dirty local methodology tree или open methodology PR branch как source of truth;
- есть риск перезаписать target-specific journal/history/state;
- branch model нельзя безопасно определить;
- generated/cloud files предлагается менять без source change.

## Output recommendation format

Detector выдаёт recommendation в machine-readable YAML:

```yaml
adoption_recommendation:
  variant: A | B | C | STOP
  confidence: high | medium | low
  reasons:
    - ...
  required_preconditions:
    - ...
  allowed_next_task:
    - ...
  forbidden_actions:
    - ...
  stable_methodology_source:
    ref: main_or_tag
    tag: v1.4.0
```

Human explanation рядом с YAML должна быть Russian-first и не должна раскрывать private target details.

## Safety rules

- Detector не читает `.env`, secrets, tokens, key material, credentials, raw logs or private data.
- Detector не печатает matching secret/header values.
- Detector не переносит private downstream details в public methodology repository.
- Detector не меняет target repository.
- Detector не создает release/tag/merge.
- Detector не разрешает adoption от methodology `developer`, `work/*` или open methodology PR branch.
- Detector сохраняет target-specific journal/history/state and local instructions.
- Detector treats dirty target tree as STOP unless a separate clean worktree is explicitly selected.

## Examples

### Variant A

```yaml
adoption_recommendation:
  variant: A
  confidence: high
  reasons:
    - docs/agent-system layer is absent
    - working tree is clean
    - stable methodology source is available
  required_preconditions:
    - confirm target branch model
  allowed_next_task:
    - audit-only adoption task
  forbidden_actions:
    - copy methodology operational history
    - read .env or private data
  stable_methodology_source:
    ref: main_or_tag
    tag: v1.4.0
```

### Variant B

```yaml
adoption_recommendation:
  variant: B
  confidence: medium
  reasons:
    - docs/agent-system layer exists
    - target-specific journal must be preserved
  required_preconditions:
    - map reusable source files separately from target state files
  allowed_next_task:
    - scoped source-update task
  forbidden_actions:
    - overwrite target CURRENT_STATE/NEXT_STEPS/DECISION_LOG
  stable_methodology_source:
    ref: main_or_tag
    tag: v1.4.0
```

### Variant C

```yaml
adoption_recommendation:
  variant: C
  confidence: high
  reasons:
    - methodology layer is partial or inconsistent
    - branch model is unclear
  required_preconditions:
    - run audit/fix task before adoption
  allowed_next_task:
    - adoption audit and cleanup task
  forbidden_actions:
    - bulk copy methodology repository
    - overwrite target-specific history
  stable_methodology_source:
    ref: main_or_tag
    tag: v1.4.0
```

### STOP

```yaml
adoption_recommendation:
  variant: STOP
  confidence: high
  reasons:
    - working tree is dirty
    - stable methodology source is not confirmed
  required_preconditions:
    - restore or isolate clean target worktree
    - confirm main/tag methodology source
  allowed_next_task:
    - status-only blocker report
  forbidden_actions:
    - adoption from developer or work branch
    - read secrets or private data
  stable_methodology_source:
    ref: main_or_tag
    tag: v1.4.0
```
