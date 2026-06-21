# TASK-0036 - METH-SOURCE-DELTA-RULE-01

## Задача

Задача для docs-maintainer: METH-SOURCE-DELTA-RULE-01.

Рекомендуемый режим исполнения:

Роль: docs-maintainer.
Исполнитель: на усмотрение архитектора.
Reasoning effort: высокий.
Запуск: Local only.
Режим: Agent.
Почему: требуется согласованно закрепить Source Delta в нескольких канонах и сохранить branch guard.

## Repository

- Repository: MaximKolomeets/agent-system-development
- Local path: `C:\neural\repos\agent-system-development`
- Base branch: `developer`
- Working branch: `work/docs-maintainer-01/source-delta-rule-01`
- Baseline SHA: `e375a27096361483184c593f071df94a97f8b81a`
- Checked at: `2026-06-21T16:26:42+07:00`
- Journal seq: `0036` из `INDEX.md`

## Scope

Allowed files:

- `docs/agent-system/templates/TASK_HEADER_COMMON.md`
- `docs/agent-system/ORCHESTRATOR_RESPONSE_STANDARD.md`
- `docs/agent-system/ENGINE_JOURNAL_CONTRACT.md`
- `docs/agent-system/templates/CODE_REVIEW_TASK_TEMPLATE.md`
- `docs/agent-system/engine-journal/input/TASK-0036-METH-SOURCE-DELTA-RULE-01.md`
- `docs/agent-system/engine-journal/output/RESULT-0036-METH-SOURCE-DELTA-RULE-01.md`
- `docs/agent-system/engine-journal/INDEX.md`

Forbidden:

- любые файлы вне whitelist;
- закрытие или переписывание прошлых journal-записей;
- ослабление governance/prohibition/safety правил;
- чтение `.env`;
- прямые изменения `main` или `developer`;
- commit, если HEAD не `work/docs-maintainer-01/source-delta-rule-01`.

## Required changes

1. `TASK_HEADER_COMMON.md`: добавить обязательный блок «Source Delta» для final report/RESULT/Передачи, формат таблицы, семантику рекомендаций и STOP-связь с manifest update для inventory add/delete/rename.
2. `ENGINE_JOURNAL_CONTRACT.md`: закрепить, что RESULT обязан персистить «Source Delta» в journal.
3. `ORCHESTRATOR_RESPONSE_STANDARD.md`: закрепить, что оркестратор ретранслирует Source Delta архитектору и запрашивает дополнение, если блок отсутствует.
4. `CODE_REVIEW_TASK_TEMPLATE.md`: закрепить, что reviewer сверяет Source Delta с фактическим diff и manifest.
5. RESULT-0036 должен сам содержать демонстрационный блок «Source Delta» для этой задачи.

## Checks

- Канон-согласованность: один полный формат Source Delta в `TASK_HEADER_COMMON`, остальные файлы ссылаются на этот канон.
- Source Delta dogfood в RESULT-0036.
- `git diff --name-only` в whitelist.
- `git diff --check`.
- `git rev-parse --abbrev-ref HEAD` -> `work/docs-maintainer-01/source-delta-rule-01`.

## STOP

- HEAD не `work/docs-maintainer-01/source-delta-rule-01`.
- Требуется изменить файл вне whitelist.
- Обнаружено противоречие с существующим journal, review или orchestrator contract.
- Файл Source Delta не классифицируется по manifest.

## Передача

Следующий: reviewer - review; затем архитектор - merge; затем engine - METH-FILE-MAP-GEN-01 (C-2); journal closure - batch перед release.
