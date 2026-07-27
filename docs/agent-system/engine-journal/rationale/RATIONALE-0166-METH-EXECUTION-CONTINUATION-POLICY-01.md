# RATIONALE-0166-METH-EXECUTION-CONTINUATION-POLICY-01

Связанный TASK file: `docs/agent-system/engine-journal/input/TASK-0166-METH-EXECUTION-CONTINUATION-POLICY-01.md`
Связанный RESULT file: `docs/agent-system/engine-journal/output/RESULT-0166-METH-EXECUTION-CONTINUATION-POLICY-01.md`
Номер sequence: 0166
Идентификатор задачи: METH-EXECUTION-CONTINUATION-POLICY-01
authoring_role: methodology-architect-01
actor_type: agent
Статус обоснования: finalized_for_review
raw_chain_of_thought_stored: no

## Решаемый вопрос
Как отличить continuation от новой задачи без обхода guards.
## Контекст и evidence
Existing dirty-tree guard безопасен для new task, но continuation требует exact scope evidence.
## Ограничения и инварианты
Readiness, human-only merge, forbidden paths и stable reference сохраняются.
## Рассмотренные варианты
1. Всегда STOP. 2. Разрешать любой dirty tree. 3. Exact predeclared continuation.
## Выбранный путь
Вариант 3.
## Причины выбора
Он допускает только проверяемое продолжение исходной работы.
## Отклонённые альтернативы
Вариант 1 блокирует безопасную финализацию; вариант 2 небезопасен.
## Компромиссы, последствия и риски
Handoff обязан быть полнее, но неизвестный scope остаётся STOP.
## Предположения, неопределённости и confidence
Предполагается доступность branch/HEAD/status evidence. Confidence: high.
## Условия пересмотра или rollback triggers
Пересмотреть при доказанном обходе scope guard.
## Что явно не решалось
Код, CI, Docker, release и downstream не менялись.
## Связь с решениями
Policy уточняет QUALITY_FIRST и orchestrator standard.
## Изменения после review
Нет.
