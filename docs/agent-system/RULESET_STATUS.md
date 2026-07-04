# RULESET_STATUS

## Machine-readable status

```yaml
ruleset_status:
  repository: MaximKolomeets/agent-system-development
  visibility: public
  verified_at: "2026-07-04T16:18:03+07:00"
  verified_by_role: release-manager-01
  verification_source: gh_api_rulesets
  evidence:
    command_summary:
      - git ls-remote origin refs/tags/v1.5.3 refs/tags/v1.5.3^{}
      - git ls-remote origin refs/tags/v1.5.2 refs/tags/v1.5.2^{} refs/tags/v1.5.1 refs/tags/v1.5.1^{}
      - git rev-parse origin/main
      - git rev-parse origin/developer
      - gh pr view 326 --repo MaximKolomeets/agent-system-development --json number,state,mergedAt,mergeCommit,url,headRefName,baseRefName,title
      - gh pr view 327 --repo MaximKolomeets/agent-system-development --json number,state,mergedAt,mergeCommit,url,headRefName,baseRefName,title
      - gh pr view 328 --repo MaximKolomeets/agent-system-development --json number,state,mergedAt,mergeCommit,url,headRefName,baseRefName,title
      - gh api repos/MaximKolomeets/agent-system-development/rulesets
      - gh api repos/MaximKolomeets/agent-system-development/rulesets/17353333
      - gh api repos/MaximKolomeets/agent-system-development/rulesets/17353368
    pr_facts:
      v1_5_3_candidate:
        target_tag: v1.5.3
        target_tag_status: absent
        base_tag: v1.5.2
        base_commit: 1859a0034b14eed11e9842c4589fdeddb295cc6d
        previous_tag: v1.5.1
        previous_commit: 2467edd8488a51d74483e8095e4887c0f512dfcd
        candidate_ref: origin/developer
        candidate_commit: f10a06e2690bc8ff5c5cdb9afff893c39bee0dfe
      pr_0155:
        number: 326
        state: MERGED
        merged_at: "2026-07-03T16:16:07Z"
        merge_commit: e7f1b01582f209ff689ff199bd3597c3e5f8321f
      pr_0156:
        number: 327
        state: MERGED
        merged_at: "2026-07-03T16:37:37Z"
        merge_commit: 48560317211e9e81e5d2345a3115a886659062d7
      pr_0157:
        number: 328
        state: MERGED
        merged_at: "2026-07-04T09:00:34Z"
        merge_commit: f10a06e2690bc8ff5c5cdb9afff893c39bee0dfe
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

Следующий: methodology-reviewer-01 - проверить release-prep v1.5.3; затем
release-manager - использовать этот snapshot как evidence перед release boundary
или обновить его после human-only изменения rulesets.
