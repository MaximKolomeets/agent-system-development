# Шаблон reviewer pass для review autoloop

## Режим

Роль: reviewer  
Режим: review-only  
Branch/PR: active work PR  
Правки файлов: запрещены  

## Входные данные

- PR URL: `<pr-url>`
- Expected head SHA: `<head-sha>`
- `max_review_cycles`: `<n>`
- Current cycle: `<n>`
- Scope summary: `<scope>`

## Проверить

1. PR head SHA совпадает с expected head SHA.
2. Diff соответствует scope задачи.
3. Checks зелёные или failures классифицированы как blocker.
4. Forbidden paths/secrets/runtime/private data отсутствуют.
5. Review feedback относится к этой task branch.
6. `max_review_cycles` не превышен.

## Вывод в PR

Reviewer оставляет feedback только в PR агента:

- `reviewer:approved` + `architect:ready-to-merge`, если blockers нет;
- `reviewer:changes-requested`, если есть blockers/actionable feedback;
- `automation:stopped-human-required`, если сработал STOP.

## STOP-условия

- secrets-risk или forbidden paths;
- failed checks, которые нельзя безопасно классифицировать;
- scope drift;
- нужен architecture/product/security decision;
- превышен `max_review_cycles`;
- PR head SHA не совпал.

## Формат verdict

```text
verdict: reviewer:approved | reviewer:changes-requested | automation:stopped-human-required
reviewed_head_sha: <sha>
cycle: <current>/<max>
blockers:
- <none | blocker list>
non_blocking_notes:
- <none | note list>
next:
- architect merge | engine fix-pass | human decision
```
