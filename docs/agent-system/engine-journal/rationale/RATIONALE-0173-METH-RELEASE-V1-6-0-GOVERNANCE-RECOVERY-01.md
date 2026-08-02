# RATIONALE-0173-METH-RELEASE-V1-6-0-GOVERNANCE-RECOVERY-01

Связанный TASK file: `docs/agent-system/engine-journal/input/TASK-0173-METH-RELEASE-V1-6-0-GOVERNANCE-RECOVERY-01.md`
Связанный RESULT file: `docs/agent-system/engine-journal/output/RESULT-0173-METH-RELEASE-V1-6-0-GOVERNANCE-RECOVERY-01.md`
Номер sequence: 0173
Идентификатор задачи: METH-RELEASE-V1-6-0-GOVERNANCE-RECOVERY-01
authoring_role: release-manager
actor_type: agent
Статус обоснования: finalized_for_review
raw_chain_of_thought_stored: no

## Решаемый вопрос

Как восстановить governance evidence для untagged candidate `v1.6.0`, когда
release и sync уже произошли до state-refresh, UAT и reviewer gate.

## Контекст и evidence

PR #355/#356 и #360/#361 фиксируются GitHub metadata как совершившиеся
исторические facts. PR #360 перенёс payload в `main`, PR #361 выполнил
zero-file-delta sync; PR #359 закрывает boundary 0172. Tag `v1.6.0` отсутствует.

## Ограничения и инварианты

Rollback main не санкционирован. Protected branches не меняются напрямую,
UAT verdict и tag остаются human-only. Provider credential используется только
через environment; raw chain of thought не хранится.

## Рассмотренные варианты

1. Автоматически rollback main.
2. Считать `v1.6.0` опубликованным по факту payload merge.
3. Зафиксировать deviation и восстановить gates отдельным docs-only PR.

## Выбранный путь

Выбран вариант 3: append-only закрыть 0172, обновить live state, подготовить
Human UAT Checklist и передать следующий reviewer gate человеку.

## Причины выбора

Rollback менял бы уже принятый payload без отдельного human решения. Отсутствие
tag и обязательных gate evidence означает, что release нельзя честно считать
опубликованным. Новый final recovery release PR необходим, чтобы восстановленные
state и gate evidence вошли в tagged main commit.

## Отклонённые альтернативы

Не приняты переписывание PR history, ручное назначение sequence, agent approval
UAT или tag и скрытие deviation в старых документах.

## Компромиссы, последствия и риски

Main временно содержит untagged candidate. Текущая разница main/developer
включает reservation-only ledger delta; это не новый payload. До human UAT и
reviewer gate release workflow остаётся заблокированным.

## Предположения, неопределённости и confidence

GitHub metadata и complete provider snapshot доступны; confidence high для
merge facts, medium для последующей human UAT/reviewer работы, которая вне scope.

## Условия пересмотра или rollback triggers

Human architect отдельно рассматривает rollback только при новом payload risk,
failed post-merge CI или owner decision. Эта задача rollback не выполняет.

## Что явно не решалось

Не выполнялись human UAT, reviewer consistency-gate, release PR, tag, GitHub
Release, sync, policy/tooling change или новая функциональность.

## Связь с решениями

Применяются `RELEASE_AUTHORITY_POLICY.md`, `HUMAN_GATE_POLICY.md`,
`UAT_WORKFLOW.md`, `ENGINE_JOURNAL_CONTRACT.md` и
`JOURNAL_SEQUENCE_RESERVATION.md`; новых канонических решений не создаётся.

## Изменения после review

На момент materialization RATIONALE review ещё не применялся.

## Передача

Следующий: reviewer — проверить recovery state и сохранение human-only gates;
owner/PO — пройти checklist только после merge recovery PR.
