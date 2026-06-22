# TASK-0047: METH-CLOUD-FRESHNESS-DEPERS-01

## Режим

Роль: docs-maintainer. Исполнитель: на усмотрение архитектора. Reasoning effort: высокий. Branch-guard обязателен.

Batch-policy: открытые journal-записи не являются blocker; closure не подмешивать.

## Цель

Сделать `docs/agent-system/tools/gen_cloud_bundle.py --check` content-parity gate: generated `cloud/` должен совпадать с bundle-содержимым, а строки `asof` и `developer_head_sha` в `cloud/README.md` остаются информационными и не ломают gate при sync-merge без content-дрейфа. Дополнительно убрать vendor-имя из upload how-to heading.

## Repo / ветки

- Репозиторий: `MaximKolomeets/agent-system-development`
- Каталог: `C:\neural\repos\agent-system-development`
- base: `developer`
- work: `work/docs-maintainer-01/cloud-freshness-depers-01`

## Preflight

1. До любого switch/pull проверить root, remote, текущую ветку и `git status --short`; dirty tree -> STOP.
2. `git fetch --all --prune`
3. `git switch developer`
4. `git pull --ff-only origin developer`
5. `git switch -c work/docs-maintainer-01/cloud-freshness-depers-01`
6. `git rev-parse --abbrev-ref HEAD` должен вернуть work-ветку.
7. Sequence взять из `INDEX`; текущая запись: `0047`.

## Allowed files

- `docs/agent-system/tools/gen_cloud_bundle.py`
- `docs/agent-system/cloud/**`
- `docs/agent-system/ORCHESTRATOR_OPERATING_CONTRACT.md`
- `docs/agent-system/BRANCH_POLICY.md`
- journal 0047

## Изменения

1. В `gen_cloud_bundle.py --check` сравнивать каждый generated flat-файл с текущим bundle source content. Для `cloud/README.md` проверять структуру/mapping/how-to, но исключить значения строк `asof` и `developer_head_sha` из равенства.
2. `generate` по-прежнему пишет freshness stamp; `--check` возвращает exit 1 только при реальном content-дрейфе зеркала или нарушении состава.
3. Заменить heading `ChatGPT / browser upload` на нейтральный `Chat UI / browser upload`; upload/Drive/rclone how-to оставить без авторизации/credentials.
4. Регенерировать `docs/agent-system/cloud/`.
5. В `ORCHESTRATOR_OPERATING_CONTRACT.md` и `BRANCH_POLICY.md` закрепить модель: cloud `--check` = content-parity; `asof`/`developer_head_sha` информационные; sync-merge без content-дрейфа не ломает gate.

## Проверки

- `python docs/agent-system/tools/gen_cloud_bundle.py --check` exit 0;
- имитация смены только `asof`/`developer_head_sha` в `cloud/README.md` не ломает `--check`;
- `python docs/agent-system/tools/gen_file_map.py --check` exit 0;
- vendor grep по active generated how-to scope (`gen_cloud_bundle.py`, `cloud/README.md`, обновлённые non-history cloud mirrors) -> 0; исторические mirror-файлы journal/state не являются depers-scope;
- diff только whitelist;
- `git diff --check`;
- branch guard.

## Journal + Source Delta + handoff

`RESULT-0047` должен содержать Source Delta и строку handoff: архитектору загрузить обновлённые source-файлы и брать обновлённые bundle-файлы из `docs/agent-system/cloud/`.

## Commit / PR

Commit:

```text
docs(agent-system): cloud check content-parity (sync-safe) + neutral how-to heading (audit CL/D)
```

Создать PR в `developer`.

## Передача

`reviewer — review (--check на content-parity, sync-merge gate не ломает; vendor-заголовок нейтрален; оба --check 0); затем архитектор — merge; затем engine — FIX-STATE; journal closure — batch перед release`.

## STOP

- HEAD не work-ветка;
- правка вне whitelist;
- `--check` всё ещё gate-ит на commit SHA;
- любой обязательный check не проходит.
