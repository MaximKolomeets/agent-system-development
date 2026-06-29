# Цикл review autoloop

## Назначение

Review autoloop описывает ограниченный автоматизированный цикл для одного active work PR:

```text
Engine PR -> Reviewer review -> Engine fix-pass -> Reviewer re-review -> architect-ready
```

Для ordinary PR итоговый lifecycle выглядит так:

```text
Engine PR -> Reviewer approve -> architect-ready -> human merge
```

Цель цикла - снять мелкие review-замечания без отдельного feedback PR и без ручного подтверждения каждого микрошага, сохранив все safety gates.

Перед первым ready-for-review PR engine применяет `docs/agent-system/QUALITY_FIRST_WORKFLOW.md`: task должен иметь acceptance criteria, engine выполняет self-review before PR, PR body проходит quality check, а fix-pass закрывает blocker IDs вместо общего cleanup.

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
| `engine:fix-pass` | Engine | Feedback относится к scope той же task branch | `engine:ready-for-review` для semantic/mixed или failed checks; `architect:ready-to-merge` для полностью закрытых machine-verifiable blockers |
| `reviewer:approved` | Reviewer | Blockers нет, checks зелёные | `architect:ready-to-merge` |
| `architect:ready-to-merge` | Architect | Reviewer approve-equivalent получен | Human merge в `developer` или human hold |
| `automation:stopped-human-required` | Любая сторона | STOP-condition или превышен лимит циклов | Architect decision |

`architect:ready-to-merge` является terminal state для ordinary PR с точки зрения engine/reviewer. После human merge не запускать automatic closure PR, не требовать re-review, не открывать cleanup PR и не считать `RESULT/INDEX` open/ready surfaces долгом, если запись содержит PR URL, reviewed head SHA и `architect:ready-to-merge` / `human_merge_allowed`. GitHub PR metadata является source of truth для `merged_at`, merge commit SHA, PR state и PR URL.

## Рекомендуемые labels/statuses

Repository labels/statuses рекомендуемые, но не заменяют GitHub review и branch protection:

- `engine:ready-for-review` - engine завершил pass и ждёт reviewer.
- `reviewer:changes-requested` - reviewer оставил blockers/actionable feedback.
- `engine:fix-pass` - engine исправляет feedback в той же task branch.
- `reviewer:approved` - reviewer не видит blockers.
- `architect:ready-to-merge` - PR готов к human merge в `developer`.
- `automation:stopped-human-required` - autoloop остановлен и передан архитектору.

Если GitHub label API недоступен, эти состояния фиксируются в PR comment и RESULT/final report.

`automation:stopped-human-required` является единым именем state/label/status для остановки цикла. Не использовать отдельный alias `stopped:human-required`, чтобы automation не плодила два разных статуса.

## Лимит циклов

Каждая task должна задавать `max_review_cycles`. Значение по умолчанию, если явно не задано: `3`.

Один cycle = reviewer feedback + один engine fix-pass + повторная reviewer проверка.

Если `max_review_cycles` исчерпан, automation ставит/пишет `automation:stopped-human-required` и передаёт PR человеку. Engine не продолжает бесконечно править PR.

## Схема reviewer feedback

Reviewer feedback в active work PR должен быть структурирован так, чтобы engine мог выполнить fix-pass без повторного уточнения у архитектора:

```yaml
blocking_findings:
  - id: B-01
    class: machine-verifiable | semantic | mixed
    title: <короткое имя blocker>
    evidence: <файл/строка/команда/наблюдение>
    required_change: <что нужно изменить>
    verification_command: <команда или explicit manual check>
    can_engine_fix_without_architect: yes | no
non_blocking_notes:
  - id: N-01
    title: <короткое имя note>
    recommendation: <что улучшить>
required_fix_scope:
  - <разрешённые файлы/область fix-pass>
re_review_policy:
  scope: none | machine_check_only | changed_blockers_only | full
  reason: <почему этого достаточно>
```

`id` обязателен для каждого blocker и должен быть стабильным в пределах PR: `B-01`, `B-02`, ... . Если blocker разбивается на несколько независимых проблем, reviewer заводит отдельные IDs вместо длинной смешанной формулировки.

## Классы blockers

`machine-verifiable` — blocker полностью закрывается детерминированной командой или проверкой: `git diff --check`, generator `--check`, отсутствие файла в diff, count-only secret scan, конкретный grep. Reviewer обязан указать `verification_command`. Если fix-pass менял только такие blockers, все команды прошли и не появился scope drift, отдельный полный reviewer pass не требуется; PR может перейти к `architect:ready-to-merge` через machine-check closure.

`semantic` — blocker требует смысловой оценки reviewer: корректность канона, consistency между документами, точность формулировки, security/privacy judgement. После fix-pass нужен reviewer re-review минимум по changed blocker scope.

`mixed` — blocker содержит machine-verifiable часть и смысловую часть. Engine закрывает проверяемую часть командами, но reviewer всё равно делает re-review по изменённым blockers.

Если `can_engine_fix_without_architect: no`, automation останавливается в `automation:stopped-human-required` и передаёт PR человеку, даже если blocker выглядит техническим.

## Minimal re-review

Повторная проверка после fix-pass должна быть минимальной:

- `none` — только если blockers отсутствуют.
- `machine_check_only` — допустимо для changed machine-verifiable blockers, когда `verification_command` прошёл и changed files остаются в разрешённом scope.
- `changed_blockers_only` — default для semantic/mixed blockers: reviewer не повторяет весь architecture review, если fix-pass не расширял scope.
- `full` — нужен при scope drift, изменении архитектурной модели, новых files вне expected diff, failed checks, конфликте, secrets-risk или явном требовании reviewer/architect.

Machine-check closure не ослабляет safety gates: failed command, forbidden path, secrets-risk, conflict или превышение `max_review_cycles` всегда переводят PR в `automation:stopped-human-required`.

## Единый ready-gate для task branch

Перед первым push/PR, после каждого engine fix-pass и перед переводом PR в `architect:ready-to-merge` engine должен запускать read-only ready-gate:

```text
python docs/agent-system/tools/check_task_ready.py --base origin/developer
```

Инструмент агрегирует branch guard, changed files summary, `git diff --check`, условные generated checks, generated EOL guard, filename-only sensitive scan, strict added-line secret scan и placeholder scan для изменённых TASK/RESULT. Он не выполняет `fetch`, `pull`, `switch`, `merge`, `stash`, `reset` или `clean`.

Для generated/cloud шума machine-verifiable команда `python docs/agent-system/tools/generated_eol_guard.py --base origin/developer` различает `content_changed`, `eol_only_changed` и `whitespace_only_changed` без изменения git state. `eol_only_changed` / `whitespace_only_changed` можно закрывать как machine-check evidence или точечно откатывать только в рамках разрешённого scope; `content_changed` в generated artifact без соответствующего source/bundle изменения остаётся blocker и требует регенерации или reviewer re-review по изменённому scope.

Для `machine-verifiable` blockers reviewer может указать эту команду как `verification_command`, если blocker покрыт её проверками. Passed output `check_task_ready.py` достаточно для machine-check closure только при отсутствии scope drift и новых blockers; `semantic`/`mixed` blockers всё равно требуют minimal reviewer re-review по изменённому blocker scope.

## Language и stable-reference gates

Reviewer проверяет Russian-first для PR title/body, commit subject/body, review summary, RESULT/final report и verdict comments. Ready-for-review PR с преимущественно англоязычной GitHub-facing metadata без явного разрешения архитектора получает blocker.

Если PR затрагивает downstream/adoption/source-update правила, reviewer проверяет `methodology_reference`: stable downstream source - `origin/main` / `main`, явно заданный release tag или published snapshot. `developer`, `work/*`, dirty local methodology tree и open methodology PR branch являются blocker как downstream source of truth. Dirty methodology worktree сам по себе не является blocker для downstream task, если stable reference читается.

## Own-PR verdict fallback

Если GitHub не позволяет reviewer token оставить formal `APPROVE` / `REQUEST_CHANGES` из-за ограничения own PR или author identity, это не blocker. Reviewer оставляет top-level PR comment с тем же verdict/schema, например `verdict: reviewer:approved` или `verdict: reviewer:changes-requested`, reviewed head SHA и blocker IDs. Такой comment является approve-equivalent или changes-requested-equivalent для autoloop; human merge всё равно остаётся только за архитектором.

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
- классифицирует feedback как blocker/non-blocking по схеме `B-01`/`machine-verifiable|semantic|mixed`;
- проверяет Russian-first GitHub-facing metadata и stable methodology reference, если они применимы к scope;
- указывает `verification_command`, `can_engine_fix_without_architect` и `re_review_policy` для каждого blocker или группы blockers;
- указывает, можно ли продолжать autoloop;
- при blockers использует статус/comment `reviewer:changes-requested`;
- при отсутствии blockers использует `reviewer:approved` и `architect:ready-to-merge`.

Шаблон: `docs/agent-system/templates/REVIEW_AUTOLOOP_REVIEWER_PASS_TEMPLATE.md`.

## Проход engine fix-pass

Engine:

- работает в той же task branch;
- исправляет только feedback, относящийся к scope PR;
- не открывает отдельный feedback PR;
- закрывает blockers по IDs и фиксирует verification result для каждого `verification_command`;
- сохраняет Russian-first для GitHub-facing metadata и не подменяет downstream stable reference на `developer`/`work/*`;
- запускает `python docs/agent-system/tools/check_task_ready.py --base origin/developer` перед возвратом PR reviewer/architect;
- если все blockers `machine-verifiable`, все checks passed и scope не расширен, может вывести machine-check closure и `architect:ready-to-merge` без полного reviewer pass;
- для `semantic`/`mixed` blockers возвращает PR на minimal reviewer re-review по `re_review_policy`;
- повторно запускает checks;
- обновляет RESULT/final report, если task ведёт journal;
- возвращает PR в `engine:ready-for-review` для re-review или в `architect:ready-to-merge` для fully passed machine-check closure.

Шаблон: `docs/agent-system/templates/REVIEW_AUTOLOOP_ENGINE_FIX_PASS_TEMPLATE.md`.

## Semantic completeness blockers

Reviewer может классифицировать semantic completeness mismatch по `docs/agent-system/SEMANTIC_COMPLETENESS_GATES.md` как `semantic` или `mixed` blocker. Типовые примеры: RESULT обещает checks, которые не запускались; PR body описывает implementation, отсутствующую в diff; docs-only PR включает tests/tools/code; acceptance spec, blocker matrix и fixture plan расходятся по scenario/blocker/fixture/status mapping; finalized journal surface нарушает `docs/agent-system/JOURNAL_FINALIZATION_POLICY.md`.

Downstream feedback blockers reviewer проверяет по `docs/agent-system/DOWNSTREAM_FEEDBACK_LOOP.md` и `docs/agent-system/DOWNSTREAM_FEEDBACK_SANITIZATION_POLICY.md`: target-specific/private leakage, target adoption до stable release boundary или чтение target repository без explicit scope являются `semantic` либо `mixed` blocker.

## Локальный orchestrator / self-hosted runner flow

Минимальный local orchestrator flow:

```powershell
gh pr view <pr> --json headRefName,headRefOid,baseRefName,state,mergeable
gh pr checks <pr>
gh pr view <pr> --comments
# Если есть reviewer:changes-requested и cycles < max_review_cycles:
git rev-parse --show-toplevel
git remote -v
git branch --show-current
git status --short
# Если git status --short не пустой: STOP. Не выполнять fetch/switch/pull/merge/rebase/stash/reset/clean.
git fetch --all --prune
git switch <headRefName>
git pull --ff-only origin <headRefName>
# Engine выполняет fix-pass по feedback.
python docs/agent-system/tools/gen_file_map.py --check
python docs/agent-system/tools/gen_cloud_bundle.py --check
python docs/agent-system/tools/check_task_ready.py --base origin/developer
git diff --check
git push
# Orchestrator запрашивает reviewer re-review для semantic/mixed blockers
# или failed machine checks; для fully passed machine-verifiable blockers
# допускается architect-ready machine-check closure.
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
