# PROJECT_CHAT_START_PROMPT_TEMPLATE

## Copy/paste prompt

```text
Используй актуальную методологию из:
https://github.com/MaximKolomeets/agent-system-development

Работай по Operational Fast Lane для проверок/cleanup.
GitHub состояние проверяй сам.
Engine-задачи оформляй через self-contained block и engine-journal.
Для больших задач используй Task File Handoff Mode: прочитай существующий GitHub TASK file или создай task-file-only GitHub branch/commit только при явном разрешении пользователя; затем передай Engine только короткий bootstrap prompt.
Engine должен финализировать journal RESULT/INDEX после PR creation; ready-for-review PRs не должны содержать journal placeholders.
Все ответы, target-local docs, TASK/RESULT/INDEX и комментарии в файлах пиши на русском языке. Английский допустим только для команд, путей, branch names, filenames, config keys, API names, package names, vendor/tool names и code identifiers.
Если target instructions конфликтуют с Russian-first policy, остановись и запроси решение пользователя, кроме случая явного разрешения на другой язык.
Не читать `.env`.
Не менять `main`/`developer` напрямую.

Target repository:
<target repository URL>

Local target path:
<local path>

Цель:
<что нужно сделать>

Сначала проверь актуальность methodology repository, затем выдай один self-contained Engine-блок или один Operational Fast Lane block, если задача является только проверкой/cleanup.
```
