# TASK-0057-METH-AUDIT-DOCS-NITS-01

Задача для docs-maintainer: METH-AUDIT-DOCS-NITS-01

## Рекомендуемый режим исполнения

Роль: docs-maintainer
Исполнитель: на усмотрение архитектора
Reasoning effort: средний
Запуск: Local only
Режим: Agent

## Цель

Закрыть подтверждённые docs-нити аудита DOC-01 и LANG-01, зафиксировать решения по append-only нитам HIST-01/HIST-02 без переписывания истории и read-only проверить спорные находки D12-A/B/C.

## Preconditions

- Base branch: `developer`
- Work branch: `work/docs-maintainer-01/audit-docs-nits-01`
- Перед стартом подтвердить, что PR #199 и PR #200 уже merged в `developer`.
- Подтвердить, что `python docs/agent-system/tools/gen_file_map.py --check` и `python docs/agent-system/tools/gen_cloud_bundle.py --check` проходят на текущем Windows checkout.

## Разрешённые файлы

- `docs/agent-system/LANGUAGE_POLICY.md`
- `docs/agent-system/ROLE_MODEL.md`
- `docs/agent-system/BRANCH_POLICY.md`
- `docs/agent-system/CURRENT_STATE.md`
- `docs/agent-system/NEW_PROJECT_ONBOARDING_GUIDE.md` только если D12-C подтвердится
- иные active docs с `cloud/README.md`, если найдены grep
- `docs/agent-system/cloud/**`
- `docs/agent-system/engine-journal/input/TASK-0057-METH-AUDIT-DOCS-NITS-01-audit-docs-nits.md`
- `docs/agent-system/engine-journal/output/RESULT-0057-METH-AUDIT-DOCS-NITS-01-audit-docs-nits.md`
- `docs/agent-system/engine-journal/INDEX.md`

## Проверки

- D12-A: проверить presence `PROJECT_CONSTITUTION_TEMPLATE.md` в manifest и file-map.
- D12-B: проверить tracking `STAGE_2_COMPLETION_CHECKLIST.md` в manifest и file-map.
- D12-C: проверить ссылку в `NEW_PROJECT_ONBOARDING_GUIDE.md`.
- `rg -n "cloud/README\.md"` по active docs вне journal/cloud -> 0.
- `python docs/agent-system/tools/gen_file_map.py --check`.
- `python docs/agent-system/tools/gen_cloud_bundle.py --check`.
- active internal link-check -> 0 broken.

## STOP-условия

- Dirty tree на preflight.
- PR #199 или #200 не merged в `developer`.
- D12-A/B требуют manifest/file-map изменений.
- Правка append-only history вместо фиксации решения.
- Diff выходит за allowed files.

## Передача

Следующий: reviewer — проверить PR, что DOC-01/LANG-01 закрыты, D12-A/B/C корректно классифицированы, history не переписана, оба `--check` и link-check проходят; затем архитектор — merge; затем engine — batch-closure journal 0055..0057; затем state-refresh + release-gate.
