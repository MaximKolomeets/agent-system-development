# TASK-0024-ASD-OPLAYER-001

Файл задачи: `docs/agent-system/engine-journal/input/TASK-0024-ASD-OPLAYER-001-project-operating-layer.md`

Идентификатор задачи: `ASD-OPLAYER-001`

Номер sequence: `0024` (вычислен из INDEX на момент выполнения: последний seq 0023 + 1)

Создано: `2026-06-19`

Автор: `docs-architect`

Target repository: `MaximKolomeets/agent-system-development` (публичный методологический репозиторий; в этой задаче он же является target)

Methodology repository: `MaximKolomeets/agent-system-development`

Агент: `docs-architect`

Engine: указывается отдельно; vendor/tool name не является role name.

## Methodology reference

```yaml
methodology_reference:
  repository: MaximKolomeets/agent-system-development
  source_branch: developer
  source_commit: 0267e36729aa69440b17174ad9e5d2a3bb1199f9
  checked_at: "2026-06-19"
  reference_type: commit
  notes: "Локальная копия методологии синхронизирована с origin/developer перед изменениями (git fetch --all --prune)."
```

Recommended Engine Mode:

- launch mode / запуск: Local only
- reasoning: High
- execution mode / режим: Agent (docs + journal)
- why this mode is required / почему: операционализация трёхслойной operating-модели с жёсткой границей нейтральности; цена ошибки (раскрытие приватных данных) высокая.

Режим источника задачи: `copy-paste`

Base branch: `developer`

Working branch: `work/docs-architect-01/asd-oplayer-001-operating-layer`

Примечание о branch naming: исходный prompt предлагал slug с vendor-токеном (`asd-claude-...`); по правилу `AGENTS.md`/`BRANCH_POLICY.md` (нет vendor/tool names в branch names) slug нейтрализован до `asd-oplayer-001-operating-layer`. Имена файлов-контрактов (`CLAUDE_PROJECT_OPERATING_LAYER.md`) сохранены по прецеденту `CHATGPT_OPERATING_CONTRACT.md` (operating-контракт ассистент-продукта).

Verified Baseline:

- checked repository: `MaximKolomeets/agent-system-development`
- checked base branch: `developer`
- working branch: `work/docs-architect-01/asd-oplayer-001-operating-layer`
- checked branch state: clean working tree до изменений
- baseline `developer` HEAD: `0267e36729aa69440b17174ad9e5d2a3bb1199f9`
- baseline verification source: local git after `git fetch --all --prune`
- baseline verification date/time: `2026-06-19`

Правило языка: Russian-first. English только для technical identifiers, команд, путей, branch names, filenames, config keys, API names, package names, vendor/tool names и literal external names.

## Цель

Зафиксировать нейтральные контракты трёхслойной operating-модели поверх repo
governance: project operating layer (один изолированный проектный контекст на
target implementation repository) и cross-project consolidation (Cowork lane).
Только docs + journal; без runtime, кода и реальных имён/данных.

## Контекст

Команда ведёт работу по target implementation repositories в изолированных
проектных контекстах ассистента и хочет безопасную сводную картину поверх
нескольких проектов без нарушения изоляции и границ данных. Нужны нейтральные,
публично-безопасные контракты.

## Разрешенные файлы

- `docs/agent-system/CLAUDE_PROJECT_OPERATING_LAYER.md`
- `docs/agent-system/CROSS_PROJECT_CONSOLIDATION_CONTRACT.md`
- `docs/agent-system/templates/TARGET_PROJECT_GOVERNANCE_PACK_TEMPLATE.md`
- `README.md`
- `docs/agent-system/DECISION_LOG.md`
- `docs/agent-system/CURRENT_STATE.md`
- `docs/agent-system/NEXT_STEPS.md`
- `docs/agent-system/engine-journal/input/TASK-0024-ASD-OPLAYER-001-project-operating-layer.md`
- `docs/agent-system/engine-journal/output/RESULT-0024-ASD-OPLAYER-001-project-operating-layer.md`
- `docs/agent-system/engine-journal/INDEX.md`

## Запрещенные файлы

- `.env`, `.venv/`, `data/`, `runtime/`, `dist/`, `backups/`, `exports/`
- credentials, tokens, private keys, real passwords
- private repository URLs
- private downstream project names
- client/customer data
- production/runtime data

## STOP-условия

- любое реальное имя проекта/клиента/данных или приватный URL;
- working tree dirty before changes без разрешения;
- forbidden files detected;
- переоткрытие принятого методологического решения;
- расширение scope за пределы docs + journal.

## Проверки

- `git status --short`
- `git diff --check`
- `git rev-parse --abbrev-ref HEAD` (должна быть work-ветка)
- forbidden tracked paths check
- sensitive grep filename-only
- проверка отсутствия реальных имён/приватных URL в добавленном тексте

## Commit policy

- одна задача = одна ветка = один PR;
- коммит только в `work/docs-architect-01/asd-oplayer-001-operating-layer`;
- не менять `main`/`developer` напрямую.

## PR policy

- PR из work-ветки в `developer`; не мержить (мерж выполняет человек-архитектор);
- `main` не трогать.

## Ожидаемый RESULT file

`docs/agent-system/engine-journal/output/RESULT-0024-ASD-OPLAYER-001-project-operating-layer.md`

## Требования к final report

Russian-first; файлы; краткое содержание контрактов; подтверждение нейтральности
(0 реальных имён); PR URL + commit SHA + checks; подтверждение «его
main/developer напрямую не менялись»; methodology feedback; финализация
RESULT/INDEX после PR.
