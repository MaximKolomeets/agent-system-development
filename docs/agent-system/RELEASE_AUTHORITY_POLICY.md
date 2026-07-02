# RELEASE_AUTHORITY_POLICY

## Назначение

Release Authority Policy фиксирует, кто может выполнять release-sensitive
действия в methodology repository и target repositories, построенных по этой
методологии.

Канон коротко:

- агент может готовить PR, проверки, release notes, evidence summary и команды
  для человека;
- человек-архитектор принимает решение и выполняет human-only действия;
- `RESULT` фиксирует actor, действие и доказательство без secret values.

Этот документ применяется вместе с `HUMAN_GATE_POLICY.md`, `BRANCH_POLICY.md`,
`WORKFLOW.md`, `RELEASE_READINESS.md` и `NEXT_STEPS.md`.

## Authority matrix

| Действие | Кто может подготовить | Кто выполняет финальное действие | Обязательное evidence в RESULT |
| --- | --- | --- | --- |
| Merge обычного work PR в `developer` | Agent/reviewer в рамках task scope | Человек-архитектор или явно назначенный human maintainer | PR URL, head SHA перед merge или reviewed head SHA, GitHub PR state. |
| Merge release PR `developer -> main` | Agent может подготовить release branch/PR и checks | Только человек-архитектор | PR URL, merge commit SHA, `merged_at`, actor source. |
| Annotated release tag | Agent может предложить tag name и target commit | Только человек-архитектор | Tag name, tag object/target commit SHA, проверка что tag указывает на release merge commit. |
| GitHub Release / public publication | Agent может подготовить notes/checklist/draft text | Только человек-архитектор, если нет отдельного approved publication automation | Release URL или publication record, source commit/tag, actor source. |
| Sync `main -> developer` после release | Agent может подготовить sync PR и verify diff | Только человек-архитектор для merge/sync decision | Sync PR URL, merge commit SHA, `merged_at`, `developer == origin/developer` после sync. |
| Branch protection/rulesets | Agent может описать desired state и read-only findings | Только человек-архитектор или repo admin | Ruleset/protection evidence без token/secret values, timestamp, actor source. |
| CI/CD или deployment policy | Agent может предложить patch, если task scope это разрешает | Human approval обязателен; production/deploy changes human-only | PR URL, approved scope, check/deployment evidence без credentials. |
| Rollback/hotfix decision | Agent может собрать факты и подготовить rollback PR/commands | Только человек-архитектор принимает решение о rollback | Decision evidence, target commit/tag, PR/incident link без private data. |

## RESULT authority fields

Любой `RESULT`, который утверждает, что выполнено release-sensitive действие,
фиксирует:

- `release_authority_action`: короткое имя действия, например `merge_main`,
  `tag_release`, `publish_release`, `sync_main_to_developer`, `rollback`.
- `release_authority_actor_type`: `human`, `agent` или `hybrid`.
- `release_authority_actor_role`: роль, например `human architect`,
  `methodology-architect-01`.
- `release_authority_evidence`: PR URL, merge commit SHA, tag SHA, release URL,
  check run URL или другой безопасный artifact.
- `release_authority_evidence_source`: `GitHub PR metadata`, `local git`,
  `human report`, `ruleset UI screenshot reference` или другой источник.
- `release_authority_checked_at`: ISO-8601 timestamp проверки evidence.

Если действие human-only выполнено вне агента, `RESULT` пишет
`release_authority_actor_type: human` и указывает источник evidence. Агент не
должен угадывать actor identity, печатать token/secret values или утверждать
release completion без evidence.

## Gate semantics

Перед release boundary:

1. Проверить, что все substantive journal entries в release scope закрыты по
   `ENGINE_JOURNAL_CONTRACT.md`.
2. Проверить generated gates: `gen_file_map.py --check`,
   `gen_cloud_bundle.py --check`, `generated_eol_guard.py` при generated diff.
3. Проверить `check_task_ready.py --base origin/main --release-boundary`.
4. Проверить Business Acceptance Gate по `UAT_WORKFLOW.md`: Human UAT Checklist
   пройден owner/PO или помечен `not_applicable` с reason/evidence.
5. Проверить `HUMAN_GATE_POLICY.md`: нет ли human-only actions, которые агент
   пытается выполнить сам.
6. После human action зафиксировать evidence в соответствующем `RESULT` или
   boundary reconciliation RESULT.

Release-sensitive `RESULT` не считается завершенным, если он говорит
`published`, `tagged`, `synced`, `rolled back` или `main updated`, но не
фиксирует actor + evidence.

## Исключения

No silent exception. Если human-only действие нужно выполнить срочно, агент
готовит факты, команды и риски, но пишет `STOP` перед финальным действием.
Экстренность не даёт агенту права merge/tag/publish/sync/rollback без человека.

Automation может выполнять технические проверки или создавать draft artifacts,
если это явно разрешено task scope. Финальное release-sensitive действие всё
равно требует human gate, пока пользователь отдельно не утвердил другой режим.

## Передача

Следующий: human architect — выполнять human-only release actions и передавать
агенту только безопасные evidence facts для journal.
