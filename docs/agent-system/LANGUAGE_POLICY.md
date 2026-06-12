# LANGUAGE_POLICY

## Назначение

Этот документ закрепляет Russian-first policy для methodology repository и для target repositories, которые применяют эту методологию.

Policy действует для ChatGPT, `engine`, target-local docs, task templates, engine journal artifacts и комментариев внутри создаваемых или изменяемых файлов.

## Основное правило

Все пользовательские ответы, Engine final reports, target-local methodology docs, TASK/RESULT/INDEX files, template guidance и описательные комментарии в файлах должны быть на русском языке.

English допускается только там, где перевод ухудшает точность или ломает технический смысл:

- code identifiers;
- command names, flags and terminal output literals;
- paths, filenames and branch names;
- API names, config keys and package names;
- vendor/tool names and literal external names;
- repository identifiers, когда они являются техническим значением.

## Engine tasks and reports

Каждый Engine-блок должен явно требовать от `engine`:

- писать final report на русском языке;
- создавать и обновлять TASK/RESULT/INDEX files на русском языке;
- использовать русские user-facing labels и descriptions в journal artifacts;
- сохранять English только для технических identifiers, commands, paths, branch names, filenames, config keys, API names, package names, vendor/tool names и literal external names.

Если TASK file, bootstrap prompt или локальные инструкции target repository конфликтуют с Russian-first policy, `engine` должен написать `STOP` и запросить решение пользователя, кроме случая, когда пользователь явно разрешил другой язык для этого target repository.

## Target adoption

Target adoption/update tasks должны переносить Russian-first policy в target `AGENTS.md` или эквивалентные target instructions.

Все target-local docs/templates, созданные или обновленные из этой методологии, должны быть Russian-first. Новый target-local methodology template не должен быть преимущественно англоязычным, кроме технических identifiers и literal external names.

## File comments

В scripts, workflows, config-like files, code и technical examples комментарии пишутся на русском языке, если комментарии нужны.

Команды, flags, paths, identifiers, config keys и API names не переводятся.

Если формат файла не поддерживает комментарии, пояснение добавляется в соседнюю документацию или schema descriptions.

## Review checks

Перед PR review нужно проверить:

- Engine TASK/RESULT templates являются Russian-first;
- target-local methodology templates являются Russian-first;
- final report requirements требуют русский язык;
- comments in generated scripts/workflows/config examples написаны на русском, если comments нужны;
- English technical identifiers сохранены и не переведены механически;
- target `AGENTS.md` или эквивалент содержит Russian-first policy после adoption/update scope.
