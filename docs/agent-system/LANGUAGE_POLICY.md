# LANGUAGE_POLICY

## Назначение

Этот документ закрепляет Russian-first policy для methodology repository и для target repositories, которые применяют эту методологию.

Policy действует для оркестратора, `engine`, target-local docs, task templates, engine journal artifacts и комментариев внутри создаваемых или изменяемых файлов.

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

## Комментарии в файлах

В scripts, workflows, config-like files, code и technical examples комментарии пишутся на русском языке, если комментарии нужны.

Команды, flags, paths, identifiers, config keys и API names не переводятся.

Если формат файла не поддерживает комментарии, пояснение добавляется в соседнюю документацию или schema descriptions.

## Проверки review

Перед PR review нужно проверить:

- TASK/RESULT templates исполнителя (engine) являются Russian-first;
- target-local methodology templates являются Russian-first;
- final report requirements требуют русский язык;
- section headings и checklist labels являются Russian-first; допустимые английские technical aliases сохранены в скобках;
- комментарии в generated scripts/workflows/config examples написаны на русском, если comments нужны;
- английские technical identifiers сохранены и не переведены механически;
- target `AGENTS.md` или эквивалент содержит Russian-first policy после adoption/update scope.
