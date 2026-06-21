# NEXT_STEPS

Методология выпущена в `main` через release PR #177 и sync PR #178. После release в `developer` завершён fix-all цикл PR #179-#183: depersonalization cleanup, Architect -> Orchestrator context handoff, adoption templates sync, closure facts authority clarification и audit nits. Журнал закрыт до 0038; записи 0039-0044 относятся к текущему batch-policy циклу и закрываются перед следующим release.

## Основной следующий шаг

1. Выполнить pre-release batch-closure journal 0039-0044: закрыть merged work PR #179-#183 и текущую state-refresh запись 0044.
2. После review/merge batch-closure выполнить release PR `developer -> main` по rule 1 (human-only merge).
3. После release переходить к downstream adoption / реальному verification-проекту по `docs/agent-system/templates/ADOPTION_PROMPT.md` с `methodology_reference` на финальный commit SHA.

## Опциональный backlog (на усмотрение архитектора)

- **Review journaling polish**: blocker по PR-C6.1 закрыт. `Journal trace: always` и `Report delivery` разведены; future polish допустим только как wording cleanup без blocker status.
- **Чистка redirect-заглушек** — выполнено (METH-BACKLOG-POLISH): 6 history-only заглушек удалены (`SHORT_TARGET_ADOPTION_PROMPT`, `REVIEW_TEMPLATE`, `NEW_PROJECT_BOOTSTRAP_PROMPT`, `PROJECT_CHAT_START_PROMPT_TEMPLATE`, `TARGET_REPOSITORY_ADOPTION_GUIDE`, `PROJECT_LIFECYCLE`); `templates/TARGET_REPOSITORY_ADOPTION_CHAT_PROMPT.md` оставлен заглушкой (внешние bookmark); живые ссылки перенаправлены на каноны; `ADOPTION_PROMPT.md` список «engine should find» обновлён на `ADOPTION_GUIDE.md`.
- **Optional polish**: отдельно можно рассмотреть vendor/public metadata hygiene и English wording там, где это не нарушает Russian-first policy; это не blocker для adoption.
- **Operating layer (`ASD-OPLAYER-001`, journal 0024)**: добавлены нейтральные контракты `ORCHESTRATOR_PROJECT_OPERATING_LAYER.md` и `CROSS_PROJECT_CONSOLIDATION_CONTRACT.md`, governance pack template расширен разделом «Три слоя управления». Опционально: при downstream adoption включать эти контракты в target governance pack как optional-файлы; реальные visibility-matrix и дайджесты держать в приватном control plane, не в публичном репозитории.

## Текущие операционные правила

1. Применять обновленный `ORCHESTRATOR_RESPONSE_STANDARD.md` и `ORCHESTRATOR_RESPONSE_TEMPLATE.md` при подготовке новых Engine-блоков.
2. Проверять Fast Lane -> Engine escalation при любой write-action recommendation.
3. Проверять русские пользовательские заголовки и описания в Engine-блоках.
4. Проверять Closure policy после сообщений о merge/release/sync: обычные work PR могут оставаться `merged; closure pending` до batch-closure перед release; release gate, audit/review consistency gate, adoption/source-update, завершение/пауза серии и явное closure-задание требуют per-task closure.
5. Если journal stale после merge в per-task exception или под release gate, создавать docs-only Engine-блок на closure cleanup вместо ответа `все закрыто`.
6. Использовать `CODE_REVIEW_TASK_TEMPLATE.md` для первого безопасного review target implementation repository только после проверки, что task явно содержит режим, объект проверки, allowed/forbidden files и правило сохранения отчета. Review-задачи всегда журналируют TASK+RESULT (`Journal trace: always`).
7. При следующем target repository dry run фиксировать methodology feedback без private data и с sanitization checkpoint.
8. Перед любым sync/checkout/switch/pull/merge применять `Repository sync / checkout guard`: root, remote, branch и `git status --short`; dirty tree → STOP.
9. Отдельной future task рассмотреть tags/releases для methodology versioning, если commit-based `methodology_reference` окажется недостаточным.
