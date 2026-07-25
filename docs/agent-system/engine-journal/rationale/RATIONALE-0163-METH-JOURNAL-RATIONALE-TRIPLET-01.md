# RATIONALE-0163-METH-JOURNAL-RATIONALE-TRIPLET-01

Связанный TASK file: `docs/agent-system/engine-journal/input/TASK-0163-METH-JOURNAL-RATIONALE-TRIPLET-01.md`

Связанный RESULT file: `docs/agent-system/engine-journal/output/RESULT-0163-METH-JOURNAL-RATIONALE-TRIPLET-01.md`

Номер sequence: 0163

Идентификатор задачи: METH-JOURNAL-RATIONALE-TRIPLET-01

authoring_role: methodology-architect-01

actor_type: agent

Статус обоснования: finalized_for_review

raw_chain_of_thought_stored: no

## Решаемый вопрос

Как сделать task-level rationale обязательным и проверяемым, не подменяя им DECISION_LOG и не переписывая legacy journal history.

## Контекст и evidence

Evidence: `ENGINE_JOURNAL_CONTRACT.md`, `TASK_CONTRACT.md`, `INDEX.md`, existing ready-gate и CI workflow. До запуска PR #335 был проверен и оказался merged; база `developer` синхронизирована fast-forward.

## Ограничения и инварианты

Журнал append-only, новые записи Russian-first, sequence четырёхзначный, hidden chain-of-thought и sensitive data не сохраняются, merge остаётся human-only.

## Рассмотренные варианты

1. Ретрофитить RATIONALE для всей истории.
2. Хранить rationale только в DECISION_LOG.
3. Требовать отдельный RATIONALE только для новых entries.

## Выбранный путь

Выбран вариант 3: новый filename contract и validator, legacy записи остаются историей с `legacy/not_required` semantics.

## Причины выбора

Он сохраняет достоверность истории и позволяет machine gate обнаруживать неполную или несовместимую новую тройку.

## Отклонённые альтернативы

Вариант 1 отклонён: потребовал бы выдумывать причины. Вариант 2 отклонён: DECISION_LOG фиксирует решения уровня методологии, а не контекст каждой задачи.

## Компромиссы, последствия и риски

Новая запись требует дополнительный файл и проверку. Риск sequence collision снимается повторной проверкой относительно свежего `origin/developer` перед architect-ready.

## Предположения, неопределённости и confidence

Предполагается, что новые TASK содержат machine-readable contract v2. Confidence: high.

## Условия пересмотра или rollback triggers

Пересмотреть контракт при обнаружении ложных блокировок validator или при необходимости отдельной policy для archive epoch.

## Что явно не решалось

Не выполнялись release, массовая Russian-first коррекция, branch cleanup и изменение чужих PR.

## Связь с решениями

Task-level RATIONALE дополняет, но не заменяет `DECISION_LOG.md` и decision notes; архитектурные решения продолжают фиксироваться отдельно.

## Изменения после review

Нет.

## Review addendum

Review finding: начальная migration INDEX смещала legacy mapping. Решение: явный `legacy/not_required` и schema validation. Review finding: transfer/archive lifecycle был неполным. Решение: RATIONALE включён в scaffold, target policy и archive pair. Review finding: отсутствовали regression tests. Решение: добавлен stdlib test package. raw_chain_of_thought_stored: no.

## Review addendum 03

Russian-first template исправлен. Добавлен finding `INDEX_ARTIFACTS_MISSING` для INDEX-only entry. Regression suite использует isolated temporary Git repository и `validate(root, base)`. Разрешённый rewrite: `4d241f3687df65b147146c0a4cb3e2df795d94e9` → `ffc6dfc4157e14805a3946aaf725d5c05607d9ab`. raw_chain_of_thought_stored: no.

## Review addendum 04

Проверены два актуальных finding PR #338: adoption allowlists уже разрешают `ENGINE_RATIONALE_FILE_TEMPLATE.md` и `engine-journal/rationale/RATIONALE-*.md`; legacy rows `0001–0162` уже мигрированы в 10-колоночный формат с `legacy/not_required`. Добавлена regression-проверка реального диапазона: она подтверждает 162 строки, десять колонок и отсутствие сдвига `Branch`/`PR`/`Status`/`Time` относительно позиции после RATIONALE. raw_chain_of_thought_stored: no.

## Review addendum 05

Подтверждённый blocker EOL guard: повторные Git-подпроцессы на Windows Docker bind mount. Guard переведён на пакетные final-state diff metadata, сохраняет scan scope и не выполняет прямой обход `.git`; добавлено stderr-progress logging. Тесты подтверждают смешанный verdict, ограниченное число Git-вызовов, INDEX/cloud mirror и исключение `.git` из text scope. raw_chain_of_thought_stored: no.
