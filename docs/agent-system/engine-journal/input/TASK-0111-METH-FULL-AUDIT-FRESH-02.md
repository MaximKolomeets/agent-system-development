```yaml
task_contract:
  version: 1
  task_id: METH-FULL-AUDIT-FRESH-02
  role: code-reviewer-01
  mode: review_only
  execution_mode: local_only
  reasoning_effort: high

  repository:
    full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    base_branch: developer
    working_branch: work/code-reviewer-01/full-audit-fresh-02

  scope:
    allowed_files:
      - docs/agent-system/engine-journal/input/TASK-0111-METH-FULL-AUDIT-FRESH-02.md
      - docs/agent-system/engine-journal/output/RESULT-0111-METH-FULL-AUDIT-FRESH-02.md
      - docs/agent-system/engine-journal/INDEX.md
      - docs/agent-system/cloud/**
    forbidden_files:
      - .env
      - .env.*
      - data/**
      - runtime/**
      - dist/**
      - backups/**
      - exports/**
      - verification/**
      - product repositories
      - docs/agent-system/** (any methodology content outside the journal/cloud surfaces above — read-only)

  policies:
    journal: required
    cloud_regen: required
    generated_checks: conditional
    review: review_only
    merge: human_only
    closure_pr: false

  checks:
    required:
      - python docs/agent-system/tools/gen_file_map.py --check
      - python docs/agent-system/tools/gen_cloud_bundle.py --check
    optional:
      - python docs/agent-system/tools/check_task_ready.py --base origin/developer

  stop_conditions:
    - dirty_tree_before_start
    - current_branch_is_main_or_developer_with_changes
    - head_not_equal_origin_developer
    - my_seq_claimed_by_other
    - working_branch_exists
    - changed_file_outside_allowlist
    - methodology_content_edit_needed
    - tag_or_release_action_needed
    - generated_check_fail
    - through_closure_break_beyond_one_terminal_fold
```

# TASK-0111-METH-FULL-AUDIT-FRESH-02 / Полный baseline-аудит + backlog-триаж

Роль: code-reviewer-01. Режим: review_only (read-only по содержанию методологии). Reasoning effort: высокий. Запуск: local only.

## Цель

Occasional сквозной read-only аудит ВСЕЙ методологии на актуальном `developer` + триаж backlog. Baseline считается НЕИЗВЕСТНЫМ и устанавливается самим исполнителем через `gh`/`git`. Подтвердить целостность/согласованность, найти несоответствия/риски, по каждому backlog-пункту дать статус, включить в объём правки архитектора, сделанные без оркестратора (Фаза 0). Контент методологии не править — findings оформляются как рекомендованные fix-PR / human-action. Изменения только journal этой задачи + cloud regen.

## Claim-протокол (выполнен)

1. `git fetch --all --prune`; `developer` == `origin/developer` (FF не требовался, уже синхронизированы).
2. Прочитан фактический INDEX: last seq = `0110` → my_seq = `0111`.
3. Чужого claim на `0111` нет: нет tracked/untracked `TASK/RESULT-0111`, чистый `git status`, нет открытого PR/origin-ветки.
4. Ветки `work/code-reviewer-01/full-audit-fresh-02` нет локально/в origin.
5. Создана `work/code-reviewer-01/full-audit-fresh-02` от свежего `origin/developer`.
6. `execution_started_at`: `2026-06-26T21:36:56+07:00` (measured).

## Объём

Фаза 0 (инвентаризация изменений с прошлого полного аудита 0089), Фаза 1 (backlog-триаж), Фаза 2 (21 пункт объёма аудита) — см. оркестраторский промпт. Проверки `--check` запускаются последовательно (канон B-WIN). Sensitive/secret scan — filename/count-only.

## Разрешённые файлы

- `docs/agent-system/engine-journal/input/TASK-0111-METH-FULL-AUDIT-FRESH-02.md` (создать)
- `docs/agent-system/engine-journal/output/RESULT-0111-METH-FULL-AUDIT-FRESH-02.md` (создать)
- `docs/agent-system/engine-journal/INDEX.md` (добавить строку)
- `docs/agent-system/cloud/**` (регенерировать через `gen_cloud_bundle.py` ПОСЛЕ INDEX)

## STOP-условия

git-гарды; FF невозможен; HEAD != origin/developer; my_seq занят; рабочая ветка существует; разрыв сквозной закрытости сверх одной terminal-записи (зафиксировать, при серьёзности — не выдавать готовность); невозможно получить commit SHA для `methodology_reference`; любой `--check` FAIL; необходимость править контент методологии или ставить тег.

## Передача

Следующий: архитектор — ОДНО триаж-решение по находкам и backlog (что взять/отложить/добавить); НЕ авто-каскад фиксов. Release/adoption держим до решения.

Source-reminder: не применимо (baseline устанавливается из gh+git в этой задаче).
