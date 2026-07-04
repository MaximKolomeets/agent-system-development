# CI_POLICY

## Назначение

CI — автоматический guardrail для public methodology repository.

Первый CI-check блокирует запрещённые tracked files и paths до merge. CI не
заменяет review, ручные проверки или repository rulesets.

Workflow `Methodology checks` запускается на PR в `developer` и на push в
`work/**`. Он оборачивает существующие локальные валидаторы и добавляет только
узкие self-enforcement checks:

- changed TASK files проходят `validate_task_contract.py`;
- PR branch проходит `check_task_ready.py --base <base>`;
- policy invariants, generated EOL guard, `gen_file_map.py --check` и
  `gen_cloud_bundle.py --check` должны проходить без drift;
- `validate_commit_message.py` проверяет commit metadata, conventional subject
  prefix, Russian-first subject/body и длину строк тела;
- `check_journal_append_only.py` запрещает удаление или удаление строк в уже
  существующих TASK/RESULT journal artifacts.

CI output должен оставаться filename/count/code oriented: не печатать matching
lines, secret values, `.env` contents или private data. English identifiers,
paths, branch names, config keys, API/package names и literal external names не
являются нарушением Russian-first policy.

Commit metadata enforcement является обязательным gate для будущих work PR:
локально его выполняет `python docs/agent-system/tools/validate_commit_message.py
--base origin/developer`, а при включении GitHub Actions check должен называться
`ci/commit-message`. Check читает только git commit metadata, не читает diff и
не печатает содержимое changed files.

`validate_commit_message.py` по умолчанию строит диапазон через
`git rev-list --no-merges`, чтобы generated GitHub merge commits не блокировали
методологический gate. Для обычного work PR gate остаётся строгим: non-merge
commit с некорректным subject/body должен давать красный результат.
Проверка тела commit является узкой эвристикой: fenced-блоки, списки, таблицы,
paths и identifiers пропускаются, а очевидная английская prose получает
`BODY_NOT_RUSSIAN_FIRST`.

Проверка policy-инвариантов является частью локального ready-gate:
`check_task_ready.py` запускает `validate_policy_invariants.py`, который
проверяет сквозные полномочия release/tag, branch-модель, учет времени/стоимости,
source reference, privacy и target adoption markers, а также self-test
существования source/template/generated paths и локальных Markdown links.
Validator остаётся lightweight: он печатает только filenames, номера строк,
issue codes и path/category details, не matching lines и не values.

На release boundary `developer -> main` `check_task_ready.py --release-boundary`
не запускает commit-message range check без явного cutoff, потому историческая
до-гейтовая история и GitHub merge commits не переписываются. Если требуется
проверить только пост-гейтовую часть release payload, запускать:

```bash
python docs/agent-system/tools/check_task_ready.py --base origin/main --release-boundary --commit-message-cutoff-ref <release-tag-or-cutoff-ref>
```

## Target adaptation

Target repository, который принимает методологию, должен включить Russian-first
commit-language enforcement как часть своих локальных checks. Для docs-only
adoption это фиксируется как обязательное требование и review checklist item; при
runtime/CI-adoption target repository заводит собственный CI-check, который
переиспользует существующие tools methodology source set:
`validate_commit_message.py` и/или `russian_first_lint.py`.

`.github/**` methodology repository не копируется в target repository verbatim.
Target workflow создаётся или адаптируется под фактические branch names,
rulesets и CI-модель target repository. Output contract тот же: filename,
count и issue-code oriented вывод, без печати commit bodies целиком, matching
lines, secret values, `.env` contents или private data.

## Запрещённые tracked paths

Repository не должен track-ить эти paths:

- `.env`
- `.env.*`, except `.env.example`
- `.venv/`
- `data/`
- `runtime/`
- `dist/`
- `backups/`
- `exports/`
- `*.log`
- `*.tmp`
- `*.bak`

## Разрешённые исключения

- `.env.example` допустим, если он не содержит реальные secrets.
- Documents могут содержать слова `token`, `password`, `secret` и `credential`
  только как security rules или examples без реальных значений.

## Ограничения

- CI проверяет только tracked files.
- CI не анализирует local untracked files.
- CI не должен читать содержимое `.env`.
- CI не должен печатать secrets.
- Secret scanning и более глубокие checks добавляются отдельными будущими задачами.

## Совместимость runtime GitHub Actions

- Forbidden-files workflow использует `actions/checkout@v5`.
- `actions/checkout@v5` выбран потому, что его action metadata объявляет
  `using: node24`.
- Если GitHub Actions снова показывает runtime deprecation warnings, сначала
  проверить upstream action metadata и только потом менять workflow.
- Не понижать action runtime до версии с deprecation warnings без явного
  принятия временного риска пользователем.

## Локальная проверка перед commit

Перед commit или push запускать эти commands:

```bash
git status --short
```

```bash
python docs/agent-system/tools/validate_commit_message.py --base origin/developer
```

```bash
python docs/agent-system/tools/check_journal_append_only.py --base origin/developer
```

```bash
git ls-files
```

```bash
git grep -I -l -i -E "token|password|secret|api_key|apikey|credential|пароль|токен" -- .
```

```bash
git grep -I -l -i -E "token|password|secret|api_key|apikey|credential|пароль|токен" -- . | wc -l
```

Safe-scan команды выше являются только manual review aid. Они выводят только
filenames или count; matching lines и values нельзя печатать в terminal, logs,
journal, PR body или final report. Если найден возможный реальный secret, не
печатать его дальше и остановиться для user review.
