# TASK-0055-METH-AUDIT-2026-06-22-01

Задача для reviewer: METH-AUDIT-2026-06-22-01

Рекомендуемый режим исполнения:

Роль: reviewer
Исполнитель: на усмотрение архитектора
Reasoning effort: высокий
Запуск: Local only
Режим: Agent
Почему: сквозной аудит по всей методологии требует высокого reasoning и полного прохода по канонам; write-scope строго ограничен journal-артефактами и регенерацией cloud-зеркала, содержимое методологии в этой задаче не правится.

## Цель

Провести сквозной тщательный read-only аудит по ВСЕЙ методологии `agent-system-development` до подготовки release `developer -> main`, чтобы найти все несоответствия, пробелы и риски сейчас — в methodology repository — и не править их потом на downstream/боевых проектах. Задача read-only по содержимому методологии: правки не вносить, каждую находку оформить как рекомендованный отдельный fix-PR. Единственные изменения файлов — journal-артефакты этой задачи и регенерация cloud-зеркала (`docs/agent-system/cloud/**`), т.к. `INDEX` входит в `orchestrator_context_bundle`.

## Контекст

`agent-system-development` — reusable methodology/template repository. По `INDEX` журнал закрыт до seq 0054 (последняя batch-closure PR #196). Фокус — production/verification readiness. Цель пользователя: «добавить всё, что нашли, чтобы потом не править на боевых проектах», поэтому аудит исчерпывающий и завершается классифицированным списком находок и планом fix-PR.

## Verified Baseline

- Repository: `MaximKolomeets/agent-system-development`
- Local path: локальная копия (worktree work-ветки)
- Base branch: `developer`
- Working branch: `work/code-reviewer-01/meth-audit-2026-06-22-01`
- Checked branch state: `origin/developer` = `7ab42730f937ea293f84d6a025b9f94642be624e`; рабочая ветка создана от этого commit; working tree clean на preflight.
- Latest relevant PR numbers/statuses: последний work PR — #196 (seq 0054, merged); release PR #197 (`developer -> main`, merged) и sync PR #198 (`main -> developer`, merged) выполнены 2026-06-22.
- Release PR status: release/sync не выполняются в этой задаче (аудит).
- Sync PR status: не применимо.
- Verification source: local git + `gh`.
- Verification date/time: 2026-06-22T16:23:20+07:00.

## Объём аудита (14 пунктов)

1. Governance правила 1–4 (main только human-merged release-PR; изоляция `work/<role>/<task>`; pre-commit branch guard; repository sync/checkout guard).
2. Closure policy (RESULT — authoritative merge-факты; INDEX — status + PR URL без полного mergeCommit; нет недопустимых final-статусов и placeholders в active templates/contracts/checklists).
3. Целостность журнала (INDEX <-> input/output парность seq+task id; непрерывность seq; нет placeholders; журнал закрыт до последнего merged work PR).
4. Parity-гейты: `gen_file_map.py --check` и `gen_cloud_bundle.py --check`.
5. Source Delta и Orchestrator context handoff закреплены во всех релевантных templates/contracts.
6. Russian-first / LANGUAGE_POLICY в active operational docs/заголовках/шапках.
7. Перекрёстные ссылки между канонами (битые ссылки в действующих доках; append-only история исключается).
8. Adoption-шаблоны <-> категории manifest.
9. Безопасность/санитизация (нет секретов/`.env`/private data/private repo URL; нейтральность feedback; engine-journal scaffold `.gitkeep`).
10. Vendor-neutrality (нет vendor/tool-имён как role/branch/task-id/report filename).
11. Полнота шаблонов (все templates, на которые ссылаются каноны, существуют).
12. methodology_reference (repository/source_branch/source_commit/checked_at/reference_type; commit SHA — обязательный anchor).
13. Operating-layer контракты + раздел «Три слоя управления».
14. State docs freshness pattern (standing/current pointer vs volatile task-факты; release-gate state-refresh).

## Разрешённые файлы (только эти)

- `docs/agent-system/engine-journal/input/TASK-0055-METH-AUDIT-2026-06-22-01-full-methodology-audit.md` (создать);
- `docs/agent-system/engine-journal/output/RESULT-0055-METH-AUDIT-2026-06-22-01-full-methodology-audit.md` (создать);
- `docs/agent-system/engine-journal/INDEX.md` (одна строка);
- `docs/agent-system/cloud/**` (регенерация ТОЛЬКО через `python docs/agent-system/tools/gen_cloud_bundle.py`).

## Запрещённые файлы и действия

- любой иной content методологии (канон-доки, templates, contracts, governance, source-снапшоты, `tools/*`) — НЕ править; находки выносить в отдельный fix-PR;
- прямые изменения `main`/`developer`; подготовка/merge release `developer -> main`;
- runtime, CI/GitHub Actions, Docker, секреты, `.env`, private downstream data;
- удаление/перезапись существующих TASK/RESULT (append-only);
- force push; прямой push в `developer`/`main`.

## Проверки

- `python docs/agent-system/tools/gen_file_map.py --check`;
- `python docs/agent-system/tools/gen_cloud_bundle.py --check`;
- INDEX <-> input/output парность (seq + task id);
- нет unresolved placeholders в active доках;
- sensitive grep — filename-only, без копирования matching lines/значений.

## STOP-условия

- dirty working tree на preflight;
- fast-forward невозможен или HEAD != origin/developer после pull;
- невозможно получить commit SHA для methodology_reference (зафиксировать blocker);
- задача потребовала бы изменить content методологии или сделать release — STOP, оформить как рекомендованный fix/release-шаг;
- риск forbidden/secret data;
- любой `--check` падает -> не «чинить» втихую: зафиксировать как blocker-finding, journal/cloud-изменения оставить консистентными.

## Требования к финальному отчёту (русский)

- Сводка audit; классификация находок (blocker/major/minor/nit) с fix-PR на каждую группу; результаты обоих `--check`; блок «Source Delta»; строка «Архитектору — загрузить в контекст оркестратора: …» с numbered cloud-именами; подтверждения (RESULT/INDEX finalized, no placeholders, Journal trace: always, Report delivery: chat); блок «Передача»; блок «Локальные действия после PR/merge» при необходимости.

Канон шапки и сквозных правил: `docs/agent-system/templates/TASK_HEADER_COMMON.md`.
