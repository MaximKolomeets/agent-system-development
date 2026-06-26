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
- Reviewed head SHA: `<sha-from-reviewer-verdict>`
- Blocker IDs/classes: `B-01`, `B-02`, ... with `machine-verifiable | semantic | mixed`
- `max_review_cycles`: `<n>`
- Current cycle: `<n>`

## Выполнить

1. Проверить clean working tree.
2. Переключиться на ту же task branch.
3. Подтянуть head branch fast-forward.
4. Исправить только feedback внутри scope PR.
5. Закрыть blockers по IDs и не смешивать unrelated cleanup.
6. Не менять forbidden paths и не читать `.env`.
7. Запустить `verification_command` для каждого blocker, task checks и generated checks, если затронуты docs/generated artifacts.
8. Обновить RESULT/final report, если task ведёт journal.
9. Push в ту же task branch.
10. Вернуть PR в `engine:ready-for-review` для semantic/mixed re-review или `architect:ready-to-merge` для fully passed machine-check closure.

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

```yaml
status: engine:ready-for-review | architect:ready-to-merge | automation:stopped-human-required
cycle: <current>/<max>
fix_pass_for_reviewed_head_sha: <sha>
new_head_sha: <sha>
fixed_blockers:
  - id: B-01
    class: machine-verifiable | semantic | mixed
    files_changed:
      - <path>
    verification_command: <command>
    verification_result: passed | failed | not-run
checks:
  - command: <command>
    result: passed | failed
requires_reviewer_rereview: yes | no
rereview_scope: none | machine_check_only | changed_blockers_only | full
architect_escalation_required: yes | no
not_fixed:
  - <none | id + reason>
next:
  - reviewer re-review | architect human merge | human decision
```

Если все fixed blockers имеют class `machine-verifiable`, все `verification_command` и checks прошли, changed files не вышли за `required_fix_scope`, а reviewer не требовал explicit re-review, engine может поставить `status: architect:ready-to-merge`, `requires_reviewer_rereview: no`, `rereview_scope: machine_check_only`. Для `semantic` и `mixed` blockers всегда нужен reviewer re-review по `changed_blockers_only` или более широкому scope, заданному reviewer.
