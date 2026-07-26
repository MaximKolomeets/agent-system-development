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
4. Нет неизвестных, untracked или forbidden files, private data, destructive Git
   actions, protected-branch changes или расширения scope.

Без любого условия — `STOP`.

## Безопасный порядок

Сначала проверить branch, HEAD и exact dirty scope. Не выполнять `reset`, `stash`,
`checkout` файлов или cleanup ради искусственной чистоты. Продолжать только
конкретный незавершённый шаг: checks, bounded fix-pass, journal finalization либо
push. Перед commit повторно проверить exact scope; лишний файл, mismatch branch/HEAD
или неясное происхождение изменений означает `STOP`.

Continuation не отменяет readiness, self-review, journal finalization, human-only
merge policy, stable-reference policy или forbidden-path checks.

## Примеры

- **ACT:** три заранее указанных journal files после failed readiness на той же
  task branch.
- **STOP:** вместе с expected scope появился неизвестный файл.
- **STOP:** continuation пытается начать новую смысловую работу.
- **ACT:** один machine-verifiable blocker исправляется в исходном allowed scope.
