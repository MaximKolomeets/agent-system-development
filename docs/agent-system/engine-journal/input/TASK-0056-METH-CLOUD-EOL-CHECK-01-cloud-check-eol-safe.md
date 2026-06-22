# TASK-0056-METH-CLOUD-EOL-CHECK-01

Задача для tooling-maintainer: METH-CLOUD-EOL-CHECK-01

## Рекомендуемый режим исполнения

Роль: tooling-maintainer
Исполнитель: на усмотрение архитектора
Reasoning effort: высокий
Запуск: Local only
Режим: Agent

## Цель

Сделать `python docs/agent-system/tools/gen_cloud_bundle.py --check` устойчивым к EOL: проверка должна проходить на Windows checkout с `core.autocrlf=true` и на LF checkout, но продолжать падать при реальном content-drift cloud bundle.

## Контекст

Аудит METH-AUDIT-2026-06-22-01 зафиксировал CL-01/F-01: committed blobs cloud-файлов имеют LF, Windows working tree получает CRLF, а `gen_cloud_bundle.py --check` сравнивал raw bytes regenerated LF snapshot с checked-out CRLF. Это давало ложный release-gate fail без реального content-drift.

PR #199 с audit seq 0055 должен быть merged в `developer` до начала этой задачи.

## Branch / baseline

- Base branch: `developer`
- Work branch: `work/tooling-maintainer-01/cloud-eol-check-01`
- Перед изменениями выполнить repository sync / checkout guard:
  - `git rev-parse --show-toplevel`
  - `git remote -v`
  - `git branch --show-current`
  - `git status --short`
  - `git fetch --all --prune`
  - `git switch developer`
  - `git pull --ff-only origin developer`
- Если working tree dirty, ff-only невозможен или `HEAD != origin/developer` -> STOP.
- Проверить, что `docs/agent-system/engine-journal/INDEX.md` содержит seq 0055 из PR #199.

## Разрешённые файлы

- `.gitattributes`
- `docs/agent-system/tools/gen_cloud_bundle.py`
- `docs/agent-system/cloud/**`
- `docs/agent-system/engine-journal/input/TASK-0056-METH-CLOUD-EOL-CHECK-01-cloud-check-eol-safe.md`
- `docs/agent-system/engine-journal/output/RESULT-0056-METH-CLOUD-EOL-CHECK-01-cloud-check-eol-safe.md`
- `docs/agent-system/engine-journal/INDEX.md`

## Требуемые изменения

1. Нормализовать line endings перед content-сравнением в `gen_cloud_bundle.py --check`, включая README freshness-normalization.
2. Добавить минимальный `.gitattributes` для generated cloud bundle, чтобы закрепить LF для `docs/agent-system/cloud/**`, не добавляя `.gitattributes` в manifest.
3. Регенерировать `docs/agent-system/cloud/**` через `python docs/agent-system/tools/gen_cloud_bundle.py`, потому что journal INDEX входит в bundle.

## Проверки

- Baseline до изменений:
  - `python docs/agent-system/tools/gen_file_map.py --check`
  - `python docs/agent-system/tools/gen_cloud_bundle.py --check`
  - `git config --get core.autocrlf`
- После изменений:
  - `python docs/agent-system/tools/gen_file_map.py --check`
  - `python docs/agent-system/tools/gen_cloud_bundle.py --check`
  - `git diff --check`
- Regression: временно внести реальный content-drift в один bundle-source, убедиться, что `gen_cloud_bundle.py --check` падает, затем вернуть файл и убедиться, что check снова проходит.

## STOP-условия

- HEAD не `work/tooling-maintainer-01/cloud-eol-check-01` перед commit.
- `gen_file_map.py --check` ломается.
- EOL-normalization маскирует реальный content-drift.
- Diff выходит за allowed files.
- Force push, direct push в `developer`/`main`, чтение `.env` или secrets.

## Передача

Следующий: reviewer — проверить PR, что cloud-check стал EOL-safe, regression подтверждает сохранение drift detection, оба `--check` зелёные; затем архитектор — merge; затем engine — Блок 2 docs-нити; journal closure — batch перед release.
