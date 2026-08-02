# RELEASE_READINESS

Дата проверки: 2026-08-02

Назначение: governance recovery после преждевременного `developer -> main -> developer`.
Следующий release candidate: `v1.6.0` (untagged, gates pending).

## Release Status

- Status: `untagged_release_candidate_governance_recovery`.
- Latest annotated tag: `v1.5.5` -> `f80e148f9e4ba965e701d1e06faa79d517b646cf`.
- Candidate `v1.6.0`: `59e645944697eac565d121e97d2dfa2ff3e9d99b` in `main`;
  tag отсутствует и запрещён до восстановления gates.
- `origin/main`: `59e645944697eac565d121e97d2dfa2ff3e9d99b`.
- Historical sync commit: `c0112ce7355cf6cdbce21dd1bf7bae6a0b9bf71b`.
- Current `developer`: historical sync плюс reservation-only ledger delta PR #362.
- Business Acceptance Gate: `pending_human_verdict`.
- Reviewer consistency-gate: `pending`.
- Следующий release action: только final recovery PR `developer -> main` после
  recovery, UAT verdict и reviewer gate.

## Release Facts

GitHub metadata фиксирует исторические факты без переписывания истории:

- PR #355: merged `developer -> main`, merge commit
  `7c00dd3a7d1e70fbe67b62a726a068aa384d5a24`.
- PR #356: merged `main -> developer`, merge commit
  `dcbace9e530ed2d9917ffe33b55fca7ca08fe602`, zero file delta.
- PR #359: boundary reconciliation merged в `developer`, merge commit
  `69a567035dd805cae8e822a462397142b3f436d0`.
- PR #360: преждевременный release `developer -> main`, merged
  `2026-08-02T09:39:56Z`, merge commit
  `59e645944697eac565d121e97d2dfa2ff3e9d99b`; post-merge CI successful.
- PR #361: преждевременный sync `main -> developer`, merged
  `2026-08-02T09:41:17Z`, merge commit
  `c0112ce7355cf6cdbce21dd1bf7bae6a0b9bf71b`, zero file delta.
- После этого исторического sync file delta отсутствовал; текущая разница
  `main/developer` — только reservation ledger PR #362 для recovery 0173.

## Journal Gate

- RESULT/INDEX 0172 и ledger transition `0172: reserved -> consumed` требуют
  финализации по GitHub merge facts PR #359.
- Recovery sequence 0173 документирует governance deviation, Human UAT Checklist
  и дальнейший порядок human-only gates.

## Generated Gates

Required for governance recovery PR:

- `python -m unittest discover -s docs/agent-system/tools/tests -p "test_*.py" -v`.
- `python docs/agent-system/tools/validate_journal_triplet.py --base origin/developer --json`.
- `python docs/agent-system/tools/validate_policy_invariants.py --json`.
- `python docs/agent-system/tools/gen_file_map.py --check`.
- `python docs/agent-system/tools/gen_cloud_bundle.py --check`.
- `python docs/agent-system/tools/check_task_ready.py --base origin/developer --json`.

## Release Recommendation

Rollback не выполняется автоматически: release payload уже в `main` и
`developer`, file delta исторического sync пуст, а tag отсутствует. `v1.6.0`
не считать published release. Сначала завершить recovery PR, Human UAT и
reviewer consistency-gate; затем подготовить новый final recovery release PR.

## Передача

Следующий: human architect — смержить recovery PR; затем owner/PO — пройти
Human UAT Checklist перед будущим final recovery release PR.
