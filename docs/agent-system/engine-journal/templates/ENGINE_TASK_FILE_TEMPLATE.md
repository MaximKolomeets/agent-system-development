# ENGINE_TASK_FILE_TEMPLATE

Task file:

Task id:

Seq:

Created at:

Created by:

Target repository:

Methodology repository:

Agent:

Engine:

Base branch:

Working branch:

Allowed files:

- `<allowed path>`

Forbidden files:

- `.env`
- `.venv/`
- `data/`
- `runtime/`
- `dist/`
- `backups/`
- `exports/`
- credentials
- tokens
- private keys
- real passwords
- private repository URLs
- private downstream project names
- client/customer data
- production/runtime data

Objective:

Context:

Preflight:

BEGIN POWERSHELL
# Вставить команды preflight для engine.
END POWERSHELL

STOP conditions:

- working tree dirty before changes;
- pull fast-forward impossible;
- forbidden files detected;
- private data or secrets required;
- scope expands beyond allowed files.

Checks:

BEGIN POWERSHELL
# Вставить команды проверки результата.
END POWERSHELL

Commit policy:

PR policy:

Expected output file:

Final report requirements:

- branch;
- commit SHA;
- PR URL;
- changed files;
- checks run;
- checks not run and why;
- forbidden files result;
- sensitive/private marker result;
- risks;
- result file finalized;
- index entry finalized;
- no journal placeholders;
- follow-up commit SHA if finalization required;
- next recommended step.
