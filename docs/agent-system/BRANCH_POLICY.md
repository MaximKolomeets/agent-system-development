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
- release-PR `developer -> main` запрещён, пока engine journal не закрыт полностью: все seq, входящие в release, должны иметь closed/merged facts; pre-release batch-closure обязателен по `docs/agent-system/ENGINE_JOURNAL_CONTRACT.md`;
- release-PR `developer -> main` запрещён, если `python docs/agent-system/tools/gen_file_map.py --check` не проходит: `PROJECT_FILE_MAP.md` должен быть синхронизирован с manifest и filesystem parity;
- release-PR `developer -> main` запрещён, если `python docs/agent-system/tools/gen_cloud_bundle.py --check` не проходит: `docs/agent-system/cloud/` должен иметь content-parity с manifest bundle и filesystem; `asof`/`developer_head_sha` в `cloud/README.md` информационные и не ломают gate при sync-merge без content-дрейфа;
- перед human merge release-PR обязателен state-refresh: `CURRENT_STATE.md` и `NEXT_STEPS.md` обновлены под фактическое состояние, `docs/agent-system/cloud/**` регенерирован, оба `--check` подтверждены в state-refresh PR; порядок gate: journal closed -> batch-closure -> `gen_file_map.py --check` -> `gen_cloud_bundle.py --check` -> state-refresh -> human merge;
- агент не делает merge release-PR даже при наличии прав; решение о переносе в `main` принимает человек.

## developer

- интеграционная ветка;
- изменения только через PR из `work/<role>/*`;
- прямой push запрещен после bootstrap, кроме отдельного решения пользователя;
- после merge в `main` должна быть синхронизирована с `main`.

## work/<role>/*

- рабочие ветки задач;
- одна задача = одна ветка;
- ветка создается от актуальной `developer`;
- после merge может быть удалена.

### Изоляция веток агентов (канон, правило 2)

- каждый агент действует ТОЛЬКО в своих ветках `work/<role>/<task>` своего role namespace;
- запрещено пушить, менять, force-пушить, переименовывать или удалять ветку другого агента (другого `work/<role>/*`);
- агент не строит свою работу поверх чужой непримёрженной рабочей ветки без отдельного решения пользователя;
- передача работы между агентами выполняется ТОЛЬКО через merged PR в `developer`, а не через правку чужих веток;
- если нужна работа поверх результата другого агента, сначала его PR мержится в `developer`, затем новая ветка создаётся от актуальной `developer`.

### Pre-commit branch guard (канон, правило 3)

- перед ЛЮБЫМ `git commit` агент проверяет текущую ветку: `git rev-parse --abbrev-ref HEAD`;
- если HEAD не его рабочая ветка задачи `work/<role>/<task>` (особенно если это `developer` или `main`) → `STOP`, переключиться на правильную work-ветку и только потом коммитить;
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
- смешивать несколько независимых задач в одной ветке.
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
