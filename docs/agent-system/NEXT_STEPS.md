# NEXT_STEPS

Консолидация методологии (`RESULT-0004`, C1–C6) завершена. После review-only прохода `METH-REVIEW-2026-06-16-01` текущая fix-задача закрывает найденные blockers. После merge этого PR основной следующий шаг — применять методологию к реальному target-проекту.

## Основной следующий шаг

1. После merge `METH-FIX-REVIEW-BLOCKERS-2026-06-16-01` применять методологию к реальному target implementation repository (adoption) по канону `docs/agent-system/templates/ADOPTION_PROMPT.md`: начать с `audit-only`, зафиксировать `methodology_reference` с commit SHA, собрать Methodology feedback с sanitization.

## Опциональный backlog (на усмотрение архитектора)

- **Review journaling polish**: blocker по PR-C6.1 закрыт. `Journal trace: always` и `Report delivery` разведены; future polish допустим только как wording cleanup без blocker status.
- **Чистка redirect-заглушек** — выполнено (METH-BACKLOG-POLISH): 6 history-only заглушек удалены (`SHORT_TARGET_ADOPTION_PROMPT`, `REVIEW_TEMPLATE`, `NEW_PROJECT_BOOTSTRAP_PROMPT`, `PROJECT_CHAT_START_PROMPT_TEMPLATE`, `TARGET_REPOSITORY_ADOPTION_GUIDE`, `PROJECT_LIFECYCLE`); `templates/TARGET_REPOSITORY_ADOPTION_CHAT_PROMPT.md` оставлен заглушкой (внешние bookmark); живые ссылки перенаправлены на каноны; `ADOPTION_PROMPT.md` список «engine should find» обновлён на `ADOPTION_GUIDE.md`.
- **Optional polish**: отдельно можно рассмотреть vendor/public metadata hygiene и English wording там, где это не нарушает Russian-first policy; это не blocker для adoption.

## Текущие операционные правила

1. Применять обновленный `CHATGPT_RESPONSE_STANDARD.md` и `CHATGPT_RESPONSE_TEMPLATE.md` при подготовке новых Engine-блоков.
2. Проверять Fast Lane -> Engine escalation при любой write-action recommendation.
3. Проверять русские пользовательские заголовки и описания в Engine-блоках.
4. Проверять post-merge journal closure после сообщений о merge/release/sync: GitHub PR state должен совпадать с RESULT/INDEX state.
5. Если journal stale после merge, создавать docs-only Engine-блок на closure cleanup вместо ответа `все закрыто`.
6. Использовать `CODE_REVIEW_TASK_TEMPLATE.md` для первого безопасного review target implementation repository только после проверки, что task явно содержит режим, объект проверки, allowed/forbidden files и правило сохранения отчета. Review-задачи всегда журналируют TASK+RESULT (`Journal trace: always`).
7. При следующем target repository dry run фиксировать methodology feedback без private data и с sanitization checkpoint.
8. Перед любым sync/checkout/switch/pull/merge применять `Repository sync / checkout guard`: root, remote, branch и `git status --short`; dirty tree → STOP.
9. Отдельной future task рассмотреть tags/releases для methodology versioning, если commit-based `methodology_reference` окажется недостаточным.
