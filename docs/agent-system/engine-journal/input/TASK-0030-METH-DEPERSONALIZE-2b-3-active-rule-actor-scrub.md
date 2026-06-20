# TASK-0030: METH-DEPERSONALIZE-2b-3 (active-rule actor-scrub)

## Режим

Роль: docs-maintainer.
Исполнитель: на усмотрение архитектора.
Reasoning effort: высокий.
Запуск: Local only.
Режим: docs-only, branch-guard.

Batch-closure policy действует: открытые прошлые journal-записи являются допустимым промежуточным состоянием внутри phase и не блокируют эту задачу. Closure выполняется batch перед release.

## Цель

Обезличить активные rule/workflow/policy/guide-файлы: vendor/tool actor-text заменить на роли, исторические и технические literal-строки не переписывать без необходимости.

## Discovery / Scope

Discovery выполнен командой:

```text
rg -il "chatgpt|codex|claude code" docs/agent-system --glob '!engine-journal/**'
```

Исключены:

- `docs/agent-system/engine-journal/**` как append-only история;
- `docs/agent-system/DECISION_LOG.md`;
- `docs/agent-system/CURRENT_STATE.md`;
- `docs/agent-system/RELEASE_READINESS.md`;
- `docs/agent-system/agents/**`;
- `docs/agent-system/STAGE_2_COMPLETION_CHECKLIST.md`;
- уже обезличенные adapter-документы и manifest.

Scope 2b-3:

- `docs/agent-system/ADOPTION_GUIDE.md`
- `docs/agent-system/CODE_REVIEW_WORKFLOW.md`
- `docs/agent-system/DOWNSTREAM_ADAPTATION_CHECKLIST.md`
- `docs/agent-system/ENGINE_ENTRYPOINT.md`
- `docs/agent-system/LANGUAGE_POLICY.md`
- `docs/agent-system/METHODOLOGY_FEEDBACK_LOOP.md`
- `docs/agent-system/NEW_PROJECT_ONBOARDING_GUIDE.md`
- `docs/agent-system/OPERATIONAL_FAST_LANE.md`
- `docs/agent-system/PR_WORKFLOW.md`
- `docs/agent-system/TASK_FILE_HANDOFF_CONTRACT.md`
- `docs/agent-system/WORKFLOW.md`
- `docs/agent-system/source/SOURCE_agent_system_index.md`
- `docs/agent-system/templates/ADOPTION_PROMPT.md`
- `docs/agent-system/templates/CODE_REVIEW_REPORT_TEMPLATE.md`
- `docs/agent-system/templates/NEW_PROJECT_PROMPT.md`

Size-guard не сработал: 15 файлов, точечные actor-text правки, без near-rewrite.

## Изменения

- `ChatGPT` как активный актор → `оркестратор`.
- `Codex/Engine` как активный актор → `исполнитель (engine)`.
- Vendor-specific bad examples → neutral placeholders (`tool-name`, `tool-review`, `docs/TOOL_REVIEW.md`).
- Role-agnostic task header placeholders обновлены до `<роль>` там, где это активная инструкция.
- Prohibition/safety правила сохранены по смыслу.
- Исторические/reserved файлы и прошлые journal-записи не трогались.

## Проверки

- `rg -i "chatgpt|codex|claude code" <scope files>` → ожидаемо 0.
- `rg -i "chatgpt|codex|claude|gpt|gemini|copilot" <scope files>` → ожидаемо 0.
- `git diff --name-only origin/developer...HEAD`
- `git diff --check`
- branch-guard перед commit

## STOP

- HEAD не `work/docs-maintainer-01/depersonalize-2b-3`.
- Diff выходит за scope/whitelist.
- `engine-journal/**` изменён вне новой записи 0030.
- Reserved/history files изменены.
- Size-guard срабатывает.

## Передача

Следующий: reviewer — review PR; затем архитектор — merge; затем engine — 2b-4 (history консервативно, последним); journal closure — batch перед release; release держим до завершения обезличивания и batch-closure.

Обновить Source-снапшот у зарегистрированных потребителей.
