# RESULT-0010-METH-CONSOLIDATION-C5B-templates-fork

Файл результата: `docs/agent-system/engine-journal/output/RESULT-0010-METH-CONSOLIDATION-C5B-templates-fork.md`

Связанный TASK file: `docs/agent-system/engine-journal/input/TASK-0010-METH-CONSOLIDATION-C5B-templates-fork.md`

Идентификатор задачи: `METH-CONSOLIDATION-C5B`

Номер sequence: `0010`

Агент: `docs-maintainer-01`

Engine: Claude Code

Timestamp (ISO-8601): `2026-06-15T12:09:46+07:00`

Baseline SHA (developer): `87c77a193dc3d08dd319ec747e4c64c9a8224e2b`

Ссылка на источник scope: [RESULT-0004 §7 «Templates: инвентаризация»](../output/RESULT-0004-METH-CONSOLIDATION-PLAN-01-consolidation-plan.md), §10 «PR-C5», §4 «Карта content-preservation», §9 «Развилки Р4/Р5».

methodology_reference: см. канон в `docs/agent-system/ENGINE_ENTRYPOINT.md` → раздел «Methodology reference»; данные текущей задачи:

```yaml
methodology_reference:
  repository: MaximKolomeets/agent-system-development
  source_branch: developer
  source_commit: 87c77a193dc3d08dd319ec747e4c64c9a8224e2b
  checked_at: 2026-06-15T12:09:46+07:00
  reference_type: commit
  notes: "Точка после merge JOURNAL-CLOSE-0009 (PR #120)."
```

## Решения архитектора (приоритетны над дефолтами плана)

- **Р4 = B** (header → канон, тела шаблонов раздельные, оба ссылаются на канон). Дефолт плана §9 рекомендовал вариант «объединить в один ENGINE_TASK_TEMPLATE»; архитектор выбрал B — зафиксировано.
- **Р5 = умеренная** (merge `NEW_PROJECT_BOOTSTRAP_PROMPT` + `PROJECT_CHAT_START_PROMPT_TEMPLATE` в один канон; `NEW_PROJECT_CHECKLIST` отдельным файлом). Дефолт плана §9 рекомендовал «глубокую консолидацию» как вариант 1; архитектор выбрал умеренную (вариант 2) — зафиксировано.

## Подтверждённый whitelist

Из §10 PR-C5 + решения архитектора (fork-файлы):

- Р4: `templates/DEVELOPMENT_TASK_TEMPLATE.md`, `templates/AGENT_RESEARCH_TASK_TEMPLATE.md`, новый канон `templates/TASK_HEADER_COMMON.md`;
- Р5: `templates/NEW_PROJECT_BOOTSTRAP_PROMPT.md`, `templates/PROJECT_CHAT_START_PROMPT_TEMPLATE.md`, новый канон `templates/NEW_PROJECT_PROMPT.md`;
- inbound по §8: `README.md`;
- журнал: `engine-journal/input/TASK-0010-*.md`, `engine-journal/output/RESULT-0010-*.md`, `engine-journal/INDEX.md`.

НЕ тронуты: `NEW_PROJECT_CHECKLIST.md` (явный запрет), `ADOPTION_TRANSFER_MANIFEST.yml` (именованных ссылок нет, wildcard `templates/**` покрывает каноны и stub'ы).

## Р4 — реализация (header → канон, тела раздельные)

### Канон TASK_HEADER_COMMON.md (создан)

Содержит общий header для engine task-шаблонов: Mandatory header, Russian-first, Recommended Engine Mode, Verified Baseline, Copy/Paste Completeness Check, Project constitution check.

### Карта content-preservation Р4

| Секция | Источник DEVELOPMENT | Источник AGENT_RESEARCH | Куда |
|---|---|---|---|
| Mandatory header | есть | есть (идентично) | канон |
| Russian-first абзац | есть (строка 19) | **отсутствовал** | канон (AGENT_RESEARCH теперь получает его через ссылку — улучшение, не потеря) |
| Recommended Engine Mode | есть | есть (идентично) | канон |
| Verified Baseline | есть | есть (идентично) | канон |
| Copy/Paste Completeness Check | есть | есть (идентично) | канон |
| Project constitution check | есть | есть (идентично) | канон |
| Task ID / Goal / Base branch / Work branch / Разрешенные / Запрещенные / Steps / Checks / Ожидаемый отчет | уникальное | — | остаётся в `DEVELOPMENT_TASK_TEMPLATE.md` |
| Research ID / Hypothesis / Scope / Files to inspect / Forbidden actions / Expected output | — | уникальное | остаётся в `AGENT_RESEARCH_TASK_TEMPLATE.md` |

`DEVELOPMENT_TASK_TEMPLATE.md` и `AGENT_RESEARCH_TASK_TEMPLATE.md` переписаны: вверху раздел «Общий header» со ссылкой на канон + перечисление общих блоков; ниже — только уникальные секции. Файлы **не удаляются** (Р4=B), stub не нужен. Бездомного контента нет.

## Р5 — реализация (два prompt → один канон, CHECKLIST отдельно)

### Канон NEW_PROJECT_PROMPT.md (создан)

Содержит: «Когда какой вариант использовать», «Короткий стартовый prompt проектного чата» (из `PROJECT_CHAT_START_PROMPT_TEMPLATE.md`, перенесён **дословно**), «Полный bootstrap prompt нового проекта» (из `NEW_PROJECT_BOOTSTRAP_PROMPT.md`, перенесён **дословно**). Явная отсылка, что `NEW_PROJECT_CHECKLIST.md` остаётся отдельным.

### Карта content-preservation Р5

| Источник | Куда в каноне |
|---|---|
| `PROJECT_CHAT_START_PROMPT_TEMPLATE.md` → «Copy/paste prompt» (весь блок) | раздел «Короткий стартовый prompt проектного чата» — дословно |
| `NEW_PROJECT_BOOTSTRAP_PROMPT.md` → весь bootstrap prompt (project profile … handoff … правила) | раздел «Полный bootstrap prompt нового проекта» — дословно |

Бездомного контента нет.

### Исход развязки Р5 (stub для обоих)

Inbound (вне self):

- `NEW_PROJECT_BOOTSTRAP_PROMPT.md` ← только append-only журнал (RESULT-0004) → **stub** (правило: append-only нельзя переписывать).
- `PROJECT_CHAT_START_PROMPT_TEMPLATE.md` ← `README.md:193` (в whitelist, **обновлён** на канон) + append-only журнал → **stub** (журнальные ссылки остаются).

Оба файла превращены в redirect-заглушки на `NEW_PROJECT_PROMPT.md`. Delete невозможен из-за append-only journal inbound; precedent C3/C5A.

## Перекрёстные ссылки (§8) — что обновлено

| Файл | Изменение |
|---|---|
| `templates/TASK_HEADER_COMMON.md` | создан (канон Р4) |
| `templates/DEVELOPMENT_TASK_TEMPLATE.md` | header → ссылка на канон; уникальный хвост сохранён |
| `templates/AGENT_RESEARCH_TASK_TEMPLATE.md` | header → ссылка на канон; уникальный хвост сохранён |
| `templates/NEW_PROJECT_PROMPT.md` | создан (канон Р5) |
| `templates/NEW_PROJECT_BOOTSTRAP_PROMPT.md` | → redirect-заглушка |
| `templates/PROJECT_CHAT_START_PROMPT_TEMPLATE.md` | → redirect-заглушка |
| `README.md:193` | ссылка на `PROJECT_CHAT_START_PROMPT_TEMPLATE.md` заменена на `NEW_PROJECT_PROMPT.md` + пометка про заглушки |

Не правились (нет именованных ссылок): `ADOPTION_TRANSFER_MANIFEST.yml` (wildcard `templates/**`), `ROLE_MODEL.md`, `WORKFLOW.md`. DEVELOPMENT/AGENT_RESEARCH ссылок по именам в docs (вне журнала) не имели — broken-ref риск при их сохранении нулевой (файлы остаются, Р4=B).

## Согласованность с авторитетным scope

- ✅ §10 whitelist соблюдён (fork-файлы + README + новые каноны + journal).
- ✅ §7 Р4: общий header вынесен в канон, оба шаблона ссылаются, тела раздельные.
- ✅ §7 Р5: два prompt → один канон, CHECKLIST не тронут.
- ✅ §4 content-preservation: все уникальные секции сохранены; бездомного контента нет (карты выше).
- ✅ Решения архитектора Р4=B, Р5=умеренная зафиксированы как приоритетные над дефолтами §9.
- ✅ append-only (journal) не переписывался; stub обеспечивает 1-hop redirect.

## Измененные файлы (этой задачей)

- `docs/agent-system/templates/TASK_HEADER_COMMON.md` (создан)
- `docs/agent-system/templates/DEVELOPMENT_TASK_TEMPLATE.md`
- `docs/agent-system/templates/AGENT_RESEARCH_TASK_TEMPLATE.md`
- `docs/agent-system/templates/NEW_PROJECT_PROMPT.md` (создан)
- `docs/agent-system/templates/NEW_PROJECT_BOOTSTRAP_PROMPT.md` (stub)
- `docs/agent-system/templates/PROJECT_CHAT_START_PROMPT_TEMPLATE.md` (stub)
- `README.md`
- `docs/agent-system/engine-journal/input/TASK-0010-METH-CONSOLIDATION-C5B-templates-fork.md`
- `docs/agent-system/engine-journal/output/RESULT-0010-METH-CONSOLIDATION-C5B-templates-fork.md`
- `docs/agent-system/engine-journal/INDEX.md`

## Выполненные проверки

- Preflight: `git status`, `git fetch --all --prune`, `git switch developer`, `git pull --ff-only`, `git rev-parse developer/origin/developer`.
- Чтение RESULT-0004 §7/§10/§4/§9 как авторитетного scope.
- Inbound-карта 4 fork-файлов через `git grep` (вне журнала) до правок.
- Чтение всех 4 исходников целиком для content-preservation.
- После правок: `git status --short` — только whitelist + journal; `git diff --check` — чисто; `git grep` именованных ссылок в manifest/README — только обновлённая README-строка; `NEW_PROJECT_CHECKLIST.md` не в списке изменённых.

## Невыполненные проверки и причина

- Markdown lint — отдельный documented lint command не подтверждён.
- Docker/production checks — запрещены scope.
- Очистка stub-ссылок из append-only журнала — нарушает append-only; работают через redirect.

## Результат проверки запрещенных файлов

`NEW_PROJECT_CHECKLIST.md` не тронут. Append-only истории не переписывались. `.env` не читался.

## Результат проверки sensitive/private markers

Секреты не вводились и не печатались.

## Результат language policy

RESULT Russian-first; English только для technical identifiers, paths, filenames и literal terms. Каноны сохраняют английский внутри copy/paste prompt блоков дословно (external user prompts) и в чеклист-пунктах Copy/Paste Completeness Check (унаследованы дословно).

## Принятые решения

- Р4=B: канон `TASK_HEADER_COMMON.md`; DEVELOPMENT и AGENT_RESEARCH остаются раздельными файлами со ссылкой на канон (без stub, файлы не удаляются).
- AGENT_RESEARCH через ссылку на канон получает Russian-first абзац, которого у него раньше не было — это согласование, не потеря.
- Р5=умеренная: канон `NEW_PROJECT_PROMPT.md`; оба исходных prompt → stub; `NEW_PROJECT_CHECKLIST.md` отдельным файлом.
- README единственный inbound-файл вне журнала, обновлён.

## Риски

- Stub'ы `NEW_PROJECT_BOOTSTRAP_PROMPT.md` и `PROJECT_CHAT_START_PROMPT_TEMPLATE.md` попадут в target adoption через wildcard `templates/**` — это валидные redirect-страницы, работают. Совокупно по C3/C5A/C5B накопилось 5 stub-файлов в templates/; при желании отдельная будущая задача может вычистить их из manifest точечным exclude (вне scope).
- В append-only journal остаются ссылки на старые пути prompt — исторический факт, работают через redirect.

## Blockers

Нет.

## Закрытие после merge

Work PR status: PR создаёт пользователь (`gh` недоступен) — closure после merge отдельной задачей по `ENGINE_JOURNAL_CONTRACT.md`.

Release/sync: возможны, фактические данные фиксируются при closure.

RESULT closed after merge: not applicable before merge.

INDEX closed after merge: not applicable before merge.

## Следующий рекомендуемый шаг

Пользователь создаёт PR `work/docs-maintainer-01/templates-fork` → `developer`. После merge — closure 0010. PR-C5 (templates cleanup) полностью завершён (C5A + C5B). Остаётся последний крупный пункт плана — **PR-C4** (adoption guides merge, требует решений по Р1/Р2/Р3) по RESULT-0004 §10.

## Methodology feedback

Р4=B (header→канон, тела раздельные) — хороший компромисс: убирает дублирование общей части без потери специфики типов задач и без рискованного слияния тел. Паттерн «общий канон + раздельные тонкие специализации» применим к будущим task-типам (review/security и т.д.).
