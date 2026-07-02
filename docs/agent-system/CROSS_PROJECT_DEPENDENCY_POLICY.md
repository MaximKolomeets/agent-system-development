# CROSS_PROJECT_DEPENDENCY_POLICY

## Назначение

Policy описывает, как фиксировать и сопровождать зависимости между target
repositories, не превращая public methodology repository в control plane
конкретных проектов.

Документ хранит только нейтральные правила. Реальные project names, private
repository URLs, dependency matrix, consumers, owners и rollout status живут в
private control plane.

## Термины

- `source project` - проект, от которого зависит другой проект.
- `consumer project` - проект, который зависит от source project.
- `dependency contract` - что именно потребляется: release, API, schema,
  package, methodology version, document snapshot или governance decision.
- `version_ref` - tag, commit SHA, release id или published snapshot.
- `impact note` - нейтральная запись о влиянии изменения без private details.

## Dependency types

| Type | Что означает | Canonical evidence |
| --- | --- | --- |
| `methodology_source` | target repository использует версию методологии | `methodology_reference` с `source_ref` и `source_commit`. |
| `release_artifact` | consumer берет release/tag/source snapshot | tag, release note, checksum или snapshot metadata. |
| `api_or_schema` | consumer зависит от API/schema/contract | versioned spec или compatibility note. |
| `shared_component` | consumer использует общий компонент | package/version/commit reference. |
| `governance_dependency` | решение одного проекта влияет на другой | private decision record и redacted impact note. |
| `operational_dependency` | rollout/status одного проекта блокирует другой | private control-plane record и freshness stamp. |

## Private dependency record

Реальная запись создается только в private control plane. Нейтральная схема:

```yaml
dependency_record:
  consumer_ref: <private neutral id>
  source_ref: <private neutral id>
  dependency_type: methodology_source | release_artifact | api_or_schema | shared_component | governance_dependency | operational_dependency
  dependency_contract: <что потребляется>
  version_ref: <tag|commit|release|snapshot>
  reference_type: stable_branch_head | stable_release_tag | published_source_snapshot | explicit_contract
  owner_decision: <human decision id or note>
  visibility_scope: <who can see this record>
  freshness:
    checked_at: <ISO-8601 timestamp>
    source_head_sha: <commit-sha or not_applicable>
    stale_after: <policy>
  breaking_change_policy: <notify|block|manual review|not_applicable>
  rollback_or_fallback: <neutral fallback note>
  private_notes_location: <private control plane pointer>
```

Эта схема не коммитится в public methodology repository с реальными значениями.

## Правила

1. **Зависимость только явная.** Зависимость существует только после решения
   owner/architect. Наблюдаемая похожесть проектов не создает dependency.
2. **Требуется стабильная ссылка.** Consumer не зависит от `developer`,
   `work/*`, dirty tree или open PR branch как stable source.
3. **Видимость не транзитивна.** Если `A` зависит от `B`, это не дает доступа к
   dependencies `B` без отдельной записи.
4. **Need-to-know по умолчанию.** Consumer видит только redacted impact, который
   разрешен private control plane.
5. **Нет cross-push.** Агент одного project не пушит и не меняет ветки другого
   project без отдельной target-local task в том repository.
6. **Stale data блокирует решения.** Если `checked_at` или source SHA stale,
   dependency record нельзя использовать для release/adoption decision без
   refresh.
7. **Breaking change является human gate.** Breaking dependency change требует
   owner decision, impact note и plan для consumer adoption или rollback.
8. **Public methodology остается generic.** В public methodology repository
   возвращаются только reusable rules/patterns, без private project facts.

## Workflow: создать dependency

1. Owner/architect выбирает dependency type и consumer/source boundary.
2. Проверить, что source evidence stable: tag, commit, release или snapshot.
3. Записать private dependency record.
4. В consumer project зафиксировать только target-local reference, если это
   нужно для воспроизводимости.
5. Если dependency раскрывает private data, оставить ее только в private control
   plane.

## Workflow: изменить dependency

1. Source project готовит change note или release note.
2. Owner/architect определяет, change breaking или compatible.
3. Consumer project получает redacted impact note.
4. Adoption/update выполняется отдельной target-local task и PR.
5. RESULT фиксирует actor, evidence, version_ref и rollback/fallback.

## Workflow: закрыть dependency

1. Подтвердить closure mode по `PROJECT_CLOSURE_GUIDE.md`.
2. Проверить active consumers в private control plane.
3. Зафиксировать final stable `version_ref` или reason for termination.
4. Не удалять public docs или history, если нет отдельного human decision.
5. Передать consumer projects через redacted private note.

## Связь с consolidation

`CROSS_PROJECT_CONSOLIDATION_CONTRACT.md` описывает read-only summary layer:
`STATE_DIGEST` и `CONSOLIDATED_VIEW`. Этот policy описывает dependency layer:
кто от чего зависит и как меняется contract.

Consolidated view не заменяет dependency record. Digest может показать, что
source project stale или blocked, но не дает права менять consumer project без
target-local task и owner decision.

## STOP conditions

Остановить cross-project dependency work, если:

- реальные project names или private URLs нужно записать в public repository;
- dependency owner неизвестен;
- source reference unstable;
- visibility scope не утвержден;
- data stale, но от него зависит release/adoption decision;
- изменение breaking, но owner decision отсутствует;
- задача просит изменить другой repository без отдельного target-local scope.

## Передача

Следующий: architect или owner - вести реальные dependency records в private
control plane; в public methodology repository возвращать только generic
улучшения policy.
