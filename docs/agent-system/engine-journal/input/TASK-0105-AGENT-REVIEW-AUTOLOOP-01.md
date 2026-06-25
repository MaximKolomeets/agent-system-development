# TASK-0105 — AGENT-REVIEW-AUTOLOOP-01

execution_started_at: `2026-06-25T18:01:37.0029226+07:00`

## Режим

Роль: methodology-architect-01  
Исполнитель: на усмотрение архитектора  
Reasoning effort: высокий  
Запуск: Local only  
Режим: Agent

## Цель

Добавить в methodology модель автоматизированного bounded review/fix цикла:

`Engine PR -> Reviewer review -> Engine fix-pass -> Reviewer re-review -> architect-ready`.

## Требования

- Reviewer не создаёт отдельный PR.
- Reviewer оставляет feedback только в PR агента.
- Engine исправляет feedback в той же task branch.
- Цикл ограничен `max_review_cycles`.
- После reviewer approve PR получает статус/label `architect:ready-to-merge`.
- Merge в `developer` остаётся только за человеком.
- При conflict, secrets-risk, forbidden paths, failed checks или превышении max cycles automation останавливается и передаёт PR человеку.

## Ожидаемый результат

- `docs/agent-system` описывает state-machine review loop.
- Добавлены recommended labels/statuses.
- Добавлены шаблоны для reviewer и engine fix-pass.
- Добавлены STOP-условия.
- Добавлен пример local orchestrator/self-hosted runner flow.
- Safety gates не ослаблены.

## Ограничения

- Не менять `main`/`developer` напрямую.
- Не читать `.env`.
- Не выводить secrets.
- Не ослаблять branch protection, human-only merge и forbidden-path gates.
- Не создавать отдельный reviewer feedback PR.

## Проверки

- `python docs/agent-system/tools/gen_file_map.py --check`
- `python docs/agent-system/tools/gen_cloud_bundle.py --check`
- `git diff --check`
- Scan по `max_review_cycles`, `architect:ready-to-merge`, `automation:stopped-human-required`.
- Filename/count-only sensitive scan без вывода matching secret values.

