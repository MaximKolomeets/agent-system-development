# BACKLOG

- Выполнено: bootstrap agent-system repository.
- Configure GitHub rulesets.
- Create local worktrees.
- Add CI forbidden files check.
- Add pre-push hook.
- Prepare private downstream repository transfer/adaptation prompt.
- Подготовить checklists для агентов.
- Future methodology simplification после release `v1.2.0`: lifecycle simplification, context handoff footer enforcement, GitHub PR state as authority, journal gate automation, adoption feedback loop automation. Не реализовывать в release-prep; рассматривать отдельными scoped задачами.

## METH-GENERATED-EOL-CANON-01 — generated/journal/cloud EOL-noise cleanup

Статус: backlog / future tooling task; не блокирует переход в target implementation repository.

Проблема:
После `gen_cloud_bundle.py` на Windows периодически появляются EOL-only изменения в generated/cloud/journal Markdown files. Содержательный diff обычно ограничен `cloud/00_README.md` и `cloud/07_ENGINE_JOURNAL_INDEX.md`, но Git может помечать дополнительные файлы как modified из-за line endings. Это создаёт operational noise и заставляет Engine вручную отделять content changes от EOL-only изменений.

Предварительное решение:
- расширить `.gitattributes` для Markdown/YAML/Python и generated/journal/template paths;
- проверить, что `gen_cloud_bundle.py` и `gen_file_map.py` явно пишут LF (`\n`) независимо от Windows default newline;
- выполнить bounded `git add --renormalize --dry-run docs/agent-system`;
- выполнять реальный renormalize только отдельным scoped PR после анализа размера diff;
- добавить lightweight EOL check для generated artifacts, если потребуется.

Ограничения:
- не выполнять перед release;
- не смешивать с target project work;
- не делать большой renormalize без отдельного отчёта и явного решения архитектора.
