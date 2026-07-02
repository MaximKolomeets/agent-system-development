# HOTFIX_AND_ROLLBACK_POLICY

## Назначение

Этот документ задает порядок emergency hotfix и rollback для methodology
repository и target repositories, которые приняли эту методологию.

Канон коротко:

- rollback/hotfix decision является human-only действием по
  `HUMAN_GATE_POLICY.md`;
- агент может собрать факты, подготовить ветку, PR, checklist, команды и
  evidence summary, но не мержит в `main` и не двигает release tag;
- emergency не отменяет `RELEASE_AUTHORITY_POLICY.md`: `RESULT` фиксирует
  actor, действие и безопасное evidence;
- rollback до tag `vX.Y.Z` выполняется как проверяемый rollback plan от текущего
  `main`, обычно через revert-коммиты и PR, а не через silent force push.

## Когда применять

Применять этот policy, если есть один из trigger:

- после release обнаружен blocker, regression, security issue или broken
  publication surface;
- нужно откатить поведение до известного release tag `vX.Y.Z`;
- нужно срочно отменить bad merge commit;
- GitHub release, documentation bundle, target adoption bundle или public docs
  содержат ошибку, требующую ускоренного пути;
- владелец явно сказал "hotfix", "rollback", "restore to tag" или "emergency".

Не применять как замену обычному release flow, если нет срочности: тогда идти
через обычный `developer -> main` release boundary.

## Authority

| Действие | Кто готовит | Кто выполняет финально | Evidence |
| --- | --- | --- | --- |
| Признать incident rollback/hotfix | Агент собирает факты и варианты | Только человек-владелец/архитектор | Incident summary, affected commit/tag/PR, risk note. |
| Создать `work/hotfix/<issue>` branch и rollback PR | Агент или human maintainer по task scope | Агент может подготовить PR; merge human-only | Branch, PR URL, reverted SHA, checks. |
| Merge hotfix/rollback PR в `main` | Агент готовит evidence | Только человек-владелец/архитектор | PR URL, merge commit SHA, actor source. |
| Annotated tag after hotfix | Агент предлагает tag/target | Только человек-владелец/архитектор | Tag name, target SHA, tag evidence. |
| Force move `main` to tag | Агент не выполняет | Только repo owner/admin, как last resort | Explicit human decision, backup, incident record. |

Ссылка на H9: все release-sensitive поля берутся из
`RELEASE_AUTHORITY_POLICY.md`:

- `release_authority_action`;
- `release_authority_actor_type`;
- `release_authority_actor_role`;
- `release_authority_evidence`;
- `release_authority_evidence_source`;
- `release_authority_checked_at`.

## Branch model

Emergency branch namespace:

```text
work/hotfix/<issue>
```

`<issue>` должен быть коротким, нейтральным и без private data, например:

```text
work/hotfix/revert-bad-release-note
work/hotfix/rollback-to-v1-5-1
work/hotfix/security-doc-patch
```

Правила:

- ветка создается от текущего `origin/main`, если hotfix должен попасть прямо в
  stable surface;
- ветка не создается поверх `developer`, если цель - срочный rollback `main`;
- после merge в `main` обязательно готовится sync path обратно в `developer`
  через human-controlled sync PR или обычную синхронизацию по branch policy;
- один incident = одна `work/hotfix/<issue>` branch и один emergency PR;
- прямой push в `main`, force push и tag creation агентом запрещены.

## Emergency rollback через revert

Основной путь rollback - PR с revert-коммитом.

Минимальная последовательность:

```powershell
git status --short
git fetch --all --prune
git switch -c work/hotfix/<issue> origin/main

# Для обычного commit:
git revert <bad-commit-sha>

# Для merge commit:
git revert -m 1 <bad-merge-sha>
```

Операторская памятка "git revert `<bad-merge-sha>`" означает: проверить, merge
это или обычный commit. Для merge commit использовать `-m 1`, потому что parent
1 должен оставаться mainline.

После revert:

```powershell
python docs/agent-system/tools/check_task_ready.py --base origin/main --release-boundary
git diff --check origin/main...HEAD
```

Если repository не содержит этих tools, target repository использует свои
эквивалентные tests/checks, указанные в target `BRANCH_POLICY.md` и CI.

## Откат до tag vX.Y.Z

Rollback "до уровня tag" не означает silent reset protected branch. Безопасный
путь:

1. Человек-владелец выбирает target tag, например `vX.Y.Z`.
2. Агент проверяет tag и first-parent commits после него:

```powershell
git fetch --tags origin
git show --no-patch --format=fuller vX.Y.Z
git log --oneline --first-parent vX.Y.Z..origin/main
```

3. Создается branch от `origin/main`:

```powershell
git switch -c work/hotfix/rollback-to-vX-Y-Z origin/main
```

4. Revert выполняется для bad merge commits после tag, обычно от newest к
   oldest, пока content/evidence не совпадут с требуемым уровнем.
5. PR проходит ускоренный review и проверки.
6. Человек-владелец мержит PR в `main`.
7. RESULT фиксирует target tag, target commit SHA, reverted SHA list,
   reviewer evidence, merge evidence и actor.

Last resort: force move `main` to tag допускается только при отдельном explicit
human decision, подтвержденном backup/evidence. Агент не выполняет force push и
не предлагает его как стандартный путь.

## Ускоренный review

Emergency review может быть короче обычного, но не пустым.

Минимум:

- reviewer проверяет, что rollback scope равен incident scope;
- reviewer сверяет bad SHA, target tag/commit и diff;
- generated/docs checks или target-equivalent checks проходят;
- PR body содержит incident summary, rollback plan, risk note и rollback
  verification;
- owner/architect принимает final merge decision.

Если checks недоступны из-за outage, RESULT фиксирует:

- какие checks не прошли из-за недоступности инфраструктуры;
- какие ручные проверки выполнены;
- кто принял human risk decision.

## Checklist для не-программиста

Использовать как ручную памятку owner/PO/архитектора.

| Шаг | Что сделать | Evidence |
| --- | --- | --- |
| 1 | Остановить дальнейшие release/publish действия. | Сообщение в incident/update thread. |
| 2 | Назвать проблему простыми словами: что сломано и кого затрагивает. | Incident summary без private data. |
| 3 | Выбрать вариант: revert bad merge или rollback до tag `vX.Y.Z`. | Decision note: chosen path and reason. |
| 4 | Убедиться, что агент не просит secrets и не предлагает force push как обычный путь. | Human gate note. |
| 5 | Проверить PR title/body: есть bad SHA, target tag, checks и risk note. | PR URL. |
| 6 | Дождаться минимального review/checks. | Reviewer comment/status checks. |
| 7 | Смержить PR в `main` только если решение принято человеком. | Merge commit SHA, actor source. |
| 8 | Проверить, что `main` указывает на ожидаемый fixed state. | `gh pr view`, `git rev-parse origin/main`, tag/commit evidence. |
| 9 | Запланировать sync обратно в `developer`. | Sync PR URL или follow-up task. |
| 10 | Закрыть RESULT/incident facts. | RESULT fields with actor + evidence. |

## RESULT fields

Для hotfix/rollback RESULT добавляет или явно заполняет:

- `incident_id`: нейтральный короткий ID или PR/issue URL.
- `hotfix_branch`: `work/hotfix/<issue>`.
- `rollback_mode`: `revert_bad_commit`, `revert_to_tag`, `docs_hotfix`,
  `manual_recovery`.
- `rollback_target_tag`: `vX.Y.Z` или `not_applicable`.
- `rollback_target_commit`: commit SHA target tag или expected fixed commit.
- `bad_commit_sha`: commit или merge SHA, который откатывается.
- `bad_merge_parent_policy`: `mainline_parent_1` для merge revert или
  `not_applicable`.
- `rollback_command_evidence`: safe command summary без secrets.
- `review_evidence`: reviewer comment/check URL или human report.
- `merge_evidence`: PR URL, merge commit SHA, `merged_at`, actor source.
- `release_authority_action`: `rollback`, `hotfix` или `restore_from_tag`.
- `release_authority_actor_type`: `human`, `agent` или `hybrid`.
- `release_authority_actor_role`: role/source, например `human architect`.
- `release_authority_evidence`: PR URL, merge commit SHA, tag SHA или
  incident record.
- `release_authority_evidence_source`: `GitHub PR metadata`, `local git`,
  `human report` или другой безопасный source.
- `release_authority_checked_at`: ISO-8601 timestamp.

Если rollback decision уже принят человеком вне agent session, RESULT не
угадывает личность. Он пишет `release_authority_actor_type: human` и фиксирует
доступный evidence source.

## STOP conditions

Agent пишет `STOP` и не продолжает rollback/hotfix action, если:

- нужен direct push в `main`;
- нужен force push/reset protected branch;
- нужно создать/переместить release tag;
- нужно прочитать или напечатать secrets/tokens;
- target tag неизвестен или не проверен;
- bad SHA не найден в expected branch history;
- revert конфликтует и требует product/domain decision;
- reviewer/owner decision отсутствует, а действие release-sensitive;
- GitHub недоступен и нет human decision на offline degraded mode.

## Передача

Следующий: human architect - принять final rollback/hotfix decision и выполнить
human-only merge/tag/publish действия; agent - готовить PR, checks и безопасное
evidence.
