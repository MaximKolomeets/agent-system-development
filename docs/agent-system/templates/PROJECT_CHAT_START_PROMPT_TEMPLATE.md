# PROJECT_CHAT_START_PROMPT_TEMPLATE

## Copy/paste prompt

```text
Используй актуальную методологию из:
https://github.com/MaximKolomeets/agent-system-development

Работай по Operational Fast Lane для проверок/cleanup.
GitHub состояние проверяй сам.
Engine-задачи оформляй через self-contained block и engine-journal.
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
