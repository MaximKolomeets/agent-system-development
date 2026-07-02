# METHODOLOGY_IMPROVEMENT_LEDGER

## Назначение

`METHODOLOGY_IMPROVEMENT_LEDGER.md` фиксирует lifecycle sanitized methodology
improvements:

```text
feedback -> MIR -> PR -> release -> adoption
```

Ledger не является intake для raw downstream details. Raw/private feedback
сначала проходит sanitization по `DOWNSTREAM_FEEDBACK_SANITIZATION_POLICY.md`.

## Граница public ledger

Разрешено хранить:

- MIR id;
- sanitized source category;
- neutral problem pattern;
- affected methodology surface;
- status;
- methodology PR;
- release tag/snapshot;
- adoption status as aggregate/category;
- private control-plane reference как neutral id без раскрытия target identity.

Запрещено хранить:

- private repository URL;
- real consumer names;
- client/customer/project names;
- internal code names;
- target branch/worktree state;
- private PR numbers;
- secrets, credentials, `.env` values;
- raw logs, raw prompts, target source snippets или real data.

## Lifecycle statuses

| Status | Значение |
| --- | --- |
| `intake` | Sanitized feedback получен, MIR еще не сформирован. |
| `mir_candidate` | MIR candidate описан, но scope не утвержден. |
| `planned` | MIR принят в план methodology work. |
| `in_pr` | Есть methodology PR в `developer`. |
| `merged_developer` | PR merged в `developer`, но release еще не опубликован. |
| `released` | Изменение доступно через `main`, tag или published snapshot. |
| `adoption_pending` | Target adoption/update ожидает private rollout. |
| `adoption_in_progress` | Private rollout идет. |
| `adopted` | Adoption завершен по private control-plane evidence. |
| `blocked` | Нужен human decision или blocker. |
| `rejected` | MIR закрыт без изменения methodology. |

## Ledger table

| MIR id | Sanitized source | Problem pattern | Affected surface | Status | PR | Release/snapshot | Adoption status | Private control-plane ref |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `MIR-YYYY-NNN` | `<category>` | `<neutral pattern>` | `<docs/templates/tools>` | `<status>` | `<PR URL or none>` | `<tag/snapshot or none>` | `<aggregate/category>` | `<private-ref-id or none>` |

## Поля

- `MIR id` — stable id формата `MIR-YYYY-NNN`.
- `Sanitized source` — `external_review`, `target_dry_run`,
  `methodology_review`, `operator_feedback`, `audit_boundary`.
- `Problem pattern` — neutral reusable pattern без private details.
- `Affected surface` — docs/templates/tools category или exact public source
  file.
- `Status` — одно из lifecycle statuses.
- `PR` — methodology PR URL, если есть.
- `Release/snapshot` — stable release tag, `main` commit или published snapshot.
- `Adoption status` — aggregate/category, не список consumers.
- `Private control-plane ref` — neutral id, который имеет смысл только в private
  registry/matrix.

## Правило обновления

Обновлять ledger, когда:

- sanitized feedback принят как MIR candidate;
- MIR получает scope и planned status;
- открывается methodology PR;
- PR merged в `developer`;
- изменение опубликовано через `main`, release tag или snapshot;
- private adoption status меняется агрегированно.

Не обновлять ledger raw target facts. Если нужен consumer-level rollout state,
использовать private templates:

- `SOURCE_CONSUMER_REGISTRY_PRIVATE_TEMPLATE.md`;
- `METHODOLOGY_ADOPTION_MATRIX_PRIVATE_TEMPLATE.md`.

## Связь с feedback loop

`METHODOLOGY_FEEDBACK_LOOP.md` и `DOWNSTREAM_FEEDBACK_LOOP.md` описывают intake
и sanitization. Этот ledger начинается только после того, как item уже безопасен
для public methodology repository.

## Передача

Следующий: methodology-architect-01/source-steward — при новом sanitized MIR
добавить или обновить ledger row без private details и связать MIR с PR/release
adoption status.
