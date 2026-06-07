# CI_POLICY

## Purpose

CI is an automatic guardrail for the public methodology repository.

The first CI check blocks forbidden tracked files and paths before they can be merged. CI does not replace review, manual checks, or repository rulesets.

## Forbidden tracked paths

The repository must not track these paths:

- `.env`
- `.env.*`, except `.env.example`
- `.venv/`
- `data/`
- `runtime/`
- `dist/`
- `backups/`
- `exports/`
- `*.log`
- `*.tmp`
- `*.bak`

## Allowed exceptions

- `.env.example` is allowed if it does not contain real secrets.
- Documents may contain the words `token`, `password`, `secret`, and `credential` only as security rules or examples without real values.

## Limitations

- CI checks only tracked files.
- CI does not analyze local untracked files.
- CI must not read `.env` contents.
- CI must not print secrets.
- Secret scanning and more advanced checks can be added as separate future tasks.

## GitHub Actions runtime compatibility

- The forbidden files workflow uses `actions/checkout@v5`.
- `actions/checkout@v5` was selected because its action metadata declares `using: node24`.
- If GitHub Actions reports runtime deprecation warnings again, verify the upstream action metadata before changing the workflow.
- Do not downgrade to an action runtime that produces deprecation warnings unless the user explicitly accepts the temporary risk.

## Local pre-check

Run these commands before commit or push:

```bash
git status --short
```

```bash
git ls-files
```

```bash
git grep -n -i "token\|password\|secret\|api_key\|apikey\|credential\|пароль\|токен"
```

`git grep` is only a manual review aid. If a possible real secret is found, do not print it further and stop for user review.
