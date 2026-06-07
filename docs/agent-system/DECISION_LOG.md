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
