# Engine Journal

In the reusable methodology/template repository this folder is scaffold only.
`input/` and `output/` are intentionally empty except `.gitkeep`; real task and
result files are created in target repositories after adoption.

Do not copy methodology operational history into target repositories.

Этот каталог хранит воспроизводимый журнал задач для `engine` и ответов `engine`.

Назначение:

- сохранить входные задачи в `input/`;
- сохранить ответы engine в `output/`;
- связать task -> result -> branch -> Pull Request -> commit/result;
- дать reviewer возможность восстановить историю проекта по GitHub files.

Правила:

- journal append-only по умолчанию;
- task/result files не удаляются и не перезаписываются без отдельного решения пользователя;
- private data, secrets, credentials, tokens, private repository URLs и production/runtime data запрещены;
- sensitive checks фиксируются только безопасным summary без matching lines.

Подробный contract:

```text
docs/agent-system/ENGINE_JOURNAL_CONTRACT.md
```
