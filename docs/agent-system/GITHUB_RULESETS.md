# GITHUB_RULESETS

## main

Рекомендуемые ручные правила GitHub branch protection/rulesets:

- require pull request before merging;
- block force pushes;
- block deletions;
- require conversation resolution, если доступно;
- restrict direct pushes для агентских tokens, если используется GitHub organization/rulesets;
- пользователь может оставаться администратором.

## developer

Рекомендуемые правила:

- require pull request before merging;
- block force pushes;
- block deletions;
- требовать, чтобы изменения приходили из `work/*`;
- не разрешать агентам прямой push после bootstrap.

## work/*

Рекомендуемые правила:

- разрешить push только соответствующему агенту/token, если технически возможно;
- не требовать protection как для `main`/`developer`;
- ветки можно удалять после merge.

## Что пока не автоматизировано

- Фактическая настройка rulesets выполняется вручную в GitHub UI.
- Granular token restrictions зависят от типа репозитория/организации.
- Если GitHub не позволяет ограничить token по namespace веток, контроль фиксируется процессом и review.
