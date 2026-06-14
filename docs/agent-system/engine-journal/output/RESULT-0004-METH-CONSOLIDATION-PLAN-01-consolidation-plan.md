# RESULT-0004-METH-CONSOLIDATION-PLAN-01-consolidation-plan

Файл результата: `docs/agent-system/engine-journal/output/RESULT-0004-METH-CONSOLIDATION-PLAN-01-consolidation-plan.md`

Связанный TASK file: `docs/agent-system/engine-journal/input/TASK-0004-METH-CONSOLIDATION-PLAN-01-consolidation-plan.md`

Идентификатор задачи: `METH-CONSOLIDATION-PLAN-01`

Номер sequence: `0004`

Агент: `qa-reviewer-01`

Engine: Claude Code

Режим: plan-only по содержимому методологии; запись только в журнал.

Тип: план консолидации (finding 5 из `REVIEW-INITIAL-01`). Сам по себе ничего не сливает и не удаляет.

Timestamp (ISO-8601): `2026-06-14T16:43:07+07:00`

Baseline SHA (developer): `4694da7dc64adcdd7801f915b57fb9a2c6bcf83e`

methodology_reference:

```yaml
methodology_reference:
  repository: MaximKolomeets/agent-system-development
  source_branch: developer
  source_commit: 4694da7dc64adcdd7801f915b57fb9a2c6bcf83e
  checked_at: 2026-06-14T16:43:07+07:00
  reference_type: commit
  notes: "Точка после merge METH-CONSISTENCY-01 (#101) и JOURNAL-CLOSE-0003 (#102)."
```

---

## 1. Снимок

- Top-level методологических docs в `docs/agent-system/*.md`: **36** (без `agents/`, `engine-journal/`, `source/`), плюс `ADOPTION_TRANSFER_MANIFEST.yml` → ~37 нормативных документов. С учётом `source/` (3) и `agents/**` (исторические отчёты ролей) — соответствует оценке «~40 docs».
- Templates в `docs/agent-system/templates/`: **26** (оценка задачи «~28» близка).
- Reading-list: после `METH-CONSISTENCY-01` источником стал сгруппированный список в `source/SOURCE_agent_system_index.md` (~28 пунктов, сгруппирован). Исходная плоская проблема «~47 обязательных» снята частично; единый **Core mandatory** ещё не зафиксирован — см. раздел 5.
- Baseline SHA: `4694da7dc64adcdd7801f915b57fb9a2c6bcf83e`.
- `METH-CONSISTENCY-01` **в `developer`** (work PR #101, closure PR #102 смержены; `developer == origin/developer`). Working tree clean.

## 2. Инвентаризация adoption-слоя

| Файл | Назначение | Уникальный контент | Пересечение |
|---|---|---|---|
| `ADOPTION_GUIDE.md` | Режимы adoption (audit-only / docs-only / runtime), transfer manifest, drift-control, ceremony/token budget, minimal first PR, new-vs-existing bootstrap, developer-vs-develop, PowerShell/UTF-8 | Канон режимов adoption; minimal first PR; ceremony budget | methodology_reference (с ENGINE_ENTRYPOINT, TARGET_REPO_GUIDE); drift (с source/README, manifest); developer-vs-develop (с TARGET_REPO_GUIDE) |
| `TARGET_REPOSITORY_ADOPTION_GUIDE.md` | Пошаговый (12 шагов) adoption в **существующий** target repo | Шаги profile→visibility→structure→governance→branches→bootstrap→review→handoff применительно к existing repo; feedback sanitization | Сильное пересечение с ADOPTION_GUIDE (режимы, methodology_reference, feedback) и с NEW_PROJECT_ONBOARDING_GUIDE (governance pack, ветки, forbidden files, handoff) |
| `NEW_PROJECT_ONBOARDING_GUIDE.md` | Практический (13 шагов) запуск **нового** проекта | Idea→profile→repo→structure→governance→branches→worktree→roles→PR→review→handoff→checklist для new project | Очень сильное пересечение с PROJECT_LIFECYCLE (та же траектория, другой уровень детализации) |
| `PROJECT_LIFECYCLE.md` | Концептуальный 11-стадийный lifecycle нового проекта | Стадийная модель Idea→…→Handoff | Дублирует NEW_PROJECT_ONBOARDING_GUIDE по сути; отличается только «концепция vs how-to» |
| `DOWNSTREAM_ADAPTATION_CHECKLIST.md` | Чеклист перед docs-only adoption/review | Формат чеклиста по 12 секциям (identity, branch, state, governance, language, commenting, freshness, manifest, security, adoption mode, review) | Содержательно повторяет правила ADOPTION_GUIDE / TARGET_REPO_GUIDE / language/commenting policy — но в проверяемой чеклист-форме |

Вывод: фактически две оси, которые методология уже различает (`new empty repository bootstrap` vs `existing repository adoption`), размазаны по 5 документам. Дублируются: governance pack, ветки, worktree, forbidden files, handoff, methodology_reference, feedback/sanitization, developer-vs-develop.

## 3. Проверка предложенной структуры (п.1–5)

1. **Reading-list → Core + Reference — confirm (с уточнением).** Двухуровневый список правильный. Уточнение: канон reading-list — `README.md` (точка входа), а `source/SOURCE_agent_system_index.md` — навигационное зеркало. Core должен жить в одном каноне, второй ссылается, иначе вернётся drift. Точный Core — раздел 5.
2. **ADOPTION_GUIDE как единый канон — adjust.** Слияние new-project onboarding в adoption guide **конфликтует с осью new-vs-existing**, которую методология намеренно разделяет (`ADOPTION_GUIDE.md` сам это правило и содержит). Рекомендованная корректировка:
   - `ADOPTION_GUIDE.md` = канон **existing repository adoption**; вбирает уникальные шаги `TARGET_REPOSITORY_ADOPTION_GUIDE.md`.
   - `NEW_PROJECT_ONBOARDING_GUIDE.md` = канон **new project bootstrap**; вбирает `PROJECT_LIFECYCLE.md` (концепцию — как вводную секцию).
   - `DOWNSTREAM_ADAPTATION_CHECKLIST.md` остаётся **единственным чеклистом**, но дедуплицируется: правила не повторяются прозой, а проверяются пунктами со ссылкой на канон. Чеклист — отдельный полезный формат (его используют как pre-merge gate), удалять не нужно.
3. **Объединить два adoption-prompt в один — confirm.** `SHORT_TARGET_ADOPTION_PROMPT.md` уже в основном указатель на `TARGET_REPOSITORY_ADOPTION_CHAT_PROMPT.md` + содержит реальные короткий/безопасный one-liner-prompts и «как действует engine». Свести в один `templates/ADOPTION_PROMPT.md` (секции: короткий prompt, безопасный короткий prompt, полный canonical prompt, как действует engine). `TARGET_REPOSITORY_ADOPTION_CHAT_PROMPT.md` — самый ссылаемый (14), поэтому каноном делать его (или новый файл с redirect-заглушкой во избежание broken refs).
4. **methodology_reference — один канон — confirm с уточнением.** Канон = `ENGINE_ENTRYPOINT.md` (там уже есть нормативный блок и это входная точка engine). `ENGINE_SELF_DISCOVERY_CONTRACT.md` сейчас methodology_reference **не содержит** — делать его каноном = переносить контент; дешевле оставить канон в ENGINE_ENTRYPOINT. Машинная схема в `ADOPTION_TRANSFER_MANIFEST.yml` остаётся (она потребляется как данные), но с пометкой «human canon: ENGINE_ENTRYPOINT.md».
5. **Templates — инвентаризация — confirm.** Выполнена, см. раздел 7.

## 4. Карта content-preservation (для каждого delete/merge — куда уезжает контент)

- `PROJECT_LIFECYCLE.md` → **merge в** `NEW_PROJECT_ONBOARDING_GUIDE.md` как вводная секция «Жизненный цикл (стадии 1–11)». Уникальное (стадийная модель) сохраняется как обзорный раздел перед how-to шагами. Бездомного контента нет.
- `TARGET_REPOSITORY_ADOPTION_GUIDE.md` → **merge в** `ADOPTION_GUIDE.md` (новый раздел «Пошаговый existing-repo adoption»). Уникальное (profile/visibility/structure/handoff шаги для existing repo, feedback sanitization шаги) переносится; sanitization уже есть и в `METHODOLOGY_FEEDBACK_LOOP.md` — оставить там канон, в ADOPTION_GUIDE ссылку.
- `SHORT_TARGET_ADOPTION_PROMPT.md` → **merge в** `templates/ADOPTION_PROMPT.md`. Уникальное (короткий и безопасный короткий one-liner-prompts, «первый результат», «как действует engine») переносится дословно.
- `DOWNSTREAM_ADAPTATION_CHECKLIST.md` → **keep, но dedupe**: прозовые повторы правил заменяются ссылками на канон; чеклист-пункты сохраняются. Контент не теряется.
- Orphan templates (раздел 7) — целевые места указаны там.
- **Бездомный контент → развилки для архитектора (раздел 9):**
  - В `ADOPTION_GUIDE` и `TARGET_REPOSITORY_ADOPTION_GUIDE` две слегка разные формулировки «developer vs develop / main-only flow» — при merge выбрать одну каноническую (развилка Р3).
  - В `NEW_PROJECT_ONBOARDING_GUIDE` и `PROJECT_LIFECYCLE` разный уровень детализации одного и того же — решить, сохранять ли «концептуальный обзор» отдельной секцией или свернуть (развилка Р1).

## 5. Reading-list: Core (~10) + Reference

Предлагаемый **Core mandatory** (читать в начале каждого чата) — 10 файлов:

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

**Reference (по необходимости):** DECISION_LOG, OPERATIONAL_FAST_LANE, TASK_FILE_HANDOFF_CONTRACT, LANGUAGE_POLICY, FILE_COMMENTING_STANDARD, CHATGPT_OPERATING_CONTRACT, CHATGPT_RESPONSE_STANDARD, ENGINE_SELF_DISCOVERY_CONTRACT, ADOPTION_GUIDE, ADOPTION_TRANSFER_MANIFEST, DOWNSTREAM_ADAPTATION_CHECKLIST, METHODOLOGY_FEEDBACK_LOOP, TARGET_PROJECT_GOVERNANCE_PACK, PROJECT_CONSTITUTION_FRAMEWORK, PR_WORKFLOW, GITHUB_RULESETS, GITHUB_TOKEN_POLICY, PUBLICATION_POLICY, SECURITY_POLICY, WORKTREE_GUIDE, CI_POLICY, RELEASE_READINESS, NEW_PROJECT_ONBOARDING_GUIDE, source/SOURCE_agent_system_index, templates/**, engine-journal/**.

**Обоснование границы Core:** оставлены документы, без которых нельзя безопасно (а) понять текущее состояние/план, (б) выбрать роль/режим, (в) соблюсти branch/review boundary, (г) корректно сдать engine-задачу и journal. Adoption/governance/security-policy документы переведены в Reference, т.к. нужны только в соответствующем scope (adoption, target governance, release), а не в каждом чате. ENGINE_ENTRYPOINT + ENGINE_JOURNAL_CONTRACT оставлены в Core, т.к. почти каждая file-changing задача проходит через journal. Граница: Core = «нужно всегда», Reference = «нужно по типу задачи».

Канон reading-list: `README.md`. `source/SOURCE_agent_system_index.md` ссылается на него и не дублирует список.

## 6. methodology_reference: дубли, канон, замена ссылками

Нормативный блок (спека) дублируется в:

- `docs/agent-system/ENGINE_ENTRYPOINT.md:26` — раздел «Methodology reference» (предлагаемый **канон**).
- `docs/agent-system/ADOPTION_GUIDE.md:71` — раздел «Methodology reference» → заменить ссылкой на канон.
- `docs/agent-system/TARGET_REPOSITORY_ADOPTION_GUIDE.md:67` — раздел «Methodology reference» → заменить ссылкой (при merge файла — учесть в ADOPTION_GUIDE один раз).
- `docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml` (`methodology_reference_schema`, `reference_type: commit`) — **оставить** как машинную схему, добавить комментарий «human canon: ENGINE_ENTRYPOINT.md».

Корректные **использования** (fill-in инстансы, НЕ дубли спеки, не трогать):
`templates/ADOPTION_AUDIT_TASK_TEMPLATE.md:91`, `templates/DOCS_ONLY_ADOPTION_TASK_TEMPLATE.md:85`, `templates/TARGET_REPOSITORY_ADOPTION_CHAT_PROMPT.md:83`, journal TASK/RESULT 0002/0003.

Действие execution: оставить полную YAML-спеку только в ENGINE_ENTRYPOINT; в ADOPTION_GUIDE и TARGET_REPO_GUIDE заменить на одну строку-ссылку «см. `ENGINE_ENTRYPOINT.md` → Methodology reference»; шаблоны/journal не менять.

Аналогично `source_snapshot` блок: канон — `source/README.md` (Source Snapshot Policy). `ADOPTION_GUIDE.md` (раздел «Source and snapshot drift control») → заменить ссылкой на `source/README.md`.

## 7. Templates: инвентаризация по использованию

Подсчёт ссылок вне самого файла шаблона и вне журнала (`git grep -l` по `docs/README/AGENTS`):

**Orphan (0 ссылок) — кандидаты:**
- `REVIEW_TEMPLATE.md` — сам указывает, что канон отчёта — `CODE_REVIEW_REPORT_TEMPLATE.md`; позиционируется как lightweight PR-review. **Merge** в `CODE_REVIEW_REPORT_TEMPLATE.md` как раздел «Облегчённый PR/comment review» (уникальное: компактный формат + journal-closure напоминание) **или** keep + wire ссылку из CODE_REVIEW_WORKFLOW. Рекомендация: merge.
- `AGENT_REPORT_TEMPLATE.md` — generic отчёт агента (Summary/Changed files/Checks/Risks/Open questions/Next step). Пересекается с journal RESULT-template и с «final report» в task-templates. **Keep + wire** ссылку из ROLE_MODEL/WORKFLOW (это полезный универсальный отчёт для не-PR работ), либо merge в WORKFLOW. Бездомного нет.
- `DECISION_TEMPLATE.md` — формат записи для `DECISION_LOG.md`. **Keep + wire** ссылку из `DECISION_LOG.md`/`WORKFLOW.md`. Не дублирует — дополняет.
- `AGENT_RESEARCH_TASK_TEMPLATE.md` и `DEVELOPMENT_TASK_TEMPLATE.md` — оба = mandatory header + Verified Baseline + Copy/Paste Completeness + Project constitution check; различаются хвостом (Hypothesis/Files/Expected output vs Steps/Goal). Сильно дублируют друг друга и `CODE_REVIEW_TASK_TEMPLATE`. **Развилка Р4:** либо объединить в один `ENGINE_TASK_TEMPLATE.md` с вариативным хвостом, либо оставить два, вынеся общий header-блок в канон (`CHATGPT_RESPONSE_STANDARD.md` уже его описывает) и сослаться. Рекомендация: объединить в один с двумя профилями (development/research).
- `NEW_PROJECT_BOOTSTRAP_PROMPT.md` — chat-prompt нового проекта; пересекается с `NEW_PROJECT_ONBOARDING_GUIDE` и `PROJECT_CHAT_START_PROMPT_TEMPLATE`. **Merge** в единый new-project prompt (см. ниже) либо wire.

**Слабо ссылаемые (1):** `NEW_PROJECT_CHECKLIST.md`, `PROJECT_CHAT_START_PROMPT_TEMPLATE.md` — проверить, не дублируют ли `NEW_PROJECT_BOOTSTRAP_PROMPT`/onboarding; кандидаты на консолидацию new-project prompt-слоя (развилка Р5).

**Adoption prompt пара:** `SHORT_TARGET_ADOPTION_PROMPT.md` (5) + `TARGET_REPOSITORY_ADOPTION_CHAT_PROMPT.md` (14) → один `ADOPTION_PROMPT.md` (раздел 3/4).

**Хорошо используемые — keep:** PROJECT_CONSTITUTION_TEMPLATE (14), TARGET_PROJECT_GOVERNANCE_PACK_TEMPLATE (12), ADOPTION_AUDIT_TASK_TEMPLATE (9), DOCS_ONLY_ADOPTION_TASK_TEMPLATE (9), CHATGPT_RESPONSE_TEMPLATE (8), BACKLOG/ENGINE_REGISTRY/PROJECT_DASHBOARD/PROJECT_GUARDRAILS/ROADMAP (7), CODE_REVIEW_TASK_TEMPLATE (6), TARGET_REPOSITORY_BOOTSTRAP_TASK_TEMPLATE (4), CODE_REVIEW_REPORT_TEMPLATE (3), NEW_PROJECT_HANDOFF/NEW_REPOSITORY_STRUCTURE/PROJECT_PROFILE (2).

Итог по templates: **keep ~17**, **merge ~6** (REVIEW_TEMPLATE, AGENT_RESEARCH+DEVELOPMENT→1, NEW_PROJECT_BOOTSTRAP_PROMPT, SHORT_TARGET_ADOPTION_PROMPT+TARGET_REPOSITORY_ADOPTION_CHAT_PROMPT→1, опц. NEW_PROJECT_CHECKLIST/PROJECT_CHAT_START_PROMPT), **wire (оставить, добавить ссылку) ~3** (AGENT_REPORT_TEMPLATE, DECISION_TEMPLATE, при решении keep — REVIEW_TEMPLATE). Чистого delete без слияния не предлагается.

## 8. Перекрёстные ссылки и манифест (что обновить, чтобы не было broken refs)

Файлы, ссылающиеся на кандидатов (по `git grep`):

- `TARGET_REPOSITORY_ADOPTION_GUIDE` ← README, ADOPTION_TRANSFER_MANIFEST.yml, ENGINE_ENTRYPOINT, STAGE_2_COMPLETION_CHECKLIST, source index, SHORT_TARGET_ADOPTION_PROMPT (+ исторические agents/docs-maintainer-01/*).
- `NEW_PROJECT_ONBOARDING_GUIDE` ← README, ADOPTION_TRANSFER_MANIFEST.yml, STAGE_2_COMPLETION_CHECKLIST.
- `PROJECT_LIFECYCLE` ← README, ADOPTION_TRANSFER_MANIFEST.yml, DECISION_LOG, STAGE_2_COMPLETION_CHECKLIST.
- `DOWNSTREAM_ADAPTATION_CHECKLIST` ← README, ADOPTION_GUIDE, ADOPTION_TRANSFER_MANIFEST.yml, DECISION_LOG, ENGINE_ENTRYPOINT, RELEASE_READINESS, STAGE_2_COMPLETION_CHECKLIST, source index, DOCS_ONLY_ADOPTION_TASK_TEMPLATE, SHORT_TARGET_ADOPTION_PROMPT, TARGET_REPOSITORY_BOOTSTRAP_TASK_TEMPLATE.
- `SHORT_TARGET_ADOPTION_PROMPT` ← README, STAGE_2_COMPLETION_CHECKLIST, TARGET_REPOSITORY_ADOPTION_GUIDE, source index.
- 6 orphan templates ← ноль ссылок (broken-ref риск при удалении = нулевой).

Обязательно обновить при execution:
1. `README.md` — список ссылок на consolidated файлы.
2. `docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml` — в `categories.generic.files` / `requires_target_adaptation` убрать удалённые/слитые пути, добавить новые (`ADOPTION_PROMPT.md`), иначе рассинхрон transfer-манифеста.
3. `docs/agent-system/ENGINE_ENTRYPOINT.md` — списки «найди в template repository».
4. `docs/agent-system/STAGE_2_COMPLETION_CHECKLIST.md`, `RELEASE_READINESS.md`, `DECISION_LOG.md` (последний — только если ссылка структурная; исторические записи не переписывать произвольно).
5. `docs/agent-system/source/SOURCE_agent_system_index.md` — уже навигационный; проверить, что ссылки указывают на canon.
6. Исторические `agents/docs-maintainer-01/*` и DECISION_LOG прошлые записи — **не переписывать** (append-only история); broken-ссылка в историческом отчёте допустима как исторический факт.
7. `ADOPTION_PROMPT.md` (или сохранённое имя `TARGET_REPOSITORY_ADOPTION_CHAT_PROMPT.md`) — если файл переименовывается, оставить redirect-заглушку для внешних bookmark (внешние чаты ссылаются на путь).

## 9. Риски и развилки для архитектора

- **Р1.** PROJECT_LIFECYCLE vs NEW_PROJECT_ONBOARDING_GUIDE: сохранять «концептуальный обзор» отдельной секцией или свернуть полностью? (рекомендация: вводная секция внутри onboarding).
- **Р2.** DOWNSTREAM_ADAPTATION_CHECKLIST: оставить отдельным чеклистом (рекомендация) или сделать приложением ADOPTION_GUIDE? Чеклист как pre-merge gate ценен отдельным файлом.
- **Р3.** Каноническая формулировка «developer / develop / main-only flow» при merge двух guide — выбрать один источник правды (рекомендация: ADOPTION_GUIDE).
- **Р4.** Объединять ли DEVELOPMENT + RESEARCH task templates в один параметризованный или оставить два с общим header-ссылкой.
- **Р5.** New-project prompt-слой (NEW_PROJECT_BOOTSTRAP_PROMPT + PROJECT_CHAT_START_PROMPT_TEMPLATE + NEW_PROJECT_CHECKLIST) — глубина консолидации.
- **Риск брендинга путей:** `TARGET_REPOSITORY_ADOPTION_CHAT_PROMPT.md` копируется/цитируется во внешних чатах; переименование требует redirect-заглушки.
- **Риск transfer-манифеста:** любое delete/merge без синхронной правки `ADOPTION_TRANSFER_MANIFEST.yml` ломает adoption flow downstream.
- **Риск over-consolidation:** не сливать policy-документы (LANGUAGE_POLICY, SECURITY_POLICY, PUBLICATION_POLICY, GITHUB_TOKEN_POLICY) — они каноничны и точечно ссылаемы; вне scope этой консолидации.
- **Риск append-only:** исторические agent-reports/DECISION_LOG не переписывать; broken-refs в истории допустимы.

## 10. Предлагаемая разбивка на execution (несколько PR)

Каждый PR — отдельная docs-задача через `work/<role>/<task>` → `developer`, с journal TASK/RESULT/INDEX.

- **PR-C1 (reading-list, низкий риск):** зафиксировать Core(10)+Reference в `README.md`; синхронизировать `source/SOURCE_agent_system_index.md`. Allowed: README.md, source/SOURCE_agent_system_index.md, journal. Delete/merge: нет.
- **PR-C2 (methodology_reference + source_snapshot канонизация, низкий риск):** оставить спеку в ENGINE_ENTRYPOINT и source/README; в ADOPTION_GUIDE/TARGET_REPO_GUIDE заменить на ссылки; комментарий в манифесте. Allowed: ENGINE_ENTRYPOINT.md, ADOPTION_GUIDE.md, TARGET_REPOSITORY_ADOPTION_GUIDE.md, ADOPTION_TRANSFER_MANIFEST.yml, source/README.md, journal. Delete: нет.
- **PR-C3 (adoption prompt merge, средний риск):** свести SHORT_TARGET_ADOPTION_PROMPT + TARGET_REPOSITORY_ADOPTION_CHAT_PROMPT → один canon (+redirect-заглушка); обновить refs (README, ENGINE_ENTRYPOINT, source index, manifest). Allowed: два prompt-файла, README.md, ENGINE_ENTRYPOINT.md, ADOPTION_TRANSFER_MANIFEST.yml, source index, journal. Merge: 2→1.
- **PR-C4 (adoption guides merge, высокий риск):** ADOPTION_GUIDE ← TARGET_REPOSITORY_ADOPTION_GUIDE; NEW_PROJECT_ONBOARDING_GUIDE ← PROJECT_LIFECYCLE; dedupe DOWNSTREAM_ADAPTATION_CHECKLIST. Обновить все refs + manifest. Требует решения по Р1/Р2/Р3. Allowed: пять adoption-файлов, README.md, ENGINE_ENTRYPOINT.md, ADOPTION_TRANSFER_MANIFEST.yml, STAGE_2/ RELEASE_READINESS (если структурные ссылки), source index, journal. Merge: PROJECT_LIFECYCLE→onboarding, TARGET_REPO_GUIDE→ADOPTION_GUIDE.
- **PR-C5 (templates cleanup, средний риск):** REVIEW_TEMPLATE→CODE_REVIEW_REPORT_TEMPLATE; DEVELOPMENT+RESEARCH→1 (по Р4); NEW_PROJECT_BOOTSTRAP_PROMPT консолидация (по Р5); wire AGENT_REPORT_TEMPLATE/DECISION_TEMPLATE. Обновить manifest (`requires_target_adaptation` шаблоны). Allowed: затронутые templates, README.md, WORKFLOW.md/ROLE_MODEL.md/DECISION_LOG.md (для wire-ссылок), ADOPTION_TRANSFER_MANIFEST.yml, journal.
- **PR-C6 (review journaling default, средний риск, см. раздел 11):** изменить дефолт review.

Порядок: C1→C2→C3→C5→C4→C6 (C4 последним из крупных, т.к. самый широкий по refs). Каждый PR независимо ревьюится и мержится.

## 11. Фикс дефолта «review-only = chat-only» → «review всегда журналирует TASK+RESULT»

Сейчас (`CODE_REVIEW_TASK_TEMPLATE.md`, `CODE_REVIEW_WORKFLOW.md`): при `Report persistence = chat-only by default` review **не создаёт** repository files и PR, т.е. TASK/RESULT в journal **не пишутся**. Это противоречит принципу воспроизводимости (вся цепочка REVIEW-INITIAL-01 → METH-CONSISTENCY-01 → closure журналировалась только потому, что задачи были file-changing).

Предлагаемое изменение для PR-C6:
- ввести правило: **любой review журналирует TASK+RESULT** (input/output + INDEX), даже когда сам отчёт возвращается в чат; «chat-only» относится к **телу отчёта**, а не к отсутствию journal-следа;
- развести два понятия: `report delivery` (chat | repository) и `journal trace` (always);
- обновить `CODE_REVIEW_WORKFLOW.md`, `CODE_REVIEW_TASK_TEMPLATE.md`, при необходимости `ENGINE_JOURNAL_CONTRACT.md` (раздел review) и `OPERATIONAL_FAST_LANE.md` (review ≠ fast-lane status-check).

**Важно (развилка/одобрение):** это **изменение поведения** review-контракта, а не чистая консолидация. Требует явного решения пользователя/архитектора (граница scope expansion) и идёт отдельным PR-C6. Здесь только зафиксировано как обязательный пункт плана.

---

## Измененные файлы (этой задачей)

- `docs/agent-system/engine-journal/input/TASK-0004-METH-CONSOLIDATION-PLAN-01-consolidation-plan.md`
- `docs/agent-system/engine-journal/output/RESULT-0004-METH-CONSOLIDATION-PLAN-01-consolidation-plan.md`
- `docs/agent-system/engine-journal/INDEX.md`

Содержимое методологии вне журнала НЕ изменено.

## Выполненные проверки

- Preflight: `git remote -v`, `git status`, `git fetch --all --prune`, `git switch developer`, `git pull --ff-only`, `git rev-parse developer/origin/developer`.
- Инвентаризация: `git ls-files` по docs/templates; подсчёт ссылок на каждый template; cross-ref map по кандидатам.
- `git grep -n "methodology_reference:"`, `reference_type: commit`, `source_snapshot:` — карта дублей.
- Чтение adoption-слоя и orphan-templates для content-preservation.

## Невыполненные проверки и причина

- Правки контента методологии — запрещены scope (plan-only).
- Markdown/YAML lint — documented lint command отсутствует.
- `gh` PR creation — см. ниже (gh недоступен).

## Результат проверки запрещенных файлов

Файлы вне whitelist не изменялись. `.env` не читался. Untracked артефакт пользователя не трогался.

## Результат проверки sensitive/private markers

Секреты не встречались и не печатались. Private downstream data не вводились.

## Результат language policy

RESULT Russian-first; English только для paths, filenames, identifiers, команд и literal terms.

## Принятые решения

- Предложение #2 скорректировано: сохранить ось new-vs-existing двумя канонами вместо одного ADOPTION_GUIDE.
- Канон methodology_reference = ENGINE_ENTRYPOINT.md; машинная схема в манифесте остаётся.
- Чистых delete не предлагается — только merge/wire с сохранением контента.
- Изменение review-default вынесено отдельным PR-C6 как behavior change, требующий одобрения.

## Риски

- Высокий ref-fan-out у adoption-guides (PR-C4) — риск broken refs; митигируется синхронной правкой README/ENGINE_ENTRYPOINT/manifest.
- Переименование canonical adoption prompt — риск внешних bookmark; митигируется redirect-заглушкой.

## Blockers

Нет.

## Закрытие после merge

Work PR status: PR создаёт пользователь (`gh` недоступен) — closure после merge отдельной задачей по `ENGINE_JOURNAL_CONTRACT.md`.

Release/sync: не применимо (journal-only PR в `developer`).

RESULT closed after merge: not applicable before merge.

INDEX closed after merge: not applicable before merge.

## Следующий рекомендуемый шаг

Пользователь создаёт PR `work/qa-reviewer-01/consolidation-plan` → `developer`. После merge — закрыть journal 0004 (closure-only) и принять решения по развилкам Р1–Р5 + PR-C6, затем запускать execution PR-C1…C6 как отдельные docs-задачи.

## Methodology feedback

Plan-only задачи с обязательным журналированием стоит сделать стандартным режимом review (см. раздел 11): journal trace всегда, доставка отчёта — отдельный параметр.
