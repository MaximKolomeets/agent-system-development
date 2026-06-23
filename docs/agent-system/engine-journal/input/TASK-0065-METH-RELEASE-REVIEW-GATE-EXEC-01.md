# TASK-0065-METH-RELEASE-REVIEW-GATE-EXEC-01

## Задача

Выполнить обязательный pre-release reviewer consistency-gate по release payload `developer -> main`.

Роль: `code-reviewer`.
Исполнитель: на усмотрение архитектора.
Режим: Local only; review по содержанию read-only.
Report delivery: chat.
Journal trace: always.

## Baseline

- Repository: `MaximKolomeets/agent-system-development`.
- Base branch: `developer`.
- Work branch: `work/code-reviewer-01/release-review-gate-exec-01`.
- Release candidate: `origin/developer` / local `developer` at `5aa98838f81a7f936b3319b491afcc9ebd7adfc1`.
- `origin/main`: `29c0f0ae98ee7ef8e8e29187360b490429da48d3`.
- Precondition: PR #208 merged; journal 0055..0064 closed/closed-at-creation.

## Scope

Проверить release payload как focused delta-review, не повторяя полный аудит методологии:

1. Payload integrity: `origin/main..origin/developer`, соответствие merged PR #199..#208.
2. Release-gate checks: `gen_file_map.py --check`, `gen_cloud_bundle.py --check`.
3. Сквозная закрытость journal 0055..0064.
4. Source Delta/context-handoff по серии.
5. Reviewer-gate canon в `BRANCH_POLICY.md` и `ENGINE_JOURNAL_CONTRACT.md`.
6. Active internal link-check по измененным markdown-докам.
7. Per-PR aggregate checks: task/result linkage, private/forbidden data, Russian-first, GitHub refs.
8. Vendor-neutrality/sanitization active payload.
9. Expected release notes composition for release-prep.

## Allowed files

- `docs/agent-system/engine-journal/input/TASK-0065-METH-RELEASE-REVIEW-GATE-EXEC-01.md`
- `docs/agent-system/engine-journal/output/RESULT-0065-METH-RELEASE-REVIEW-GATE-EXEC-01.md`
- `docs/agent-system/engine-journal/INDEX.md`
- `docs/agent-system/cloud/**` after `gen_cloud_bundle.py`

## Forbidden

- Не менять methodology content, generators, manifest, file-map, `.gitattributes`, runtime/CI/secrets/private data.
- Не открывать release PR и не менять `main`/`developer` напрямую.
- Findings фиксировать как recommended fix-PR, без исправления payload в этой задаче.

## Expected output

- Verdict: `GATE PASS` или `GATE BLOCKED`.
- Статус по всем 9 gate-пунктам.
- Findings с классификацией и recommended fix-PR.
- Source Delta, Source-reminder, context handoff.
- Передача следующему участнику.
