# EXTERNAL_REVIEW_LEDGER - <документ или решение> (template)

Статус: `draft`. Заполняется в target repository или task-local docs scope.
См. `docs/agent-system/EXTERNAL_REVIEW_LEDGER_PATTERN.md`.

Baseline rule: `N=<число>` rounds "только polishing" -> baseline / ready for
approval.

## Applied

| source (round/reviewer) | proposal | where recorded |
| --- | --- | --- |
| round-1 / reviewer-role | Что внесено | PR/revision/path |

## Deferred

| source | proposal | stage/PR |
| --- | --- | --- |
| round-1 / reviewer-role | Что отложено | stage or PR |

## Rejected With Reason

| source | proposal | reason |
| --- | --- | --- |
| round-1 / reviewer-role | Что не принимаем | Почему не переоткрывать |

## Анти-loop отметка

Новое remark блокирует только если относится к critical categories:
correctness, security/privacy, legal/compliance, testability,
integrity/boundary mixing. Иначе remark фиксируется строкой выше, а команда
продолжает работу.
