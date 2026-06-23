# RESULT-0063-METH-RELEASE-REVIEW-GATE-01

Статус: ready for review.

## Summary

Закреплён обязательный pre-release reviewer consistency-gate:

- `BRANCH_POLICY.md` теперь запрещает release PR `developer -> main` до journaled reviewer consistency-gate по release payload и включает этот шаг в порядок gate.
- `ENGINE_JOURNAL_CONTRACT.md` получил раздел «Pre-release reviewer consistency-gate» с focused delta-review release payload, checklist и отличием от полного аудита методологии.
- Новый шаблон не создавался; канон использует существующий reviewer task pattern.
- `docs/agent-system/cloud/**` регенерирован.

## Exact canon changes

### BRANCH_POLICY

- Добавлен bullet: release PR запрещён, пока не выполнен journaled reviewer consistency-gate по release payload; reviewer read-only по содержанию, `Journal trace: always`, ветка `work/<reviewer-role>/<task>`, docs-only PR в `developer`; канон проверок — `ENGINE_JOURNAL_CONTRACT.md` → «Pre-release reviewer consistency-gate».
- Порядок gate обновлён: `journal closed -> batch-closure -> gen_file_map.py --check -> gen_cloud_bundle.py --check -> state-refresh -> reviewer consistency-gate -> human merge`.

### ENGINE_JOURNAL_CONTRACT

Добавлен раздел «Pre-release reviewer consistency-gate»:

- gate обязателен перед каждым release `developer -> main`, после state-refresh и до human merge;
- это focused delta-review release payload, не повтор полного аудита;
- роль reviewer работает read-only по содержанию, с `Journal trace: always`, `Report delivery: chat`, через `work/<reviewer-role>/<task>` и docs-only journal PR;
- release payload определяется как `origin/main...origin/developer`;
- reviewer проверяет соответствие payload merged-серии по `INDEX`, оба `--check`, сквозную закрытость journal, Source Delta/context handoff по серии, release notes, отсутствие placeholders и агрегированное применение per-PR checks;
- любой невыполненный пункт блокирует release;
- reviewer-gate закрывается per-task в release-prep;
- полный аудит методологии остаётся отдельным baseline-проходом по необходимости, не регулярным release gate.

## Checks

- `python docs/agent-system/tools/gen_file_map.py --check` -> exit 0.
- `python docs/agent-system/tools/gen_cloud_bundle.py --check` -> exit 0.
- active internal link-check -> `broken_links 0`.
- `git diff --check` -> exit 0.
- BRANCH_POLICY gate order scan -> exit 0: `reviewer consistency-gate -> human merge` present.
- ENGINE_JOURNAL_CONTRACT section scan -> exit 0: `Pre-release reviewer consistency-gate` present.
- branch guard before commit -> `work/docs-maintainer-01/release-review-gate-01`.

## Source Delta

| путь | действие | категория | Source-рекомендация | manifest обновлён? |
| --- | --- | --- | --- | --- |
| `docs/agent-system/BRANCH_POLICY.md` | modified | source | update | n-a |
| `docs/agent-system/ENGINE_JOURNAL_CONTRACT.md` | modified | source | update | n-a |
| `docs/agent-system/engine-journal/INDEX.md` | modified | journal | none | n-a |
| `docs/agent-system/engine-journal/input/TASK-0063-METH-RELEASE-REVIEW-GATE-01.md` | added | journal | none | n-a |
| `docs/agent-system/engine-journal/output/RESULT-0063-METH-RELEASE-REVIEW-GATE-01.md` | added | journal | none | n-a |
| `docs/agent-system/cloud/00_README.md` | modified | generated | none | n-a |
| `docs/agent-system/cloud/04_BRANCH_POLICY.md` | modified | generated | none | n-a |
| `docs/agent-system/cloud/05_ENGINE_JOURNAL_CONTRACT.md` | modified | generated | none | n-a |
| `docs/agent-system/cloud/07_ENGINE_JOURNAL_INDEX.md` | modified | generated | none | n-a |

Source-reminder: каноны менялись. Обновить Source-снапшот у зарегистрированных потребителей: `<заполнить по docs/agent-system/SOURCE_CONSUMERS.md в потребляющем развёртывании>`; upstream registry scaffold-only и не содержит реальных потребителей.

## Context handoff

Архитектору — загрузить в контекст оркестратора: `00_README.md` (src: generated bundle guide), `04_BRANCH_POLICY.md` (src: `docs/agent-system/BRANCH_POLICY.md`), `05_ENGINE_JOURNAL_CONTRACT.md` (src: `docs/agent-system/ENGINE_JOURNAL_CONTRACT.md`), `07_ENGINE_JOURNAL_INDEX.md` (src: `docs/agent-system/engine-journal/INDEX.md`); asof: `2026-06-23T09:11:07+07:00`; developer_head_sha: `6d685d8b4504c20d3312ad5fe9fca55665f24a7c`.

## Journal finalization

- PR URL: https://github.com/MaximKolomeets/agent-system-development/pull/207
- PR status after journal finalization: OPEN; mergeable: MERGEABLE.
- PR head after first publication: `593b8b87c21da06c25b1987a597d23443e22d266`.
- RESULT finalized: yes.
- INDEX finalized: yes.
- No journal placeholders: yes.

## Локальные действия после PR/merge

- PR #207 создан; RESULT/INDEX финализированы фактическим PR URL/status; follow-up commit допушен в тот же PR.
- После merge PR: engine должен закрыть pre-release journal, выполнить journaled reviewer consistency-gate по release payload и продолжить release-prep; release держать до прохождения reviewer-gate.

## Передача

Следующий: reviewer — проверить PR; затем архитектор — merge PR; затем engine — по обновлённому runway closure + journaled reviewer consistency-gate по release payload + release-prep; release держим до прохождения нового reviewer-gate.
