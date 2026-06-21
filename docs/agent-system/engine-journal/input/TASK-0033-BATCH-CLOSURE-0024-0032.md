# Задача для docs-maintainer-01: BATCH-CLOSURE 0024...0032 (pre-release, terminal)

## Режим

Роль: docs-maintainer.
Исполнитель: на усмотрение архитектора.
Reasoning effort: средний.
branch-guard.

Closure-only terminal задача по `docs/agent-system/templates/BATCH_CLOSURE_TASK_TEMPLATE.md`.
Разрешено финализировать чужие journal-записи как исключение из обычного правила
append-only: содержательная история RESULT не переписывается, добавляется только
closure-stamp и обновляется статус в `INDEX.md`.

## Цель

Закрыть все merged-but-unclosed записи engine journal перед release `developer -> main`,
чтобы снять release-gate.

## Discovery

Исходная задача ожидала набор 0027...0032. При INDEX-driven discovery также найдены
merged-but-unclosed записи 0024, 0025 и 0026; они включены в closure-set, чтобы
после batch-closure в INDEX не осталось открытых merged-записей.

Closure-set:

- 0024 -> PR #160
- 0025 -> PR #161
- 0026 -> PR #162
- 0027 -> PR #163
- 0028 -> PR #164
- 0029 -> PR #165
- 0030 -> PR #166
- 0031 -> PR #167
- 0032 -> PR #168

## Allowed files

Только engine journal:

- `docs/agent-system/engine-journal/INDEX.md`
- `docs/agent-system/engine-journal/input/TASK-0033-BATCH-CLOSURE-0024-0032.md`
- `docs/agent-system/engine-journal/output/RESULT-0024-*`
- `docs/agent-system/engine-journal/output/RESULT-0025-*`
- `docs/agent-system/engine-journal/output/RESULT-0026-*`
- `docs/agent-system/engine-journal/output/RESULT-0027-*`
- `docs/agent-system/engine-journal/output/RESULT-0028-*`
- `docs/agent-system/engine-journal/output/RESULT-0029-*`
- `docs/agent-system/engine-journal/output/RESULT-0030-*`
- `docs/agent-system/engine-journal/output/RESULT-0031-*`
- `docs/agent-system/engine-journal/output/RESULT-0032-*`
- `docs/agent-system/engine-journal/output/RESULT-0033-BATCH-CLOSURE-0024-0032.md`

## Проверки

- `gh pr view <PR> --json number,url,state,mergedAt,mergeCommit,headRefOid`
- `git diff --check`
- `git diff --name-only developer...HEAD`
- `git rev-parse --abbrev-ref HEAD`
- stale-status scan по closure-set и `INDEX.md`

## Передача

Следующий: reviewer — review closure-PR (журнал консистентен, факты совпадают с gh); затем архитектор — merge; затем архитектор — release dev->main (rule 1, human-only).
