# TASK-0068-METH-BATCH-CLOSURE-0065-0067

Статус: closed-at-creation; terminal batch-closure.

## Задача

Закрыть merged-but-unclosed journal-записи 0065, 0066 и 0067 перед повторным release reviewer consistency-gate.

## Режим

- Роль: docs-maintainer.
- Branch guard: `work/docs-maintainer-01/batch-closure-0065-0067`.
- Closure-only: разрешены только RESULT/INDEX/journal terminal entry и `cloud/**` regen.
- Batch-policy: terminal closure закрывается при создании; собственный mergeCommit проставляется при merge.

## Закрываемый набор

| seq | PR | Ожидаемое состояние |
| --- | --- | --- |
| 0065 | #209 | merged |
| 0066 | #210 | merged |
| 0067 | #211 | merged |

## Требования

- Получить merge-факты через `gh pr view`, не из памяти.
- В RESULT-0065/0066/0067 добавить append-only closure-stamp.
- Верхний status-marker RESULT-0065/0066/0067 привести к `closed`.
- В `INDEX.md` перевести 0065/0066/0067 в `closed` + PR URL, без полного mergeCommit.
- Создать RESULT-0068 closed-at-creation.
- Регенерировать `docs/agent-system/cloud/**` после изменения INDEX.
- Проверить `gen_file_map.py --check`, `gen_cloud_bundle.py --check`, final-state rescan и branch guard.

## STOP

- Любой PR из 0065/0066/0067 не `MERGED`.
- HEAD не рабочая ветка задачи.
- Diff выходит за journal/cloud allowlist.
- В INDEX остаётся own-PR-open wording или pre-merge status для закрываемого набора.
