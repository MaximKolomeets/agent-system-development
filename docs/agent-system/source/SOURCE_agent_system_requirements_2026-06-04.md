# SOURCE_agent_system_requirements_2026-06-04

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
- Перенос утвержденной структуры в CORP_KNOWLEDGE_PLATFORM позже отдельной задачей.
