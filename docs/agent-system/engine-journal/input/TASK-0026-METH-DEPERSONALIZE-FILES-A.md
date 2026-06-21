# TASK-0026-METH-DEPERSONALIZE-FILES-A

## Метаданные

- Задача: `METH-DEPERSONALIZE-FILES-A` (phase-2a: vendor-файлы -> role-based).
- Роль: docs-maintainer.
- Исполнитель: на усмотрение архитектора.
- Reasoning effort: высокий.
- Запуск: Local only.
- Base branch: `developer`.
- Work branch: `work/docs-maintainer-01/depersonalize-files-a`.
- Baseline SHA (`origin/developer`): `13d5540cb3694b8876f5ce13cb8d9d42ecca57af`.
- Timestamp (ISO-8601): `2026-06-20T14:46:54.8405243+07:00`.

## Цель

Убрать vendor-имена из имён файлов методологии (Major 1 / finding B): переименовать vendor-named файлы в role-based имена, обновить живые ссылки, manifest и содержимое переименованных файлов.

## Allowed files

- `AGENTS.md`
- `README.md`
- `docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml`
- `docs/agent-system/CROSS_PROJECT_CONSOLIDATION_CONTRACT.md`
- `docs/agent-system/CURRENT_STATE.md`
- `docs/agent-system/DECISION_LOG.md`
- `docs/agent-system/ENGINE_ENTRYPOINT.md`
- `docs/agent-system/NEXT_STEPS.md`
- `docs/agent-system/OPERATIONAL_FAST_LANE.md`
- `docs/agent-system/RELEASE_READINESS.md`
- `docs/agent-system/STAGE_2_COMPLETION_CHECKLIST.md`
- `docs/agent-system/agents/docs-maintainer-01/DOC_SYNC_REPORT.md`
- `docs/agent-system/agents/docs-maintainer-01/NEXT_CHAT_PROMPT.md`
- `docs/agent-system/templates/TARGET_PROJECT_GOVERNANCE_PACK_TEMPLATE.md`
- `docs/agent-system/ORCHESTRATOR_OPERATING_CONTRACT.md`
- `docs/agent-system/ORCHESTRATOR_RESPONSE_STANDARD.md`
- `docs/agent-system/templates/ORCHESTRATOR_RESPONSE_TEMPLATE.md`
- `docs/agent-system/ORCHESTRATOR_PROJECT_OPERATING_LAYER.md`
- `docs/agent-system/engine-journal/input/TASK-0026-METH-DEPERSONALIZE-FILES-A.md`
- `docs/agent-system/engine-journal/output/RESULT-0026-METH-DEPERSONALIZE-FILES-A.md`
- `docs/agent-system/engine-journal/INDEX.md`

## Required changes

1. Через `git mv` переименовать четыре прежних vendor-named файла в role-based имена:
   - `docs/agent-system/ORCHESTRATOR_OPERATING_CONTRACT.md`
   - `docs/agent-system/ORCHESTRATOR_RESPONSE_STANDARD.md`
   - `docs/agent-system/templates/ORCHESTRATOR_RESPONSE_TEMPLATE.md`
   - `docs/agent-system/ORCHESTRATOR_PROJECT_OPERATING_LAYER.md`
2. Обновить живые ссылки на новые role-based пути.
3. Обновить `ADOPTION_TRANSFER_MANIFEST.yml`.
4. В телах переименованных файлов обновить заголовки, самоссылки и vendor-specific формулировки.
5. Старые append-only journal `TASK/RESULT` предыдущих seq не переписывать; они являются историей.

## Checks

- Проверка старых vendor-named file identifiers вне `docs/agent-system/engine-journal/**` -> 0.
- Полная проверка старых vendor-named file identifiers допускает только append-only journal прошлых записей.
- `git diff --check`.
- Branch guard перед commit: `work/docs-maintainer-01/depersonalize-files-a`.

## Передача

Следующий: reviewer — review PR (vendor-имён в файлах/живых ссылках нет; refs целы).
