# RULESET_STATUS

## Machine-readable status

```yaml
ruleset_status:
  repository: MaximKolomeets/agent-system-development
  visibility: public
  verified_at: "2026-07-04T18:01:52+07:00"
  verified_by_role: release-manager-01
  verification_source: gh_api_rulesets
  evidence:
    command_summary:
      - git fetch --all --prune --tags
      - git rev-parse origin/main
      - git rev-parse origin/developer
      - git rev-parse v1.5.3^{commit}
      - git diff --name-only origin/main...origin/developer
      - gh pr view 330 --repo MaximKolomeets/agent-system-development --json number,state,mergedAt,mergeCommit,url,headRefName,baseRefName,title
      - gh pr view 331 --repo MaximKolomeets/agent-system-development --json number,state,mergedAt,mergeCommit,url,headRefName,baseRefName,title
      - gh api repos/MaximKolomeets/agent-system-development/rulesets
      - gh api repos/MaximKolomeets/agent-system-development/rulesets/17353333
      - gh api repos/MaximKolomeets/agent-system-development/rulesets/17353368
    release_facts:
      v1_5_3:
        release_pr:
          number: 330
          state: MERGED
          merged_at: "2026-07-04T10:47:17Z"
          merge_commit: f0c75a965e19b78f9c018c406680b12caaf255c1
        tag:
          name: v1.5.3
          peeled_commit: f0c75a965e19b78f9c018c406680b12caaf255c1
        publication:
          github_release: not_applicable
          mode: tag_only
        sync_pr:
          number: 331
          state: MERGED
          merged_at: "2026-07-04T10:53:42Z"
          merge_commit: 12ead1aa00797f22ad0c674b11bd23c2ba130056
        origin_main: f0c75a965e19b78f9c018c406680b12caaf255c1
        origin_developer: 12ead1aa00797f22ad0c674b11bd23c2ba130056
        main_developer_file_delta_after_sync: none
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
- Release PR #330, tag `v1.5.3` и sync PR #331 завершены до этой задачи;
  rulesets не менялись.
- Изменение rulesets является human-gate действием: агент может подготовить
  evidence/status, но не меняет branch protection/rulesets без явного решения
  человека.

## Передача

Следующий: methodology architect - выбрать next methodology-hardening item или
downstream adoption task после `v1.5.3`; перед будущей release boundary обновить
этот snapshot при необходимости.
