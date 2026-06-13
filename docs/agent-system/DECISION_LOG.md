# DECISION_LOG

## 2026-06-06 - GitHub as source of truth

Решение:
GitHub является основным источником правды для проекта "Создание агентской системы".

Причина:
Нужно хранить файлы, историю, ветки, PR, отчеты и состояние проекта в одном проверяемом месте.

## 2026-06-06 - Source as navigation index

Решение:
Source используется не как полное хранилище всех файлов, а как индекс и краткий слепок состояния.

Причина:
Количество файлов будет расти, их удобнее хранить и версионировать в GitHub.

## 2026-06-06 - Vendor-neutral agent names

Решение:
Не использовать в названиях агентов Codex, Claude, Gemini, Copilot и другие vendor/tool names.

Причина:
Инструменты-исполнители могут меняться, а роль агента должна оставаться стабильной.

Принято:

- использовать role-based имена агентов;
- engine указывать отдельно;
- стартовые агенты:
  - `dev-implementer-01`;
  - `solution-architect-01`;
  - `qa-reviewer-01`;
  - `security-reviewer-01`;
  - `docs-maintainer-01`.

## 2026-06-13 - Vendor-neutral code review workflow

Решение:
Ввести review-only workflow для code reviewers. Reviewer roles не используют vendor/tool names, не исправляют код по умолчанию и создают report PR в `work/<role>/*`.

Причина:
Внешние engines могут предлагать review prompts с vendor-specific branches и прямой работой от `main`. Это нарушает branch policy и role model.

Последствия:
Code review отделяется от implementation. Findings превращаются в отдельные PR только после решения пользователя.

## 2026-06-13 - Fast Lane write boundary and Russian-first Engine blocks

Решение:
ChatGPT обязан перейти из Operational Fast Lane в полный self-contained Engine-блок, если review/status answer превращается в write-action recommendation.

ChatGPT обязан применять Russian-first policy не только к final reports и journal files, но и к самим Engine-блокам.

Причина:
Это предотвращает hybrid shortcuts, неполные Engine prompts и нарушение методологии еще до запуска Engine.

Последствия:
Fast Lane остается read-only/status/cleanup-only. File-changing follow-ups требуют полного scope. Engine-блоки должны иметь русские пользовательские заголовки.

Privacy:
Downstream-specific details не фиксируются.

## 2026-06-06 - Bootstrap merged to main

Решение:
Bootstrap-каркас проекта `agent-system-development` перенесен в `main` через PR #1.

Причина:
Нужна стабильная базовая версия репозитория, от которой дальше будут стартовать `developer` и рабочие ветки.

Последствия:

- `main` считается стабильной веткой;
- `developer` становится интеграционной веткой;
- прямые изменения в `developer` после bootstrap запрещены без отдельного разрешения пользователя;
- все новые задачи должны выполняться через `work/<role>/*`.

## 2026-06-06 - Work branch workflow after bootstrap

Решение:
После bootstrap все изменения выполняются через рабочие ветки `work/<agent-role>/*`.

Причина:
Нужно закрепить правило "одна задача = одна ветка = один PR" и не загрязнять `developer` прямыми изменениями.

## 2026-06-06 - agent-system-development made public

Решение:
Репозиторий `agent-system-development` переведен в public.

Причина:
Репозиторий содержит методологию, шаблоны, workflow и документацию агентской разработки без секретов и клиентских данных.

Последствия:

- GitHub rulesets можно использовать в public repository на GitHub Free;
- весь контент репозитория считается публичным;
- запрещено добавлять секреты, `.env`, клиентские данные и рабочие данные.

## 2026-06-06 - Active rulesets for main and developer

Решение:
Rulesets `Protect main` и `Protect developer` включены в Active по ручной проверке пользователя в GitHub UI.

Причина:
Нужно защитить стабильную и интеграционную ветки от прямых изменений и закрепить workflow через PR.

Последствия:

- задачи должны идти через `work/<role>/*`;
- `developer` принимает изменения через PR;
- `main` принимает изменения через PR из `developer`.

## 2026-06-06 - No external project names in public methodology repository

Решение:
В публичном методологическом репозитории запрещено упоминать конкретные внешние проекты, клиентские проекты, приватные репозитории и внутренние кодовые имена.

Причина:
Репозиторий является публичным шаблоном и не должен раскрывать связь с конкретными приватными внедрениями.

Последствия:

- использовать только нейтральные термины;
- downstream/private проекты описывать обобщенно;
- перед merge проверять отсутствие конкретных внешних названий.

## 2026-06-06 - Local worktree workflow

Решение:
Для выполнения задач агентов используется локальная схема Git worktree.

Причина:
Worktree позволяет держать стабильную/интеграционную ветку отдельно от рабочих веток агентов и снижает риск случайных изменений не в той ветке.

Последствия:

- engine-исполнитель должен запускаться из worktree-папки соответствующей роли;
- перед запуском всегда проверяется текущая ветка;
- рабочие ветки имеют формат `work/<role>/<task>`;
- основная папка репозитория не используется как место выполнения задач агентов.

## 2026-06-06 - CI forbidden tracked files check

Решение:
Добавить GitHub Actions CI-проверку для запрещенных tracked files.

Причина:
Публичный методологический репозиторий не должен принимать `.env`, рабочие директории, временные файлы, логи и другие запрещенные tracked paths.

Последствия:

- pull request должен проходить CI forbidden files check;
- CI проверяет tracked paths, но не заменяет review;
- `.env.example` разрешен только без реальных секретов;
- более сложные проверки секретов выносятся в отдельные будущие задачи.

## 2026-06-07 - Reusable new project bootstrap doctrine

Решение:
`agent-system-development` должен быть не только текущим проектом, но и универсальной доктриной для запуска новых проектов через GitHub, роли, worktree, отчеты агентов и ручной запуск engine-исполнителей.

Причина:
Нужен повторяемый безопасный процесс, который помогает пользователю начинать новый проект с project profile, branch policy, role/worktree setup, первых PR, отчетов и handoff без переноса приватных данных в public repository.

Последствия:

- lifecycle запуска нового проекта фиксируется в `PROJECT_LIFECYCLE.md`;
- reusable templates хранятся в `docs/agent-system/templates/`;
- GitHub остается source of truth для файлов, веток, PR, отчетов и решений;
- чат помогает формулировать задачи и проверять отчеты, но не заменяет GitHub;
- пользователь принимает финальные решения;
- engine-исполнители запускаются пользователем вручную.

## 2026-06-07 - New project onboarding guide

Решение:
Добавить practical onboarding guide, который объясняет, как применять lifecycle и templates для запуска нового проекта.

Причина:
После фиксации lifecycle и templates нужен человекочитаемый пошаговый документ, чтобы пользователь мог запускать новый проект без догадок и без переноса приватных данных в public repository.

Последствия:

- onboarding guide становится входной точкой после README;
- templates остаются reusable artifacts;
- handoff/checklist/project profile используются как части одного процесса.

## 2026-06-07 - GitHub Actions Node.js 24 compatibility

Решение:
Обновить `actions/checkout` в forbidden files workflow с `v4` на `v5`.

Причина:
GitHub Actions показывает warning о deprecated Node.js 20 actions. Проверка upstream metadata `actions/checkout@v5` подтвердила `using: node24`.

Последствия:

- forbidden files workflow использует checkout action с Node.js 24 runtime;
- Node.js 20 deprecation warning для `actions/checkout@v4` должен исчезнуть;
- при будущих runtime warnings нужно проверять upstream action metadata перед обновлением workflow.

## 2026-06-07 - Target repository adoption readiness

Решение:
Добавить target repository adoption guide, stage completion checklist и target repository bootstrap task template.

Причина:
После lifecycle, onboarding guide и CI runtime compatibility нужен финальный пакет, который позволяет безопасно применить методологию к отдельному target implementation repository без переноса приватных данных в public methodology repository.

Последствия:

- target repository adoption guide становится bridge-документом между public methodology repository и target implementation repository;
- stage completion checklist фиксирует готовность этапа;
- target bootstrap task template становится основой первого dry run;
- после PR-2d можно начинать первый target repository dry run.

## 2026-06-07 - Engine entrypoint and repository self-discovery contract

Решение:
Встроить repository self-discovery и short prompt adoption mode в methodology repository.

Причина:
Пользователь не должен каждый раз вставлять длинный universal prompt. `engine` должен сам читать template repository и локальные инструкции target repository.

Последствия:

- agent-system-development становится полноценным template repository;
- короткий prompt становится достаточным для старта;
- `engine` обязан начинать с self-discovery;
- первый target repository action должен быть adoption audit;
- риск работы в неправильном repository снижается.

## 2026-06-07 - Target repository methodology feedback loop

Решение:
Добавить feedback loop из target repository dry run обратно в methodology repository.

Причина:
При реальном применении methodology repository могут обнаруживаться отсутствующие шаблоны, неудобные ручные шаги, safety gaps и возможности автоматизации. Эти наблюдения должны превращаться в отдельные безопасные PR в `agent-system-development`.

Последствия:

- final report target repository должен содержать `Methodology feedback`;
- feedback не должен раскрывать private data;
- улучшения methodology repository выполняются отдельными PR;
- target repository dry run становится источником безопасного улучшения методологии.

## 2026-06-07 - Adoption modes and transfer manifest

Решение:
Разделить применение methodology repository к target repository на режимы `audit-only`, `docs-only adoption` и `runtime adoption`, а также добавить machine-readable manifest переносимых файлов.

Причина:
Первый target repository dry run показал, что короткий adoption prompt должен безопасно приводить к минимальному audit, а не к неявному копированию template repository state. Нужны явные правила для файлов, которые можно переносить как generic, которые требуют target adaptation и которые отражают состояние methodology repository.

Последствия:

- первый безопасный результат adoption - только `docs/agent-system/ADOPTION_AUDIT.md`;
- `CURRENT_STATE.md`, `NEXT_STEPS.md` и `DECISION_LOG.md` нельзя копировать verbatim;
- branch model, worktree paths, current state, visibility и CI branch filters адаптируются под target repository;
- runtime adoption отделяется от документационного bootstrap и требует отдельного архитектурного решения;
- `ADOPTION_TRANSFER_MANIFEST.yml` становится машинной подсказкой для безопасного переноса документов;
- `DOWNSTREAM_ADAPTATION_CHECKLIST.md` становится review checklist для target adaptation.

## 2026-06-07 - Adoption task templates

Решение:
Добавить reusable task templates для audit-only и docs-only adoption.

Причина:
После adoption modes и transfer manifest нужен короткий путь от adoption mode к конкретной задаче engine без длинного ручного prompt.

Последствия:

- audit-only и docs-only adoption получают отдельные task templates;
- engine может выбирать template по adoption mode;
- target repository adoption становится более повторяемым;
- docs-only adoption не смешивается с runtime adoption.

## 2026-06-09 - Repository role and engine task header

Решение:
Явно закрепить, что `agent-system-development` является reusable methodology/template repository, а не центральным репозиторием управления downstream-проектами.

Также закрепить обязательную русскоязычную шапку задач для `engine`: `Задача для <agent-name>: <task-id>` и блок рекомендуемого режима запуска, модели, reasoning, режима работы и причины выбора режима.

Причина:
Методология будет переиспользоваться в target repositories. Нужно предотвратить перенос project-specific state, отчетов, секретов и рабочих веток обратно в public methodology repository, а также сделать задачи для engine сопоставимыми с GitHub issue, Pull Request, task id или внутренним номером работы проекта.

Последствия:

- после adoption рабочие ветки, worktree, отчеты и Pull Request ведутся в target repository;
- универсальные улучшения возвращаются в `agent-system-development` только отдельными methodology PR;
- task templates требуют role-based `<agent-name>`, а не vendor/tool name;
- `<task-id>` связывает задачу, ветку, отчет и Pull Request.

## 2026-06-09 - Target project governance pack

Решение:
Target repositories должны получать governance pack, который фиксирует цель, roadmap, backlog, current state, next steps, decisions, guardrails и engine registry.

Причина:
После adoption target repository должен иметь не только роли, ветки и task templates, но и управляемый контур состояния проекта. Это снижает риск scope drift, несопоставимых задач, устаревших state docs и смешивания methodology repository state с downstream project-specific state.

Последствия:

- `agent-system-development` хранит reusable governance templates и adoption rules;
- project-specific governance state создается и обновляется только в target repository;
- docs-only adoption может включать governance pack без runtime code, Docker, CI или production data;
- после значимых PR target repository обновляет минимум `CURRENT_STATE.md` и при необходимости `NEXT_STEPS.md`, `ROADMAP.md`, `BACKLOG.md`, `DECISION_LOG.md`;
- `ENGINE_REGISTRY.md` отделяет stable agent roles от replaceable engines.

## 2026-06-10 - Project Constitution Framework

Решение:
Добавить Project Constitution Framework как reusable методологический слой для target repositories.

Причина:
Target repository должен до implementation PR фиксировать mission, success criteria, out-of-scope, architectural principles, active strategic goal, agent authority, decision authority и scope expansion control. Это снижает риск scope drift и неявного расширения проекта без решения пользователя.

Последствия:

- target repository получает `PROJECT_CONSTITUTION.md` или явно фиксирует reason, почему constitution отложен;
- `PROJECT_CONSTITUTION.md` является target-specific file и не копируется verbatim из methodology repository;
- Agent Authority Matrix фиксирует allowed scope, forbidden scope и approval conditions для ролей;
- Level 3+ decisions требуют explicit user approval;
- major scope expansion является stop condition.

## 2026-06-10 - Reusable target adoption chat prompt

Решение:
Добавить canonical copy/paste prompt для запуска adoption в target repository из нового project chat.

Причина:
Пользователю нужен версионируемый prompt в methodology repository, чтобы не создавать длинную инструкцию заново в каждом чате. Первый шаг adoption должен оставаться audit-only и не должен превращаться в full docs-only adoption без review.

Последствия:

- canonical prompt хранится в `docs/agent-system/templates/TARGET_REPOSITORY_ADOPTION_CHAT_PROMPT.md`;
- README, adoption guide, engine entrypoint и short prompt ссылаются на новый prompt;
- ChatGPT в target project chat готовит задачу для engine, но не меняет файлы сам;
- первая задача engine создает только `docs/agent-system/ADOPTION_AUDIT.md`;
- full docs-only adoption и governance pack применяются отдельным PR после audit.

## 2026-06-10 - Unified ChatGPT response, methodology freshness and commenting standard

Решение:
`agent-system-development` закрепляет единый формат ответов ChatGPT: одна engine-задача выводится одним самодостаточным copy/paste-блоком; ручные terminal-действия разделяются по независимым задачам; перед формированием и выполнением engine-задач проверяется актуальный methodology repository; target governance docs проходят language consistency audit; создаваемые и изменяемые скрипты/технические файлы получают русские комментарии для нужных строк и блоков.

Причина:
Пользователь должен иметь возможность скопировать весь prompt для engine одним нажатием и вставить его в engine без ручного сбора команд, ограничений и проверок из разных частей ответа. Методология должна применяться только из актуального `agent-system-development`, а файлы должны оставаться понятными русскоязычной команде.

Последствия:

- появляется `CHATGPT_RESPONSE_STANDARD.md`;
- появляется `CHATGPT_RESPONSE_TEMPLATE.md`;
- появляется `FILE_COMMENTING_STANDARD.md`;
- adoption prompts требуют standardized ChatGPT response;
- engine block становится самодостаточным;
- audit-only tasks проверяют language consistency;
- docs-only adoption может включать нормализацию языка governance docs;
- в target scripts/workflows/templates добавляются русские комментарии для нужных строк;
- methodology repository freshness check становится обязательным;
- methodology feedback оформляется отдельным нейтральным блоком, если нужна доработка `agent-system-development`;
- public methodology repository не раскрывает private downstream data.

## 2026-06-11 - PR-2m merged and methodology release readiness

Решение:
После merge PR-2m в `developer` считать unified ChatGPT response standard, `FILE_COMMENTING_STANDARD`, methodology freshness check и language consistency rule принятыми как актуальная методология для следующих target repository adoption chats.

Причина:
PR-2m добавил reusable response standard и template, а также закрепил self-contained Engine-блоки, разделение manual terminal tasks, обязательную синхронизацию methodology repository и нейтральный methodology feedback без private downstream data.

Последствия:

- `developer` содержит актуальную версию unified response standard;
- state docs обновляются отдельным PR-2n перед release readiness review;
- release `developer` -> `main` выполняется только после решения пользователя;
- новые target repository adoption chats должны использовать текущие response/template rules после release или явной проверки актуального `developer`.

## 2026-06-11 - Release readiness review before main release

Решение:
Перед созданием release PR `developer` -> `main` фиксировать отдельный release readiness review в `docs/agent-system/RELEASE_READINESS.md`.

Причина:
После PR-2m и PR-2n нужно проверить pre-PR-2o snapshot, forbidden paths, sensitive/private markers, актуальность state docs и readiness checklist без неявного выполнения release. Финальный release candidate должен быть пересобран после merge PR-2o в `developer`.

Последствия:

- PR-2o документирует pre-release snapshot для `developer` -> `main`;
- перед release PR требуется post-PR-2o refresh с актуальным `origin/developer`;
- release PR в `main` не создается без явного решения пользователя;
- следующий шаг после merge PR-2o - release PR или target adoption dry run по решению пользователя;
- public methodology repository framing сохраняется без private downstream data.

## 2026-06-11 - Repository context safety after methodology sync

Решение:
Engine-facing templates должны явно разделять синхронизацию methodology repository и работу в target repository.

Причина:
Если после `cd <METHODOLOGY_REPOSITORY_LOCAL_PATH>` engine не возвращается в target repository, проверки remote, branch, working tree и последующие изменения могут быть выполнены в `agent-system-development`, а не в target repository. Кроме того, `git pull --ff-only` сам по себе не подтверждает, что локальная methodology branch равна remote source of truth, если локально есть незапушенные commits.

Последствия:

- после `git pull --ff-only origin <METHODOLOGY_BASE_BRANCH>` engine проверяет `HEAD == origin/<METHODOLOGY_BASE_BRANCH>`;
- если local HEAD отличается от remote branch, engine пишет `STOP`;
- после синхронизации methodology repository engine обязан выполнить `cd <TARGET_REPOSITORY_LOCAL_PATH>` перед target checks или target changes;
- release PR #49 должен быть re-checked после merge PR-2q в `developer`.

## 2026-06-11 - Engine journal contract

Решение:
Ввести воспроизводимый engine journal в `docs/agent-system/engine-journal/` для задач `engine` и ответов `engine`.

Причина:
GitHub хранит историю commits и Pull Requests, но для восстановления проекта также нужна явная связь между входной задачей, ответом `engine`, веткой, PR, commit/result и следующим шагом. Без task/result artifacts сложно понять, какая задача породила какой результат.

Последствия:

- появляется `ENGINE_JOURNAL_CONTRACT.md`;
- появляется структура `docs/agent-system/engine-journal/input/`, `output/`, `templates/`;
- task/result files именуются в формате `TASK-0001-<task-id>-<slug>.md` и `RESULT-0001-<task-id>-<slug>.md`;
- task/result files являются append-only и не удаляются/не перезаписываются без решения пользователя;
- target repository adoption должен создавать собственный engine journal в target repository;
- private data, secrets, credentials и private repository URLs запрещены в journal.

## 2026-06-12 - Post-merge Journal Closure

Решение:
Закрепить обязательное правило Post-merge Journal Closure для target repository journal: после merge рабочего PR, release PR или sync PR `RESULT` и `INDEX` не должны оставаться в pre-merge статусах.

Причина:
Post-PR finalization закрывает journal после создания PR, но без отдельного post-merge правила target repositories могут сохранить `RESULT` или `INDEX` в статусах `PR open`, `ready for review`, `draft open`, `pending at file materialization` или `see Engine final report` уже после фактического merge.

Последствия:

- `ENGINE_JOURNAL_CONTRACT.md` требует фиксировать PR status `merged`, merge commit SHA и `merged_at`, если доступно;
- release PR и sync PR фиксируются в journal, если такие шаги выполнялись;
- Operational Fast Lane включает проверку journal closure после merge/release/sync;
- Task File Handoff и target adoption templates требуют post-merge closure fields;
- reviewer должен считать stale merged journal entry blocker;
- methodology repository по-прежнему не хранит real TASK/RESULT operational history target repositories.

## 2026-06-13 - Engine handoff baseline completeness

Решение:
Закрепить, что Recommended Engine Mode, Verified execution baseline и другой обязательный execution context должны находиться внутри Engine-блока или TASK file.

Причина:
Нужно предотвратить split-context Engine handoffs, когда часть GitHub/local baseline, branch state, PR state, release/sync state или safety assumptions остается только в обычном тексте перед Engine-блоком.

Последствия:

- ChatGPT перед отправкой Engine-блока проверяет copy/paste completeness;
- TASK file фиксирует recommended engine mode, verified baseline и assertion, что bootstrap prompt не содержит уникальных execution data;
- `engine` должен написать `STOP`, если bootstrap prompt и TASK file конфликтуют;
- impact: docs-only;
- runtime impact: none;
- downstream-specific data: none.

## 2026-06-13 - New repository bootstrap branch gate

Решение:
Для нового пустого target repository с выбранным `standard developer workflow` ветка `developer` обязательна до первой рабочей ветки. `Fallback-to-main` для рабочих PR запрещен.

Причина:
Реальный bootstrap target repository показал, что разрешение рабочей ветке использовать `main` как base branch при отсутствии `developer` может остановить downstream workflow.

Последствия:

- методология разделяет `new empty repository bootstrap` и `existing repository adoption`;
- отсутствие `developer` в стандартной схеме является bootstrap blocker или explicit bootstrap creation step;
- existing repository adoption продолжает поддерживать осознанный `main-only flow`, если это фактическая модель target repository или отдельное решение пользователя;
- runtime impact: none;
- downstream-specific data: none.
