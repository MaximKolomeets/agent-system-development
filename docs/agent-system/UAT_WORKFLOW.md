# UAT_WORKFLOW

## Назначение

UAT Workflow задает human business acceptance gate перед переносом `developer`
в `main`. Цель gate: владелец/PO проверяет поведение глазами и действиями
пользователя, а не только code diff, tests или agent report.

UAT обязателен перед approval release PR, если release меняет:

- UI, frontend, layout, визуальное поведение или пользовательский путь;
- API, CLI, integration contract или externally visible behavior;
- бизнес-правило, acceptance criteria, workflow пользователя;
- документацию, которая является пользовательской инструкцией для выполнения
  бизнес-действия.

Если release не содержит user-facing/UI/API/business-facing изменений, UAT
строка всё равно фиксируется как `not_applicable` с причиной и evidence.

## Роли

| Роль | Ответственность |
| --- | --- |
| Agent/engine | Генерирует Human UAT Checklist из acceptance scenarios, готовит staging/build notes, фиксирует safe evidence references. |
| Reviewer | Проверяет, что checklist связан с acceptance scenarios и не заменяет machine checks. |
| Owner/PO | Вручную проходит checklist, подтверждает или отклоняет business acceptance. |
| Human architect | Учитывает UAT verdict перед approval/merge release PR. |

Agent не может поставить owner/PO approval за человека.

## Порядок UAT gate

1. Stabilize `developer`: все work PR для release scope merged, generated checks
   чистые, release-prep/state-refresh выполнены.
2. Сгенерировать Human UAT Checklist по
   `ACCEPTANCE_SPEC_COMPLETENESS_PATTERN.md` и
   `BUSINESS_ACCEPTANCE_CHECKLIST.md`.
3. Owner/PO проходит button-click/API/visual scenarios вручную в безопасной
   среде.
4. Owner/PO фиксирует verdict:
   - `accepted`;
   - `accepted_with_known_limitations`;
   - `rejected`;
   - `not_applicable`.
5. Release PR `developer -> main` получает approval только если verdict
   `accepted`, `accepted_with_known_limitations` с явным owner decision или
   `not_applicable` с причиной.
6. RESULT release-prep/release-boundary фиксирует UAT actor, verdict и evidence.

## Button-click scenarios

Button-click scenario описывает действие так, чтобы не-программист мог пройти
его без чтения кода.

Минимальные поля:

- `uat_id`;
- user role;
- стартовая страница/экран/entrypoint;
- шаги: click/type/select/submit или эквивалентное API/CLI действие;
- expected visible/API result;
- pass/fail/block verdict;
- evidence reference.

Запрещено требовать real credentials, production secrets или private customer
data. Тестовые данные должны быть synthetic или approved safe fixtures.

## Visual acceptance

Для UI/frontend changes владелец/PO проверяет:

- ключевой user path выполняется от начала до конца;
- текст не перекрывает controls/content;
- responsive viewports выглядят пригодно для работы;
- loading/empty/error states понятны;
- визуальное состояние соответствует acceptance scenario;
- screenshots/video references не раскрывают private data.

## API acceptance

Для API/CLI/integration changes владелец/PO или назначенный human delegate
проверяет:

- happy path request/command;
- expected status/result body/output;
- error path из acceptance scenario;
- backwards compatibility или явно approved breaking change;
- отсутствие secret values в evidence.

API evidence фиксируется как command summary, response status, sanitized output
или link на безопасный artifact. Secret headers, tokens и cookies не печатаются.

## RESULT поля

Release-prep, release-boundary или explicit UAT RESULT фиксирует:

- `business_acceptance_gate`: `passed`, `passed_with_limitations`, `failed`,
  `not_applicable`.
- `uat_actor_type`: `human` или `hybrid`.
- `uat_actor_role`: owner/PO/human architect/delegate.
- `uat_checklist_ref`: path, PR comment, issue, release note или artifact link.
- `uat_evidence`: safe screenshot/API/output references без private data.
- `uat_checked_at`: ISO-8601 timestamp.
- `uat_decision`: approve release, approve with limitations, block release или
  not applicable with reason.

Если UAT выполнен человеком вне agent session, agent записывает только safe facts
и source evidence. Agent не угадывает human identity и не подменяет manual
approval.

## STOP conditions

Agent/reviewer пишет `STOP`, если:

- release PR готовится в `main`, но Human UAT Checklist отсутствует и нет
  `not_applicable` reason;
- owner/PO verdict `rejected`;
- evidence содержит private data, credentials или production secrets;
- UI/API scenario не может быть проверен из-за missing environment или blocker;
- UAT approval пытается поставить агент вместо человека.

## Передача

Следующий: owner/PO — пройти Human UAT Checklist перед approval release PR.
