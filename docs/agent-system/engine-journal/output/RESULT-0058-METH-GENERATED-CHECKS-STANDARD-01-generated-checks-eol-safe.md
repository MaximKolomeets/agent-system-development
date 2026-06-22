# RESULT-0058-METH-GENERATED-CHECKS-STANDARD-01

Статус: open; materialized before PR creation.

## Кратко

Кодифицировано правило из RESULT-0056 / PR #200: generated text `--check` должен быть content-oriented и EOL-safe, чтобы Windows checkout / `core.autocrlf` не создавали false drift, а реальный content-drift всё ещё ловился.

## Baseline

- Repository: `MaximKolomeets/agent-system-development`
- Base branch: `developer`
- Work branch: `work/docs-maintainer-01/generated-checks-standard-01`
- Baseline developer SHA: `b6cd0a817f93b06e09b28c88a460b670cf6b4aae`
- PR #199: `MERGED`; merge commit `813bbb676703a439aed255d0654ca2f65cd240f2`; merged at `2026-06-22T12:57:48Z`.
- PR #200: `MERGED`; merge commit `01d99a6716f38b6301c3ae87b7cc2c71d2b0c7fb`; merged at `2026-06-22T13:24:52Z`.
- Verification timestamp: `2026-06-22T20:52:27+07:00`.

## Что изменено

- Выбранный канон: `docs/agent-system/ORCHESTRATOR_OPERATING_CONTRACT.md`.
- Обоснование выбора: этот файл уже содержит human canon для cloud staging и `gen_cloud_bundle.py --check` content-parity gate; новое правило помещено рядом с существующим gate без создания нового inventory-файла.
- В `ORCHESTRATOR_OPERATING_CONTRACT.md` добавлен раздел «Проверки generated text artifacts: content-oriented / EOL-safe».
- В `docs/agent-system/BRANCH_POLICY.md` release-gate добавлена кросс-ссылка на этот раздел.
- `docs/agent-system/cloud/**` регенерирован после изменения bundle-файлов и INDEX.
- Journal: создан TASK/RESULT 0058 и добавлена строка INDEX.

## Нормативное правило

- Generated text artifact checks сравнивают content, а не байтовую форму checkout.
- Перед сравнением text-content нормализует `CRLF`, `CR` и `LF` к `LF`.
- Windows checkout и `core.autocrlf` не должны создавать false drift.
- Новый generator с `--check` обязан иметь regression-проверку: EOL-only drift не ломает gate, реальный content-drift приводит к ненулевому exit.
- Generated-bundle paths закрепляются через `.gitattributes` как `text eol=lf`; это дополняет normalized compare, но не заменяет его.

## Методологические закономерности

- Применим: для всех будущих generated text gates нужен единый минимум review: EOL-only drift должен быть tolerated, реальный content-drift должен оставаться fail-fast, а generated paths желательно фиксировать через `.gitattributes`. Это уже применено как standing rule в каноне, без расширения в отдельный framework.

## Проверки

- `python docs/agent-system/tools/gen_file_map.py --check` -> exit 0.
- `python docs/agent-system/tools/gen_cloud_bundle.py --check` -> exit 0.
- active internal link-check (new cross-link) -> exit 0: `BRANCH_POLICY.md` ссылается на `docs/agent-system/ORCHESTRATOR_OPERATING_CONTRACT.md` → «Проверки generated text artifacts: content-oriented / EOL-safe», heading найден.
- `git diff --check` -> exit 0.
- Branch guard перед commit -> `work/docs-maintainer-01/generated-checks-standard-01`.

## Source Delta

| путь | действие | категория | Source-рекомендация | manifest обновлён? |
| --- | --- | --- | --- | --- |
| `docs/agent-system/ORCHESTRATOR_OPERATING_CONTRACT.md` | modified | source | update | n-a |
| `docs/agent-system/BRANCH_POLICY.md` | modified | source | update | n-a |
| `docs/agent-system/cloud/00_README.md` | modified | generated | none | n-a |
| `docs/agent-system/cloud/01_ORCHESTRATOR_OPERATING_CONTRACT.md` | modified | generated | none | n-a |
| `docs/agent-system/cloud/04_BRANCH_POLICY.md` | modified | generated | none | n-a |
| `docs/agent-system/cloud/07_ENGINE_JOURNAL_INDEX.md` | modified | generated | none | n-a |
| `docs/agent-system/engine-journal/input/TASK-0058-METH-GENERATED-CHECKS-STANDARD-01-generated-checks-eol-safe.md` | added | journal | none | n-a |
| `docs/agent-system/engine-journal/output/RESULT-0058-METH-GENERATED-CHECKS-STANDARD-01-generated-checks-eol-safe.md` | added | journal | none | n-a |
| `docs/agent-system/engine-journal/INDEX.md` | modified | journal | none | n-a |

Source-reminder: обновить Source-снапшот у зарегистрированных потребителей: `docs/agent-system/SOURCE_CONSUMERS.md` scaffold-only, upstream registry has no concrete consumers; consuming deployments should update their own registered source snapshots.

Архитектору — загрузить в контекст оркестратора: `00_README.md` (src: generated bundle guide), `01_ORCHESTRATOR_OPERATING_CONTRACT.md` (src: `docs/agent-system/ORCHESTRATOR_OPERATING_CONTRACT.md`), `04_BRANCH_POLICY.md` (src: `docs/agent-system/BRANCH_POLICY.md`), `07_ENGINE_JOURNAL_INDEX.md` (src: `docs/agent-system/engine-journal/INDEX.md`); asof: `2026-06-22T20:47:50+07:00`; developer_head_sha: `b6cd0a817f93b06e09b28c88a460b670cf6b4aae`.

## Journal finalization

- PR URL: pending after PR creation.
- PR status after journal finalization: pending.
- RESULT finalized: no, pending PR creation.
- INDEX finalized: no, pending PR creation.
- No journal placeholders: no, pending PR creation.
- Report delivery: chat.
- Journal trace: always.

## Локальные действия после PR/merge

- После PR creation обновить RESULT/INDEX фактическими PR URL/status и допушить follow-up commit.
- После merge этой задачи journal closure остаётся batch перед release вместе с seq 0055/0056 и следующими блоками.

## Передача

Следующий: reviewer — проверить PR, что EOL-safe/content-oriented rule закреплён в каноне, release-gate ссылается на него, генераторы не менялись, оба `--check` и link-check проходят; затем архитектор — merge PR; затем engine — batch-closure journal (0055/0056/Блок2/Блок3); затем state-refresh + оба `--check`; затем release `developer -> main` (merge выполняет архитектор) + sync.
