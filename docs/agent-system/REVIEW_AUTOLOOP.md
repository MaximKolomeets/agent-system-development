# Цикл review autoloop

## Назначение

Review autoloop описывает ограниченный автоматизированный цикл для одного active work PR:

```text
Engine PR -> Reviewer review -> Engine fix-pass -> Reviewer re-review -> architect-ready
```

Цель цикла - снять мелкие review-замечания без отдельного feedback PR и без ручного подтверждения каждого микрошага, сохранив все safety gates.

## Область применения

Autoloop применим только к active work PR в основной task branch `work/<role>/<task>`.

Не применять autoloop:

- к release PR `developer -> main`;
- к direct push в `main` или `developer`;
- к review-only задачам, которые не являются feedback по активному work PR;
- к PR с secrets-risk, forbidden paths, runtime/private data или scope drift;
- если reviewer явно требует human decision.

## Машина состояний

| State | Кто владеет шагом | Условие входа | Следующее состояние |
|---|---|---|---|
| `engine:ready-for-review` | Engine | PR открыт, checks зелёные, RESULT/INDEX финализированы насколько применимо | `reviewer:reviewing` |
| `reviewer:reviewing` | Reviewer | Reviewer читает diff/head SHA и checks | `reviewer:approved` или `reviewer:changes-requested` |
| `reviewer:changes-requested` | Reviewer | Есть blockers или actionable comments | `engine:fix-pass` |
| `engine:fix-pass` | Engine | Feedback относится к scope той же task branch | `engine:ready-for-review` |
| `reviewer:approved` | Reviewer | Blockers нет, checks зелёные | `architect:ready-to-merge` |
| `architect:ready-to-merge` | Architect | Reviewer approve-equivalent получен | Human merge в `developer` или human hold |
| `stopped:human-required` | Любая сторона | STOP-condition или превышен лимит циклов | Architect decision |

## Рекомендуемые labels/statuses

Repository labels/statuses рекомендуемые, но не заменяют GitHub review и branch protection:

- `engine:ready-for-review` - engine завершил pass и ждёт reviewer.
- `reviewer:changes-requested` - reviewer оставил blockers/actionable feedback.
- `engine:fix-pass` - engine исправляет feedback в той же task branch.
- `reviewer:approved` - reviewer не видит blockers.
- `architect:ready-to-merge` - PR готов к human merge в `developer`.
- `automation:stopped-human-required` - autoloop остановлен и передан архитектору.

Если GitHub label API недоступен, эти состояния фиксируются в PR comment и RESULT/final report.

## Лимит циклов

Каждая task должна задавать `max_review_cycles`. Значение по умолчанию, если явно не задано: `3`.

Один cycle = reviewer feedback + один engine fix-pass + повторная reviewer проверка.

Если `max_review_cycles` исчерпан, automation ставит/пишет `automation:stopped-human-required` и передаёт PR человеку. Engine не продолжает бесконечно править PR.

## STOP-условия

Automation немедленно останавливается и передаёт PR архитектору, если обнаружено:

- merge conflict или невозможность fast-forward/rebase/merge без отдельного решения;
- secrets-risk, credentials, `.env`, private keys, tokens или matching secret values;
- forbidden paths: runtime, `data/`, `dist/`, `exports/`, `.venv`, CI/rulesets/branch protection без scope;
- failed checks после engine fix-pass;
- generated drift, который не устраняется штатной регенерацией;
- scope drift или требование новой substantive task;
- reviewer требует architecture/product/security decision;
- превышен `max_review_cycles`;
- GitHub/API permissions не позволяют безопасно поставить status/label/comment;
- требуется force-push или rewrite уже pushed/merged history без явного решения архитектора.

## Проход reviewer

Reviewer:

- проверяет фактический PR head SHA;
- оставляет feedback только в PR агента;
- не создаёт отдельный PR для feedback;
- классифицирует feedback как blocker/non-blocking;
- указывает, можно ли продолжать autoloop;
- при blockers использует статус/comment `reviewer:changes-requested`;
- при отсутствии blockers использует `reviewer:approved` и `architect:ready-to-merge`.

Шаблон: `docs/agent-system/templates/REVIEW_AUTOLOOP_REVIEWER_PASS_TEMPLATE.md`.

## Проход engine fix-pass

Engine:

- работает в той же task branch;
- исправляет только feedback, относящийся к scope PR;
- не открывает отдельный feedback PR;
- повторно запускает checks;
- обновляет RESULT/final report, если task ведёт journal;
- возвращает PR в `engine:ready-for-review`.

Шаблон: `docs/agent-system/templates/REVIEW_AUTOLOOP_ENGINE_FIX_PASS_TEMPLATE.md`.

## Локальный orchestrator / self-hosted runner flow

Минимальный local orchestrator flow:

```powershell
gh pr view <pr> --json headRefName,headRefOid,baseRefName,state,mergeable
gh pr checks <pr>
gh pr view <pr> --comments
# Если есть reviewer:changes-requested и cycles < max_review_cycles:
git fetch --all --prune
git switch <headRefName>
git pull --ff-only origin <headRefName>
# Engine выполняет fix-pass по feedback.
python docs/agent-system/tools/gen_file_map.py --check
python docs/agent-system/tools/gen_cloud_bundle.py --check
git diff --check
git push
# Orchestrator запрашивает reviewer re-review.
```

Self-hosted runner может выполнять те же шаги, но не получает права merge в `developer` и не обходит branch protection. Любой secrets-risk или forbidden path останавливает runner и требует human review.

## Инварианты safety gates

- Merge в `developer` выполняет только человек-архитектор.
- Release PR `developer -> main` не входит в autoloop.
- Reviewer не меняет production/source files.
- Engine не меняет scope без отдельного решения.
- `.env` не читается и не выводится.
- Secrets/matching lines не печатаются.
- Direct push в `main`/`developer` запрещён.
