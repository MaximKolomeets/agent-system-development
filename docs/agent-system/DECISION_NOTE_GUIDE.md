# DECISION_NOTE_GUIDE

## Назначение

Decision note guide отделяет обычную строку в `DECISION_LOG.md` от отдельного
документа решения. Цель - не превращать каждый мелкий выбор в ADR, но иметь
достаточно структуры для крупных продуктовых, стековых, governance и Level 3/4
решений.

## Строка в DECISION_LOG

Использовать строку или короткий раздел в `DECISION_LOG.md`, когда решение:

- локально для methodology/workflow;
- не меняет product architecture level;
- не требует сравнения нескольких существенных вариантов;
- не вводит новый owner approval boundary;
- может быть понято по `date / decision / reason / consequences`.

`DECISION_LOG.md` остается append-only. Исторические решения не переписываются
ради нового формата.

## Отдельная decision note

Создавать отдельный decision note, когда решение:

- крупное продуктовое, архитектурное, стековое или governance-level;
- имеет несколько реальных alternatives/trade-offs;
- меняет Level 3/4 authority, scope expansion или compliance boundary;
- должно быть прочитано target repository отдельно от полного history log;
- требует явного owner approval через PR.

Рекомендуемые поля:

- `status`: `proposed`, `accepted`, `deprecated`, `superseded`;
- `decision`;
- `context`;
- `options_considered`;
- `reason`;
- `consequences`;
- `approval`;
- `follow_up_actions`;
- `links`: PR, DECISION_LOG entry, related policy/control IDs.

## Level 3/4 approval

Level 3/4 decision до approval имеет статус `proposed`. Owner approval
фиксируется через PR review/comment или другой явный repository-approved
artifact, определенный target instructions.

После merge фактический approve фиксируется в `DECISION_LOG.md`:

- date;
- PR URL или decision note path;
- approver role/name, если policy target repository это разрешает;
- итоговый статус `accepted`.

Если approval не получен, decision note не должна описывать решение как
accepted. Она остается `proposed` или получает `rejected/deferred` с причиной.

## Связь с governance patterns

- `POLICY_STATUS_PATTERN.md` использует decision note, когда изменение статуса
  policy меняет authority или blocking behavior.
- `ERROR_CATALOG_PATTERN.md` обычно не требует отдельной decision note для
  добавления codes, но может требовать ее при смене severity model или
  blocking semantics.
- `CONTROL_MATRIX_PATTERN.md` может ссылаться на decision note как source для
  hard-инварианта.
- `TARGET_PROJECT_GOVERNANCE_PACK.md` включает decision note как target-local
  artifact для крупных решений.

## Review checklist

- Крупное решение не спрятано только в PR body или RESULT.
- Обычное решение не раздуто в отдельный документ без причины.
- Level 3/4 decision не помечено `accepted` до owner approval.
- DECISION_LOG содержит короткую ссылку на accepted decision note после merge.
- Decision note не содержит private data, client data, private repository URLs
  или target-specific sensitive details в public methodology repository.
