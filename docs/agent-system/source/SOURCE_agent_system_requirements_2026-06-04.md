# SOURCE_agent_system_requirements_2026-06-04

```yaml
source_snapshot:
  source_of_truth: GitHub
  source_repository: MaximKolomeets/agent-system-development
  source_commit: cb950132ee779b3632d0df396ab65115ba46864d
  generated_at: 2026-06-14T14:23:07.1492210+07:00
  staleness_policy: use GitHub files if this snapshot differs from repository state
```

Краткая версия требований:

- GitHub source of truth.
- Source as index/snapshot.
- Role-based agents.
- Protected `main`/`developer`.
- One task = one branch = one PR.
- Security rules: не читать `.env`, не коммитить секреты и рабочие данные.
- Стартовые роли агентов:
  - `dev-implementer-01`;
  - `solution-architect-01`;
  - `qa-reviewer-01`;
  - `security-reviewer-01`;
  - `docs-maintainer-01`.
- Перенос утвержденной структуры в private downstream repository позже отдельной задачей.
