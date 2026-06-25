# BRANCH_POLICY

## main

- стабильная ветка;
- изменения только через PR из `developer`;
- прямой push запрещен для агентов;
- force push запрещен.

### Обновление main (канон, правило 1)

- `main` обновляется ТОЛЬКО через release-PR `developer -> main`;
- release-PR мержит человек-архитектор (пользователь), а не агент;
- агент может ПОДГОТОВИТЬ release-PR (создать release-ветку/PR из `developer` в `main`), но НЕ мержит его и НЕ пушит в `main` напрямую;
- release-PR `developer -> main` запрещён, пока engine journal не закрыт полностью: все substantive seq, входящие в release, должны иметь closed/merged facts; lifecycle-only `terminal-fold accepted` допустим и не blocker; pre-release batch-closure обязателен по `docs/agent-system/ENGINE_JOURNAL_CONTRACT.md`;
- release-PR `developer -> main` запрещён, если `python docs/agent-system/tools/gen_file_map.py --check` не проходит: `PROJECT_FILE_MAP.md` должен быть синхронизирован с manifest и filesystem parity;
- release-PR `developer -> main` запрещён, если `python docs/agent-system/tools/gen_cloud_bundle.py --check` не проходит: `docs/agent-system/cloud/` должен иметь content-parity с manifest bundle и filesystem; `asof`/`developer_head_sha` в `cloud/00_README.md` информационные и не ломают gate при sync-merge без content-дрейфа; generated text checks следуют EOL-safe/content-oriented правилу из `docs/agent-system/ORCHESTRATOR_OPERATING_CONTRACT.md` → «Проверки generated text artifacts: content-oriented / EOL-safe»;
- перед human merge release-PR обязателен state-refresh: `CURRENT_STATE.md` и `NEXT_STEPS.md` обновлены под фактическое состояние, `docs/agent-system/cloud/**` регенерирован, оба `--check` подтверждены в state-refresh PR;
- release-PR `developer -> main` запрещён, пока не выполнен journaled reviewer consistency-gate по release payload: reviewer read-only по содержанию, с `Journal trace: always`, через ветку `work/<reviewer-role>/<task>` и docs-only PR в `developer`, подтверждает release payload, оба `--check`, сквозную закрытость substantive journal entries, допустимость accepted terminal fold и release notes по канону `docs/agent-system/ENGINE_JOURNAL_CONTRACT.md` → «Pre-release reviewer consistency-gate»;
- порядок gate: journal closed (substantive entries closed; accepted terminal fold allowed) -> batch-closure -> `gen_file_map.py --check` -> `gen_cloud_bundle.py --check` -> state-refresh -> reviewer consistency-gate -> human merge release-PR -> human annotated release tag on the resulting `main` release merge commit;
- после human merge release-PR человек-архитектор ставит annotated tag на release merge commit в `main`; агент не создаёт tag и не публикует GitHub Release. Release считается fully published только после проверки, что tag указывает на release merge commit `main`;
- для v1.0.0, если annotated tag ещё отсутствует, человек-архитектор должен поставить `v1.0.0` на release merge commit `123a126afd812255f7d671d98169c077cf33a319`; это human-only действие и не выполняется engine;
- агент не делает merge release-PR даже при наличии прав; решение о переносе в `main` принимает человек.

## developer

- интеграционная ветка;
- изменения только через итоговый PR из основной `work/<role>/<task>`;
- прямой push запрещен после bootstrap, кроме отдельного решения пользователя;
- после merge в `main` должна быть синхронизирована с `main`.

## work/<role>/<task-id>

- основная task branch агента для одной substantive task;
- одна substantive task = одна основная task branch и один итоговый PR в `developer`;
- ветка создается от актуальной `developer`;
- engine владеет task branch до состояния `ready_for_merge`, включая исправление review feedback;
- после merge итогового PR может быть удалена.

## work/<role>/<task-id>/*

- внутренние temporary/sub-branches той же задачи;
- используются только внутри namespace основной task branch, если engine нужно разложить работу на шаги;
- сливаются обратно в `work/<role>/<task-id>` до итогового PR;
- не открывают отдельные PR в `developer`, кроме отдельного явного решения пользователя;
- после использования удаляются или оставляются только как локальная диагностика до cleanup.

### Изоляция веток агентов (канон, правило 2)

- каждый агент действует ТОЛЬКО в своих ветках `work/<role>/<task>` и внутренних `work/<role>/<task>/*` своего role namespace;
- запрещено пушить, менять, force-пушить, переименовывать или удалять ветку другого агента (другого `work/<role>/*`);
- агент не строит свою работу поверх чужой непримёрженной рабочей ветки без отдельного решения пользователя;
- передача работы между агентами выполняется ТОЛЬКО через merged PR в `developer`, а не через правку чужих веток;
- если нужна работа поверх результата другого агента, сначала его PR мержится в `developer`, затем новая ветка создаётся от актуальной `developer`.

### Agent-owned task branch workflow

- orchestrator и пользователь задают цель, allowed/forbidden files, checks и STOP-условия;
- engine выполняет задачу в основной task branch и не ждет подтверждения после каждого микрошагa, пока остается в scope и не сработали STOP-условия;
- engine может создавать внутренние sub-branches в `work/<role>/<task-id>/*`, самостоятельно сливать их обратно в task branch и продолжать работу;
- reviewer проверяет итоговый PR, оставляет comments/blockers, но не создает отдельный PR для feedback без явного решения пользователя;
- review feedback исправляется в той же task branch, после чего engine повторно запускает checks и доводит PR до `ready_for_merge`;
- `developer` получает один итоговый PR по substantive task.

### Pre-commit branch guard (канон, правило 3)

- перед ЛЮБЫМ `git commit` агент проверяет текущую ветку: `git rev-parse --abbrev-ref HEAD`;
- если HEAD не его основная рабочая ветка задачи `work/<role>/<task>` и не внутренняя sub-branch `work/<role>/<task>/*` (особенно если это `developer` или `main`) → `STOP`, переключиться на правильную work-ветку и только потом коммитить;
- прямой коммит в `developer` или `main` запрещён даже локально (не только push); локальный коммит в `developer`/`main` считается нарушением, даже если он ещё не запушен;
- обоснование: инцидент journal 0013 — resume сессии оставил HEAD на `developer`, и коммит сначала лёг туда; remote `developer` уцелел только потому, что пушилась work-ветка. Проверка ветки перед commit предотвращает это.

### Repository sync / checkout guard (канон, правило 4)

Перед любым `git switch`, `git checkout`, `git pull`, `git merge`, `git rebase`, repository synchronization sequence или multi-repo sync script агент выполняет safety gate для каждого repository отдельно:

```powershell
git rev-parse --show-toplevel
git remote -v
git branch --show-current
git status --short
```

Если `git status --short` не пустой, агент пишет `STOP` и не выполняет checkout, switch, pull, merge, rebase, reset, clean или stash в этом repository.

Запрещено автоматически скрывать локальные изменения через `git stash`, `git reset --hard`, `git clean -fd`, checkout поверх локальных изменений или pull/merge поверх dirty tree без отдельного явного решения пользователя.

Для синхронизации используется только `git pull --ff-only`. Если fast-forward невозможен, агент пишет `STOP` и сообщает факты.

В multi-repo sync dirty working tree в одном repository не должен приводить к продолжению опасных действий в этом repository. Другой repository можно обрабатывать только после его отдельной проверки root/remote/branch/status.

Если нужно продолжить работу при dirty tree, пользователь принимает отдельное решение: commit, stash, discard или отдельный clean worktree.

## work/dev-implementer-01/*

- задачи разработки.

## work/solution-architect-01/*

- архитектурные исследования и предложения.

## work/qa-reviewer-01/*

- проверки качества и тестов.

## work/code-reviewer-01/*

- code review, external review и consulting review;
- review-отчеты и findings;
- не используется для исправления production-кода без отдельной implementation task.

## work/security-reviewer-01/*

- проверки безопасности.

## work/docs-maintainer-01/*

- документация и Source summaries.

## Запрещено

- force push в `main`/`developer`;
- прямой push агентами в `main`;
- прямой push агентами в `developer` после bootstrap;
- смешивать несколько независимых substantive tasks в одной основной task branch.
- использовать model/vendor-specific ветки вида `<vendor-name>/*`.

## Review branch policy

Канонический namespace для review-задач в standard developer workflow:

```text
work/<reviewer-role>/<task-id>
```

Примеры:

```text
work/code-reviewer-01/<task-id>
work/qa-reviewer-01/<task-id>
work/security-reviewer-01/<task-id>
```

Namespace `review/*` не используется как канонический branch namespace этого repository без отдельного будущего решения пользователя и обновления branch policy.

Если review-отчет разрешено сохранить в repository, это остается docs-only работой в ветке `work/<reviewer-role>/<task-id>` с PR в `developer`.
