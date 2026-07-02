# BUSINESS_ACCEPTANCE_CHECKLIST

## Назначение

Business Acceptance Checklist — reusable шаблон Human UAT Checklist для release
boundary. Его заполняет agent/engine по acceptance scenarios, а проходит вручную
owner/PO перед approval release PR.

Checklist не заменяет automated tests, code review, generated checks или release
authority gate. Он добавляет human business verdict: поведение видно, понятно и
приемлемо для владельца.

## Header

```text
Release / milestone:
Repository:
Release PR:
Developer branch / build:
UAT environment:
Owner/PO:
Checked at:
Verdict: accepted | accepted_with_known_limitations | rejected | not_applicable
Evidence policy: no credentials, no secret values, no private customer data
```

Если UAT `not_applicable`, указать:

```text
Reason:
Evidence:
Approved by:
```

## Scenario table

| UAT ID | Source scenario | Surface | Human action | Expected behavior | Evidence | Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| UAT-001 | `<scenario_id>` | UI/API/CLI/docs | Click/type/request/read step | Visible/API result | screenshot/link/sanitized output | pass/fail/blocked |  |

Правила:

- каждый business-facing acceptance scenario получает UAT row;
- один UAT row может покрывать несколько low-level fixtures только если user
  behavior один и тот же;
- `blocked` требует blocker code и release decision;
- `fail` блокирует release PR, пока owner/PO явно не принимает limitation.

## Button-click UI checks

Для каждого UI scenario:

- [ ] Стартовая страница/экран доступен без real credentials в evidence.
- [ ] Primary action выполняется через click/tap/keyboard path.
- [ ] Expected result виден человеку без чтения логов.
- [ ] Текст, кнопки и controls не перекрываются.
- [ ] Empty/loading/error state приемлемы для сценария.
- [ ] Desktop viewport проверен.
- [ ] Mobile/responsive viewport проверен, если продукт имеет mobile/web UI.
- [ ] Screenshot/video reference безопасен для публикации в RESULT/PR summary.

## API / CLI checks

Для каждого API/CLI scenario:

- [ ] Happy path request/command выполнен в safe environment.
- [ ] Expected status/output совпадает с acceptance scenario.
- [ ] Error path проверен или явно deferred с blocker.
- [ ] Breaking change явно approved, если compatibility меняется.
- [ ] Evidence sanitised: headers, cookies, tokens и secret values не печатаются.

## Documentation-as-product checks

Если release меняет пользовательские инструкции:

- [ ] Owner/PO может пройти инструкцию без дополнительных устных пояснений.
- [ ] Команды/пути/flags актуальны.
- [ ] Human-only actions явно отделены от agent-prep actions.
- [ ] Private data или project-specific internal names не появились в public docs.

## Release verdict

Owner/PO выбирает один verdict:

| Verdict | Release meaning |
| --- | --- |
| `accepted` | Release PR может быть approved при выполнении остальных gates. |
| `accepted_with_known_limitations` | Release PR может быть approved только если limitations перечислены и owner/PO принимает риск. |
| `rejected` | Release PR blocked до fix-pass или scope decision. |
| `not_applicable` | Нет business-facing/UI/API/docs behavior в release; reason и evidence обязательны. |

## RESULT summary template

```text
business_acceptance_gate:
uat_actor_type:
uat_actor_role:
uat_checklist_ref:
uat_evidence:
uat_checked_at:
uat_decision:
```

Evidence должен быть ссылкой или кратким sanitized summary. Не включать
credentials, tokens, cookies, private customer data, private repository URLs или
screenshots с sensitive data.

## Передача

Следующий: owner/PO — заполнить verdict и передать human architect решение для
release PR.
