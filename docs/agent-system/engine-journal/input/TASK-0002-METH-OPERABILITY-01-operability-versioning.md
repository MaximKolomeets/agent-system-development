# TASK-0002-METH-OPERABILITY-01-operability-versioning

## Задача для docs-maintainer-01: METH-OPERABILITY-01

Рекомендуемый режим Codex:

Запуск: Local only
Модель: GPT-5
Reasoning: High
Режим: Agent
Почему: docs-only methodology hardening затрагивает несколько reusable документов, templates и engine journal artifacts, поэтому нужен полный branch/PR/journal workflow.

## Verified baseline

- Repository: `MaximKolomeets/agent-system-development`
- Local path: `C:\neural\repos\agent-system-development`
- Base branch: `developer`
- Base commit: `cb950132ee779b3632d0df396ab65115ba46864d`
- Working branch: `work/docs-maintainer-01/meth-operability-01`
- GitHub issue: none
- Task source: пользовательский attachment `METH-OPERABILITY-01`
- Scope: docs-only methodology repository update

## Methodology reference

```yaml
methodology_reference:
  repository: MaximKolomeets/agent-system-development
  source_branch: developer
  source_commit: cb950132ee779b3632d0df396ab65115ba46864d
  checked_at: 2026-06-14T00:00:00+07:00
  reference_type: commit
  notes: "Стартовая точка после PR #94 sync developer."
```

## Цель

Сделать operability pass после review guardrails:

- добавить lightweight solo-operator mode и multi-agent governed mode;
- уточнить boundaries для `orchestrator`, `engine` и `reviewer`;
- объяснить, что `CHATGPT_*` docs являются adapter/implementation-specific layer, а не исключением из vendor-neutral policy;
- добавить methodology versioning/reference policy через `methodology_reference`;
- добавить drift-control для Source/snapshot docs;
- уточнить token/ceremony policy для solo vs governed mode;
- усилить sanitization policy для Methodology feedback;
- добавить anti-overengineering checkpoint.

## Allowed files

- `README.md`
- `docs/agent-system/*.md`
- `docs/agent-system/*.yml`
- `docs/agent-system/templates/*.md`
- `docs/agent-system/source/*.md`
- `docs/agent-system/engine-journal/**`

## Forbidden files

- runtime code
- tests
- `.github/workflows/**`
- Docker files
- package manifests
- lockfiles
- `.env`
- `.venv/`
- `data/`
- `runtime/`
- `dist/`
- `backups/`
- `exports/`

## Required checks

- `git status --short`
- `git diff --check`
- `git diff --name-only origin/developer...HEAD`
- vendor/tool naming scan for docs
- source/snapshot wording scan
- journal placeholder scan before ready-for-review

## Final report requirements

Final report must be Russian-first and include sections 1-16 from the user task, plus a concrete `Локальные действия после PR/merge` block.
