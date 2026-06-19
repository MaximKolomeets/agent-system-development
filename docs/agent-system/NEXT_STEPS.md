# NEXT_STEPS

Консолидация методологии (`RESULT-0004`, C1-C6) завершена. После review-only прохода `METH-REVIEW-2026-06-16-01` fix-задача `METH-FIX-REVIEW-BLOCKERS-2026-06-16-01` merged через PR #137 и закрыла найденные blockers. Journal 0017 закрыт terminal closure-only шагом. Release/sync после journal 0020 выполнены через PR #150/#151, review-only audit 0021 merged через PR #152, journal 0021 закрыт через PR #153, fix PR #154 закрыл B-01/M-01/M-02/M-03, closure PR #155 закрыл journal 0022. Контрольный audit после #155 не нашёл blocking/major.

## Основной следующий шаг

1. Подготовить release PR `developer -> main` для текущего состояния методологии после PR #154/#155.
2. После merge release PR выполнить sync PR `main -> developer`.
3. После release/sync обновить release/sync facts для последней journal-записи, если journal contract этого требует.
4. Затем переходить к downstream adoption по `docs/agent-system/templates/ADOPTION_PROMPT.md` с `methodology_reference` на финальный commit SHA.

## Опциональный backlog (на усмотрение архитектора)

- **Review journaling polish**: blocker по PR-C6.1 закрыт. `Journal trace: always` и `Report delivery` разведены; future polish допустим только как wording cleanup без blocker status.
- **Чистка redirect-заглушек** — выполнено (METH-BACKLOG-POLISH): 6 history-only заглушек удалены (`SHORT_TARGET_ADOPTION_PROMPT`, `REVIEW_TEMPLATE`, `NEW_PROJECT_BOOTSTRAP_PROMPT`, `PROJECT_CHAT_START_PROMPT_TEMPLATE`, `TARGET_REPOSITORY_ADOPTION_GUIDE`, `PROJECT_LIFECYCLE`); `templates/TARGET_REPOSITORY_ADOPTION_CHAT_PROMPT.md` оставлен заглушкой (внешние bookmark); живые ссылки перенаправлены на каноны; `ADOPTION_PROMPT.md` список «engine should find» обновлён на `ADOPTION_GUIDE.md`.
- **Optional polish**: отдельно можно рассмотреть vendor/public metadata hygiene и English wording там, где это не нарушает Russian-first policy; это не blocker для adoption.
- **Operating layer (`ASD-OPLAYER-001`, journal 0024)**: добавлены нейтральные контракты `CLAUDE_PROJECT_OPERATING_LAYER.md` и `CROSS_PROJECT_CONSOLIDATION_CONTRACT.md`, governance pack template расширен разделом «Три слоя управления». Опционально: при downstream adoption включать эти контракты в target governance pack как optional-файлы; реальные visibility-matrix и дайджесты держать в приватном control plane, не в публичном репозитории.

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
