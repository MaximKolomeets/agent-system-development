# CLOSURE_TASK_TEMPLATE

Самодостаточный шаблон per-task closure-only задачи для закрытия одной journal-записи после merge PR.

````text
# Задача для docs-maintainer: closure-only journal <seq> after PR #<NNN>

## Рекомендуемый режим исполнения

Роль: docs-maintainer
Исполнитель: на усмотрение архитектора
Reasoning effort: низкий
Запуск: Local only
Режим: Agent
Почему: задача меняет только journal-факты после merge и требует branch-guard.

## Режим

closure-only, docs-only, branch-guard.
Terminal: да. Эта closure-задача не требует собственной follow-up closure, если она закрывает последний PR перед release или выполняется как explicit closure gate.

## Ветки

base: <base-branch>
work: work/<role>/closure-<seq>-pr-<NNN>

## Preflight

```powershell
git rev-parse --show-toplevel
git remote -v
git status --short
git fetch --all --prune
git switch <base-branch>
git pull --ff-only origin <base-branch>
gh pr view <NNN> --json state,mergedAt,mergeCommit,headRefOid,url
git status --short
git switch -c work/<role>/closure-<seq>-pr-<NNN>
git rev-parse --abbrev-ref HEAD
```

Если HEAD не `work/<role>/closure-<seq>-pr-<NNN>` — STOP.
Если PR #<NNN> не `MERGED` — STOP и вернуть фактический state.
Если working tree dirty до создания work-ветки — STOP.

## Allowed files

Только journal-файлы закрываемой записи:

```text
docs/agent-system/engine-journal/output/RESULT-<seq>-*.md
docs/agent-system/engine-journal/INDEX.md
```

Новый TASK/RESULT не создавать.

## Изменения

- RESULT-<seq> и строку INDEX <seq> обновить фактическими merge-данными PR #<NNN>:
  - status: `merged`;
  - mergedAt;
  - merge commit SHA;
  - final head SHA;
  - PR URL;
  - `RESULT closed after merge: yes`;
  - `INDEX closed after merge: yes`;
  - `No journal placeholders: yes`;
  - safe summary checks;
  - next step after closure.
- Снять stale `open`, `not merged`, `ready for review`, `PR open`, `draft open`, `pending at file materialization`, `see Engine final report`, если они относятся к final status закрываемой записи.
- Historical task/result content не переписывать произвольно.

## Проверки

```powershell
git diff --check
git diff --name-only <base-branch>...HEAD
git rev-parse --abbrev-ref HEAD
```

`git diff --name-only <base-branch>...HEAD` должен показывать только allowed files.

## Commit / PR

```powershell
git add docs/agent-system/engine-journal/output/RESULT-<seq>-*.md docs/agent-system/engine-journal/INDEX.md
git commit -m "docs(agent-system): close journal <seq> after PR #<NNN> merge"
git push -u origin work/<role>/closure-<seq>-pr-<NNN>
gh pr create --base <base-branch> --head work/<role>/closure-<seq>-pr-<NNN> --title "docs(agent-system): close journal <seq> after PR #<NNN> merge"
```

## Final report

Вернуть на русском:

- branch;
- PR URL;
- closed seq;
- merge facts used;
- changed files;
- checks run;
- risks;
- Source-reminder: не применимо (методология не менялась);
- Передача: `Следующий: архитектор — merge closure-PR; запись <seq> закрыта`.

## STOP

- PR #<NNN> не merged;
- HEAD не work-ветка;
- diff содержит файлы вне allowed files;
- нет merge facts из GitHub и local git history;
- появились placeholders в final status.
````
