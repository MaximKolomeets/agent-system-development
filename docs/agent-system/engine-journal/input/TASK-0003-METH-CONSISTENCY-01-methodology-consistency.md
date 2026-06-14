# TASK-0003-METH-CONSISTENCY-01-methodology-consistency

## Задача для docs-maintainer-01: METH-CONSISTENCY-01

Рекомендуемый режим engine:

Запуск: Local only
Engine: Claude Code (или иной docs-capable engine)
Модель: docs-capable engine
Reasoning: Medium
Режим: Agent, file-changing, строгий allowed-files whitelist
Почему: цель узкая — снять документационные рассинхроны после `REVIEW-INITIAL-01` и привести документацию к фактическому состоянию после `METH-OPERABILITY-01`; методология по сути не меняется.

## Verified baseline

- Repository: `MaximKolomeets/agent-system-development`
- Local path: `C:\neural\repos\agent-system-development`
- Base branch: `developer`
- Base commit: `f45fe5fb539e9e2de7c24b090c7f7902230d21d0`
- Working branch: `work/docs-maintainer-01/methodology-consistency`
- Task source: пользовательский attachment `METH-CONSISTENCY-01`
- Source отчёта правок: `REVIEW-INITIAL-01` (вердикт Hold, минорные docs-правки)
- Baseline verification source: local git
- Baseline verification date/time: `2026-06-14`

## Methodology reference

```yaml
methodology_reference:
  repository: MaximKolomeets/agent-system-development
  source_branch: developer
  source_commit: f45fe5fb539e9e2de7c24b090c7f7902230d21d0
  checked_at: 2026-06-14
  reference_type: commit
  notes: "Стартовая точка после PR #100 sync main -> developer."
```

## Цель

Привести документацию repository в соответствие с фактическим состоянием после закрытия `METH-OPERABILITY-01` и устранить рассинхроны из `REVIEW-INITIAL-01`. Ожидаемый результат — один docs-only PR в `developer`. Методология по сути не меняется; scope не расширяется сверх указанных findings.

## Allowed files

- `docs/agent-system/CURRENT_STATE.md`
- `docs/agent-system/source/SOURCE_agent_system_index.md`
- `docs/agent-system/CODE_REVIEW_WORKFLOW.md`
- `docs/agent-system/templates/CODE_REVIEW_REPORT_TEMPLATE.md`
- `docs/agent-system/templates/CODE_REVIEW_TASK_TEMPLATE.md`
- `docs/agent-system/GITHUB_TOKEN_POLICY.md`
- `.gitignore`
- engine journal: `TASK-0003`, `RESULT-0003`, `INDEX.md` (следующий порядковый номер; RESULT прошлых задач не редактировать)

## Forbidden files

- любые файлы вне whitelist;
- `.env`, `.env.*`, `.venv/`, `data/`, `runtime/`, `dist/`, `backups/`, `exports/`;
- прямые изменения `main` и `developer`;
- редактирование RESULT прошлых задач;
- Docker, production scripts, установка зависимостей;
- удаление untracked артефактов пользователя, включая `branch_cleanup_verify_log.txt`;
- расширение задачи до методологических изменений.

## Изменения по findings

1. `CURRENT_STATE.md`: `METH-OPERABILITY-01` → merged/closed; `REVIEW-INITIAL-01` → завершён; поля «Текущий этап» и «Следующий шаг» в соответствие с фактом и `NEXT_STEPS.md`.
2. `source/SOURCE_agent_system_index.md`: устранить drift тела относительно header — сократить до навигационного индекса, зафиксировать GitHub как source of truth, удалить устаревшие поля «Текущий этап»/«Следующий шаг».
3. Vendor-neutral heading: `## 9. Кандидаты на будущие задачи Codex/Engine` → `## 9. Кандидаты на будущие задачи Engine` в `CODE_REVIEW_WORKFLOW.md`, `CODE_REVIEW_REPORT_TEMPLATE.md`, `CODE_REVIEW_TASK_TEMPLATE.md` (только heading).
4. `GITHUB_TOKEN_POLICY.md`: добавить two-mode нюанс (solo-operator — recommended hardening; multi-agent governed — обязателен), согласовано по смыслу с `AGENTS.md` (`AGENTS.md` не менять).
5. `.gitignore`: добавить узкий паттерн `*_verify_log.txt` (без широкого `*_log.txt`).

## Проверки

- `git status --short --untracked-files=all`
- `git diff --name-only`
- `git diff --check`
- `git grep -n '^## .*Codex/Engine' -- docs`
- `git grep -n 'METH-OPERABILITY-01' -- docs/agent-system/CURRENT_STATE.md docs/agent-system/source/SOURCE_agent_system_index.md`

## STOP-условия

- origin не `MaximKolomeets/agent-system-development`;
- нет ветки `developer`; `developer` расходится с `origin/developer`;
- рабочее дерево не clean, кроме `branch_cleanup_verify_log.txt`;
- требуются правки вне whitelist;
- найден секрет (значение не печатать);
- задача требует изменения методологии по сути;
- конфликт с Russian-first;
- невозможно определить journal convention/следующий номер без риска перезаписи;
- `git push` невозможен без ввода credentials в среде engine.

## Commit / push / PR

- Один commit: `docs(agent-system): align methodology consistency docs`.
- Push в `work/docs-maintainer-01/methodology-consistency`.
- PR в `developer` через `gh`, если доступен и авторизован; иначе PR создаёт пользователь по переданной команде/URL (не ошибка).

## Требования к final report

Russian-first; что изменено по пунктам 1-5; branch; commit SHA; PR URL или пометка «PR создаёт пользователь» + команда/URL; список файлов; выполненные проверки; был ли `gh` доступен; подтверждение, что вне whitelist ничего не тронуто, `.env` не читался, Docker не запускался.
