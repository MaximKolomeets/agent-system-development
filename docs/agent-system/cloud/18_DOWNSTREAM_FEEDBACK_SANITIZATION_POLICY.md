# DOWNSTREAM_FEEDBACK_SANITIZATION_POLICY

## Назначение

Policy определяет, как превращать downstream observations в public-safe reusable methodology feedback. Цель - сохранить полезный методологический сигнал и удалить все private, target-specific и secret-bearing details до попадания item в `agent-system-development`.

Sanitized feedback описывает pattern, category, reusable rule и acceptance expectation. Он не описывает конкретный private project.

## Forbidden content

В public methodology feedback запрещено включать:

- private customer data;
- real measurements;
- real protocols;
- real methodology files;
- credentials/tokens/secrets;
- `.env` values;
- private file paths with sensitive context;
- target-specific implementation details;
- exact proprietary data model names if project-private;
- real organization names unless public and intended;
- raw logs with protected data;
- matching secret/header values;
- target-specific branch/worktree state as methodology fact.

Запрет действует на human output, JSON output, TASK/RESULT/INDEX, PR body, comments, state docs, backlog entries и generated/context bundle.

## Allowed abstraction

Разрешено переносить только:

- neutral problem pattern;
- reusable methodology category;
- affected canonical surface as generic path/category;
- expected policy or checklist behavior;
- non-sensitive blocker class;
- synthetic/minimal example;
- count-only или filename-only evidence без matching value;
- future task id без private target context.

Allowed abstraction не должна позволять восстановить private repository, customer, protocol, measurement, branch state или proprietary implementation detail.

## Sanitization checklist

Перед переносом feedback в methodology repository проверить:

- repository/project/customer names removed or generalized;
- private URLs and sensitive local paths removed;
- credentials, tokens, cookies, passwords, API keys and `.env` values absent;
- Authorization/session/header values absent;
- real measurements, real protocols and real data absent;
- logs and source snippets are not quoted;
- target branch/worktree state is not stated as reusable methodology fact;
- problem still makes sense as reusable methodology pattern;
- proposed change belongs to methodology docs/templates/tooling, not target product work;
- adoption boundary says target repositories receive changes only after `main`, release tag or published snapshot.
- target adoption detector recommendation does not include private repository identity, `.env`, secrets, raw logs or target-specific branch/worktree facts beyond safe STOP categories.

## Redaction rules

Use neutral replacements:

- private repository name -> `target implementation repository`;
- private downstream repository -> `private downstream repository`;
- private file path -> `target docs path`, `target test path`, `target config path` или generic category;
- real protocol/measurement/data -> `real data`, `real measurement`, `real protocol`;
- branch/worktree details -> `target-local branch/worktree state`;
- secret/header value -> `matching secret/header value`;
- customer/project/org names -> `customer`, `project`, `organization`, если сам факт не раскрывает identity.

Не заменять sensitive value фиктивным похожим value внутри public doc, если это может выглядеть как реальный credential. Для examples использовать явно synthetic/minimal language.

## Examples: unsafe -> safe

Unsafe: "In project X file Y line Z had blocker code ABC missing."

Safe: "Downstream dry-run showed repeated mismatch between acceptance scenario, blocker code and fixture expectation."

Unsafe: "This customer protocol used real device serial number..."

Safe: "Feedback category: real-data boundary must be explicit before protocol generation."

Unsafe: "Repository X branch Y had uncommitted tests..."

Safe: "Feedback category: task scope must distinguish docs-only, fixture-only and implementation slices."

## Reviewer checklist

Reviewer verifies:

- no forbidden content category is present;
- examples are synthetic/minimal and do not identify a private target;
- feedback is classified as reusable methodology, template, tooling, semantic gate, release/adoption boundary or target-only;
- PR body and RESULT do not claim target adoption before stable release boundary;
- methodology task did not read or change target repositories unless task explicitly allowed it;
- output exposes only count, filenames and category for safety scans;
- matching secret/header values are not printed.

## STOP conditions

STOP and request architect decision if:

- feedback cannot be sanitized without losing its meaning;
- any matching secret/header value is present;
- any `.env` value or credential-like value is present;
- private downstream identity remains visible;
- task needs target repository access but scope does not allow it;
- proposed change would alter product/runtime/CI/branch protection;
- public methodology would treat target-specific branch/worktree state as reusable fact.
