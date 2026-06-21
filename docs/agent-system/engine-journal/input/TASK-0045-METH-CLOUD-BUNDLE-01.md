# TASK-0045: METH-CLOUD-BUNDLE-01

## Режим

Роль: docs-maintainer. Исполнитель: на усмотрение архитектора. Reasoning effort: высокий. Branch-guard обязателен.

Batch-policy: открытые journal-записи не являются blocker; closure не подмешивать.

## Цель

Создать generated cloud staging folder для Architect -> Orchestrator context handoff: единый manifest bundle, stdlib generator, flat cloud files, upload/Drive how-to без credentials и release-gate parity.

## Repo / ветки

- Репозиторий: `MaximKolomeets/agent-system-development`
- Каталог: `C:\neural\repos\agent-system-development`
- base: `developer`
- work: `work/docs-maintainer-01/cloud-bundle-01`

## Preflight

1. `git fetch --all --prune`
2. `git switch developer`
3. `git pull --ff-only origin developer`
4. `git switch -c work/docs-maintainer-01/cloud-bundle-01`
5. `git rev-parse --abbrev-ref HEAD` должен вернуть work-ветку.
6. Sequence взять из `INDEX`; ожидается `0045`.

## Allowed files

- `docs/agent-system/tools/gen_cloud_bundle.py`
- `docs/agent-system/cloud/**`
- `docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml`
- `docs/agent-system/PROJECT_FILE_MAP.md`
- `docs/agent-system/ORCHESTRATOR_OPERATING_CONTRACT.md`
- `docs/agent-system/templates/TASK_HEADER_COMMON.md`
- `docs/agent-system/BRANCH_POLICY.md`
- `docs/agent-system/OPERATIONAL_FAST_LANE.md`
- journal 0045

## Изменения

1. В `ADOPTION_TRANSFER_MANIFEST.yml` добавить `orchestrator_context_bundle` как единый машинный источник состава bundle и зарегистрировать `gen_cloud_bundle.py` как `source`, `cloud/**` как `generated`.
2. Добавить `docs/agent-system/tools/gen_cloud_bundle.py`: stdlib generator с режимами generate и `--check`.
3. Сгенерировать `docs/agent-system/cloud/**` с flat filenames, `cloud/README.md`, freshness stamp, upload how-to, Drive for Desktop и `rclone` шаблоном без авторизации/credentials.
4. Регенерировать `PROJECT_FILE_MAP.md`.
5. Обновить handoff/release-gate/fast-lane hooks: `ORCHESTRATOR_OPERATING_CONTRACT.md`, `TASK_HEADER_COMMON.md`, `BRANCH_POLICY.md`, `OPERATIONAL_FAST_LANE.md`.

## Проверки

- `python docs/agent-system/tools/gen_cloud_bundle.py --check` exit 0;
- `python docs/agent-system/tools/gen_file_map.py --check` exit 0;
- `docs/agent-system/cloud/` содержит не больше 25 flat files;
- `cloud/README.md` содержит `asof`, `developer_head_sha`, upload how-to и Drive/rclone how-to без credentials;
- diff только whitelist;
- `git diff --check`;
- branch guard.

## Journal + Source Delta + handoff

`RESULT-0045` должен содержать Source Delta и handoff-строку с пометкой, что обновлённые bundle-файлы скопированы в `docs/agent-system/cloud/`.

## Commit / PR

Commit:

```text
docs(agent-system): cloud staging bundle + generator + parity + release-gate (orchestrator handoff)
```

Создать PR в `developer`.

## Передача

`reviewer — review (cloud --check exit 0; ≤25 плоских файлов = bundle; единый источник списка; Drive how-to без авторизации; release-gate hook); затем архитектор — merge; затем engine — pre-release BATCH-CLOSURE 0039…0045; затем release dev→main`.

## STOP

- HEAD не work-ветка;
- правка вне whitelist;
- `cloud --check` не сходится;
- больше 25 файлов в bundle;
- попытка Drive-авторизации/credentials;
- size-guard требует split.
