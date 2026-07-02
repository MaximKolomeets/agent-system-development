# SOURCE_CONSUMER_REGISTRY_PRIVATE_TEMPLATE

## Назначение

Этот template предназначен для private control plane, где owner/source-steward
ведет реальные consumers методологии.

`agent-system-development` хранит только generic template. Реальные repository
names, private URLs, owner names, project aliases, internal code names и rollout
status НЕ коммитятся в public methodology repository.

## Где хранить

Хранить заполненный registry только в одном из private-safe мест:

- private downstream repository;
- private governance repository;
- private workspace notes, если они не публикуются;
- другой approved private control plane.

Не хранить заполненный registry в:

- public methodology repository;
- public PR body;
- public engine journal;
- public Source/cloud snapshot;
- публичных issue/comment/release notes.

## Registry table

| repository_alias | visibility | current_methodology_release | current_source_commit | last_update_pr | owner_role | update_status | blocked_reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `<neutral-alias>` | `<private/internal/public>` | `<tag or snapshot>` | `<sha>` | `<PR URL or private ref>` | `<role>` | `<current/pending/blocked/archived>` | `<reason or none>` |

## Поля

- `repository_alias` — neutral alias, который не раскрывает private identity.
- `visibility` — `private`, `internal` или `public`.
- `current_methodology_release` — release tag, branch snapshot или published
  Source/cloud snapshot.
- `current_source_commit` — exact methodology source commit для сверки.
- `last_update_pr` — private PR reference или `not_applicable`.
- `owner_role` — роль владельца update, например `source-steward`.
- `update_status` — `current`, `pending`, `blocked`, `archived`.
- `blocked_reason` — safe category: `waiting_release`, `local_conflict`,
  `human_decision_required`, `security_review`, `not_applicable`.

## Rules

- Не писать реальные private repository URLs.
- Не писать имена клиентов, организаций, внутренних проектов или code names.
- Не переносить private branch/worktree state в public methodology.
- Для public-safe reports использовать только counts/categories:
  `consumers_pending_count`, `blocked_count`, `adoption_status_summary`.
- Если registry нужно обсудить в public methodology PR, заменить все entries на
  synthetic/minimal examples.

## Связанные документы

- `SOURCE_CONSUMERS.md` — scaffold-only public registry в methodology repository.
- `METHODOLOGY_ADOPTION_MATRIX_PRIVATE_TEMPLATE.md` — matrix управления rollout.
- `METHODOLOGY_IMPROVEMENT_LEDGER.md` — public-safe MIR lifecycle ledger для
  sanitized improvements.
- `PUBLICATION_POLICY.md` — privacy/publication boundary.

## Передача

Следующий: source-steward — заполнить этот template только в private control
plane и отдавать в public methodology только sanitized counts/categories.
