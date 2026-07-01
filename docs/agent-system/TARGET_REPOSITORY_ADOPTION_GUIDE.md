# TARGET_REPOSITORY_ADOPTION_GUIDE

## Назначение

Этот файл - короткий вход для adoption target implementation repository. Полный рабочий маршрут остается в `docs/agent-system/ADOPTION_GUIDE.md`, `docs/agent-system/templates/DOCS_ONLY_ADOPTION_TASK_TEMPLATE.md`, `docs/agent-system/DOWNSTREAM_ADAPTATION_CHECKLIST.md` и `docs/agent-system/TARGET_PROJECT_GOVERNANCE_PACK.md`.

## Stable methodology reference

Target/downstream adoption читает methodology repository только из stable reference:

- по умолчанию `origin/main` / `main`;
- release tag или published Source/cloud snapshot - только если архитектор явно указал это в задаче;
- `developer`, `work/*`, dirty local tree и open methodology PR branch не используются как source of truth для target repository.

Dirty рабочая ветка в `agent-system-development` не блокирует target adoption, если `origin/main` или явно заданный stable snapshot доступен и читается.

## Минимальный порядок

1. Выполнить `docs/agent-system/TARGET_ADOPTION_DETECTOR.md` и выбрать Variant A/B/C или STOP.
2. Зафиксировать target repository, base branch, working branch и selected branch model.
3. Прочитать stable methodology reference без `git switch/pull/checkout/reset/clean/stash` в рабочем methodology repository.
4. Добавить в TASK/RESULT/adoption artifact блок `methodology_reference` с `ref: origin/main`, `stable_only: true`, `source_commit` и `checked_at`.
5. Перенести Russian-first policy в target `AGENTS.md` или эквивалентные target instructions, если scope меняет такие инструкции.
6. Материализовать только target-adapted docs: project state, branch names, governance pack и journal history не копируются verbatim из methodology repository.

## Обязательные политики

- Все user-facing answers, TASK/RESULT/INDEX, final report, PR title/body, commit message, review summary и target-local docs/templates пишутся на русском языке.
- Английский сохраняется только для technical identifiers, команд, flags, paths, filenames, branch names, config keys, API names, package names, machine-readable status values и literal external names.
- `.env` не читается, matching secret lines не печатаются, private downstream data не переносится в public methodology repository.

## Передача

Следующий: docs-maintainer - применяет `docs/agent-system/ADOPTION_GUIDE.md` и этот stable-reference вход при подготовке target adoption task.
