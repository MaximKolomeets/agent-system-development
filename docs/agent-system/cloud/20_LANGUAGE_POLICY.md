# LANGUAGE_POLICY

## Назначение

Этот документ закрепляет Russian-first policy для methodology repository и для target repositories, которые применяют эту методологию.

Policy действует для оркестратора, `engine`, reviewer, target-local docs, task templates, engine journal artifacts, GitHub-facing артефактов и комментариев внутри создаваемых или изменяемых файлов.

## Основное правило

Все пользовательские ответы, final reports исполнителя (engine), target-local methodology docs, TASK/RESULT/INDEX files, template guidance и описательные комментарии в файлах должны быть на русском языке.

English допускается только там, где перевод ухудшает точность или ломает технический смысл:

- code identifiers;
- command names, flags and terminal output literals;
- paths, filenames and branch names;
- API names, config keys and package names;
- vendor/tool names and literal external names;
- repository identifiers, когда они являются техническим значением.

Section headings, checklist labels и другие user-facing названия разделов пишутся на русском языке. Если англоязычный режим, protocol name или другой technical literal нужен для точности, его можно оставить как alias в скобках после русского названия, например `Лёгкий solo-operator режим (Lightweight solo-operator mode)`.

## Задачи и отчеты исполнителя (engine)

Каждый блок для исполнителя (engine) должен явно требовать от `engine`:

- писать final report на русском языке;
- создавать и обновлять TASK/RESULT/INDEX files на русском языке;
- использовать русские user-facing labels и descriptions в journal artifacts;
- сохранять English только для технических identifiers, commands, paths, branch names, filenames, config keys, API names, package names, vendor/tool names и literal external names.

Если TASK file, bootstrap prompt или локальные инструкции target repository конфликтуют с Russian-first policy, `engine` должен написать `STOP` и запросить решение пользователя, кроме случая, когда пользователь явно разрешил другой язык для этого target repository.

## Adoption target repository

Target adoption/update tasks должны переносить Russian-first policy в target `AGENTS.md` или эквивалентные target instructions.

Все target-local docs/templates, созданные или обновленные из этой методологии, должны быть Russian-first. Новый target-local methodology template не должен быть преимущественно англоязычным, кроме технических identifiers и literal external names.

## Commit и PR metadata / GitHub-facing artifacts

Commit messages, PR titles, PR bodies, review summaries, PR comments с вердиктом, release/sync task summaries и final reports также соблюдают Russian-first policy.

- commit subject/body — Russian-first;
- PR title/body — Russian-first;
- review summary / PR verdict comment — Russian-first;
- final report — Russian-first;
- смысловая часть GitHub metadata должна быть на русском языке;
- technical identifiers не переводятся: branch names, task ids, filenames, paths, commands, config keys, API names, role ids, package names, SHA values, machine-readable status values;
- conventional prefix допускается как technical identifier, например `docs(agent-system):`, но текст после `:` должен быть Russian-first;
- если нужен English alias для поиска, он допускается в скобках после русского смысла, но не вместо него;
- уже pushed/merged commits не переписываются без отдельного явного решения архитектора на force-push/rewrite history.

### Разрешенные commit scope

`validate_commit_message.py` читает разрешенные conventional-commit scope из
`commit_metadata.allowed_scopes` в этом файле. Если блок отсутствует, tool
использует безопасный default `[agent-system]`.

```yaml
commit_metadata:
  allowed_scopes:
    - agent-system
```

Target repositories должны расширять этот список собственным нейтральным
scope, не удаляя `agent-system`, например:

```yaml
commit_metadata:
  allowed_scopes:
    - agent-system
    - verification
```

Scope является technical identifier: он не переводится, пишется стабильно в
commit subject и не должен раскрывать private downstream project names.

Корректные commit messages:

- `docs(agent-system): закрепить русский язык для commit и PR metadata`
- `docs(verification): обновить target-local методологию`
- `journal(agent-system): закрыть записи 0073-0076 после merge`
- `docs(agent-system): добавить fallback для zero-match scan на Windows`

Некорректные commit messages:

- `docs(agent-system): add zero-match scan fallback`
- `docs(agent-system): batch closure for v1.1 fix series`
- `fix docs after review`

## Комментарии в файлах

В scripts, workflows, config-like files, code и technical examples комментарии пишутся на русском языке, если комментарии нужны.

Команды, flags, paths, identifiers, config keys и API names не переводятся.

Если формат файла не поддерживает комментарии, пояснение добавляется в соседнюю документацию или schema descriptions.

## Проверки review

Перед PR review нужно проверить:

- TASK/RESULT templates исполнителя (engine) являются Russian-first;
- target-local methodology templates являются Russian-first;
- final report requirements требуют русский язык;
- commit subject/body, PR title/body и review summary являются Russian-first;
- section headings и checklist labels являются Russian-first; допустимые английские technical aliases сохранены в скобках;
- комментарии в generated scripts/workflows/config examples написаны на русском, если comments нужны;
- английские technical identifiers сохранены и не переведены механически;
- target `AGENTS.md` или эквивалент содержит Russian-first policy после adoption/update scope.

Reviewer классифицирует как blocker:

- новая или измененная GitHub-facing metadata в ready-for-review PR преимущественно англоязычная без явного разрешения пользователя;
- TASK/RESULT/INDEX или final report не Russian-first;
- downstream/adoption task не требует перенести Russian-first policy в target instructions при соответствующем scope;
- target instructions конфликтуют с Russian-first policy, а task не требует `STOP`.

Reviewer классифицирует как minor finding:

- отдельный английский technical alias можно заменить русским описанием без изменения смысла;
- исторический pushed/merged commit message не Russian-first, но его нельзя безопасно исправить без rewrite history;
- draft artifact содержит неполную формулировку, но ready-for-review state еще не заявлен.
