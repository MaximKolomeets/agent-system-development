# RESULT-0006-METH-CONSOLIDATION-C1-reading-list-tiering

Файл результата: `docs/agent-system/engine-journal/output/RESULT-0006-METH-CONSOLIDATION-C1-reading-list-tiering.md`

Связанный TASK file: `docs/agent-system/engine-journal/input/TASK-0006-METH-CONSOLIDATION-C1-reading-list-tiering.md`

Идентификатор задачи: `METH-CONSOLIDATION-C1`

Номер sequence: `0006`

Агент: `docs-maintainer-01`

Engine: Claude Code

Timestamp (ISO-8601): `2026-06-14T20:32:14+07:00`

Baseline SHA (developer): `1f294cff2d31e29d81130ef97db78dfbccf76f03`

Ссылка на источник scope: [RESULT-0004 §10 «PR-C1»](../output/RESULT-0004-METH-CONSOLIDATION-PLAN-01-consolidation-plan.md) и §5 «Reading-list: Core (~10) + Reference».

methodology_reference:

```yaml
methodology_reference:
  repository: MaximKolomeets/agent-system-development
  source_branch: developer
  source_commit: 1f294cff2d31e29d81130ef97db78dfbccf76f03
  checked_at: 2026-06-14T20:32:14+07:00
  reference_type: commit
  notes: "Точка после merge JOURNAL-CLOSE-0005 (PR #110)."
```

## Подтверждённый whitelist (из RESULT-0004 §10)

PR-C1, цитата: «Allowed: README.md, source/SOURCE_agent_system_index.md, journal. Delete/merge: нет.»

Whitelist текущей задачи:

- `README.md` — добавить канонический раздел «Обязательное чтение» (Core + Reference);
- `docs/agent-system/source/SOURCE_agent_system_index.md` — заменить дублирующий reading-list на короткий pointer на README;
- журнал: `engine-journal/input/TASK-0006-*.md`, `engine-journal/output/RESULT-0006-*.md`, `engine-journal/INDEX.md`.

## Fork-guard

Развилки Р1–Р5 из плана относятся к PR-C4 (Р1/Р2/Р3 — adoption guides merge) и PR-C5 (Р4/Р5 — templates). **C1 от Р1–Р5 не зависит**: §5 фиксирует Core и Reference авторитетно. Fork-guard не сработал.

## Что перенесено в Core / Reference

### Core (10 файлов, согласно §5 дословно)

1. `AGENTS.md`
2. `README.md`
3. `docs/agent-system/CURRENT_STATE.md`
4. `docs/agent-system/NEXT_STEPS.md`
5. `docs/agent-system/ROLE_MODEL.md`
6. `docs/agent-system/WORKFLOW.md`
7. `docs/agent-system/BRANCH_POLICY.md`
8. `docs/agent-system/CODE_REVIEW_WORKFLOW.md`
9. `docs/agent-system/ENGINE_ENTRYPOINT.md`
10. `docs/agent-system/ENGINE_JOURNAL_CONTRACT.md`

### Reference (27 пунктов — 26 из §5 + 1 augmentation для preservation)

§5 Reference (26):

- `DECISION_LOG.md`, `LANGUAGE_POLICY.md`, `FILE_COMMENTING_STANDARD.md`
- `OPERATIONAL_FAST_LANE.md`, `PR_WORKFLOW.md`, `WORKTREE_GUIDE.md`
- `ENGINE_SELF_DISCOVERY_CONTRACT.md`, `TASK_FILE_HANDOFF_CONTRACT.md`, `CHATGPT_OPERATING_CONTRACT.md`, `CHATGPT_RESPONSE_STANDARD.md`
- `ADOPTION_GUIDE.md`, `ADOPTION_TRANSFER_MANIFEST.yml`, `DOWNSTREAM_ADAPTATION_CHECKLIST.md`, `METHODOLOGY_FEEDBACK_LOOP.md`, `NEW_PROJECT_ONBOARDING_GUIDE.md`, `TARGET_PROJECT_GOVERNANCE_PACK.md`, `PROJECT_CONSTITUTION_FRAMEWORK.md`
- `SECURITY_POLICY.md`, `PUBLICATION_POLICY.md`, `GITHUB_RULESETS.md`, `GITHUB_TOKEN_POLICY.md`, `CI_POLICY.md`, `RELEASE_READINESS.md`
- `templates/**`, `engine-journal/**`, `source/SOURCE_agent_system_index.md`

Preservation augmentation (1):

- `docs/agent-system/TARGET_REPOSITORY_ADOPTION_GUIDE.md` — присутствует в текущем 28-пунктовом reading-list (entry 20 в `source/SOURCE_agent_system_index.md` до этой задачи), отсутствует в §5 Reference, поскольку запланирован к merge в `ADOPTION_GUIDE.md` в PR-C4. Чтобы соблюсти правило «ни один пункт не исчезает», добавлен в Reference с явной пометкой про PR-C4. После merge PR-C4 этот пункт уберётся из Reference вместе с файлом.

## Content-preservation check (28 → Core/Reference)

Прежний reading-list (`source/SOURCE_agent_system_index.md` до задачи) — 28 пунктов, сгруппированы 5 блоками. Сопоставление:

| # | Прежний пункт | Куда перенесён |
|---|---|---|
| 1 | AGENTS.md | Core |
| 2 | README.md | Core |
| 3 | CURRENT_STATE.md | Core |
| 4 | NEXT_STEPS.md | Core |
| 5 | DECISION_LOG.md | Reference |
| 6 | BRANCH_POLICY.md | Core |
| 7 | ROLE_MODEL.md | Core |
| 8 | WORKFLOW.md | Core |
| 9 | PR_WORKFLOW.md | Reference |
| 10 | OPERATIONAL_FAST_LANE.md | Reference |
| 11 | CODE_REVIEW_WORKFLOW.md | Core |
| 12 | LANGUAGE_POLICY.md | Reference |
| 13 | ENGINE_ENTRYPOINT.md | Core |
| 14 | ENGINE_SELF_DISCOVERY_CONTRACT.md | Reference |
| 15 | ENGINE_JOURNAL_CONTRACT.md | Core |
| 16 | TASK_FILE_HANDOFF_CONTRACT.md | Reference |
| 17 | CHATGPT_OPERATING_CONTRACT.md | Reference |
| 18 | CHATGPT_RESPONSE_STANDARD.md | Reference |
| 19 | FILE_COMMENTING_STANDARD.md | Reference |
| 20 | TARGET_REPOSITORY_ADOPTION_GUIDE.md | Reference (preservation, до PR-C4) |
| 21 | ADOPTION_GUIDE.md | Reference |
| 22 | ADOPTION_TRANSFER_MANIFEST.yml | Reference |
| 23 | DOWNSTREAM_ADAPTATION_CHECKLIST.md | Reference |
| 24 | METHODOLOGY_FEEDBACK_LOOP.md | Reference |
| 25 | TARGET_PROJECT_GOVERNANCE_PACK.md | Reference |
| 26 | PROJECT_CONSTITUTION_FRAMEWORK.md | Reference |
| 27 | templates/ | Reference (`templates/**`) |
| 28 | engine-journal/ | Reference (`engine-journal/**`) |

Все 28 прежних пунктов покрыты. Подтверждено `grep`-ом: каждый прежний путь присутствует в README после правки (счётчики ≥ 1).

Дополнительно §5 Reference вводит файлы, ранее не входившие в reading-list: `WORKTREE_GUIDE`, `NEW_PROJECT_ONBOARDING_GUIDE`, `SECURITY_POLICY`, `PUBLICATION_POLICY`, `GITHUB_RULESETS`, `GITHUB_TOKEN_POLICY`, `CI_POLICY`, `RELEASE_READINESS` — добавлены как Reference (это расширение coverage, не удаление).

## Изменения по файлам

### README.md

Между секциями «После bootstrap…» и «## Роль репозитория» добавлен новый раздел `## Обязательное чтение` с пояснением границы Core/Reference, ссылкой на §5 за обоснованием, нумерованным списком Core (10) и сгруппированным Reference (27 пунктов в шести тематических блоках: decisions/language/commenting; operational/branch/PR/worktree; engine/handoff/orchestrator interface; adoption; security/publication/release/CI/rulesets; templates/journal/source-index). Существующая структура README ниже не менялась (включая «Быстрый старт», «Роль репозитория», «Формат задач для Engine» и список pointer-ссылок).

### docs/agent-system/source/SOURCE_agent_system_index.md

Секция `## Читать в начале каждого нового чата` (28 нумерованных пунктов в 5 группах) заменена на короткий pointer: «Канонический reading-list — раздел «Обязательное чтение» в `README.md` (Core и Reference)»; пояснение «здесь список не дублируется, чтобы не было drift; при расхождении использовать `README.md`»; сохранён pointer «полный набор документов и шаблонов смотреть в каталоге `docs/agent-system/` в GitHub». Остальные секции файла (header snapshot, репозиторий, ветки, rulesets, «Важно») не менялись.

## Согласованность с авторитетным scope

- ✅ §10 whitelist соблюдён буквально: только README.md, source-index, journal.
- ✅ §10 «Delete/merge: нет» соблюдено: ни один файл не удалён и не слит.
- ✅ §5 «Core» список взят дословно (10 файлов, без перестановок).
- ✅ §5 «Канон reading-list: README.md» реализован: список перенесён в README, source-index ссылается без дубля.
- ✅ §5 обоснование границы процитировано в README со ссылкой на сам §5.
- ✅ Контент не потерян (см. таблицу 28→Core/Reference).

## Измененные файлы (этой задачей)

- `README.md`
- `docs/agent-system/source/SOURCE_agent_system_index.md`
- `docs/agent-system/engine-journal/input/TASK-0006-METH-CONSOLIDATION-C1-reading-list-tiering.md`
- `docs/agent-system/engine-journal/output/RESULT-0006-METH-CONSOLIDATION-C1-reading-list-tiering.md`
- `docs/agent-system/engine-journal/INDEX.md`

## Выполненные проверки

- Preflight: `git status`, `git fetch --all --prune`, `git switch developer`, `git pull --ff-only`, `git rev-parse developer/origin/developer`.
- Чтение RESULT-0004 §5 и §10 как авторитетного scope перед правками.
- `git diff --check` — чисто.
- `git status --short` — изменены только whitelist + journal.
- `grep` Core в README — ровно 10 пронумерованных пунктов.
- `grep` Reference в README — 27 пунктов (26 §5 + 1 preservation).
- `grep` по каждому из 28 прежних reading-list путей — каждый присутствует в README (count ≥ 1).
- Канон `README.md`, source-index pointer без дубля — сверено визуально.

## Невыполненные проверки и причина

- Markdown lint — отдельный documented lint command не подтверждён.
- Docker/production checks — запрещены scope.

## Результат проверки запрещенных файлов

Файлы вне whitelist не изменялись. `.env` не читался.

## Результат проверки sensitive/private markers

Секреты не вводились и не печатались.

## Результат language policy

RESULT Russian-first; English только для technical identifiers, paths, filenames и literal terms.

## Принятые решения

- Canon reading-list = `README.md` (раздел «Обязательное чтение»), source-index — pointer без дубля.
- Reference в README сгруппирован тематически (6 блоков) для читаемости, при этом каждый файл из §5 присутствует ровно один раз.
- `TARGET_REPOSITORY_ADOPTION_GUIDE.md` сохранён в Reference как preservation augmentation; будет удалён из Reference после merge PR-C4.
- Раздел «Обязательное чтение» вставлен между «После bootstrap…» и «Роль репозитория», чтобы быть максимально заметным и не ломать существующую структуру README.

## Риски

- В README остаются исторические pointer-ссылки на отдельные файлы (типа «Lifecycle описан в `PROJECT_LIFECYCLE.md`»). Это не дубль reading-list, а контекстные указатели; их консолидация — задача PR-C4 (adoption guides merge), не C1.

## Blockers

Нет.

## Закрытие после merge

Work PR status: PR создаёт пользователь (`gh` недоступен) — closure после merge отдельной задачей по `ENGINE_JOURNAL_CONTRACT.md`.

Release/sync: возможны (как в C6), фактические данные фиксируются при closure.

RESULT closed after merge: not applicable before merge.

INDEX closed after merge: not applicable before merge.

## Следующий рекомендуемый шаг

Пользователь создаёт PR `work/docs-maintainer-01/reading-list-tiering` → `developer`. После merge — closure 0006 (closure-only). Затем переходить к PR-C2 (methodology_reference + source_snapshot канонизация) по порядку из RESULT-0004 §10.

## Methodology feedback

Тиринг reading-list уже сам по себе уменьшает когнитивный вес «начала чата» с 28 до 10 пунктов. Это значимое улучшение для solo-operator mode без потери Reference-материала.
