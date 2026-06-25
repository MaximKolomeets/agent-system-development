# Шаблон engine fix-pass для review autoloop

## Режим

Роль: engine
Режим: fix-pass in active work PR
Branch: `work/<role>/<task>`
Новый PR: запрещён

## Входные данные

- PR URL: `<pr-url>`
- Current head SHA: `<sha>`
- Review feedback source: PR comments/review threads
- `max_review_cycles`: `<n>`
- Current cycle: `<n>`

## Выполнить

1. Проверить clean working tree.
2. Переключиться на ту же task branch.
3. Подтянуть head branch fast-forward.
4. Исправить только feedback внутри scope PR.
5. Не менять forbidden paths и не читать `.env`.
6. Запустить task checks и generated checks, если затронуты docs/generated artifacts.
7. Обновить RESULT/final report, если task ведёт journal.
8. Push в ту же task branch.
9. Вернуть PR в `engine:ready-for-review`.

## STOP-условия

- feedback требует новую substantive task;
- merge conflict без безопасного ff-only решения;
- secrets-risk или forbidden paths;
- failed checks после fix-pass;
- generated drift не сходится;
- требуется force-push/rewrite;
- превышен `max_review_cycles`;
- reviewer или architect запросил human decision.

## Вывод в PR

```text
status: engine:ready-for-review | automation:stopped-human-required
cycle: <current>/<max>
fixed:
- <item list>
checks:
- <command> -> <exit/result>
not_fixed:
- <none | item + reason>
next:
- reviewer re-review | human decision
```
