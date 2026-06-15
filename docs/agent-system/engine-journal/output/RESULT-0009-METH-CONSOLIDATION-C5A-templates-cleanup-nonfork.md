# RESULT-0009-METH-CONSOLIDATION-C5A-templates-cleanup-nonfork

Файл результата: `docs/agent-system/engine-journal/output/RESULT-0009-METH-CONSOLIDATION-C5A-templates-cleanup-nonfork.md`

Связанный TASK file: `docs/agent-system/engine-journal/input/TASK-0009-METH-CONSOLIDATION-C5A-templates-cleanup-nonfork.md`

Идентификатор задачи: `METH-CONSOLIDATION-C5A`

Номер sequence: `0009`

Агент: `docs-maintainer-01`

Engine: Claude Code

Timestamp (ISO-8601): `2026-06-15T11:43:02+07:00`

Baseline SHA (developer): `3b5c9094d8852ad5a7ed5259bb7a3e51f0f4f7dd`

Ссылка на источник scope: [RESULT-0004 §7 «Templates: инвентаризация»](../output/RESULT-0004-METH-CONSOLIDATION-PLAN-01-consolidation-plan.md), §10 «PR-C5», §4 «Карта content-preservation», §9 «Риски и развилки» (Р4/Р5 — цитируются ниже).

methodology_reference: см. канон в `docs/agent-system/ENGINE_ENTRYPOINT.md` → раздел «Methodology reference»; данные текущей задачи:

```yaml
methodology_reference:
  repository: MaximKolomeets/agent-system-development
  source_branch: developer
  source_commit: 3b5c9094d8852ad5a7ed5259bb7a3e51f0f4f7dd
  checked_at: 2026-06-15T11:43:02+07:00
  reference_type: commit
  notes: "Точка после merge JOURNAL-CLOSE-0008 (PR #116)."
```

## Подтверждённый whitelist (из RESULT-0004 §10)

PR-C5 цитата: «Allowed: затронутые templates, README.md, WORKFLOW.md/ROLE_MODEL.md/DECISION_LOG.md (для wire-ссылок), ADOPTION_TRANSFER_MANIFEST.yml, journal.»

Whitelist текущей задачи C5A (4 файла методологии + journal):

- `docs/agent-system/templates/CODE_REVIEW_REPORT_TEMPLATE.md` — приём merge из REVIEW_TEMPLATE;
- `docs/agent-system/templates/REVIEW_TEMPLATE.md` — развязка после merge;
- `docs/agent-system/WORKFLOW.md` — wire-ссылка на AGENT_REPORT_TEMPLATE и DECISION_TEMPLATE и CODE_REVIEW_REPORT_TEMPLATE;
- `docs/agent-system/DECISION_LOG.md` — структурная wire-ссылка на DECISION_TEMPLATE.md в преамбуле (исторические записи не тронуты);
- журнал: `engine-journal/input/TASK-0009-*.md`, `engine-journal/output/RESULT-0009-*.md`, `engine-journal/INDEX.md`.

Из whitelist по §10 НЕ потребовалось править: `README.md`, `ROLE_MODEL.md`, `ADOPTION_TRANSFER_MANIFEST.yml` — конкретных упоминаний REVIEW_TEMPLATE/AGENT_REPORT_TEMPLATE/DECISION_TEMPLATE по именам в них нет; wildcard `templates/**` в manifest и Reference-блок в README покрывают эти файлы без точечной правки.

**Fork-шаблоны в whitelist НЕ включены** (явный запрет таски): `DEVELOPMENT_TASK_TEMPLATE.md`, `AGENT_RESEARCH_TASK_TEMPLATE.md`, `NEW_PROJECT_BOOTSTRAP_PROMPT.md`, `NEW_PROJECT_CHECKLIST.md`, `PROJECT_CHAT_START_PROMPT_TEMPLATE.md` — не тронуты.

## Fork-guard

Развилки Р4 (DEVELOPMENT+RESEARCH→1) и Р5 (new-project prompt-слой) — fork-часть; **не исполнены**, вынесены в раздел «Развилки к решению архитектора» дословно с вариантами (см. ниже).

Не-fork часть оказалась полностью fork-независимой: REVIEW_TEMPLATE → CODE_REVIEW_REPORT_TEMPLATE и wire AGENT_REPORT/DECISION_TEMPLATE не пересекаются с Р4/Р5.

## Исход развязки (REVIEW_TEMPLATE → stub)

Inbound-карта REVIEW_TEMPLATE.md по `git grep`:

| Источник | Тип |
|---|---|
| `engine-journal/output/RESULT-0001-METH-GUARDRAILS-01-review-guardrails-local-sync.md:107` | append-only history (список изменённых файлов в исторической задаче) |
| `engine-journal/output/RESULT-0004-METH-CONSOLIDATION-PLAN-01-consolidation-plan.md` | append-only history (план) |

Все ссылки — в append-only истории engine-journal. Правка append-only нарушает §8 rule 6 и `ENGINE_JOURNAL_CONTRACT.md`. По правилу таски п.5 («если хоть одну ссылку нельзя чисто перенаправить → НЕ удалять, оставить redirect-заглушку») и precedent'у из C3: **REVIEW_TEMPLATE превращён в stub** на `CODE_REVIEW_REPORT_TEMPLATE.md`.

Тонкое отличие от правила «ссылок 0 → delete»: формально grep даёт > 0 ссылок, но все они в append-only истории. §8 rule 6 разрешает считать такие broken-refs «допустимым историческим фактом», однако stub-precedent C3 единообразен и безопаснее.

## Карта content-preservation (§4)

### REVIEW_TEMPLATE.md → CODE_REVIEW_REPORT_TEMPLATE.md (раздел «Облегчённый PR / comment review»)

| Источник (REVIEW_TEMPLATE) | Куда в каноне |
|---|---|
| Вступление «канон отчёта — CODE_REVIEW_REPORT_TEMPLATE.md; этот лёгкий формат — для PR/comment review» | заменено вступительной строкой нового раздела «Облегчённый PR / comment review» с указанием Journal trace: always |
| Раздел `## PR/branch` | подраздел `### PR / branch` |
| `## Scope` | `### Scope` |
| `## Files reviewed` | `### Files reviewed` |
| `## Checks run` | `### Checks run` |
| `## Findings` | `### Findings` |
| `## Journal closure` (правила + блокирующие замечания) | `### Journal closure` — перенесён дословно |
| `## Required changes` | `### Required changes` |
| `## Recommendation` (approve/changes required/hold) | `### Recommendation` |

Бездомного контента нет. Все 8 разделов прежнего REVIEW_TEMPLATE присутствуют в каноне.

### AGENT_REPORT_TEMPLATE.md (wire, не merge)

Файл сохранён без изменений. Добавлена wire-ссылка из `WORKFLOW.md` → раздел «Шаблоны отчётов и решений»: «Универсальный отчёт роли … `templates/AGENT_REPORT_TEMPLATE.md` (Summary, Changed files, Checks, Risks, Open questions, Next step)». Файл больше не orphan.

### DECISION_TEMPLATE.md (wire, не merge)

Файл сохранён без изменений. Добавлены wire-ссылки:
- `DECISION_LOG.md` (преамбула): «Формат новой записи: см. `templates/DECISION_TEMPLATE.md` … Этот файл append-only: исторические записи не переписывать». Это **структурная** ссылка (§8 п.4 разрешает); исторические записи DECISION_LOG не тронуты.
- `WORKFLOW.md` → раздел «Шаблоны отчётов и решений»: «Запись решения для `DECISION_LOG.md`: `templates/DECISION_TEMPLATE.md` (Date, Decision, Context, Options considered, Reason, Consequences, Follow-up actions)».

Файл больше не orphan.

## Перекрёстные ссылки (§8) — что обновлено

| Файл | Изменение |
|---|---|
| `templates/CODE_REVIEW_REPORT_TEMPLATE.md` | в конец добавлен раздел «Облегчённый PR / comment review» (8 подразделов) |
| `templates/REVIEW_TEMPLATE.md` | заменён на redirect-заглушку на канон |
| `WORKFLOW.md` | в конец добавлен раздел «Шаблоны отчётов и решений» с тремя wire-ссылками (AGENT_REPORT_TEMPLATE, DECISION_TEMPLATE, CODE_REVIEW_REPORT_TEMPLATE) |
| `DECISION_LOG.md` | в преамбулу (после заголовка `# DECISION_LOG`) добавлена структурная ссылка на `templates/DECISION_TEMPLATE.md`; исторические записи не тронуты |

**Не правились (нет именованных ссылок на затронутые шаблоны):**

- `README.md` — Reference в разделе «Обязательное чтение» уже покрывает `templates/**` wildcard'ом (PR-C1); конкретных упоминаний REVIEW_TEMPLATE/AGENT_REPORT_TEMPLATE/DECISION_TEMPLATE по именам нет.
- `ROLE_MODEL.md` — конкретных упоминаний нет.
- `ADOPTION_TRANSFER_MANIFEST.yml` — `templates/**` wildcard в `requires_target_adaptation` уже покрывает; конкретных имён нет; stub не нужно переносить в target (но wildcard технически его захватит — это допустимо, поскольку stub является валидным redirect-файлом и не несёт уникального контента).

## Согласованность с авторитетным scope

- ✅ §10 whitelist соблюдён буквально (включая разрешённые WORKFLOW/DECISION_LOG для wire-ссылок).
- ✅ §7 не-fork операции: REVIEW_TEMPLATE→CODE_REVIEW_REPORT_TEMPLATE (merge с stub), AGENT_REPORT_TEMPLATE (wire), DECISION_TEMPLATE (wire) — выполнены полностью.
- ✅ §7 fork-операции (Р4: DEVELOPMENT+RESEARCH; Р5: NEW_PROJECT_BOOTSTRAP_PROMPT+NEW_PROJECT_CHECKLIST+PROJECT_CHAT_START_PROMPT_TEMPLATE) — НЕ исполнены, файлы не тронуты; вынесены в раздел развилок.
- ✅ §4 content-preservation: все 8 разделов REVIEW_TEMPLATE перенесены в канон; бездомного контента нет.
- ✅ §8 rule 6 (append-only) соблюдено: исторические RESULT-0001/0004 не правились; DECISION_LOG исторические записи не правились (добавлена только структурная преамбула).
- ✅ §8 rule 7 (redirect для исторических ссылок) — REVIEW_TEMPLATE.md stub.

## Развилки к решению архитектора (выносится из C5A в отдельное решение)

Цитаты из RESULT-0004 §9 дословно:

### Р4 — DEVELOPMENT_TASK_TEMPLATE + AGENT_RESEARCH_TASK_TEMPLATE → 1

> **Р4.** Объединять ли DEVELOPMENT + RESEARCH task templates в один параметризованный или оставить два с общим header-ссылкой.

Подробнее из RESULT-0004 §7:

> `AGENT_RESEARCH_TASK_TEMPLATE.md` и `DEVELOPMENT_TASK_TEMPLATE.md` — оба = mandatory header + Verified Baseline + Copy/Paste Completeness + Project constitution check; различаются хвостом (Hypothesis/Files/Expected output vs Steps/Goal). Сильно дублируют друг друга и `CODE_REVIEW_TASK_TEMPLATE`. **Развилка Р4:** либо объединить в один `ENGINE_TASK_TEMPLATE.md` с вариативным хвостом, либо оставить два, вынеся общий header-блок в канон (`CHATGPT_RESPONSE_STANDARD.md` уже его описывает) и сослаться. Рекомендация: объединить в один с двумя профилями (development/research).

**Варианты:**
1. **Объединить в один `ENGINE_TASK_TEMPLATE.md`** с двумя профилями (development / research) — рекомендация плана; уменьшает duplication, требует stub для обоих старых файлов; внешние bookmark/цитирования на эти пути встречаются редко.
2. **Оставить два файла**, вынеся общий header-блок в `CHATGPT_RESPONSE_STANDARD.md` как канон и заменив дубль в обоих template на ссылку.

### Р5 — New-project prompt-слой

> **Р5.** New-project prompt-слой (NEW_PROJECT_BOOTSTRAP_PROMPT + PROJECT_CHAT_START_PROMPT_TEMPLATE + NEW_PROJECT_CHECKLIST) — глубина консолидации.

Подробнее из RESULT-0004 §7:

> `NEW_PROJECT_BOOTSTRAP_PROMPT.md` — chat-prompt нового проекта; пересекается с `NEW_PROJECT_ONBOARDING_GUIDE` и `PROJECT_CHAT_START_PROMPT_TEMPLATE`. **Merge** в единый new-project prompt (см. ниже) либо wire.
> **Слабо ссылаемые (1):** `NEW_PROJECT_CHECKLIST.md`, `PROJECT_CHAT_START_PROMPT_TEMPLATE.md` — проверить, не дублируют ли `NEW_PROJECT_BOOTSTRAP_PROMPT`/onboarding; кандидаты на консолидацию new-project prompt-слоя (развилка Р5).

**Варианты:**
1. **Глубокая консолидация:** все три файла → один `NEW_PROJECT_PROMPT.md` (короткий + checklist + start-prompt внутри), по образцу PR-C3 ADOPTION_PROMPT. Stub для исходных трёх. Уменьшает размер templates/-слоя на 3 файла.
2. **Умеренная:** только NEW_PROJECT_BOOTSTRAP_PROMPT → NEW_PROJECT_ONBOARDING_GUIDE (поглощается guide'ом); CHECKLIST и START_PROMPT остаются как самостоятельные wire-кандидаты.
3. **Минимальная (wire):** все три оставить как есть, добавить wire-ссылки из README/ONBOARDING_GUIDE; без удалений.

### Прочие пункты §7, помеченные как Р-развилки

В §7 указанных как Р-развилки только Р4 и Р5. Других fork-кандидатов в C5 нет.

## Измененные файлы (этой задачей)

- `docs/agent-system/templates/CODE_REVIEW_REPORT_TEMPLATE.md`
- `docs/agent-system/templates/REVIEW_TEMPLATE.md`
- `docs/agent-system/WORKFLOW.md`
- `docs/agent-system/DECISION_LOG.md`
- `docs/agent-system/engine-journal/input/TASK-0009-METH-CONSOLIDATION-C5A-templates-cleanup-nonfork.md`
- `docs/agent-system/engine-journal/output/RESULT-0009-METH-CONSOLIDATION-C5A-templates-cleanup-nonfork.md`
- `docs/agent-system/engine-journal/INDEX.md`

## Выполненные проверки

- Preflight: `git status`, `git fetch --all --prune`, `git switch developer`, `git pull --ff-only`, `git rev-parse developer/origin/developer`.
- Чтение RESULT-0004 §7, §10, §4, §9 как авторитетного scope.
- Inbound-карта для REVIEW_TEMPLATE, AGENT_REPORT_TEMPLATE, DECISION_TEMPLATE через `git grep` до правок.
- Чтение REVIEW_TEMPLATE и CODE_REVIEW_REPORT_TEMPLATE целиком для content-preservation.
- Проверка manifest/README на конкретные имена 3 шаблонов — отсутствуют (wildcard покрытие); правка не требуется.
- После правок: `git status --short` — только whitelist + journal; `git diff --check` — чисто.

## Невыполненные проверки и причина

- Markdown/YAML lint — отдельный documented lint command не подтверждён.
- Docker/production checks — запрещены scope.
- Очистка REVIEW_TEMPLATE из append-only RESULT-0001/RESULT-0004 — нарушает append-only; ссылки работают через stub.

## Результат проверки запрещенных файлов

Fork-шаблоны (DEVELOPMENT_TASK_TEMPLATE, AGENT_RESEARCH_TASK_TEMPLATE, NEW_PROJECT_BOOTSTRAP_PROMPT, NEW_PROJECT_CHECKLIST, PROJECT_CHAT_START_PROMPT_TEMPLATE) не тронуты. Append-only истории (engine-journal/output/RESULT-0001, RESULT-0004 и пр.; исторические записи DECISION_LOG) не правились. `.env` не читался.

## Результат проверки sensitive/private markers

Секреты не вводились и не печатались.

## Результат language policy

RESULT Russian-first; English только для technical identifiers, paths, filenames и literal terms (включая 8 английских названий подразделов в каноне «Облегчённый PR/comment review», унаследованных из REVIEW_TEMPLATE дословно).

## Принятые решения

- REVIEW_TEMPLATE → stub после merge (а не delete): inbound в append-only истории, precedent C3 единообразен.
- AGENT_REPORT_TEMPLATE и DECISION_TEMPLATE — keep + wire (как рекомендовано §7).
- Wire AGENT_REPORT_TEMPLATE — из WORKFLOW.md (один файл; добавление аналогичной ссылки в ROLE_MODEL.md избыточно для уже не-orphan статуса).
- Wire DECISION_TEMPLATE — из WORKFLOW.md + структурная преамбула DECISION_LOG.md (исторические записи не правились).
- README/ROLE_MODEL/manifest не правились — конкретных имён нет, wildcard покрывает.
- Р4 и Р5 не исполнены, дословно процитированы как развилки.

## Риски

- Stub REVIEW_TEMPLATE.md остаётся в `requires_target_adaptation` через wildcard `templates/**` в manifest. При следующем target adoption stub'ы трёх файлов (REVIEW_TEMPLATE из C5A + SHORT_TARGET_ADOPTION_PROMPT + TARGET_REPOSITORY_ADOPTION_CHAT_PROMPT из C3) могут попасть в target копию — это валидные redirect-страницы, и они продолжат работать. Альтернатива (точечный exclude в manifest) — избыточно для текущего scope.
- В RESULT-0001 (append-only) останется устаревшая ссылка на REVIEW_TEMPLATE.md как «изменённый файл задачи». Это исторический факт.

## Blockers

Нет.

## Закрытие после merge

Work PR status: PR создаёт пользователь (`gh` недоступен) — closure после merge отдельной задачей по `ENGINE_JOURNAL_CONTRACT.md`.

Release/sync: возможны, фактические данные фиксируются при closure.

RESULT closed after merge: not applicable before merge.

INDEX closed after merge: not applicable before merge.

## Следующий рекомендуемый шаг

Пользователь создаёт PR `work/docs-maintainer-01/templates-cleanup-nonfork` → `developer`. После merge — closure 0009. Затем архитектор принимает решения по Р4/Р5 (см. варианты выше) → выполняется отдельный PR-C5B (fork-часть) при необходимости. Параллельно/далее можно переходить к **PR-C4** (adoption guides merge, требует Р1/Р2/Р3) по плану RESULT-0004 §10.

## Methodology feedback

Разделение C5 на не-fork (C5A) + fork (Р4/Р5) — хороший паттерн для крупных консолидационных PR: безопасные операции делаются сразу, рискованные/спорные выносятся на решение архитектора. Это позволяет продвигать план не блокируясь на каждом fork-вопросе.
