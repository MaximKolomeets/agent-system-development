# RULESET_STATUS

## Machine-readable status

```yaml
ruleset_status:
  repository: MaximKolomeets/agent-system-development
  visibility: public
  verified_at: "2026-07-02T15:33:24+07:00"
  verified_by_role: docs-maintainer-01
  verification_source: gh_api_rulesets
  evidence:
    command_summary:
      - gh pr view 303 --repo MaximKolomeets/agent-system-development --json number,state,mergedAt,mergeCommit,url,headRefName,baseRefName,title
      - gh pr view 304 --repo MaximKolomeets/agent-system-development --json number,state,mergedAt,mergeCommit,url,headRefName,baseRefName,title
      - gh pr view 305 --repo MaximKolomeets/agent-system-development --json number,state,mergedAt,mergeCommit,url,headRefName,baseRefName,title
      - gh api repos/MaximKolomeets/agent-system-development/rulesets
    pr_facts:
      release_prep_pr:
        number: 303
        state: MERGED
        merged_at: "2026-07-02T02:11:11Z"
        merge_commit: e3c4210dade210f20b573196ed0d9da64961dc75
      release_pr:
        number: 304
        state: MERGED
        merged_at: "2026-07-02T06:46:16Z"
        merge_commit: 2467edd8488a51d74483e8095e4887c0f512dfcd
      sync_pr:
        number: 305
        state: MERGED
        merged_at: "2026-07-02T06:48:28Z"
        merge_commit: 2407cd4950b05fd2bb03583f9ccb1fe84d53eac5
  protected_refs:
    main:
      ruleset_name: Protect main
      ruleset_id: 17353333
      target: branch
      ref_include:
        - refs/heads/main
      status: active
      ruleset_updated_at: "2026-06-06T23:23:48.675+07:00"
      rules:
        deletion: enabled
        non_fast_forward: enabled
        pull_request:
          enabled: true
          required_review_thread_resolution: true
          required_approving_review_count: 0
      required_checks: []
    developer:
      ruleset_name: Protect developer
      ruleset_id: 17353368
      target: branch
      ref_include:
        - refs/heads/developer
      status: active
      ruleset_updated_at: "2026-06-06T23:23:58.421+07:00"
      rules:
        deletion: enabled
        non_fast_forward: enabled
        pull_request:
          enabled: true
          required_review_thread_resolution: true
          required_approving_review_count: 0
      required_checks: []
  staleness_policy:
    before_release_boundary:
      max_age_days: 14
      stale_status: advisory
      blocker_if_unverifiable: false
      action: refresh RULESET_STATUS.md before release gate
    before_ruleset_change:
      max_age_days: 0
      stale_status: blocker
      action: human-only decision and fresh GitHub ruleset verification required
```

## Интерпретация

- `Protect main` и `Protect developer` активны и применяются к соответствующим
  веткам.
- Rulesets блокируют deletion и non-fast-forward, требуют pull request workflow и
  resolution review threads.
- Required status checks на момент проверки не заданы в rulesets; ручная проверка
  gates остаётся частью release/workflow discipline до отдельного решения
  архитектора.
- Изменение rulesets является human-gate действием: агент может подготовить
  evidence/status, но не меняет branch protection/rulesets без явного решения
  человека.

## Передача

Следующий: docs-maintainer-01 — обновлять этот snapshot перед release boundary или
после human-only изменения rulesets.
