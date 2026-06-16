# NEXT_STEPS

Консолидация методологии (`RESULT-0004`, C1–C6) завершена. Методология финальная и облегчённая; основной следующий шаг — применять её к реальному target-проекту.

## Основной следующий шаг

1. Применять методологию к реальному target implementation repository (adoption) по канону `docs/agent-system/templates/ADOPTION_PROMPT.md`: начать с `audit-only`, зафиксировать `methodology_reference` с commit SHA, собрать Methodology feedback с sanitization.

## Опциональный backlog (на усмотрение архитектора)

- **PR-C6.1**: согласовать `ENGINE_JOURNAL_CONTRACT.md` (явная отметка про review-journal) и `OPERATIONAL_FAST_LANE.md` (review ≠ Fast Lane) с дефолтом «review журналирует всегда» (отложено из C6).
- **Чистка redirect-заглушек** — выполнено (METH-BACKLOG-POLISH): 6 history-only заглушек удалены (`SHORT_TARGET_ADOPTION_PROMPT`, `REVIEW_TEMPLATE`, `NEW_PROJECT_BOOTSTRAP_PROMPT`, `PROJECT_CHAT_START_PROMPT_TEMPLATE`, `TARGET_REPOSITORY_ADOPTION_GUIDE`, `PROJECT_LIFECYCLE`); `templates/TARGET_REPOSITORY_ADOPTION_CHAT_PROMPT.md` оставлен заглушкой (внешние bookmark); живые ссылки перенаправлены на каноны; `ADOPTION_PROMPT.md` список «engine should find» обновлён на `ADOPTION_GUIDE.md`.

## Текущие операционные правила

1. Применять обновленный `CHATGPT_RESPONSE_STANDARD.md` и `CHATGPT_RESPONSE_TEMPLATE.md` при подготовке новых Engine-блоков.
2. Проверять Fast Lane -> Engine escalation при любой write-action recommendation.
3. Проверять русские пользовательские заголовки и описания в Engine-блоках.
4. Проверять post-merge journal closure после сообщений о merge/release/sync: GitHub PR state должен совпадать с RESULT/INDEX state.
5. Если journal stale после merge, создавать docs-only Engine-блок на closure cleanup вместо ответа `все закрыто`.
6. Использовать `CODE_REVIEW_TASK_TEMPLATE.md` для первого безопасного review target implementation repository только после проверки, что task явно содержит режим, объект проверки, allowed/forbidden files и правило сохранения отчета. Review-задачи всегда журналируют TASK+RESULT (`Journal trace: always`).
7. При следующем target repository dry run фиксировать methodology feedback без private data и с sanitization checkpoint.
8. Отдельной future task рассмотреть tags/releases для methodology versioning, если commit-based `methodology_reference` окажется недостаточным.
