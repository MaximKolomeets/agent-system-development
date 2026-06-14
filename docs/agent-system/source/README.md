# Source Snapshot Policy

`docs/agent-system/source/` хранит только derived context: индекс, краткие требования и snapshots для навигации.

GitHub repository files, commits, branches and Pull Requests остаются source of truth.

Любой новый или обновленный snapshot должен начинаться с metadata block:

```yaml
source_snapshot:
  source_of_truth: GitHub
  source_repository: MaximKolomeets/agent-system-development
  source_commit: <commit-sha>
  generated_at: <ISO-8601 timestamp>
  staleness_policy: use GitHub files if this snapshot differs from repository state
```

Если snapshot не содержит metadata block или расходится с repository files, использовать GitHub/repository files и зафиксировать drift в RESULT или review report.

Snapshot не должен быть основанием для изменения repository state без проверки canonical files.

Этот документ — канон политики `source_snapshot` для всего methodology repository. Остальные документы ссылаются на него.
