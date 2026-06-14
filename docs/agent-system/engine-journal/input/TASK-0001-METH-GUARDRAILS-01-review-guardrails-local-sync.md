# METH-GUARDRAILS-01 - task

Файл задачи: `docs/agent-system/engine-journal/input/TASK-0001-METH-GUARDRAILS-01-review-guardrails-local-sync.md`

Идентификатор задачи: `METH-GUARDRAILS-01`

Номер sequence: `0001`

Создано: `2026-06-14`

Автор: пользователь через ChatGPT

Target repository: `MaximKolomeets/agent-system-development`

Methodology repository: `MaximKolomeets/agent-system-development`

Агент: `docs-maintainer-01`

Engine: Codex

Recommended Engine Mode:

- launch mode / запуск: Local only
- model / модель: GPT-5.5, если доступна; иначе GPT-5.3-Codex
- reasoning: High
- execution mode / режим: Agent
- why this mode is required / почему: docs-only methodology hardening с branch policy, review workflow, templates и engine journal.

Режим источника задачи: `copy-paste attachment`

Task source commit SHA: не применимо, задача передана через attachment в чате.

Task file blob SHA: будет проверен после materialization commit при необходимости.

Ссылка на bootstrap prompt: не применимо.

Примечание об источнике правды: source of truth - пользовательская задача `METH-GUARDRAILS-01`, переданная во вложении `pasted-text.txt`.

Base branch: `origin/developer`

Working branch: `work/docs-maintainer-01/meth-guardrails-01`

Verified Baseline:

- checked repository: `C:\neural\repos\agent-system-development`
- checked base branch: `developer`
- working branch: `work/docs-maintainer-01/meth-guardrails-01`
- checked branch state: локальная `developer` синхронизирована с `origin/developer` на `b9ea1d63dffd21a562cb43971e41eb9deaeb7fa5`
- baseline verification source: local git after `git fetch --all --prune`
- baseline verification date/time: `2026-06-14`

Copy/Paste Completeness Check:

- [x] TASK/Engine block can be executed without reading surrounding chat text.
- [x] Recommended Engine Mode is included.
- [x] Verified baseline is included.
- [x] Repository/base branch/working branch are included.
- [x] Allowed files are included.
- [x] Forbidden files are included.
- [x] Checks are included.
- [x] STOP conditions are included.
- [x] Final report requirements are included.
- [x] No required execution context exists only in surrounding chat.

## Цель

Закрепить в методологии проекта правила работы review-агентов перед первым review проекта `agent-system-development`.

## Требуемые изменения

- Review-агент проверяет PR, branch, commit, diff или files и не становится исполнителем разработки без отдельной задачи.
- Review-агент не запускает Codex/Engine, не меняет очередь исполнителя и не формулирует себе implementation task.
- Запрещены model/vendor-specific branch, file и agent names, включая `claude/*`, `gpt/*`, `gemini/*`, `docs/CLAUDE_REVIEW.md`, `docs/GPT_REVIEW.md`, `docs/GEMINI_REVIEW.md`.
- Branch policy должна выбрать один вариант для review branch namespace и убрать противоречия.
- Review по умолчанию стартует от `developer`, PR, diff, branch, commit или files; `main` используется только по явному указанию пользователя.
- Review report по умолчанию возвращается в чат; сохранение в repository требует явного docs-only разрешения.
- Коммит review report допустим только docs-only и только после явного разрешения пользователя.
- Review task template должен содержать режим, объект проверки, base branch, working branch, allowed/forbidden files, commands, report format, report persistence и PR permission.
- Review report template должен использовать обязательную структуру из 10 разделов.
- Добавить анти-паттерн с `claude/initial-review` и `docs/CLAUDE_REVIEW.md`.
- Добавить безопасный пример `REVIEW-INITIAL-01`.
- Добавить обязательный блок `Локальные действия после PR/merge`.
- Создать TASK/RESULT/INDEX для этой задачи и финализировать после PR creation.

## Разрешенные файлы

- `AGENTS.md`
- `README.md`
- `docs/agent-system/**/*.md`
- `docs/agent-system/**/*.yml`
- `docs/agent-system/**/*.yaml`
- `docs/agent-system/engine-journal/**`

## Запрещенные файлы и изменения

- `.env`
- `.env.*`
- `.venv/`
- `data/`
- `runtime/`
- `dist/`
- `backups/`
- `exports/`
- production-код
- тесты
- CI
- manifests
- lock-файлы
- runtime configs

## Preflight

```powershell
git status --short
git fetch --all --prune
git branch --show-current
git rev-parse origin/developer
git rev-parse developer
git rev-parse origin/developer
```

## STOP-условия

- working tree dirty before task start;
- local `developer` diverged from `origin/developer`;
- невозможно безопасно создать рабочую ветку от актуального `developer` или `origin/developer`;
- scope требует production code, tests, CI, manifests, lock files или runtime configs;
- требуется чтение `.env` или `.env.*`;
- обнаружено требование раскрыть private data или credentials.

## Проверки результата

```powershell
git status --short
git diff --check
git diff --name-only origin/developer...HEAD
```

## Commit policy

Commit message:

```text
docs(agent-system): add review guardrails and local sync guidance
```

## PR policy

Создать PR в `developer`, если это соответствует текущему workflow.

PR description должен содержать:

```text
Task-id: METH-GUARDRAILS-01
GitHub issue: none
```

## Требования к final report

Финальный отчет должен быть на русском языке и содержать:

- что изменено;
- измененные файлы;
- где правило размещено канонически;
- где оставлены ссылки вместо дублей;
- Branch policy: итог по `review/*`;
- Review templates: статус;
- Engine journal: TASK/RESULT/INDEX;
- запущенные проверки;
- что не запускалось и почему;
- риски;
- PR URL / SHA / checks;
- локальные действия после PR/merge;
- следующий шаг: провести `REVIEW-INITIAL-01` проекта `agent-system-development` по обновленной методологии.
