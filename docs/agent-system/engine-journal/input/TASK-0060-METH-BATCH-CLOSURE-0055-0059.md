# TASK-0060-METH-BATCH-CLOSURE-0055-0059

Задача для docs-maintainer: METH-BATCH-CLOSURE-0055-0059

## Рекомендуемый режим исполнения

Роль: docs-maintainer
Исполнитель: на усмотрение архитектора
Reasoning effort: средний
Запуск: Local only
Режим: Agent

## Цель

Pre-release terminal batch-closure для merged-but-unclosed seq 0055..0059. Перевести их в closed-состояние перед release `developer -> main`. Контента методологии не менять.

## Preconditions

- Base branch: `developer`
- Work branch: `work/docs-maintainer-01/batch-closure-0055-0059`
- PR #199..#203 должны быть `MERGED`.
- `docs/agent-system/engine-journal/INDEX.md` содержит seq 0055..0059.
- `python docs/agent-system/tools/gen_file_map.py --check` и `python docs/agent-system/tools/gen_cloud_bundle.py --check` проходят.

## Разрешённые файлы

- `docs/agent-system/engine-journal/output/RESULT-0055..0059-*.md` (только append closure-stamp)
- `docs/agent-system/engine-journal/INDEX.md`
- `docs/agent-system/engine-journal/input/TASK-0060-METH-BATCH-CLOSURE-0055-0059.md`
- `docs/agent-system/engine-journal/output/RESULT-0060-METH-BATCH-CLOSURE-0055-0059.md`
- `docs/agent-system/cloud/**` (регенерация через `gen_cloud_bundle.py`)

## Запрещено

- Любой контент методологии вне journal/cloud mirror.
- Переписывать тела RESULT-0055..0059; только append closure-stamp.
- Дублировать полный mergeCommit в INDEX.
- Трогать `main`/`developer` напрямую, runtime/CI/secrets/.env/private downstream data, force push, удалять/перезаписывать существующие TASK/RESULT.

## Проверки

- `python docs/agent-system/tools/gen_file_map.py --check`
- `python docs/agent-system/tools/gen_cloud_bundle.py --check`
- INDEX строки 0055..0059 закрыты и имеют PR URL без полного mergeCommit.
- RESULT 0055..0059 имеют closure-stamp с merge commit SHA / merged_at / PR URL.
- `git diff --check`
- Branch guard перед commit.

## Передача

Следующий: reviewer — consistency-gate PR closure (RESULT-stamps 0055..0059 vs GitHub, INDEX status+URL, terminal 0060 closed-at-creation, оба `--check`); затем архитектор — merge PR; затем engine — state-refresh (последний pre-release PR, per-task closure); затем release `developer -> main` (мержит архитектор) + tag; затем sync.
