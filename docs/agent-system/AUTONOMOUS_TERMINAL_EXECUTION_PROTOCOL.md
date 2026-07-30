# AUTONOMOUS_TERMINAL_EXECUTION_PROTOCOL

## Назначение

Этот документ задаёт единый канон автономного выполнения substantive
file-changing Engine-задач. Terminal outcome такой задачи — не факт запуска
отдельной команды, а либо готовый к human review PR с проверяемым evidence,
либо доказанный `stopped_human_required`.

`EXECUTION_CONTINUATION_POLICY.md` остаётся каноном для new task,
continuation, fix-pass, journal finalization и expected dirty scope. Этот
протокол определяет, как engine доводит разрешённую substantive-задачу до
terminal outcome без бесконечного ожидания и без обхода guardrails.

## Два terminal outcome

### `ready_for_human_review`

Engine может объявить это состояние только когда опубликован один PR в
разрешённую base branch и evidence содержит final branch/HEAD, exact changed
files, обязательные local checks, CI именно final SHA, self-review и итог
review cycle. Human merge остаётся отдельным действием человека.

### `stopped_human_required`

STOP допустим только по закрытой taxonomy ниже. Отчёт обязан назвать причину,
команду, finding или иной воспроизводимый evidence, уже использованные
безопасные попытки, residual risk, минимальное следующее действие и точные
paths для необходимого scope amendment. Failed отдельный check сам по себе
STOP не является.

## Recoverable failure и STOP taxonomy

Если failure диагностируется и его минимальная правка остаётся в adaptive
scope, engine обязан выполнить её, штатно регенерировать dependency closure и
повторить применимые checks. Это относится к собственным ошибкам, generated
drift, machine-verifiable findings и review feedback, который не требует нового
решения владельца.

`stopped_human_required` допустим только если:

1. отсутствует обязательный prerequisite, который нельзя безопасно обойти;
2. нужен неразрешённый архитектурный выбор владельца;
3. требуется path вне adaptive scope;
4. требуется destructive Git action, protected-branch write, доступ к secrets,
   реальным данным или расширение доступа;
5. выявлена security/integrity проблема, не исправимая в scope;
6. исчерпан заранее объявленный iteration budget.

Residual risk не заменяет acceptance outcome: finding можно пометить только
`closed`, когда критерий принятия доказан; `closed_with_residual_risk`, когда
критерий выполнен и остаточный риск явно принят человеком; либо `blocked`,
когда критерий не выполнен. Нельзя закрывать невыполненный outcome словами
«residual risk», future backlog или «исправить позже».

## Decision fallback

Когда конкретное действие не задано напрямую, engine выбирает первое
однозначное безопасное решение в таком порядке:

1. сохранить security и integrity;
2. сохранить development/test-контур;
3. выбрать минимальное обратимое изменение без расширения product scope;
4. получить воспроизводимое machine-verifiable evidence.

Если этот порядок не даёт одного безопасного решения, нужен
`stopped_human_required`, а не предположение от имени владельца.

## Adaptive scope envelope

Каждая substantive TASK заранее перечисляет dependency closure для связанного
изменения:

```text
source -> registry/order -> manifest -> capacity/limit -> generated mirrors -> checks
```

Envelope описывает concrete paths и их назначение. Если проверка выявляет
необходимый path вне этого closure, engine не расширяет scope молча: требуется
scope amendment или STOP. Штатная регенерация уже перечисленных generated
artifacts не является новым продуктовым решением.

## Ограниченные iteration budgets

TASK должна явно объявлять отдельные положительные budgets для:

- targeted check reruns;
- full readiness runs;
- CI fix-pass;
- integration-stack attempts.

Engine фиксирует фактическое использование в RESULT и final report. Исчерпание
бюджета не оправдывает обход check: оно даёт честный terminal report с
доказанным состоянием, remaining blocker и human next action.

## Обязательный terminal report

RESULT, PR evidence и final report фиксируют branch/HEAD/PR, prerequisites,
изменённые файлы с классификацией source/generated/journal, решения по
развилкам, checks и CI с источником verdict, использованные budgets, residual
risks, unresolved review threads, отсутствие merge и точный следующий шаг.

## Неподлежащие ослаблению границы

Протокол не разрешает менять `main` или `developer` напрямую, ослаблять
validators/CI/security, читать secrets, скрывать dirty tree через
`reset`/`stash`/`clean`, выполнять rebase/force-push или расширять product
scope. Human-only merge, branch isolation, Russian-first и journal/accounting
rules сохраняются полностью.
