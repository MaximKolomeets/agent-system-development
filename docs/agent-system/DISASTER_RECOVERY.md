# DISASTER_RECOVERY

## Назначение

Disaster Recovery описывает действия, когда обычный repository workflow
нарушен: сломан локальный checkout, GitHub недоступен, потеряны tokens или нужно
восстановиться из release tag.

Цель: сохранить source of truth, не раскрыть secrets, не потерять branch history
и не превратить emergency в неучтенный обход `HUMAN_GATE_POLICY.md`.

## Общие принципы

- Сначала остановить изменения, потом диагностировать.
- Не читать `.env`, не печатать token values, не просить credentials в чате.
- Не выполнять `git reset --hard`, `git clean -fd`, force push или branch delete
  без explicit human decision.
- GitHub repository, protected branches, PR metadata и annotated tags остаются
  source of truth, когда GitHub доступен.
- Если GitHub недоступен, не объявлять local clone новым source of truth.
- Любой recovery RESULT фиксирует actor + evidence по
  `RELEASE_AUTHORITY_POLICY.md`, если действие release-sensitive.

## Сценарий: локальный repository сломан

Признаки:

- `git status` падает с ошибкой;
- working tree содержит непонятные conflict/lock/index errors;
- генераторы или checks не могут прочитать файлы из-за повреждения checkout;
- local branch graph не совпадает с `origin/*` и причина не ясна.

Порядок:

1. Остановить file edits.
2. Сохранить только безопасные diagnostics:

```powershell
git rev-parse --show-toplevel
git remote -v
git branch --show-current
git status --short
```

3. Если diagnostics не проходят, не лечить checkout destructive-командами.
4. Создать новый clean checkout в отдельной папке или worktree по обычному
   repository policy.
5. Сравнить `origin/main`, `origin/developer`, active PR branch и last known
   good commit.
6. Продолжать работу только в clean checkout и только после branch/status guard.

Запрещено по умолчанию:

```powershell
git reset --hard
git clean -fd
git stash
```

Эти команды допустимы только после отдельного human decision, если ясно, что
локальные изменения не нужны.

## Сценарий: GitHub недоступен

Признаки:

- `gh pr view`, `git fetch`, `git push` или GitHub UI недоступны;
- GitHub Actions не возвращают status;
- PR/merge/tag evidence нельзя проверить.

Порядок:

1. Зафиксировать outage evidence без secrets: timestamp, команда, краткий error
   class.
2. Не мержить, не публиковать и не создавать tag без GitHub evidence.
3. Если работа может продолжаться локально, вести ее в обычной work branch и
   пометить RESULT как `blocked_by_github_outage` до push/PR.
4. Если нужен emergency rollback во время outage, человек-владелец принимает
   degraded-mode decision. Agent готовит offline plan, но не объявляет recovery
   завершенным без последующей GitHub reconciliation.
5. После восстановления GitHub выполнить reconciliation: fetch, PR metadata,
   checks, tags, branch heads, journal RESULT/INDEX.

GitHub outage не является разрешением на прямой push в `main`, force push или
секретный side-channel release.

## Сценарий: tokens потеряны или скомпрометированы

Признаки:

- agent cannot authenticate;
- token accidentally exposed;
- account permissions changed unexpectedly;
- push/PR/check operations fail with auth errors.

Порядок:

1. Agent пишет `STOP`, если действие требует token.
2. Не печатать token, не просить token value, не сохранять token в repository.
3. Human admin revokes/rotates token через provider UI.
4. Human admin проверяет scopes и least privilege.
5. Agent возобновляет работу только после того, как auth восстановлен без
   раскрытия secret value.
6. RESULT фиксирует auth recovery как safe summary:
   `token_rotated_by_human`, timestamp, affected role/account class, без token
   value.

Если token мог дать доступ к production secrets, применяется также target
security incident process. Этот public methodology repository не должен
содержать private incident details.

## Сценарий: восстановление из tag

Использовать, когда нужно вернуться к известной опубликованной версии.

Порядок проверки tag:

```powershell
git fetch --tags origin
git show --no-patch --format=fuller vX.Y.Z
git rev-parse vX.Y.Z
```

Порядок safe restore:

1. Проверить, что tag `vX.Y.Z` существует и соответствует expected release.
2. Создать clean branch от `origin/main`, а не detached manual edit:

```powershell
git switch -c work/hotfix/rollback-to-vX-Y-Z origin/main
```

3. По `HOTFIX_AND_ROLLBACK_POLICY.md` построить rollback PR: revert bad merge
   commits после tag или точечный hotfix.
4. Запустить release-boundary или target-equivalent checks.
5. Провести expedited review.
6. Human architect мержит rollback PR в `main`.
7. После recovery выполнить sync/reconciliation обратно в `developer`.

Если repository настолько поврежден, что rollback PR невозможен, force move
protected branch to tag является last resort и только human/admin action.
Agent может подготовить impact note и checklist, но не выполняет force push.

## Минимальный recovery checklist

| Шаг | Вопрос | Evidence |
| --- | --- | --- |
| 1 | Что сломано: local checkout, GitHub, token, release state или tag restore? | Safe incident summary. |
| 2 | Есть ли clean source of truth? | `origin/main`, `origin/developer`, tag/PR metadata. |
| 3 | Нужен ли human-only action? | Human gate note. |
| 4 | Есть ли риск secrets/private data? | Подтверждение: secrets not read/printed. |
| 5 | Можно ли восстановиться через PR вместо force action? | PR/rollback plan. |
| 6 | Какие checks доступны? | Check run URLs или unavailable reason. |
| 7 | Кто принял решение? | Actor type/role/source. |
| 8 | Как закрывается journal? | RESULT/INDEX with evidence. |

## RESULT fields

Для disaster recovery RESULT добавляет:

- `disaster_recovery_mode`: `local_repo_broken`, `github_unavailable`,
  `token_lost`, `restore_from_tag`, `mixed`.
- `incident_summary`: нейтральное описание без private data.
- `source_of_truth_checked`: `github`, `local_git`, `human_report`,
  `not_available`.
- `github_availability`: `available`, `degraded`, `unavailable`.
- `token_status`: `not_involved`, `rotated_by_human`, `blocked`,
  `compromised_suspected`.
- `restore_tag`: tag name или `not_applicable`.
- `restore_tag_commit`: commit SHA или `not_applicable`.
- `recovery_branch`: branch name или `not_applicable`.
- `recovery_evidence`: safe PR/commit/check/tag evidence.
- `release_authority_action`: `restore_from_tag`, `rollback`, `hotfix`,
  `auth_recovery` или `not_applicable`.
- `release_authority_actor_type`, `release_authority_actor_role`,
  `release_authority_evidence`, `release_authority_evidence_source`,
  `release_authority_checked_at`.

Если recovery не дошел до PR/merge/tag, RESULT не пишет `recovered`; он пишет
`blocked`, `prepared` или `awaiting_human_action`.

## STOP conditions

Agent останавливается, если:

- recovery требует secret/token value;
- предлагается force push/reset protected branch без explicit human decision;
- невозможно определить source of truth;
- GitHub недоступен, а задача требует merge/tag/publish evidence;
- local checkout dirty перед sync/checkout/pull/merge;
- target tag не найден или не соответствует expected release;
- rollback меняет scope шире incident без owner decision.

## Передача

Следующий: human architect - принять recovery/rollback decision при human-only
действиях; agent - подготовить safe diagnostics, PR, checks и journal evidence.
