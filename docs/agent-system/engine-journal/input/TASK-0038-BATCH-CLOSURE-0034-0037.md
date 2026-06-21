# Задача для docs-maintainer-01: BATCH-CLOSURE 0034...0037 (pre-release, terminal)

## Режим

Роль: docs-maintainer.
Исполнитель: на усмотрение архитектора.
Reasoning effort: средний.
branch-guard.

Closure-only terminal задача по `docs/agent-system/templates/BATCH_CLOSURE_TASK_TEMPLATE.md`.
Разрешено финализировать чужие journal-записи как исключение из обычного append-only правила:
содержательная история RESULT не переписывается, добавляется только closure-stamp и обновляется статус в `INDEX.md`.

## Цель

Закрыть все merged-but-unclosed записи engine journal перед release `developer -> main`.

## Discovery

INDEX-driven discovery нашёл ожидаемый набор:

- 0034 -> PR #172
- 0035 -> PR #173
- 0036 -> PR #174
- 0037 -> PR #175

Все PR подтверждены как `MERGED` через:

```powershell
gh pr view <PR> --json url,state,mergedAt,mergeCommit,headRefOid
```

## Allowed files

Только engine journal:

- `docs/agent-system/engine-journal/INDEX.md`
- `docs/agent-system/engine-journal/input/TASK-0038-BATCH-CLOSURE-0034-0037.md`
- `docs/agent-system/engine-journal/output/RESULT-0034-METH-DEPERS-COMPLETE-01.md`
- `docs/agent-system/engine-journal/output/RESULT-0035-METH-MANIFEST-PARITY-01.md`
- `docs/agent-system/engine-journal/output/RESULT-0036-METH-SOURCE-DELTA-RULE-01.md`
- `docs/agent-system/engine-journal/output/RESULT-0037-METH-FILE-MAP-GEN-01.md`
- `docs/agent-system/engine-journal/output/RESULT-0038-BATCH-CLOSURE-0034-0037.md`

## Проверки

- `python docs/agent-system/tools/gen_file_map.py --check`
- `git diff --check`
- `git diff --name-only developer...HEAD`
- `git rev-parse --abbrev-ref HEAD`
- stale-status scan по closure-set и `INDEX.md`

## Передача

Следующий: reviewer — review closure-PR (журнал сходится с GitHub facts, `--check` exit 0); затем архитектор — merge; затем архитектор — release dev->main (rule 1, human-only).
