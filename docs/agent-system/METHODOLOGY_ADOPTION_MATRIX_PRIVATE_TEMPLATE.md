# METHODOLOGY_ADOPTION_MATRIX_PRIVATE_TEMPLATE

## Назначение

Этот template описывает private adoption cockpit: какие target repositories
используют какую версию methodology и какие updates ожидают adoption.

В public methodology repository хранится только template. Заполненная matrix с
реальными consumers, repository names, private URLs, project aliases и rollout
state живет только в private control plane.

## Matrix

| project_alias | current_methodology_tag | current_source_commit | last_source_sync | local_divergences | pending_update_pr | blockers | next_action | owner_role |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<neutral-alias>` | `<tag or snapshot>` | `<sha>` | `<date/sha>` | `<none/category>` | `<private PR ref or none>` | `<none/category>` | `<safe next action>` | `<role>` |

## Поля

- `project_alias` — нейтральный alias, не раскрывающий private identity.
- `current_methodology_tag` — stable release tag или snapshot id.
- `current_source_commit` — exact source commit methodology repository для сверки.
- `last_source_sync` — дата/SHA последней синхронизации.
- `local_divergences` — safe category: `none`, `target_policy_override`,
  `local_branch_model`, `deferred_adoption`, `unknown`.
- `pending_update_pr` — private PR reference или `none`.
- `blockers` — safe category: `none`, `human_decision_required`,
  `release_not_available`, `target_conflict`, `security_review`.
- `next_action` — один следующий безопасный шаг.
- `owner_role` — роль владельца adoption/update.

## Rollup summary for public reports

Если public methodology PR должен упомянуть adoption state, использовать только
агрегаты:

| Metric | Value |
| --- | --- |
| consumers_current_count | `<number>` |
| consumers_pending_count | `<number>` |
| consumers_blocked_count | `<number>` |
| unknown_state_count | `<number>` |
| next_release_required | `<yes/no>` |

Не переносить consumer list, private repository URLs, branch names, private PR
numbers, internal aliases или target-specific blockers в public docs.

## Правило update

Обновлять matrix после:

- methodology release tag;
- published Source/cloud snapshot;
- target adoption/update PR;
- обнаружения blocker;
- human decision по adoption pause/rollback.

## Связанные документы

- `SOURCE_CONSUMER_REGISTRY_PRIVATE_TEMPLATE.md`;
- `METHODOLOGY_IMPROVEMENT_LEDGER.md`;
- `STABLE_METHODOLOGY_REFERENCE_POLICY.md`;
- `TARGET_ADOPTION_DETECTOR.md`;
- `DOWNSTREAM_ADAPTATION_CHECKLIST.md`;
- `PUBLICATION_POLICY.md`.

## Передача

Следующий: source-steward — вести matrix только в private control plane и
публиковать наружу только sanitized rollup summary.
