# AGENT_INITIATIVE_PROTOCOL

## Назначение

Этот протокол задает безопасный канал для инициативных предложений агента.

Проблема H12: агент может заметить technical debt, risk, vulnerability,
устаревшую библиотеку, слабый gate, дублирование policy или более простой
workflow, но эта находка не входит в текущий scope. Без отдельного канала агент
либо молчит, либо чинит это молча и нарушает границы задачи.

Правильное поведение: агент фиксирует предложение, но не расширяет текущую
задачу без явного решения архитектора.

## Когда предложение обязательно

Агент должен добавить proposal, если во время выполнения задачи обнаружил:

- риск безопасности, privacy или publication boundary;
- повторяющийся manual step, который стоит автоматизировать;
- противоречие между policy-документами, templates или gates;
- missing template/checklist/tooling, из-за которого задача стала хрупкой;
- technical debt, который может повлиять на следующий PR/release;
- полезный library/tool/process upgrade, который не входит в текущий scope;
- reviewer finding, который не должен чиниться reviewer role напрямую.

Если предложений нет, RESULT и final report всё равно содержат раздел
`## Unprompted Project Proposals` со значением `нет`.

## Что нельзя делать

- Не реализовывать proposal внутри текущей задачи, если это не входит в
  explicit allowed scope.
- Не менять backlog, MIR ledger или roadmap так, будто proposal уже утвержден
  как planned task.
- Не назначать implementation role напрямую из reviewer task.
- Не переносить private repository URL, real consumer names, client/customer
  data, internal code names, secrets, `.env` values, raw logs или raw source
  snippets в public methodology repository.
- Не превращать proposal в release blocker без evidence и явной связи с
  текущими acceptance criteria.

## Формат proposal

Использовать шаблон:

```text
docs/agent-system/templates/AGENT_PROPOSAL_TEMPLATE.md
```

Короткое предложение допустимо прямо в RESULT/final report, если оно содержит:

- problem pattern;
- почему это вне текущего scope;
- suggested owner role;
- suggested next artifact: `BACKLOG.md`, `METHODOLOGY_IMPROVEMENT_LEDGER.md`
  или отдельная task file;
- privacy/sanitization note.

## Поток обработки

1. Агент фиксирует proposal в `## Unprompted Project Proposals` своего RESULT и
   final report.
2. Если proposal пришёл из target repository, агент сначала нейтрализует его по
   `DOWNSTREAM_FEEDBACK_SANITIZATION_POLICY.md`.
3. Orchestrator или architect triage решает disposition:
   `reject`, `backlog_candidate`, `MIR_candidate`, `immediate_separate_task`.
4. Только после triage proposal попадает в `BACKLOG.md` как candidate или в
   `METHODOLOGY_IMPROVEMENT_LEDGER.md` как public-safe MIR lifecycle item.
5. Implementation выполняется отдельной задачей, отдельной веткой и отдельным
   PR.

## Связь с Methodology feedback

`## Methodology feedback` отвечает на вопрос: что улучшить в методологии по
итогам выполнения задачи.

`## Unprompted Project Proposals` отвечает на вопрос: какие вне-scope идеи или
риски агент заметил и предлагает отправить на triage.

Оба раздела обязательны для новых finalized RESULT. Пустое значение фиксируется
как `нет`, а не опускается.

## Reviewer roles

Reviewer roles обязаны явно отделять:

- finding/blocker по текущему объекту review;
- recommendation, которая относится к текущему PR и может быть исправлена
  исполнителем в той же ветке;
- proposal для будущей задачи, который уходит на triage и не выполняется
  reviewer role.

Reviewer role не запускает исполнителя, не меняет очередь, не создает
implementation branch и не чинит production/source files без режима
`fix-allowed`.

## Backlog intake

`BACKLOG.md` является live intake для утвержденных candidate/planned задач.

Proposal не становится backlog item автоматически. Он становится backlog item
только после architect/orchestrator triage и должен быть public-safe,
role-scoped и иметь ожидаемый next artifact.

## Acceptance

Протокол соблюден, если:

- RESULT содержит `## Methodology feedback`;
- RESULT содержит `## Unprompted Project Proposals`;
- предложения не раскрывают private data;
- вне-scope предложения не были реализованы без отдельного allowed scope;
- reviewer roles не назначили implementation task напрямую;
- approved proposal попал в `BACKLOG.md` или MIR lifecycle отдельным действием.

## Передача

Следующий: orchestrator/architect — triage новых proposals и выбор
`reject`, `backlog_candidate`, `MIR_candidate` или отдельной scoped task.
