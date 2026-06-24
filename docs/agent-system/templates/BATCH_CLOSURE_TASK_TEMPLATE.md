# BATCH_CLOSURE_TASK_TEMPLATE

Самодостаточный шаблон pre-release batch-closure задачи для закрытия нескольких merged-but-unclosed journal-записей одним PR.

````text
# Задача для docs-maintainer: pre-release batch-closure journal <seq-range>

## Рекомендуемый режим исполнения

Роль: docs-maintainer
Исполнитель: на усмотрение архитектора
Reasoning effort: средний
Запуск: Local only
Режим: Agent
Почему: задача сверяет GitHub merge facts с RESULT closure-stamps и закрывает только journal перед release.
Время начала выполнения (execution_started_at) [measured/engine]: <ISO-8601 timestamp with timezone>
Время оркестрации, по факту (orchestration_time_reported) [reported/human, опционально]: <свободное значение или пусто>

## Режим

batch-closure-only, docs-only, branch-guard.
Terminal: да. Запускается перед release `developer -> main`.

Собственная batch-closure запись после merge становится lifecycle-only `terminal-fold accepted`; она не порождает следующую closure-задачу только ради own terminal fold.

## Ветки

base: <base-branch>
work: work/<role>/batch-closure-<seq-range>

## Preflight

```powershell
git rev-parse --show-toplevel
git remote -v
git status --short
git fetch --all --prune
git switch <base-branch>
git pull --ff-only origin <base-branch>
git status --short
git switch -c work/<role>/batch-closure-<seq-range>
git rev-parse --abbrev-ref HEAD
```

Если HEAD не `work/<role>/batch-closure-<seq-range>` — STOP.
Если working tree dirty до создания work-ветки — STOP.

## Discovery

1. Прочитать `docs/agent-system/engine-journal/INDEX.md`.
2. Найти все substantive seq в диапазоне `<seq-range>`, где PR уже merged, но `RESULT` не содержит closure-stamp или `INDEX` не содержит закрытый status + PR URL. Lifecycle-only `terminal-fold accepted` не включать в closure-set.
3. Для каждого PR выполнить:

```powershell
gh pr view <NNN> --json state,mergedAt,mergeCommit,headRefOid,url
```

Если любой PR из closure-set не `MERGED` — STOP и вернуть список незакрываемых seq.

## Allowed files

Только journal-файлы закрываемых записей и собственная запись batch-closure:

```text
docs/agent-system/engine-journal/input/TASK-<batch-seq>-*.md
docs/agent-system/engine-journal/output/RESULT-<batch-seq>-*.md
docs/agent-system/engine-journal/output/RESULT-<closed-seq>-*.md
docs/agent-system/engine-journal/INDEX.md
```

Новый TASK/RESULT создавать только для самой batch-closure задачи. Для закрываемых seq новые TASK/RESULT не создавать.

## Изменения

Для каждого закрываемого seq:

- В RESULT-<seq> добавить closure-stamp с фактическими merge-данными соответствующего PR:
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
- В строке INDEX <seq> обновить только status + PR URL и safe one-line summary; optional mergedAt date допустима для навигации. Полный merge commit SHA в INDEX не дублировать: авторитетные merge-факты находятся в RESULT closure-stamp.
- Снять stale `open`, `not merged`, `ready for review`, `PR open`, `draft open`, `pending at file materialization`, `see Engine final report`, если они относятся к final status закрываемой записи.
- Очистить final-state surfaces для каждого закрываемого seq: верхний status-marker закрываемого RESULT привести к closed-статусу, согласованному с closure-stamp. Lifecycle-only terminal INDEX summary переводить в `terminal-fold accepted; PR URL authoritative; not release/reviewer blocker`, без self-reference на собственный head SHA.
- Historical task/result content не переписывать произвольно.

Для собственной batch-closure записи:

- seq взять из актуального INDEX на момент выполнения;
- TASK/RESULT/INDEX создать и финализировать после PR creation;
- RESULT перечисляет closure-set, PR facts source, baseline SHA, timestamp, проверки;
- INDEX status сразу формулировать как `terminal-fold accepted pending own PR merge; PR URL authoritative after merge`;
- после merge batch-closure PR не создавать следующую closure-задачу только ради собственной terminal fold.

## Проверки

```powershell
git diff --check
git diff --name-only <base-branch>...HEAD
git rev-parse --abbrev-ref HEAD
```

`git diff --name-only <base-branch>...HEAD` должен показывать только allowed files.

Перед PR final report проверить, что в closure-set не осталось stale final statuses:

```powershell
rg -n "PR open|ready for review|draft open|open; not merged|merged; closure pending|pending at file materialization|see Engine final report" docs/agent-system/engine-journal/output docs/agent-system/engine-journal/INDEX.md
```

Если совпадения относятся к историческим литералам вне closure-set, перечислить их в RESULT. Если совпадения относятся к final status closure-set — STOP.

Completion checklist:

- [ ] final-state surfaces cleared: верхние RESULT-статусы закрываемых substantive seq чисты; terminal lifecycle-only rows либо closed, либо `terminal-fold accepted`.

## Commit / PR

```powershell
git add docs/agent-system/engine-journal/input/TASK-<batch-seq>-*.md docs/agent-system/engine-journal/output/RESULT-<batch-seq>-*.md docs/agent-system/engine-journal/output/RESULT-<closed-seq>-*.md docs/agent-system/engine-journal/INDEX.md
git commit -m "docs(agent-system): batch-close journal <seq-range> before release"
git push -u origin work/<role>/batch-closure-<seq-range>
gh pr create --base <base-branch> --head work/<role>/batch-closure-<seq-range> --title "docs(agent-system): batch-close journal <seq-range> before release"
```

## Final report

Вернуть на русском:

- branch;
- PR URL;
- closed seq range;
- closure-set;
- merge facts source;
- changed files;
- checks run;
- remaining open seq, если есть;
- risks;
- Source-reminder: не применимо (методология не менялась), если задача только закрывала journal;
- Передача: `Следующий: архитектор — merge batch-closure PR; затем engine — release/reviewer gate без отдельной closure только ради accepted terminal fold`.

## STOP

- HEAD не work-ветка;
- diff содержит файлы вне allowed files;
- любой PR из closure-set не merged;
- невозможно получить merge facts;
- после правки closure-set содержит stale final status;
- обнаружен незакрытый seq, входящий в release, но отсутствующий в closure-set.
````
