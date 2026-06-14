# ADOPTION_AUDIT_TASK_TEMPLATE

## Mandatory header

```text
Задача для <agent-name>: <task-id>

Рекомендуемый режим <engine-name>:

Запуск: <Local only | Cloud allowed | Hybrid>
Модель: <model recommendation>
Reasoning: <Low | Medium | High>
Режим: <Agent | Ask | Manual review>
Почему: <краткое обоснование выбора режима>
```

Задача формулируется на русском языке. `<task-id>` должен быть связан с GitHub issue, Pull Request, task id или внутренним номером работы проекта.

## Recommended Engine Mode

Заполнить блок `Рекомендуемый режим <engine-name>` в mandatory header: launch mode / запуск, model / модель, reasoning, execution mode / режим и why this mode is required / почему.

## Verified Baseline

- Repository:
- Local path, если применимо:
- Methodology repository:
- Methodology source branch:
- Methodology source commit:
- Methodology checked at:
- Repository lifecycle mode:
- Selected branch model:
- Developer branch existence:
- Fallback-to-main allowed:
- Base branch:
- Working branch:
- Checked branch state:
- Latest relevant PR numbers/statuses, если применимо:
- Release PR status, если применимо:
- Sync PR status, если применимо:
- Open PR state, если relevant:
- Verification source:
- Verification date/time:

## Copy/Paste Completeness Check

- [ ] This TASK/Engine block can be executed without reading surrounding chat text.
- [ ] Recommended Engine Mode is included.
- [ ] Verified baseline is included or explicitly marked as not applicable.
- [ ] Repository/base branch/working branch are included.
- [ ] Allowed files are included.
- [ ] Forbidden files are included.
- [ ] Checks are included.
- [ ] STOP conditions are included.
- [ ] Final report requirements are included.
- [ ] No required execution context exists only in surrounding chat.

## Task

`<task title>`

## Target repository

`<owner/repository>`

## Adoption mode

`audit-only`

## Base branch

`<main or target base branch>`

## Working branch

`work/<role>/<task>`

## Role

`docs-maintainer-01`

## Goal

Использовать только engine journal scaffold/templates из methodology repository. Не копировать methodology operational history. Audit создает target-specific task/result files и target-specific index entry.

Выполнить repository self-discovery, проверить language consistency и создать только `docs/agent-system/ADOPTION_AUDIT.md` plus engine journal artifacts для этой audit-задачи.

Зафиксировать methodology reference, использованную для audit:

```yaml
methodology_reference:
  repository: MaximKolomeets/agent-system-development
  source_branch: <developer или явно заданная branch>
  source_commit: <commit-sha>
  checked_at: <ISO-8601 timestamp>
  reference_type: commit
  notes: <short Russian note>
```

Если `source_commit` получить нельзя, написать `STOP` или зафиксировать blocker и не считать audit ready-for-review.

Все ответы, target-local docs, TASK/RESULT/INDEX и комментарии в файлах писать на русском языке. Английский допустим только для команд, путей, branch names, filenames, config keys, API names, package names, vendor/tool names и code identifiers.

Если target `AGENTS.md` или эквивалентные target instructions еще не содержат Russian-first policy, зафиксировать это в audit и рекомендовать добавить правило в следующий adoption/update scope.

## Allowed files

- `docs/agent-system/ADOPTION_AUDIT.md`
- `docs/agent-system/engine-journal/README.md`
- `docs/agent-system/engine-journal/INDEX.md`
- `docs/agent-system/engine-journal/input/TASK-<SEQ>-<task-id>-<slug>.md`
- `docs/agent-system/engine-journal/output/RESULT-<SEQ>-<task-id>-<slug>.md`
- `docs/agent-system/engine-journal/templates/ENGINE_TASK_FILE_TEMPLATE.md`
- `docs/agent-system/engine-journal/templates/ENGINE_RESULT_FILE_TEMPLATE.md`

## Forbidden changes

- `AGENTS.md`
- `README.md`
- `.github/workflows/**`
- Docker files
- runtime code
- architecture docs
- Source mirror
- `.env`
- `.venv/`
- `data/`
- `runtime/`
- `dist/`
- `backups/`
- `exports/`

## Required preflight

- выполнить `ENGINE_SELF_DISCOVERY_CONTRACT.md`;
- прочитать local `AGENTS.md`;
- прочитать local `README.md`;
- прочитать local architecture/status docs, если есть;
- проверить working tree;
- если working tree dirty - использовать clean worktree или STOP;
- sensitive grep только filename-only.
- подготовить task file и expected result file по `ENGINE_JOURNAL_CONTRACT.md`.

## Output

Создать audit file с разделами:

- repository self-discovery;
- repository lifecycle mode;
- selected branch model;
- developer branch existence;
- fallback-to-main allowed: yes/no with reason;
- current project state;
- template repository summary;
- fit analysis;
- language consistency audit;
- список файлов с нерусскими governance descriptions;
- рекомендация по унификации языка;
- проверка скриптов, workflow и templates на достаточные русские комментарии для нужных строк/блоков;
- adoption recommendation;
- risks;
- open questions;
- Methodology feedback;
- нейтральный `Methodology repository improvement request`, если audit показал, что methodology repository нужно улучшить.

Создать journal artifacts:

- task file в `docs/agent-system/engine-journal/input/`;
- result file в `docs/agent-system/engine-journal/output/`;
- строку в `docs/agent-system/engine-journal/INDEX.md`.

Если audit-задача передана через Task File Handoff Mode, TASK file является source of truth, а result file должен зафиксировать task source commit SHA или blob SHA.

TASK и RESULT должны содержать `methodology_reference`.

После создания PR обновить target-specific `RESULT` и `INDEX` фактическими PR/commit/status/checks значениями.

После merge рабочего PR, release PR или sync PR выполнить Post-merge Journal Closure: обновить target-specific `RESULT` и `INDEX` статусом `merged`, merge commit SHA, release/sync PR данными при наличии, `RESULT closed after merge: yes`, `INDEX closed after merge: yes` и `No journal placeholders: yes`.

Выполнить placeholder scan journal files. Если placeholders остались, задачу нельзя считать ready-for-review.

Language consistency rule:

- все ответы, target-local docs, TASK/RESULT/INDEX и комментарии в файлах пишутся на русском языке;
- English allowed only for code identifiers, paths, commands, config keys, vendor/tool names, upstream package names, API names, branch names, filenames and literal external names;
- governance descriptions target repository должны быть Russian-first;
- mixed-language sections должны быть либо оправданы, либо рекомендованы к нормализации.

Methodology feedback не должен включать private downstream data, private repository URLs, client data, customer data, internal code names или secrets.

## Checks

- git status --short
- git branch --show-current
- git diff --check
- git ls-files
- forbidden tracked paths check
- sensitive grep filename-only
- language consistency audit
- commenting consistency audit
- methodology reference present with source commit SHA
- engine journal index/task/result consistency
- task-file-handoff metadata consistency, если режим использовался
- engine journal placeholder scan
- проверка Post-merge Journal Closure

## Final report

- final report на русском языке;
- working branch;
- repository lifecycle mode;
- selected branch model;
- developer branch existence;
- fallback-to-main allowed: yes/no with reason;
- engine task file;
- engine result file;
- created files;
- changed files;
- checks;
- forbidden tracked paths result;
- sensitive grep result без matching lines;
- language consistency result;
- commenting consistency result;
- methodology reference;
- RESULT finalized: yes/no;
- INDEX finalized: yes/no;
- No journal placeholders: yes/no;
- статус PR после review (`PR status after review`);
- merge commit SHA после merge, если доступен;
- release PR URL/status/merge commit SHA, если release выполнялся;
- sync PR URL/status/merge commit SHA, если sync выполнялся;
- RESULT закрыт после merge: yes/no/not applicable;
- INDEX закрыт после merge: yes/no/not applicable;
- проверка Post-merge Journal Closure;
- risks;
- Methodology feedback;
- Methodology repository improvement request, если есть;
- commit SHA;
- push status;
- PR link/number.
