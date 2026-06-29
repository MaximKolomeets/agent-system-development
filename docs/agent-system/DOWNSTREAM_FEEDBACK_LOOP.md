# DOWNSTREAM_FEEDBACK_LOOP

## Назначение

Документ задает reusable loop, по которому наблюдения из downstream dry-run превращаются в безопасные улучшения methodology repository. Loop защищает public methodology от private details и отделяет методологические правила от состояния конкретного target implementation repository.

Downstream feedback не является автоматическим изменением methodology. Любой item сначала проходит sanitization checkpoint, затем classification и только после этого может попасть в backlog или отдельную methodology task.

## Что считается downstream feedback

Downstream feedback - это обобщенное наблюдение о том, что reusable methodology оказалась неполной, неоднозначной или небезопасной при применении к target implementation repository.

Допустимые категории:

- неясный task contract, STOP condition или allowed-files boundary;
- повторяющийся разрыв между RESULT, PR body, state docs и фактическим diff;
- нехватка reusable checklist, policy, template или review pattern;
- небезопасный output pattern, где tool или report может раскрыть matching secret/header value;
- потребность в release/adoption boundary, чтобы target repositories получали изменения только после main/tag release;
- необходимость лучше различать docs-only, fixture-only, tooling и implementation slices.

## Что не считается reusable methodology feedback

Не является reusable methodology feedback:

- конкретный дефект target repository, который чинится только в этом repository;
- приватная branch/worktree ситуация target repository как methodology fact;
- product/runtime/CI/branch protection решение target repository;
- real data, customer data, internal code name или private repository URL;
- запрос перенести target-specific implementation details в active methodology docs;
- попытка использовать target repository как source of truth для reusable methodology.

Target repository не является source of truth для reusable methodology. Source of truth для reusable changes - `agent-system-development` через отдельную work branch, PR в `developer`, human merge, а для downstream adoption - последующий `main`/tag release или явно опубликованный stable snapshot.

## Feedback intake

Feedback intake начинается только с безопасного, обобщенного текста. Оркестратор или engine не читает target repository ради methodology task, если task явно не разрешает такой доступ.

Минимальный intake item:

- neutral problem pattern;
- reusable methodology gap;
- affected methodology docs/templates/tooling category;
- explicit forbidden-data confirmation;
- suggested backlog grouping or task boundary.

Dirty/open target work branches не являются blocker для methodology repository work. Они остаются состоянием target repository и не переносятся в public methodology как факт.

## Sanitization checkpoint

Перед classification каждый item проходит `docs/agent-system/DOWNSTREAM_FEEDBACK_SANITIZATION_POLICY.md`.

Checkpoint отвечает на вопросы:

- нет private customer data, real data, credentials, `.env` values или matching secret/header values;
- нет private repository URLs, sensitive local paths, internal code names или project-private data model names;
- нет target-specific branch/worktree state как methodology fact;
- сохранен только reusable problem pattern;
- item можно опубликовать в public methodology repository без раскрытия private downstream context.

Если item нельзя безопасно обобщить, он остается в private downstream repository или private notes и не превращается в methodology backlog.

## Classification

После sanitization item классифицируется:

- `methodology_doc_gap` - нужен reusable policy, pattern или checklist;
- `template_gap` - нужен reusable task/report/template text;
- `tooling_gap` - нужен lightweight guard или validator;
- `semantic_gate_gap` - нужен reviewer checklist или reusable consistency rule;
- `release_adoption_gap` - нужен clearer boundary между `developer`, `main`, tag и target adoption;
- `target_only` - feedback не переносится в methodology.

Classification должна быть нейтральной и не должна раскрывать источник downstream observation.

## Backlog grouping

Backlog grouping объединяет близкие reusable items только если они имеют общий policy surface и общий review scope.

Правила grouping:

- не смешивать target-only fixes с methodology hardening;
- не объединять docs-only policy с production generator/tests/fixtures, если это расширяет scope;
- оставлять future tasks отдельными, если для них требуется target repository access или implementation work;
- писать статус как `candidate` или `future`, если задача еще не начата;
- закрывать исходный downstream feedback item как sanitized/reusable variant только после появления нейтрального methodology task или canonical doc.

## Methodology task creation

Reusable change создается только через отдельную task branch в `agent-system-development`:

```text
work/<role>/<task-id>
```

Task должна содержать:

- Russian-first task text;
- `task_contract`;
- allowed files и forbidden files;
- STOP conditions для private data, `.env`, target repository access, runtime/Docker/CI/branch protection;
- checks;
- journal TASK/RESULT/INDEX;
- Source Delta и context handoff, если меняются canon/source files.

Methodology task не читает target repository, если task явно не включает это в scope. Для sanitized downstream feedback default - работать только с уже обобщенным intake.

## Review expectations

Reviewer проверяет:

- feedback прошел sanitization checkpoint;
- private/target-specific leakage отсутствует;
- methodology diff соответствует заявленному PR body и RESULT;
- scope не расширен до target repository, product/runtime/CI, branch protection или real data;
- docs-only task не содержит tests/tools/code/runtime, если это не разрешено;
- generated manifest, file map и cloud bundle согласованы, если добавлены source docs.

Reviewer может классифицировать private/target-specific leakage как blocker.

## Release boundary

Merge methodology PR в `developer` не делает правило доступным для target repositories автоматически.

Target repositories получают methodology updates только после одного из stable sources:

- `main`;
- release tag;
- explicitly published Source/cloud snapshot.

Обычный post-merge closure PR для methodology task не нужен. Boundary reconciliation выполняется только перед release/audit boundary, batch reconciliation или по explicit architect request.

## Adoption into target repositories

Adoption into target repositories выполняется отдельной downstream/adoption task после stable release boundary.

Adoption task:

- сначала определяет Variant A/B/C или STOP по `docs/agent-system/TARGET_ADOPTION_DETECTOR.md`;
- фиксирует stable methodology reference;
- не использует `developer`, `work/*`, dirty local methodology tree или open methodology PR branch как downstream source of truth;
- адаптирует target-local docs по target facts;
- не копирует methodology operational history;
- не переносит private downstream data обратно в public methodology.

## STOP conditions

STOP и не открывать ready-for-review PR, если:

- feedback содержит private/customer/project details;
- требуется читать target repository без явного task scope;
- item нельзя безопасно обобщить;
- changed files выходят за allowed scope;
- task меняет product/runtime/CI/branch protection;
- task создает release PR, tag или merge без отдельного решения;
- state docs утверждают, что target adoption уже выполнена до `main`/tag release;
- journal RESULT/INDEX обещают факты, которые не подтверждены diff/checks.

## Examples

Safe:

- "Downstream dry-run showed repeated mismatch between acceptance scenario, blocker code and fixture expectation."
- "Feedback category: real-data boundary must be explicit before protocol generation."
- "Feedback category: task scope must distinguish docs-only, fixture-only and implementation slices."

Unsafe:

- "In project X file Y line Z had blocker code ABC missing."
- "This customer protocol used real device serial number..."
- "Repository X branch Y had uncommitted tests..."
