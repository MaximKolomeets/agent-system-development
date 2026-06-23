# TASK-0061-METH-STATE-REFRESH-PRE-RELEASE-01

Роль: docs-maintainer.
Исполнитель: на усмотрение архитектора.
Reasoning effort: средний.
Запуск: Local only.
Режим: Agent.

## Цель

Освежить живые state-секции перед release: `CURRENT_STATE.md` и `NEXT_STEPS.md` должны отражать, что pre-adoption аудит, cleanup-серия и terminal batch-closure завершены, journal закрыт по актуальному `INDEX`, оба generated-check зелёные и EOL-safe, следующий шаг — release `developer -> main` + tag, затем sync и downstream adoption.

## Baseline

- Repository: `MaximKolomeets/agent-system-development`.
- Base branch: `developer`.
- Work branch: `work/docs-maintainer-01/state-refresh-pre-release-01`.
- Baseline `developer`: `533899996a5d69196b4be12c325217f5c2b4abb2`.
- Verification source: local git + GitHub PR state.
- Verification timestamp: `2026-06-23T08:46:46+07:00`.
- Preconditions verified:
  - PR #204 state: `MERGED`.
  - `developer` == `origin/developer`.
  - `INDEX` содержит 0055..0060 в closed/closed-at-creation статусах.
  - `gen_file_map.py --check` и `gen_cloud_bundle.py --check` прошли до правок.

## Scope

Allowed files:

- `docs/agent-system/CURRENT_STATE.md`
- `docs/agent-system/NEXT_STEPS.md`
- `docs/agent-system/engine-journal/input/TASK-0061-METH-STATE-REFRESH-PRE-RELEASE-01.md`
- `docs/agent-system/engine-journal/output/RESULT-0061-METH-STATE-REFRESH-PRE-RELEASE-01.md`
- `docs/agent-system/engine-journal/INDEX.md`
- `docs/agent-system/cloud/**`

Forbidden:

- Каноны, шаблоны, контракты вне state-доков.
- Генераторы, manifest, file-map, `.gitattributes`.
- Переписывание append-only истории.
- Новые per-file `asof` / `developer_head_sha` штампы в state-доках.
- `.env`, runtime/CI/secrets/private downstream data.

## Requirements

1. Обновить live/standing sections `CURRENT_STATE.md` и `NEXT_STEPS.md` без hardcode PR/seq как source of truth.
2. Сохранить freshness deferral на `engine-journal/INDEX.md` и GitHub branch/tag state.
3. Не переписывать HIST-01 vendor literal, если он находится в append-only истории.
4. Не добавлять vendor literals в новые live sections.
5. Регенерировать `docs/agent-system/cloud/**`.
6. Проверить:
   - `python docs/agent-system/tools/gen_file_map.py --check`
   - `python docs/agent-system/tools/gen_cloud_bundle.py --check`
   - active internal link-check -> broken links 0
   - `git diff --check`

## Передача

Следующий: reviewer — проверить state-refresh PR; затем архитектор — merge state-refresh PR; затем engine — release-prep (закрыть 0061 per-task и подготовить release PR `developer -> main`, не мержить); затем архитектор — merge release PR + tag; затем engine — sync `main -> developer`, чистка веток, downstream adoption на tag.
