# Задача для docs-maintainer: METH-RUSSIAN-COMMIT-PR-METADATA-CANON-01

Рекомендуемый режим исполнения:

Роль: docs-maintainer
Исполнитель: на усмотрение архитектора
Reasoning effort: средний
Запуск: Local only
Режим: Agent
Почему: нужно закрепить Russian-first правило не только для задач, отчётов и headings, но и для commit messages / PR title / PR body. Историю не переписываем, но методологически запрещаем повторение.
Время начала выполнения (execution_started_at) [measured/engine]: 2026-06-24T00:28:12.2805633+07:00
Время оркестрации, по факту (orchestration_time_reported) [reported/human, опционально]: не отслеживалось

## Цель

Закрепить в методологии правило: commit messages, PR titles и PR bodies должны быть Russian-first, кроме технических identifiers.

## Контекст

- Russian-first policy уже действует для задач, отчётов и headings.
- На практике commit metadata в предыдущих задачах была оформлена на английском.
- Архитектор подтвердил: текущую задачу не останавливать, английские commits текущей серии допустимы как исторический факт.
- Прошлое не переписываем; force-push/rewrite history запрещён без отдельного явного решения архитектора.

## Verified baseline

- Repository: `MaximKolomeets/agent-system-development`
- Local path: `C:\neural\repos\agent-system-development`
- Base branch: `developer`
- Baseline SHA: `167472d70b4c4fa8662b752819236d28d1c35aec`
- Working branch: `work/docs-maintainer-01/russian-commit-pr-metadata-canon-01`
- Seq: `0078`, вычислен из фактического `INDEX.md` после merge PR #224.

## Scope правок

- `docs/agent-system/LANGUAGE_POLICY.md`: раздел `Commit и PR metadata` с правилом и примерами.
- `docs/agent-system/PR_WORKFLOW.md`: checkpoint перед commit/push/PR и запрет force-push без решения архитектора.
- `docs/agent-system/ORCHESTRATOR_RESPONSE_STANDARD.md`: checklist self-contained task block требует язык commit/PR metadata.
- `docs/agent-system/templates/TASK_HEADER_COMMON.md`: общее правило metadata language в commit/push/PR policy.
- `docs/agent-system/ENGINE_JOURNAL_CONTRACT.md`: RESULT фиксирует нарушение metadata-language, если безопасно не исправлено до push.
- `docs/agent-system/ORCHESTRATOR_OPERATING_CONTRACT.md`: короткое правило в copy/paste contract.
- Journal/cloud: TASK/RESULT/INDEX и cloud regen.

## Allowed files

- `docs/agent-system/LANGUAGE_POLICY.md`
- `docs/agent-system/PR_WORKFLOW.md`
- `docs/agent-system/ORCHESTRATOR_RESPONSE_STANDARD.md`
- `docs/agent-system/templates/TASK_HEADER_COMMON.md`
- `docs/agent-system/ENGINE_JOURNAL_CONTRACT.md`
- `docs/agent-system/ORCHESTRATOR_OPERATING_CONTRACT.md`
- `docs/agent-system/engine-journal/input/TASK-0078-METH-RUSSIAN-COMMIT-PR-METADATA-CANON-01.md`
- `docs/agent-system/engine-journal/output/RESULT-0078-METH-RUSSIAN-COMMIT-PR-METADATA-CANON-01.md`
- `docs/agent-system/engine-journal/INDEX.md`
- `docs/agent-system/cloud/**`

## Forbidden

- переписывать уже merged commits;
- force-push без отдельного явного решения архитектора;
- менять `main`/`developer` напрямую;
- читать `.env`;
- печатать secrets;
- расширять scope на массовый перевод старых PR/commit сообщений;
- менять unrelated methodology content.

## Проверки

- `cmd /c "python docs\agent-system\tools\gen_file_map.py --check"`
- `cmd /c "python docs\agent-system\tools\gen_cloud_bundle.py --check"`
- `git diff --check`
- wording scan: `commit subject`, `PR title`, `PR body`, `Russian-first`
- active link-check по изменённым docs
- placeholder scan
- sensitive filename-only/count-only scan без печати matching lines
- branch-guard

## Передача

Следующий: архитектор — review/merge; затем engine — batch-closure должна включить 0078 тоже.
