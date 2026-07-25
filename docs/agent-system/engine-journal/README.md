# Engine Journal

В target transfer mode этот каталог передаётся только как scaffold: `README.md`,
`INDEX.md`, `input/`, `rationale/`, `output/` и templates без operational rows.
В methodology operation mode repository хранит собственную append-only историю
TASK/RATIONALE/RESULT; она не переносится в target repository.

Do not copy methodology operational history into target repositories.

Этот каталог хранит воспроизводимый журнал задач для `engine` и ответов `engine`.

Назначение:

- сохранить входные задачи в `input/`;
- сохранить RATIONALE в `rationale/`;
- сохранить ответы engine в `output/`;
- связать TASK -> RATIONALE -> RESULT -> branch -> Pull Request -> commit/result;
- дать reviewer возможность восстановить историю проекта по GitHub files.

Правила:

- journal append-only по умолчанию;
- TASK/RATIONALE/RESULT files не удаляются и не перезаписываются без отдельного решения пользователя;
- старые finalized RESULT могут переноситься в `archive/vX.Y.Z/` только
  отдельным post-release archive PR по `JOURNAL_ARCHIVING_POLICY.md`;
- archive files не входят в default context bundle;
- private data, secrets, credentials, tokens, private repository URLs и production/runtime data запрещены;
- sensitive checks фиксируются только безопасным summary без matching lines.

Подробный contract:

```text
docs/agent-system/ENGINE_JOURNAL_CONTRACT.md
```
