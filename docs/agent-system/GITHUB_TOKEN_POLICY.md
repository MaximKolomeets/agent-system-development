# GITHUB_TOKEN_POLICY

- Token должен иметь минимально необходимые права.
- Требуется read access к репозиторию.
- Write access разрешается только в разрешенный namespace веток, если технически возможно.
- Реальные токены не хранить в репозитории.
- Токены не писать в Source.
- Токены не передавать в чат.

## Token separation по режимам

Уровень разделения токенов зависит от режима применения методологии (см. `ROLE_MODEL.md`, `WORKFLOW.md`).

- В `lightweight solo-operator mode` агент может быть logical role внутри пользовательского окружения. Отдельный token на агента является recommended hardening, но не blocker для docs-only локальной задачи, если пользователь явно разрешил выполнение и все изменения идут через PR.
- В `multi-agent governed mode` отдельные tokens/accounts на агентов обязательны (один агент = один GitHub TOKEN).
- Если token separation не настроена, final report должен честно указать это как operational risk.
