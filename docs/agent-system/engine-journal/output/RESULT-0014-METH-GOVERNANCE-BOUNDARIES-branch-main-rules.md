# RESULT-0014-METH-GOVERNANCE-BOUNDARIES-branch-main-rules

Файл результата: `docs/agent-system/engine-journal/output/RESULT-0014-METH-GOVERNANCE-BOUNDARIES-branch-main-rules.md`

Связанный TASK file: `docs/agent-system/engine-journal/input/TASK-0014-METH-GOVERNANCE-BOUNDARIES-branch-main-rules.md`

Идентификатор задачи: `METH-GOVERNANCE-BOUNDARIES`

Номер sequence: `0014`

Агент: `docs-maintainer-01`

Engine: Claude Code

Timestamp (ISO-8601): `2026-06-16T07:28:36+07:00`

Baseline SHA (developer): `6551022b90bd142949fb5385d1244915d8a43814`

methodology_reference: см. канон в `docs/agent-system/ENGINE_ENTRYPOINT.md` → раздел «Methodology reference»; данные текущей задачи:

```yaml
methodology_reference:
  repository: MaximKolomeets/agent-system-development
  source_branch: developer
  source_commit: 6551022b90bd142949fb5385d1244915d8a43814
  checked_at: 2026-06-16T07:28:36+07:00
  reference_type: commit
  notes: "Точка после merge METH-BACKLOG-POLISH (PR #129)."
```

## Подтверждённый whitelist

- `docs/agent-system/BRANCH_POLICY.md` — канон обоих правил;
- `docs/agent-system/ROLE_MODEL.md` — короткие ссылки на канон;
- `AGENTS.md` — короткие ссылки на канон (в существующих forbidden-bullets);
- журнал: `engine-journal/input/TASK-0014-*.md`, `engine-journal/output/RESULT-0014-*.md`, `engine-journal/INDEX.md`.

## Правило 1 — агент не пушит/не мержит в main

**Канон** добавлен в `BRANCH_POLICY.md` → секция «main» → подраздел «Обновление main (канон, правило 1)»:

- `main` обновляется ТОЛЬКО через release-PR `developer -> main`;
- release-PR мержит человек-архитектор (пользователь), а не агент;
- агент может ПОДГОТОВИТЬ release-PR (создать release-ветку/PR из `developer` в `main`), но НЕ мержит его и НЕ пушит в `main`;
- агент не делает merge release-PR даже при наличии прав.

**Ссылки на канон (без дублирования прозой):**

- `AGENTS.md` — bullet «Не менять `main` напрямую» дополнен ссылкой на `BRANCH_POLICY.md → «Обновление main»` с краткой формулировкой (release-PR мержит человек, агент может подготовить, но не мержит/не пушит);
- `ROLE_MODEL.md` — новый подраздел «Границы веток и main» содержит одну строку-ссылку на канон.

## Правило 2 — агент работает только в своих ветках

**Канон** добавлен в `BRANCH_POLICY.md` → секция «work/<role>/*» → подраздел «Изоляция веток агентов (канон, правило 2)»:

- каждый агент действует только в своих `work/<role>/<task>` своего role namespace;
- запрещено пушить, менять, force-пушить, переименовывать или удалять ветку другого агента;
- агент не строит работу поверх чужой непримёрженной рабочей ветки без решения пользователя;
- передача работы между агентами — только через merged PR в `developer`, не через правку чужих веток;
- для работы поверх результата другого агента сначала его PR мержится в `developer`, затем новая ветка создаётся от актуальной `developer`.

**Ссылки на канон:**

- `ROLE_MODEL.md` — подраздел «Границы веток и main» содержит строку-ссылку на `BRANCH_POLICY.md → «Изоляция веток агентов»`;
- `AGENTS.md` — bullet «Каждый агент работает только в своем namespace веток» дополнен ссылкой на канон с краткой формулировкой.

## Согласованность с существующим текстом (без противоречий)

- BRANCH_POLICY «main»: существующее «изменения только через PR из `developer`; прямой push запрещен для агентов; force push запрещен» — новый подраздел уточняет, что merge release-PR делает человек, не противоречит, а конкретизирует.
- BRANCH_POLICY «Запрещено»: уже содержит «прямой push агентами в `main`», «force push в main/developer» — новый канон согласован.
- AGENTS: bullets :20 (main) и :24 (namespace) **дополнены** ссылками, не продублированы новой прозой в других местах.
- ROLE_MODEL: Engine-секция уже говорит «не меняет main/developer напрямую» — новый подраздел даёт каноническую ссылку, не повторяя правило прозой.
- Правила сформулированы каноном в одном файле (BRANCH_POLICY); ROLE_MODEL и AGENTS только ссылаются.

## Измененные файлы (этой задачей)

- `docs/agent-system/BRANCH_POLICY.md`
- `docs/agent-system/ROLE_MODEL.md`
- `AGENTS.md`
- `docs/agent-system/engine-journal/input/TASK-0014-METH-GOVERNANCE-BOUNDARIES-branch-main-rules.md`
- `docs/agent-system/engine-journal/output/RESULT-0014-METH-GOVERNANCE-BOUNDARIES-branch-main-rules.md`
- `docs/agent-system/engine-journal/INDEX.md`

## Выполненные проверки

- Preflight: `git status`, `git fetch --all --prune`, `git switch developer`, `git pull --ff-only` (developer обновлён до `6551022` после merge PR #129), `git rev-parse developer/origin/developer`.
- Чтение BRANCH_POLICY, ROLE_MODEL, AGENTS целиком до правок.
- `git status --short` — только whitelist + journal; `git diff --check` — чисто.
- Ручная сверка: канон в одном файле, остальные ссылаются, противоречий со старым текстом нет.

## Невыполненные проверки и причина

- Markdown lint — documented lint command не подтверждён.
- Docker/production — запрещены scope.

## Результат проверки запрещенных файлов

Файлы вне whitelist не изменялись. Правила не продублированы прозой в нескольких местах (канон + ссылки). `.env` не читался.

## Результат проверки sensitive/private markers

Секреты не вводились и не печатались.

## Результат language policy

RESULT Russian-first; English только для technical identifiers, paths, filenames и literal terms.

## Принятые решения

- Канон обоих правил — `BRANCH_POLICY.md` (правило 1 в секции «main», правило 2 в секции «work/<role>/*»).
- ROLE_MODEL получил один новый подраздел «Границы веток и main» с двумя строками-ссылками.
- AGENTS — дополнены два существующих forbidden-bullet, без новых дублирующих пунктов.

## Риски

- Нет. Изменения документационные, согласованы с существующими правилами.

## Blockers

Нет.

## Закрытие после merge

Work PR status: создаётся в этой задаче через `gh` (доступен).

Release/sync: фиксируются при closure по факту.

RESULT closed after merge: not applicable before merge.

INDEX closed after merge: not applicable before merge.

## Следующий рекомендуемый шаг

После merge — closure 0014. Два governance-правила закреплены каноном; далее — adoption на реальном target-проекте по `ADOPTION_PROMPT.md`.

## Methodology feedback

Закрепление «канон + ссылки» вместо повтора прозой держит правила в одном месте и упрощает их будущее изменение — менять нужно только BRANCH_POLICY, а ROLE_MODEL/AGENTS остаются ссылками. Полезный паттерн для любых cross-cutting governance-правил.
