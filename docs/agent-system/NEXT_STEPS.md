# NEXT_STEPS

1. Применять обновленный `CHATGPT_RESPONSE_STANDARD.md` и `CHATGPT_RESPONSE_TEMPLATE.md` при подготовке новых Engine-блоков.
2. Проверять Fast Lane -> Engine escalation при любой write-action recommendation.
3. Проверять русские пользовательские заголовки и описания в Engine-блоках.
4. Проверять post-merge journal closure после сообщений о merge/release/sync: GitHub PR state должен совпадать с RESULT/INDEX state.
5. Если journal stale после merge, создавать docs-only Engine-блок на closure cleanup вместо ответа `все закрыто`.
6. После merge `METH-OPERABILITY-01` провести `REVIEW-INITIAL-01` проекта `agent-system-development` по обновленной review-методологии.
7. В `REVIEW-INITIAL-01` проверить lightweight solo-operator mode, multi-agent governed mode, role boundaries, adapter layer для `CHATGPT_*`, `methodology_reference`, source snapshot drift control и anti-overengineering checkpoint.
8. Использовать `CODE_REVIEW_TASK_TEMPLATE.md` для первого безопасного review target implementation repository только после проверки, что task явно содержит режим, объект проверки, allowed/forbidden files и правило сохранения отчета.
9. При следующем target repository dry run фиксировать methodology feedback без private data и с sanitization checkpoint.
10. Отдельной future task рассмотреть tags/releases для methodology versioning, если commit-based `methodology_reference` окажется недостаточным.
