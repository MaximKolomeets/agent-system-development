# RELEASE_READINESS

Дата проверки: 2026-08-09

Назначение: governance recovery после преждевременного `developer -> main -> developer`.
Следующий release candidate: `v1.6.0` (untagged, Human UAT PASS recorded).

## Release Status

- Status: `untagged_release_candidate_governance_recovery_complete`.
- Latest annotated tag: `v1.5.5` -> `f80e148f9e4ba965e701d1e06faa79d517b646cf`.
- Candidate `v1.6.0`: `59e645944697eac565d121e97d2dfa2ff3e9d99b` in `main`;
  tag отсутствует и запрещён до восстановления gates.
- `origin/main`: `59e645944697eac565d121e97d2dfa2ff3e9d99b`.
- Historical sync commit: `c0112ce7355cf6cdbce21dd1bf7bae6a0b9bf71b`.
- Current `developer`: historical sync, recovery PR #363, reservation PR #364,
  merged PR #365 с closure sequence 0174, merged policy fix PR #371 с closure
  sequence 0176 и merged full-payload reviewer gate PR #368 с closure sequence
  0175, а также merged governance-recovery gates PR #378 с closure sequence
  0177; это governance/journal delta, не новый release payload.
- Business Acceptance Gate: `human_pass_recorded`; authoritative decision:
  Human UAT v1.6.0 PASS для UAT-0173-01—05, owner/human architect, 2026-08-03.
- Reviewer consistency-gate: sequence 0175 завершена после human merge PR #368;
  RESULT/INDEX закрыты после merge, reservation consumed. Gate проверил полный
  release payload от peeled `v1.5.5^{}` (`f80e148f9e4ba965e701d1e06faa79d517b646cf`)
  до immutable reviewed head `fdf5b4cec319d91fcf202934de31f8414f2c3949`.
  `origin/main...origin/developer` не использовался как единственный range,
  поскольку `main` уже содержит преждевременно перенесённый payload.
- Governance-recovery gates: PR #378 merged в `developer`, merge commit
  `a554a71060b700b3b27a980160fbdb2ba2788b40`; sequence 0177 закрыта после
  merge, reservation consumed, snapshot-bound recovery evidence завершено.
- Следующий release action: первый этап полного final release pass — новая
  journaled reviewer consistency-gate на точном актуальном payload; immutable
  gate 0175 повторно не используется. Только после её human merge и closure
  выполняется release-policy gate и готовится отдельный PR `developer -> main`.
  Release merge, tag `v1.6.0`, GitHub Release и sync ещё не выполнялись.

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
- Сразу после этого исторического sync file delta отсутствовал; первым
  последующим delta был reservation ledger PR #362 для recovery 0173.
  Актуальный `developer` также содержит merged recovery PR #363 и reservation
  PR #364 для sequence 0174.
- PR #363: recovery PR merged в `developer` at `2026-08-03T05:30:33Z`, merge
  commit `4bb0640074490ee832466d3dafdecf5dffda5801`.
- PR #364: reservation PR merged в `developer` at `2026-08-03T07:07:00Z`, merge
  commit `22be882a230d4378fd737c031474213b3e5cfd38`; sequence 0174 принадлежит
  factual Human UAT evidence.
- PR #365: Human UAT evidence merged в `developer` at `2026-08-04T07:45:40Z`,
  merge commit `3342e128696f4f5900576504cd8ef64dce5d3e48`; sequence 0174
  закрыта, а reservation consumed.
- PR #378: governance-recovery gates merged в `developer` at
  `2026-08-09T12:21:25Z`, merge commit
  `a554a71060b700b3b27a980160fbdb2ba2788b40`; sequence 0177 закрыта после
  merge, reservation consumed.

## Journal Gate

- PR #359 merged; RESULT-0172 имеет status `merged`, INDEX-0172 закрыт, а
  ledger transition `0172: reserved -> consumed` уже записан.
- Recovery sequence 0173 документирует governance deviation и Human UAT Checklist.
- Sequence 0174 закрыта authoritative Human UAT PASS. Sequence 0175 завершила
  отдельную обязательную journaled reviewer consistency-gate задачу: PR #368
  merged, RESULT/INDEX закрыты после merge, reservation consumed.
- Sequence 0176 закрыла policy fix exact pre-merge verdict. Sequence 0177
  закрыла governance-recovery gates и snapshot-bound recovery evidence после
  human merge PR #378; RESULT/INDEX закрыты, reservation consumed.

## Generated Gates

Исторический набор ниже был обязательным для уже завершённого governance-recovery PR:

- `python -m unittest discover -s docs/agent-system/tools/tests -p "test_*.py" -v`.
- `python docs/agent-system/tools/validate_journal_triplet.py --base origin/developer --json`.
- `python docs/agent-system/tools/validate_policy_invariants.py --json`.
- `python docs/agent-system/tools/gen_file_map.py --check`.
- `python docs/agent-system/tools/gen_cloud_bundle.py --check`.
- `python docs/agent-system/tools/check_task_ready.py --base origin/developer --json`.

Для активного полного final release pass `v1.6.0` release manager обязан повторить
полный methodology check-set на точном кандидате и отдельно выполнить production
release-policy gate:

- `python docs/agent-system/tools/release_gate.py --version v1.6.0 --governance-recovery --json`.

Флаг `--governance-recovery` обязателен для текущего recovery-baseline, где
`main` уже опережает последний release tag; он не пропускает стандартные gates
и не заменяет полный final release pass.

## Release Recommendation

Rollback не выполняется автоматически: release payload уже в `main` и
`developer`, file delta исторического sync пуст, а tag отсутствует. `v1.6.0`
не считать published release. Human UAT PASS, full-payload reviewer gate,
policy fix и governance-recovery evidence sequences 0174–0177 завершены.
Следующий шаг — новая journaled reviewer consistency-gate на точном актуальном payload как первый этап полного final release pass; release merge, tag, GitHub Release и
sync остаются невыполненными human-only действиями.

## Передача

Следующий: release manager — начать полный final release pass с новой journaled reviewer consistency-gate на точном актуальном payload; после её human merge и closure подготовить
release PR `developer -> main`; merge, tag `v1.6.0`, GitHub Release и sync не
выполнять до отдельных human-authorized циклов.
