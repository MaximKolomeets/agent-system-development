# TASK-0035 - METH-MANIFEST-PARITY-01

## Задача

Задача для docs-maintainer: METH-MANIFEST-PARITY-01.

Рекомендуемый режим исполнения:

Роль: docs-maintainer.
Исполнитель: на усмотрение архитектора.
Reasoning effort: высокий.
Запуск: Local only.
Режим: Agent.
Почему: требуется классифицировать каждый файл manifest как source, target-generated, template, history/state, journal или scaffold и сохранить branch guard.

## Repository

- Repository: MaximKolomeets/agent-system-development
- Local path: `C:\neural\repos\agent-system-development`
- Base branch: `developer`
- Working branch: `work/docs-maintainer-01/manifest-parity-01`
- Baseline SHA: `13f12c83800b595a329d3386d45f38bfd73a387e`
- Checked at: `2026-06-21T16:08:29+07:00`
- Journal seq: `0035` из `INDEX.md`

## Scope

Allowed files:

- `docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml`
- `docs/agent-system/engine-journal/input/TASK-0035-METH-MANIFEST-PARITY-01.md`
- `docs/agent-system/engine-journal/output/RESULT-0035-METH-MANIFEST-PARITY-01.md`
- `docs/agent-system/engine-journal/INDEX.md`

Forbidden:

- любые файлы вне whitelist;
- закрытие или переписывание прошлых journal-записей;
- ослабление governance/prohibition/safety правил;
- чтение `.env`;
- прямые изменения `main` или `developer`;
- commit, если HEAD не `work/docs-maintainer-01/manifest-parity-01`.

## Required changes

1. В `ADOPTION_TRANSFER_MANIFEST.yml` ввести явное разделение `source` vs `target_generated`.
2. Пометить как `target_generated` target-local files, которые создаются из source templates и не ожидаются в source checkout:
   - `PROJECT_GUARDRAILS.md`
   - `ENGINE_REGISTRY.md`
   - `PROJECT_DASHBOARD.md`
   - `ROADMAP.md`
   - `RUNBOOK.md`
   - `DECISIONS.md`
   - `ADOPTION_AUDIT.md`
3. Дописать в `source` живые canonical/operational docs:
   - `README.md`
   - `CODE_REVIEW_WORKFLOW.md`
   - `CROSS_PROJECT_CONSOLIDATION_CONTRACT.md`
   - `FILE_COMMENTING_STANDARD.md`
   - `GITHUB_RULESETS.md`
   - `GITHUB_TOKEN_POLICY.md`
   - `OPERATIONAL_FAST_LANE.md`
   - `SECURITY_POLICY.md`
   - и иные canonical/operational docs из file-map, если они отсутствуют в source.
4. Явно категоризировать вне `source`:
   - `docs/agent-system/agents/**`, `docs/agent-system/source/**`, `BACKLOG.md`, `CURRENT_STATE.md`, `DECISION_LOG.md`, `NEXT_STEPS.md`, `RELEASE_READINESS.md`, `STAGE_2_COMPLETION_CHECKLIST.md` как `history_state`;
   - `docs/agent-system/engine-journal/**` как `journal`;
   - `docs/agent-system/SOURCE_CONSUMERS.md` как `scaffold`.
5. Цель parity: каждый `source` существует; каждый target-generated source template существует; каждый canonical/operational не-history file либо в `source`, либо явно в `target_generated`, `template`, `journal`, `scaffold`, `history_state`.

## Checks

- `source` -> все listed files существуют.
- `target_generated` files не ожидаются в source и не входят в `source`.
- `source_templates` для `target_generated` существуют.
- Нет неучтенных tracked canonical/operational docs в operational scope.
- `git diff --name-only` в whitelist.
- `git diff --check`.
- `git rev-parse --abbrev-ref HEAD` -> `work/docs-maintainer-01/manifest-parity-01`.

## STOP

- HEAD не `work/docs-maintainer-01/manifest-parity-01`.
- Требуется изменить файл вне whitelist.
- Файл не классифицируется однозначно.
- Working tree dirty перед sync/checkout/switch/pull/merge.

## Передача

Следующий: reviewer - review (parity = 0 расхождений); затем архитектор - merge; затем engine - METH-SOURCE-DELTA-01; journal closure - batch перед release.
