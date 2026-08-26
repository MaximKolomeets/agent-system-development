# RATIONALE-0180-METH-PORTABLE-REMOTE-INTEGRATION-SKILLS-01

Связанный TASK file: `docs/agent-system/engine-journal/input/TASK-0180-METH-PORTABLE-REMOTE-INTEGRATION-SKILLS-01.md`
Связанный RESULT file: `docs/agent-system/engine-journal/output/RESULT-0180-METH-PORTABLE-REMOTE-INTEGRATION-SKILLS-01.md`
Номер sequence: 0180
Идентификатор задачи: METH-PORTABLE-REMOTE-INTEGRATION-SKILLS-01
authoring_role: methodology-maintainer
actor_type: agent
Статус обоснования: finalized_for_review
raw_chain_of_thought_stored: no

## Решаемый вопрос

Как сократить повторное безопасное подключение удалённого project contour и
project-scoped Vault с нескольких дней до одного bounded runbook, не превращая
частный downstream-код в публичный канон.

## Контекст и evidence

В реальном применении были подтверждены рабочие reverse SSH, Caddy, restricted
relay-user, observer-only MCP и WebDAV Vault MCP. Повторные ошибки возникали в
PowerShell quoting, SSH host-key/AllowUsers, healthcheck, WebDAV history COPY и
ASGI receive middleware. Issue #385 требует сохранить эти уроки нейтрально.

## Ограничения и инварианты

Публичный skill не содержит project names, IP, credentials или private URLs.
Private tunnel key остаётся на target host. VPS слушает reverse ports только на
loopback. Yandex app password имеет Disk-wide capability аккаунта; folder scope
обеспечивает MCP, а provider boundary — отдельный аккаунт/shared folder.

## Рассмотренные варианты

1. Хранить только prose runbook.
2. Копировать downstream deployment package как есть.
3. Поставлять skill, references, validators и generic assets template.

## Выбранный путь

Вариант 3: он сохраняет исполняемую основу, но требует явной target adaptation
config/secrets и independent acceptance.

## Причины выбора

Prose недостаточно для быстрого повторения, а прямое копирование раскрывает
private topology и закрепляет случайные project defaults. Generic template
снижает ручной набор и оставляет security decisions видимыми.

## Отклонённые альтернативы

Отклонены inbound port-forwarding target host, `StrictHostKeyChecking=no`,
Docker socket tunnel, Docker commit, общее WebDAV credential между trust
boundaries и заявление о folder-scoped app password.

## Компромиссы, последствия и риски

VPS mutation остаётся human/root gate. Provider credential Vault MCP способен
видеть весь Disk своего аккаунта при компрометации process, если не используется
отдельный аккаунт. Templates требуют pinning image digest в target.

## Предположения, неопределённости и confidence

Docker Compose, OpenSSH, Caddy и Yandex WebDAV остаются доступными. Confidence
high: паттерны подтверждены runtime evidence, а reusable копии проходят offline
tests и fail-closed validators.

## Условия пересмотра или rollback triggers

Иной transport, более двух endpoints, provider-level folder ACL или изменение
MCP transport требуют отдельного review template/API contract.

## Что явно не решалось

Не выполняются target deploy, VPS mutation, secret creation, DNS change и merge.

## Связь с решениями

Применяются `SECURITY_POLICY.md`, `ADOPTION_TRANSFER_MANIFEST.yml`,
`DOWNSTREAM_FEEDBACK_SANITIZATION_POLICY.md` и human-only merge boundary.

## Изменения после review

Нет; self-review и CI evidence фиксируются в RESULT.

## Передача

Следующий: methodology reviewer — проверить PR #386 и выполнить human merge
только после зелёных checks.
