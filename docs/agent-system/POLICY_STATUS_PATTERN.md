# POLICY_STATUS_PATTERN

## Назначение

Policy status pattern задает target-local реестр статусов политик и их
согласование с фактической стадией repository. Он нужен, когда документы
политик уже описывают production-grade ожидания, а repository еще находится на
scaffold, Stage 1 или переходной стадии.

Pattern не снижает требования политики. Он явно показывает, что является
каноном сейчас, что является proposed/draft ожиданием, и какой минимальный этап
нужен, чтобы политика считалась применимой как blocking gate.

## Когда применять

- В target repository есть несколько policy-документов, и их статус неочевиден.
- Policy-документ описывает будущий уровень зрелости, но repository еще не
  достиг этой стадии.
- Review спорит не о тексте политики, а о том, является ли она уже blocking.
- Нужен короткий слой между policy text, control matrix и текущим repo-state.

Для маленького repository с одним явным policy-документом pattern можно не
материализовать отдельным файлом: достаточно строки статуса в самом документе.

## Канонические статусы

- `canonical` - политика действует как источник истины для указанного scope.
- `proposed` - политика согласована как направление, но еще требует approval,
  materialization или stage transition.
- `draft` - рабочий черновик; не используется как blocking gate без явного
  решения.
- `deprecated` - больше не применяется; ссылка должна указывать replacement или
  причину снятия.

Статус стабилен как контракт. Не переопределять смысл существующего статуса в
target repository; при необходимости добавить новый статус отдельным решением.

## Минимальные поля

| Поле | Назначение |
| --- | --- |
| `document` | Путь к policy-документу или разделу. |
| `status` | Один из канонических статусов. |
| `canonical_for` | Scope, для которого policy является источником истины. |
| `minimum_stage` | Минимальная стадия repository, где policy становится blocking. |
| `repo_alignment` | Соответствие текущей стадии repository: aligned / partial / future / conflict. |
| `owner` | Роль, отвечающая за актуальность статуса. |
| `review_trigger` | Когда строку нужно пересмотреть. |

## Alignment: политика vs repo-state

Каждый POLICY_STATUS должен иметь раздел alignment:

- текущая стадия repository;
- какие policies уже blocking;
- какие policies являются future/proposed;
- какие controls еще не имеют реализации, теста или CI-gate;
- какое событие переводит proposed/draft policy в canonical blocking state.

Если policy имеет статус `canonical`, но control matrix показывает отсутствующий
test/CI-gate для hard-инварианта, это не повод молча ослаблять policy.
Нужно явно зафиксировать `repo_alignment: partial` и открыть follow-up или
STOP, если текущая задача заявляет full compliance.

## Связь с другими документами

- `CONTROL_MATRIX_PATTERN.md` операционализирует policy-инварианты через
  implementation/test/CI-gate/stage.
- `ERROR_CATALOG_PATTERN.md` задает стабильные blocker/error codes, если
  несоответствие policy должно блокировать acceptance-сценарий.
- `DECISION_NOTE_GUIDE.md` описывает, когда изменение статуса policy требует
  отдельной decision note или Level 3/4 owner approval.
- `TARGET_PROJECT_GOVERNANCE_PACK.md` включает POLICY_STATUS как target-local
  governance artifact, когда repository достиг Stage 2+ или явно принял этот
  pattern.

## Review checklist

- У каждой policy есть статус или явная причина отсутствия отдельного статуса.
- `canonical_for` не шире фактического scope policy.
- `minimum_stage` согласован с текущим roadmap/stage.
- Alignment не обещает production-grade compliance, если repository находится
  на scaffold/transition стадии.
- Blocking claims согласованы с control matrix и acceptance/spec blockers.
- Target-specific facts не переносятся в public methodology repository.
