# EXECUTION_CONTINUATION_POLICY

## Назначение

Канон различает безопасный старт новой file-changing задачи и продолжение уже
начатой задачи. Continuation не является способом обойти branch, scope, readiness
или forbidden-path guards.

## Термины

- **New task** — новая задача, ещё не имеющая подготовленного scope в рабочем дереве.
- **Continuation** — явно объявленное продолжение той же task branch и task ID.
- **Fix-pass** — ограниченное исправление machine-verifiable или review blocker в
  исходном allowed scope.
- **Journal finalization** — фиксация доступных PR/check/time facts в уже созданных
  артефактах TASK/RATIONALE/RESULT/INDEX.
- **Expected dirty scope** — заранее перечисленный точный набор изменённых paths.

## New task

Для new task действует безусловное правило: `dirty tree before start -> STOP`.
До создания work branch проверить root, remote, branch и `git status --short`;
после чистого preflight получить `origin/developer`, выполнить только
fast-forward update `developer` и создать новую work branch.

## Допустимый continuation

Continuation разрешён только одновременно при следующих условиях:

1. Это та же task branch и тот же task ID.
2. Новый handoff прямо называет continuation, branch, ожидаемый HEAD или связь с PR,
   exact permitted dirty paths и незавершённый шаг.
3. `git status --short` содержит только заранее перечисленные paths; каждый path
   находится в allowed scope исходной задачи.
4. Untracked-файл допустим только как заранее перечисленный expected dirty scope:
   он назван в continuation handoff/prompt, входит в allowed scope исходной
   задачи, имеет понятные происхождение и назначение, не является private,
   secret или forbidden. Неизвестные либо не перечисленные untracked-файлы
   означают `STOP`.
5. Нет unknown files, private data, destructive Git actions, protected-branch
   changes или расширения scope.

Без любого условия — `STOP`.

## Безопасный порядок

Сначала проверить branch, HEAD и exact dirty scope. Не выполнять `reset`, `stash`,
`checkout` файлов или cleanup ради искусственной чистоты. Продолжать только
конкретный незавершённый шаг: checks, bounded fix-pass, journal finalization либо
push. Перед commit повторно проверить exact scope; лишний файл, mismatch branch/HEAD
или неясное происхождение изменений означает `STOP`.

Continuation не отменяет readiness, self-review, journal finalization, human-only
merge policy, stable-reference policy или forbidden-path checks.

## Terminal execution

Этот документ задаёт execution safeguards для continuation и дополняет
`AUTONOMOUS_TERMINAL_EXECUTION_PROTOCOL.md`, который является authoritative
canon terminal outcome, STOP taxonomy, decision fallback и iteration budgets.
Каждая file-changing задача заканчивается ровно одним
состоянием:

- `ready_for_human_review`: PR опубликован, readiness успешен, обязательные
  checks и CI для final SHA успешно завершены;
- `stopped_human_required`: безопасное завершение объективно требует решения
  человека.

Преодолимая ошибка, повторная генерация, failed local check или review feedback
не являются самостоятельным основанием остановить работу. Формулировки
«отложено», «следующая задача» или backlog вместо исправления безопасного scoped
дефекта не являются terminal outcome.

## Самостоятельное доведение и выбор действия

Engine сам исправляет собственные ошибки и machine-verifiable failures,
повторяет checks после точечной правки, регенерирует generated artifacts,
финализирует journal/accounting/readiness, выполняет commit/push/PR/CI и закрывает
review feedback в той же task branch. Bounded fix-pass обязателен, если решение
остаётся в разрешённом scope.

При непредусмотренной развилке применять по порядку: безопасность и integrity;
branch/scope/protected-branch safeguards; минимальное обратимое изменение;
работоспособность development-контура; отсутствие изменения продуктового поведения
за пределами задачи. Если этот порядок однозначно определяет безопасное минимальное
действие, Engine применяет его и фиксирует обоснование в RESULT/PR.

## Adaptive scope

Для заранее доказуемой технической цепочки Engine определяет минимально
необходимые paths: source canon → registry/order/manifest/limit → generated
artifacts → validator/unit test → journal/result. Такая цепочка не расширяет
`task_contract.scope.allowed_files`: до правки отсутствующего path требуется
обновлённый self-contained task contract или явное scope amendment владельца.
После подтверждения новый path и обоснование отражаются в RESULT/PR; изменение не
должно менять архитектурное или продуктовое решение либо ослаблять validator,
security, CI или branch guard, а затем выполняются все применимые checks.

## Настоящий STOP и граница автономности

`STOP` допустим только при новом архитектурном, финансовом, продуктовом или
governance решении без однозначного безопасного выбора; path вне allowlist без
обновлённого task contract или явного scope amendment; destructive Git/data action;
protected branch; secrets/private data; недоступной после разумных повторных попыток
внешней зависимости; действительном противоречии требований; либо исчерпании
`max_review_cycles` по `REVIEW_AUTOLOOP.md`. В последнем случае Engine передаёт PR
человеку в каноническом статусе autoloop, не выполняя бесконечные fix-pass. STOP
report обязан назвать причину, evidence, команды/ошибку, минимальный безопасный
вариант продолжения и точные extra paths.

Terminal execution не разрешает менять `main`/`developer`, ослаблять CI,
validators, checks или security controls, менять release/version policy, исключать
обязательный context document ради лимита, расширять продуктовый scope либо
использовать `reset`, `stash`, `checkout` files, `clean`, rebase или force-push.

## Примеры

- **ACT:** три заранее указанных journal files после failed readiness на той же
  task branch.
- **STOP:** вместе с expected scope появился неизвестный файл.
- **STOP:** continuation пытается начать новую смысловую работу.
- **ACT:** один machine-verifiable blocker исправляется в исходном allowed scope.
