# Шаблон reviewer pass для review autoloop

## Режим

Роль: reviewer
Режим: review-only
Branch/PR: active work PR
Правки файлов: запрещены

## Входные данные

- PR URL: `<pr-url>`
- Expected head SHA: `<head-sha>`
- `max_review_cycles`: `<n>`
- Current cycle: `<n>`
- Scope summary: `<scope>`

## Проверить

1. PR head SHA совпадает с expected head SHA.
2. Diff соответствует scope задачи.
3. Checks зелёные или failures классифицированы как blocker.
4. Forbidden paths/secrets/runtime/private data отсутствуют.
5. Review feedback относится к этой task branch.
6. PR title/body, commit metadata, review summary и journal/final report соблюдают Russian-first policy.
7. Если PR меняет downstream/adoption/source-update правила, `methodology_reference` использует stable ref `origin/main` / `main`, release tag или явно заданный snapshot, а не `developer`/`work/*`.
8. `max_review_cycles` не превышен.

## Вывод в PR

Reviewer оставляет feedback только в PR агента:

- `reviewer:approved` + `architect:ready-to-merge`, если blockers нет;
- `reviewer:changes-requested`, если есть blockers/actionable feedback;
- `automation:stopped-human-required`, если сработал STOP.
- Если GitHub не позволяет formal review из-за own-PR / author limitation, оставить top-level PR comment с тем же `verdict`, `reviewed_head_sha` и blocker IDs; это approve-equivalent / changes-requested-equivalent для autoloop.

## STOP-условия

- secrets-risk или forbidden paths;
- failed checks, которые нельзя безопасно классифицировать;
- scope drift;
- Russian-first metadata/report violation в ready-for-review PR;
- downstream stable methodology reference подменён на `developer`, `work/*` или open methodology PR branch;
- нужен architecture/product/security decision;
- превышен `max_review_cycles`;
- PR head SHA не совпал.

## Формат verdict

```yaml
verdict: reviewer:approved | reviewer:changes-requested | automation:stopped-human-required
reviewed_head_sha: <sha>
cycle: <current>/<max>
blocking_findings:
  - id: B-01
    class: machine-verifiable | semantic | mixed
    title: <короткое имя blocker>
    evidence: <файл/строка/команда/наблюдение>
    required_change: <что нужно изменить>
    verification_command: <команда или explicit manual check>
    can_engine_fix_without_architect: yes | no
non_blocking_notes:
  - id: N-01
    title: <короткое имя note>
    recommendation: <что улучшить>
required_fix_scope:
  - <разрешённые файлы/область fix-pass>
commands_to_rerun:
  - <command>
re_review_policy:
  scope: none | machine_check_only | changed_blockers_only | full
  reason: <почему этого достаточно>
own_pr_review_limitation:
  applies: yes | no
  fallback_comment_url: <url-or-n-a>
next:
  - architect merge | engine fix-pass | human decision
```

Правила классов:

- `machine-verifiable`: закрывается указанной `verification_command`; при passed command и unchanged scope допускается `machine_check_only` без полного re-review.
- `semantic`: требует reviewer re-review по changed blocker scope.
- `mixed`: machine-часть закрывается командами, но semantic часть требует re-review.
