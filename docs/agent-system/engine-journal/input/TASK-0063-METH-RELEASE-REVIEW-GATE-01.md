# TASK-0063-METH-RELEASE-REVIEW-GATE-01

Роль: docs-maintainer.
Исполнитель: на усмотрение архитектора.
Reasoning effort: высокий.
Запуск: Local only.
Режим: Agent.

## Цель

Закрепить обязательный pre-release reviewer consistency-gate как часть release-gate перед human merge `developer -> main`.

## Baseline

- Repository: `MaximKolomeets/agent-system-development`.
- Base branch: `developer`.
- Work branch: `work/docs-maintainer-01/release-review-gate-01`.
- Baseline `developer`: `6d685d8b4504c20d3312ad5fe9fca55665f24a7c`.
- Verification timestamp: `2026-06-23T09:13:04+07:00`.
- Preconditions verified:
  - PR #205 merged.
  - PR #206 merged.
  - `developer` == `origin/developer`.
  - `INDEX` contains 0061 and 0062.
  - `gen_file_map.py --check` and `gen_cloud_bundle.py --check` passed before edits.

## Scope

Allowed files:

- `docs/agent-system/BRANCH_POLICY.md`
- `docs/agent-system/ENGINE_JOURNAL_CONTRACT.md`
- `docs/agent-system/engine-journal/input/TASK-0063-METH-RELEASE-REVIEW-GATE-01.md`
- `docs/agent-system/engine-journal/output/RESULT-0063-METH-RELEASE-REVIEW-GATE-01.md`
- `docs/agent-system/engine-journal/INDEX.md`
- `docs/agent-system/cloud/**`

Forbidden:

- Новый шаблон reviewer task.
- Иные каноны/шаблоны/контракты вне двух указанных файлов.
- Генераторы, `.gitattributes`, manifest, file-map.
- Append-only history rewrite.
- `main`/`developer` direct changes, release merge, tag creation.
- `.env`, secrets, runtime/CI/private downstream data.

## Requirements

1. `BRANCH_POLICY.md`: добавить reviewer consistency-gate как обязательный шаг перед human merge release PR; порядок gate должен включать `reviewer consistency-gate`.
2. `ENGINE_JOURNAL_CONTRACT.md`: добавить раздел «Pre-release reviewer consistency-gate» с focused delta-review, проверками release payload и отличием от полного аудита.
3. Не создавать новый шаблон.
4. Регенерировать `docs/agent-system/cloud/**`.
5. Проверить:
   - `python docs/agent-system/tools/gen_file_map.py --check`
   - `python docs/agent-system/tools/gen_cloud_bundle.py --check`
   - active internal link-check -> broken links 0
   - `git diff --check`

## Передача

Следующий: reviewer — проверить PR; затем архитектор — merge PR; затем engine — по обновлённому runway закрыть pre-release journal, выполнить journaled reviewer consistency-gate по release payload и продолжить release-prep; release держим до прохождения нового reviewer-gate.
