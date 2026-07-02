# RULESET_STATUS

## Machine-readable status

```yaml
ruleset_status:
  repository: MaximKolomeets/agent-system-development
  visibility: public
  verified_at: "2026-07-03T00:42:55+07:00"
  verified_by_role: methodology-architect-01
  verification_source: gh_api_rulesets
  evidence:
    command_summary:
      - gh pr view 306 --repo MaximKolomeets/agent-system-development --json number,state,mergedAt,mergeCommit,url,headRefName,baseRefName,title,headRefOid
      - gh pr view 307 --repo MaximKolomeets/agent-system-development --json number,state,mergedAt,mergeCommit,url,headRefName,baseRefName,title,headRefOid
      - gh pr view 308 --repo MaximKolomeets/agent-system-development --json number,state,mergedAt,mergeCommit,url,headRefName,baseRefName,title,headRefOid
      - gh pr view 309 --repo MaximKolomeets/agent-system-development --json number,state,mergedAt,mergeCommit,url,headRefName,baseRefName,title,headRefOid
      - gh pr view 322 --repo MaximKolomeets/agent-system-development --json number,state,mergedAt,mergeCommit,url,headRefName,baseRefName,title
      - gh api repos/MaximKolomeets/agent-system-development/rulesets
      - gh api repos/MaximKolomeets/agent-system-development/rulesets/17353333
      - gh api repos/MaximKolomeets/agent-system-development/rulesets/17353368
    pr_facts:
      v1_5_2_candidate:
        base_tag: v1.5.1
        base_commit: 2467edd8488a51d74483e8095e4887c0f512dfcd
        candidate_ref: origin/developer
        candidate_commit: 97e874883afbe3ac38ccd815d48f63ca964c5737
      pr_1_h1:
        number: 306
        state: MERGED
        merged_at: "2026-07-02T09:00:28Z"
        merge_commit: f993dba56d03682d80f757cf034616fe954f1ea4
      pr_2_h2:
        number: 307
        state: MERGED
        merged_at: "2026-07-02T09:28:36Z"
        merge_commit: 9fc59150f508f4846fef2b34d9738f49b81e7fb2
      pr_3_h3:
        number: 308
        state: MERGED
        merged_at: "2026-07-02T10:07:47Z"
        merge_commit: 85f14f204b8dc77f032af096c417f9130476478c
      pr_4_h4:
        number: 309
        state: MERGED
        merged_at: "2026-07-02T10:29:51Z"
        merge_commit: 4818b553beaa5b426334404696507c48e95d0d22
      batch_closure_pr:
        number: 322
        state: MERGED
        merged_at: "2026-07-02T17:37:05Z"
        merge_commit: 97e874883afbe3ac38ccd815d48f63ca964c5737
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

Следующий: methodology-reviewer-01 - проверить release-prep v1.5.2; затем
release-manager - использовать этот snapshot как evidence перед release boundary
или обновить его после human-only изменения rulesets.
