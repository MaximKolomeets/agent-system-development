# TASK-0032: METH-BATCH-CLOSURE-POLICY

## Режим

Роль: docs-maintainer.
Исполнитель: на усмотрение архитектора.
Reasoning effort: высокий.
branch-guard.

Batch-policy в действии: открытые прошлые journal-записи 0027–0031 не являются blocker. Closure не подмешивать. Эта задача — последнее методологическое изменение перед pre-release batch-closure; её собственная запись 0032 остаётся open и закрывается тем batch-проходом, который задача вводит.

## Цель

Закрепить batch-closure policy, per-task исключения, статусную развилку, шаблоны per-task/batch closure, batch-friendly handoff и release-gate.

## Ветки

- base: `developer`
- work: `work/docs-maintainer-01/batch-closure-policy`

## Allowed files

```text
docs/agent-system/ENGINE_JOURNAL_CONTRACT.md
docs/agent-system/templates/TASK_HEADER_COMMON.md
docs/agent-system/templates/CODE_REVIEW_TASK_TEMPLATE.md
docs/agent-system/templates/CLOSURE_TASK_TEMPLATE.md
docs/agent-system/templates/BATCH_CLOSURE_TASK_TEMPLATE.md
docs/agent-system/BRANCH_POLICY.md
docs/agent-system/engine-journal/input/TASK-0032-METH-BATCH-CLOSURE-POLICY.md
docs/agent-system/engine-journal/output/RESULT-0032-METH-BATCH-CLOSURE-POLICY.md
docs/agent-system/engine-journal/INDEX.md
```

`engine-journal/**` кроме новой записи 0032 не трогать.

## Изменения

1. `ENGINE_JOURNAL_CONTRACT.md`: добавить раздел `Closure policy`, где default = batch; pre-merge/closure-pending состояние допустимо до batch-closure; следующий work PR той же фазы не STOP-ается из-за незакрытой предыдущей записи; перед release `developer -> main` обязателен closure-only проход по merged-but-unclosed seq; release запрещён, пока journal не закрыт полностью; per-task closure ограничен исключениями.
2. `CLOSURE_TASK_TEMPLATE.md`: новый role-agnostic terminal-шаблон per-task closure-only по фактам из `gh`.
3. `BATCH_CLOSURE_TASK_TEMPLATE.md`: новый role-agnostic terminal-шаблон batch-closure по `INDEX.md` перед release.
4. `TASK_HEADER_COMMON.md`: добавить статусную развилку batch-closure policy и batch-friendly handoff.
5. `CODE_REVIEW_TASK_TEMPLATE.md`: выровнять handoff/closure wording с batch policy.
6. `BRANCH_POLICY.md`: добавить release-gate: release `developer -> main` запрещён, пока journal не закрыт полностью.

## Проверки

- diff только whitelist;
- `git diff --check`;
- branch-guard перед commit;
- новые шаблоны role-agnostic, без vendor/tool/model имён.

## Передача

Следующий: reviewer — review PR; затем архитектор — merge; затем engine — pre-release BATCH-CLOSURE по 0027…0032; затем release dev→main.

Обновить Source-снапшот у зарегистрированных потребителей: по `docs/agent-system/SOURCE_CONSUMERS.md`.

## STOP

- HEAD не work-ветка;
- правка вне whitelist;
- противоречие с journal contract;
- size-guard требует split.
