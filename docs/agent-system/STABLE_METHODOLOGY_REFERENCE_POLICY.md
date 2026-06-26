# STABLE_METHODOLOGY_REFERENCE_POLICY

## Назначение

Этот канон закрепляет, какую версию methodology repository должны читать target/downstream задачи. Цель - не блокировать downstream работу из-за грязной или экспериментальной локальной ветки методологии и не переносить в target repository незарелизованные правила из `developer` или `work/*`.

## Stable reference

Для target implementation repository, private downstream repository и любой docs-only adoption/source-update задачи stable methodology reference по умолчанию:

- remote ref: `origin/main`;
- локальное имя branch, если нужен checkout чистой reference-копии: `main`;
- release tag: допустим только если архитектор явно указал tag как source of truth для задачи;
- published Source/cloud snapshot: допустим только если архитектор явно указал snapshot и его `source_commit`.

`developer`, `work/*`, dirty local methodology tree, open methodology PR branch, reviewer branch или engine branch не являются stable methodology reference для downstream.

## Правило чтения

Downstream задача должна читать stable reference без переключения рабочей methodology ветки. Рекомендуемые варианты:

```powershell
git -C C:\neural\repos\agent-system-development fetch --all --prune
git -C C:\neural\repos\agent-system-development show origin/main:docs/agent-system/cloud/00_README.md
```

или отдельная чистая reference-копия:

```text
C:\neural\refs\agent-system-development-main
```

В downstream task запрещено выполнять в рабочем methodology repository команды `git switch`, `git checkout`, `git pull`, `git merge`, `git reset`, `git clean` или `git stash` только ради чтения методологии. `git fetch --all --prune` допустим, если task разрешает сетевую синхронизацию и guard пройден.

## STOP conditions

Downstream задача пишет `STOP`, если:

- `origin/main` или явно указанный release tag/snapshot недоступен;
- stable reference читается, но нужный файл отсутствует;
- snapshot указан архитектором, но в нем нет `source_commit` или freshness stamp;
- target instructions требуют использовать `developer`, `work/*` или dirty local methodology tree как source of truth без явного решения пользователя.

Dirty `agent-system-development/developer`, dirty `work/*` или open methodology PR не являются STOP для downstream задачи сами по себе, если stable reference доступен через `origin/main`, release tag или явно указанный snapshot.

## task_contract

В downstream/adoption задачах `task_contract` должен фиксировать stable reference:

```yaml
methodology_reference:
  repository_full_name: MaximKolomeets/agent-system-development
  local_path: C:\neural\repos\agent-system-development
  ref: origin/main
  stable_only: true
  source_commit: <origin/main commit sha или release tag commit sha>
  checked_at: <ISO-8601 timestamp>
```

Для задач, которые меняют сам methodology repository, допустимо `stable_only: false`, потому что source of truth такой задачи - указанная рабочая ветка от `developer`. Этот режим нельзя переносить в downstream task без явного решения архитектора.

## Release visibility

После merge methodology PR в `developer` новые правила не видны downstream задачам, которые корректно читают `origin/main`. Архитектор должен отдельно продвинуть methodology `developer -> main` через release PR, если новая политика нужна target/downstream проектам.

## Review policy

Reviewer классифицирует как blocker:

- downstream TASK/RESULT/adoption artifact использует `developer` или `work/*` как stable methodology reference без явного исключения;
- downstream task требует `git switch/pull/checkout/reset/clean/stash` в methodology repository для чтения методологии;
- `methodology_reference.stable_only: true`, но `ref` не является `origin/main`, `main`, явным release tag или явно указанным snapshot.

Reviewer классифицирует как minor finding:

- stable reference корректен, но `source_commit` или `checked_at` оформлены неполно в неготовом draft artifact;
- текст использует старое поле `source_branch`, но значение фактически указывает на `origin/main` и не меняет поведение.
