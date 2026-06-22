# TASK-0058-METH-GENERATED-CHECKS-STANDARD-01

Задача для docs-maintainer: METH-GENERATED-CHECKS-STANDARD-01

## Рекомендуемый режим исполнения

Роль: docs-maintainer
Исполнитель: на усмотрение архитектора
Reasoning effort: средний
Запуск: Local only
Режим: Agent

## Цель

Закрепить standing rule: generated text artifacts и их `--check` сравнения обязаны быть content-oriented / EOL-safe. Сравнения нормализуют `CRLF`/`CR`/`LF`, Windows `core.autocrlf` не должен давать false drift, новые generators с `--check` должны иметь regression-проверку, которая пропускает EOL-only drift и ловит реальный content-drift. Generated-bundle paths закрепляются `eol=lf` через `.gitattributes`.

Контекст: кодификация паттерна из RESULT-0056 / PR #200. Код генераторов не менять.

## Preconditions

- Base branch: `developer`
- Work branch: `work/docs-maintainer-01/generated-checks-standard-01`
- Перед стартом подтвердить, что PR #199 и PR #200 merged в `developer`.
- Dirty tree на preflight -> STOP.
- Следующий seq вычислить из `docs/agent-system/engine-journal/INDEX.md`, не предсказывать.

## Разрешённые файлы

- выбранный существующий канон-док для нормативного раздела;
- `docs/agent-system/BRANCH_POLICY.md`;
- `docs/agent-system/engine-journal/input/TASK-0058-METH-GENERATED-CHECKS-STANDARD-01-generated-checks-eol-safe.md`;
- `docs/agent-system/engine-journal/output/RESULT-0058-METH-GENERATED-CHECKS-STANDARD-01-generated-checks-eol-safe.md`;
- `docs/agent-system/engine-journal/INDEX.md`;
- `docs/agent-system/cloud/**` (регенерация через `gen_cloud_bundle.py`).

## Запрещено

- Менять `docs/agent-system/tools/gen_file_map.py`, `docs/agent-system/tools/gen_cloud_bundle.py` или `.gitattributes`.
- Создавать новый отдельный standard file, если есть подходящий существующий канон.
- Трогать `main`/`developer` напрямую, runtime/CI/secrets/.env/private downstream data, append-only history вне новой journal-записи.

## Изменения

1. Добавить нормативный раздел про EOL-safe / content-oriented generated checks в существующий канон рядом с content-parity gate.
2. В `BRANCH_POLICY.md` release-gate добавить короткую кросс-ссылку на это правило.
3. Регенерировать cloud bundle после изменения bundle-файлов и INDEX.

## Проверки

- `python docs/agent-system/tools/gen_file_map.py --check`
- `python docs/agent-system/tools/gen_cloud_bundle.py --check`
- Новая внутренняя ссылка active docs резолвится.
- `git diff --check`
- Branch guard перед commit.

## Передача

Следующий: reviewer — проверить, что EOL-safe/content-oriented правило закреплено без правки генераторов, release-gate ссылается на канон, оба `--check` проходят, cloud bundle регенерирован; затем архитектор — merge PR; затем engine — batch-closure journal (0055/0056/Блок2/Блок3); затем state-refresh + оба `--check`; затем release `developer -> main` (merge выполняет архитектор) + sync.
