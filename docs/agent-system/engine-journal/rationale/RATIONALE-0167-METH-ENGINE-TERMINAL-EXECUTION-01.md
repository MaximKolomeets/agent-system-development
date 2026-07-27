# RATIONALE-0167-METH-ENGINE-TERMINAL-EXECUTION-01

Связанный TASK file: `docs/agent-system/engine-journal/input/TASK-0167-METH-ENGINE-TERMINAL-EXECUTION-01.md`
Связанный RESULT file: `docs/agent-system/engine-journal/output/RESULT-0167-METH-ENGINE-TERMINAL-EXECUTION-01.md`
Номер sequence: 0167
Идентификатор задачи: METH-ENGINE-TERMINAL-EXECUTION-01
authoring_role: methodology-architect-01
actor_type: agent
Статус обоснования: finalized_for_review
raw_chain_of_thought_stored: no

## Решаемый вопрос

Как закрепить самостоятельное доведение file-changing задачи до PR/CI или
объективного STOP, не ослабляя safeguards continuation и human merge.

## Контекст и evidence

Continuation policy уже ограничивает dirty scope, но не формулирует единый
terminal outcome и порядок выбора безопасного минимального действия.

## Ограничения и инварианты

Новая задача требует clean tree; continuation требует проверяемую связь и
expected dirty scope. Protected branches, secrets, private data и destructive
операции остаются human/STOP boundary.

## Рассмотренные варианты

1. Оставить terminal behaviour распределённым по нескольким документам.
2. Создать отдельную параллельную policy.
3. Расширить существующий continuation canon и дать остальным документам ссылки.

## Выбранный путь

Вариант 3: `EXECUTION_CONTINUATION_POLICY.md` становится authoritative document
для terminal execution, adaptive scope и критериев настоящего STOP.

## Причины выбора

Continuation и terminal execution управляют одной границей автономности; единый
canon уменьшает противоречия и не создаёт второй competing policy.

## Отклонённые альтернативы

Распределённое правило оставляет неясный owner; отдельный документ дублирует
scope/STOP logic.

## Компромиссы, последствия и риски

Engine получает обязанность исправлять безопасные scoped failures, но не новые
архитектурные решения; adaptive scope ограничен доказуемой технической цепочкой.

## Предположения, неопределённости и confidence

Предполагается, что RESULT/PR фиксируют added paths и evidence. Confidence: high.

## Условия пересмотра или rollback triggers

Пересмотр нужен, если terminal execution приводит к обходу validators, branch
guards или human decision boundary.

## Что явно не решалось

Не меняются CI, Docker/runtime, release/version policy и downstream repositories.

## Связь с решениями

Решение дополняет записанный continuation expected dirty scope и agent-owned
task branch workflow.

## Изменения после review

- allowlist `task_contract.scope.allowed_files` сохранён жёсткой границей:
  adaptive chain определяет необходимые paths, но не добавляет их без
  обновлённого self-contained task contract или явного scope amendment;
- `ready_for_human_review` требует успешных обязательных local checks и CI для
  final SHA;
- исчерпание `max_review_cycles` передаёт PR человеку по канону
  `REVIEW_AUTOLOOP.md`, не допуская бесконечный fix-pass.
