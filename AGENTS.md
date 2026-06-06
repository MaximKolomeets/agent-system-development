# AGENTS

## Agent development workflow

- Отвечать на русском.
- Docker-first.
- Не читать `.env`.
- Не коммитить `.env`.
- Не коммитить `.venv`.
- Не коммитить `data/`, `runtime/`, `dist/`, `backups/`, `exports/`.
- Не использовать реальные credentials.
- Не менять `main` напрямую.
- Не менять `developer` напрямую без отдельного разрешения.
- Все изменения через отдельную ветку и Pull Request после bootstrap-этапа.
- Одна задача = одна ветка = один PR.
- Каждый агент работает только в своем namespace веток.
- Рабочие ветки создаются от актуальной `developer` в формате `work/<role>/<task>`.
- После bootstrap `developer` принимает изменения только через PR из `work/<role>/*`, кроме отдельного решения пользователя.
- Каждый агент использует свой GitHub TOKEN.
- Research/Review агенты не ставят задачи development executor напрямую.
- После задачи агент обязан обновить свой отчет.
- После архитектурного решения обновляется `docs/agent-system/DECISION_LOG.md`.
- После изменения состояния проекта обновляется `docs/agent-system/CURRENT_STATE.md`.
- Названия агентов не должны содержать Codex, Claude, Gemini, Copilot и другие vendor/tool names.
- Конкретный инструмент указывается отдельно как engine.
