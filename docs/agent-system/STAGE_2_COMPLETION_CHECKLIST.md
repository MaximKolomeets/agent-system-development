# STAGE_2_COMPLETION_CHECKLIST

## Назначение

Этот checklist нужен для проверки готовности methodology stage перед первым target repository dry run.

## Required artifacts

- [ ] `PROJECT_LIFECYCLE.md` exists.
- [ ] `NEW_PROJECT_ONBOARDING_GUIDE.md` exists.
- [ ] `TARGET_REPOSITORY_ADOPTION_GUIDE.md` exists.
- [ ] `ADOPTION_GUIDE.md` exists.
- [ ] `ADOPTION_TRANSFER_MANIFEST.yml` exists.
- [ ] `DOWNSTREAM_ADAPTATION_CHECKLIST.md` exists.
- [ ] `ENGINE_ENTRYPOINT.md` exists.
- [ ] `ENGINE_SELF_DISCOVERY_CONTRACT.md` exists.
- [ ] `METHODOLOGY_FEEDBACK_LOOP.md` exists.
- [ ] `SHORT_TARGET_ADOPTION_PROMPT.md` exists.
- [ ] reusable templates exist.
- [ ] branch policy exists.
- [ ] workflow exists.
- [ ] PR workflow exists.
- [ ] worktree guide exists.
- [ ] publication policy exists.
- [ ] CI policy exists.
- [ ] forbidden files CI exists.
- [ ] docs-maintainer reports exist.
- [ ] handoff template exists.
- [ ] target repository bootstrap task template exists.
- [ ] short prompt adoption mode documented.
- [ ] audit-only, docs-only adoption and runtime adoption modes documented.
- [ ] minimal first PR creates only `ADOPTION_AUDIT.md`.
- [ ] downstream checklist includes repository name, branch model, worktree paths, current state and visibility.
- [ ] developer vs develop and CI branch filters are documented.
- [ ] PowerShell/UTF-8 note for Russian Markdown is documented.
- [ ] `CURRENT_STATE.md` verbatim copy is forbidden.
- [ ] target repository final report includes Methodology feedback.
- [ ] feedback does not expose private data.

## Process readiness

- [ ] one task = one branch = one PR;
- [ ] work branches use `work/<role>/<task>`;
- [ ] developer receives changes through PR;
- [ ] main receives stable state from developer;
- [ ] developer sync after main release is handled through PR if ruleset requires it;
- [ ] user manually launches engine;
- [ ] ChatGPT reviews reports and prepares next tasks;
- [ ] user makes final decisions.

## Security readiness

- [ ] `.env` is forbidden;
- [ ] `.venv/` is forbidden;
- [ ] `data/`, `runtime/`, `dist/`, `backups/`, `exports/` are forbidden;
- [ ] real credentials/tokens/passwords/API keys are forbidden;
- [ ] sensitive grep is part of review;
- [ ] public repository rules are documented;
- [ ] target repository visibility is handled separately.

## Documentation readiness

- [ ] `CURRENT_STATE.md` is current;
- [ ] `NEXT_STEPS.md` is current;
- [ ] `DECISION_LOG.md` has current decisions;
- [ ] Source index is current;
- [ ] docs-maintainer summary is current;
- [ ] next chat prompt is current.

## Known issues

- На момент PR-2c workflow был updated to Node.js 24 compatible checkout action.
- Если GitHub Actions снова покажет runtime warning, это должно идти отдельным PR.
- Practical target repository dry run еще не выполнен.
- First target repository dry run feedback показал, что нужны adoption modes, transfer manifest и более строгий minimal first PR.

## Completion criteria

Этап считается готовым, если:

- PR-2g merged в `developer`;
- PR-2g released в `main`;
- `developer` синхронизирован с `main`;
- stage checklist заполнен;
- следующий шаг - повторный target repository dry run в `audit-only` режиме.
