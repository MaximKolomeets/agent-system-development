# RESULT-0008-METH-CONSOLIDATION-C3-adoption-prompt-merge

Файл результата: `docs/agent-system/engine-journal/output/RESULT-0008-METH-CONSOLIDATION-C3-adoption-prompt-merge.md`

Связанный TASK file: `docs/agent-system/engine-journal/input/TASK-0008-METH-CONSOLIDATION-C3-adoption-prompt-merge.md`

Идентификатор задачи: `METH-CONSOLIDATION-C3`

Номер sequence: `0008`

Агент: `docs-maintainer-01`

Engine: Claude Code

Timestamp (ISO-8601): `2026-06-14T21:05:00+07:00`

Baseline SHA (developer): `c3c6cac2b51f05104a78bfd47083dd7e4d46ecb2`

Ссылка на источник scope: [RESULT-0004 §10 «PR-C3»](../output/RESULT-0004-METH-CONSOLIDATION-PLAN-01-consolidation-plan.md), §3 «Объединить два adoption-prompt в один», §8 «Перекрёстные ссылки и манифест», §4 «Карта content-preservation».

methodology_reference: см. канон в `docs/agent-system/ENGINE_ENTRYPOINT.md` → раздел «Methodology reference»; данные текущей задачи:

```yaml
methodology_reference:
  repository: MaximKolomeets/agent-system-development
  source_branch: developer
  source_commit: c3c6cac2b51f05104a78bfd47083dd7e4d46ecb2
  checked_at: 2026-06-14T21:05:00+07:00
  reference_type: commit
  notes: "Точка после merge JOURNAL-CLOSE-0007 (PR #114)."
```

## Подтверждённый whitelist (из RESULT-0004 §10)

PR-C3 цитата: «Allowed: два prompt-файла, README.md, ENGINE_ENTRYPOINT.md, ADOPTION_TRANSFER_MANIFEST.yml, source index, journal. Merge: 2→1.»

Whitelist текущей задачи (6 файлов методологии + journal):

- `docs/agent-system/templates/ADOPTION_PROMPT.md` — новый канон;
- `docs/agent-system/templates/SHORT_TARGET_ADOPTION_PROMPT.md` — старый файл, развязка;
- `docs/agent-system/templates/TARGET_REPOSITORY_ADOPTION_CHAT_PROMPT.md` — старый файл, развязка;
- `README.md` — inbound-ссылки;
- `docs/agent-system/ENGINE_ENTRYPOINT.md` — inbound-ссылка;
- `docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml` — путь в `categories.generic.files`;
- `docs/agent-system/source/SOURCE_agent_system_index.md` — проверен, явных упоминаний прежних путей нет (после C1 он навигационный); фактически не правился;
- журнал: `engine-journal/input/TASK-0008-*.md`, `engine-journal/output/RESULT-0008-*.md`, `engine-journal/INDEX.md`.

## Fork-guard

Развилки Р1–Р5 относятся к PR-C4/C5 — **C3 от них не зависит**. §3 авторитетно фиксирует имя канона как `templates/ADOPTION_PROMPT.md` (архитекторское решение из таски); §8 rule 7 явно требует redirect-заглушку для переименованных prompt-файлов из-за внешних bookmark. Fork-guard не сработал.

## Исход развязки (stub для обоих старых файлов)

**Архитектурное правило таски** разрешает delete, если `git grep` показал 0 ссылок на старые пути. Поскольку **inbound-ссылок > 0 в файлах вне whitelist PR-C3 и в append-only истории**, применено правило таски (п.5): **«если хоть одну ссылку нельзя чисто перенаправить → НЕ удалять, оставить redirect-заглушку»**.

Перекрыт stub-дефолт плана (§3 предлагал redirect только для самого ссылаемого файла): **stub применён к обоим файлам**, потому что у обоих есть inbound-ссылки из не-whitelist + append-only истории.

### Какие ссылки помешали delete'у

| Цель | Источник ссылки | В whitelist PR-C3? | Тип |
|---|---|---|---|
| `SHORT_TARGET_ADOPTION_PROMPT.md` | `STAGE_2_COMPLETION_CHECKLIST.md:20` | **нет** | not in whitelist |
| `SHORT_TARGET_ADOPTION_PROMPT.md` | `TARGET_REPOSITORY_ADOPTION_GUIDE.md:32` | **нет** | not in whitelist |
| `SHORT_TARGET_ADOPTION_PROMPT.md` | `agents/docs-maintainer-01/DOC_SYNC_REPORT.md` (3 строки) | — | append-only history (§8 rule 6) |
| `SHORT_TARGET_ADOPTION_PROMPT.md` | `agents/docs-maintainer-01/NEXT_CHAT_PROMPT.md` | — | append-only history |
| `TARGET_REPOSITORY_ADOPTION_CHAT_PROMPT.md` | `ADOPTION_GUIDE.md:106` | **нет** | not in whitelist |
| `TARGET_REPOSITORY_ADOPTION_CHAT_PROMPT.md` | `CURRENT_STATE.md:175` | **нет** | not in whitelist |
| `TARGET_REPOSITORY_ADOPTION_CHAT_PROMPT.md` | `DECISION_LOG.md:404` | — | append-only history (§8 rule 6) |
| `TARGET_REPOSITORY_ADOPTION_CHAT_PROMPT.md` | `NEW_PROJECT_ONBOARDING_GUIDE.md:14` | **нет** | not in whitelist |
| `TARGET_REPOSITORY_ADOPTION_CHAT_PROMPT.md` | `RELEASE_READINESS.md:60` | **нет** | not in whitelist |
| `TARGET_REPOSITORY_ADOPTION_CHAT_PROMPT.md` | `STAGE_2_COMPLETION_CHECKLIST.md:38` | **нет** | not in whitelist |
| `TARGET_REPOSITORY_ADOPTION_CHAT_PROMPT.md` | `TARGET_REPOSITORY_ADOPTION_GUIDE.md:16` | **нет** | not in whitelist |
| `TARGET_REPOSITORY_ADOPTION_CHAT_PROMPT.md` | `agents/docs-maintainer-01/*` | — | append-only history |
| `TARGET_REPOSITORY_ADOPTION_CHAT_PROMPT.md` | journal TASK-0004/RESULT-0004/RESULT-0007 | — | append-only history |

Расширять scope/whitelist для приведения этих ссылок в порядок запрещено таской. Менять append-only истории нарушает §8 rule 6 и `ENGINE_JOURNAL_CONTRACT.md`. Stub гарантирует, что все эти ссылки продолжают работать через 1-hop redirect, и обновятся естественным образом в более широких PR (например, PR-C4 для TARGET_REPOSITORY_ADOPTION_GUIDE и других не-whitelist файлов).

## Карта content-preservation (§4)

Канон `templates/ADOPTION_PROMPT.md` собран из двух источников; уникальное переносится **до** превращения старых файлов в stub.

### Содержание SHORT_TARGET_ADOPTION_PROMPT.md → канон

| Источник | Куда в каноне |
|---|---|
| Раздел «Full copy/paste prompt» (указатель на TARGET_REPOSITORY_ADOPTION_CHAT_PROMPT) | заменён вступительным разделом «Когда какой вариант использовать» канона |
| «Обязательная шапка задачи» (Russian-first + Post-merge Closure + methodology_reference) | раздел «Обязательная шапка задачи» канона |
| «Короткий prompt» (one-liner) | раздел «Короткий prompt» канона |
| «Безопасный короткий prompt» | раздел «Безопасный короткий prompt» канона |
| «Как должен действовать engine» (список template repository файлов + выбор adoption task template) | раздел «Как должен действовать engine» канона |
| «Первый результат» (audit-only + список содержимого audit) | раздел «Первый результат» канона |
| «Ограничения» | раздел «Ограничения» канона |

### Содержание TARGET_REPOSITORY_ADOPTION_CHAT_PROMPT.md → канон

| Источник | Куда в каноне |
|---|---|
| Заголовок и «Назначение» | переформулировано во вступительной части канона |
| «Copy/paste prompt» — полный многострочный prompt | раздел «Полный canonical copy/paste prompt» канона, перенесён **дословно** |
| «Как использовать» — пошаговая инструкция | раздел «Как использовать» канона, расширен указанием на выбор варианта |

Бездомного контента нет. Дубли между двумя источниками (упоминание шапки задачи, Russian-first reminder, methodology_reference) консолидированы в один раздел канона.

## Перекрёстные ссылки (§8) — что обновлено

| Файл | Изменение |
|---|---|
| `README.md:110` («Откройте файл: TARGET_REPOSITORY_ADOPTION_CHAT_PROMPT.md») | заменён на канон, обновлено название раздела для копирования |
| `README.md:183` (Canonical copy/paste prompt) | заменено на канон + явная пометка про redirect-заглушки |
| `README.md:207` (Шаблон короткого prompt) | заменено на канон (разделы Короткий/Безопасный короткий) |
| `docs/agent-system/ENGINE_ENTRYPOINT.md:182` (block с путём к prompt) | заменён на канон + пометка про заглушки |
| `docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml:52` (`categories.generic.files`) | путь заменён на `ADOPTION_PROMPT.md`; YAML-комментарий поясняет, что прежние два файла — redirect-заглушки и переносить их не нужно |
| `docs/agent-system/source/SOURCE_agent_system_index.md` | явных упоминаний прежних путей не было после C1 (он навигационный); reading-list-канон в `README.md`, который уже обновлён; правки в этом файле не требовались |

Файлы вне whitelist (`TARGET_REPOSITORY_ADOPTION_GUIDE.md`, `STAGE_2_COMPLETION_CHECKLIST.md`, `NEW_PROJECT_ONBOARDING_GUIDE.md`, `RELEASE_READINESS.md`, `CURRENT_STATE.md`, `ADOPTION_GUIDE.md`) продолжают ссылаться на прежние пути; их ссылки работают через 1-hop redirect (stub) и будут обновлены в дальнейших PR (например, PR-C4 для adoption guides).

## Согласованность с авторитетным scope

- ✅ §10 whitelist соблюдён буквально (6 файлов методологии + journal; источник index файл не правился — это допустимо, изменений в нём не требовалось).
- ✅ §3 имя канона `templates/ADOPTION_PROMPT.md` (4 раздела: короткий prompt, безопасный короткий prompt, полный canonical prompt, как действует engine + первый результат + ограничения + как использовать).
- ✅ §4 content-preservation: каждый уникальный пункт обоих источников перенесён в канон до stub.
- ✅ §8 rule 6 (append-only) соблюдено: `agents/docs-maintainer-01/*`, `DECISION_LOG.md`, журнал не правились.
- ✅ §8 rule 7 (redirect-заглушка для внешних bookmark) реализовано.
- ✅ Архитекторское правило таски (stub при наличии не-перенаправляемых ссылок) применено явно с журналируемым обоснованием.

## Проверка отсутствия broken refs

`git grep -n "SHORT_TARGET_ADOPTION_PROMPT\|TARGET_REPOSITORY_ADOPTION_CHAT_PROMPT"` показал, что все упоминания старых путей теперь указывают на:
- сами файлы-заглушки (которые существуют и ведут на канон);
- README/ENGINE_ENTRYPOINT/manifest — где явно поясняется, что это redirect-заглушки;
- файлы вне whitelist (продолжают работать через 1-hop redirect);
- append-only истории (исторический факт, broken refs допустимы по §8 rule 6).

Broken refs нет: все ссылки разрешаются.

## Измененные файлы (этой задачей)

- `docs/agent-system/templates/ADOPTION_PROMPT.md` (создан)
- `docs/agent-system/templates/SHORT_TARGET_ADOPTION_PROMPT.md` (содержание заменено на stub)
- `docs/agent-system/templates/TARGET_REPOSITORY_ADOPTION_CHAT_PROMPT.md` (содержание заменено на stub)
- `README.md`
- `docs/agent-system/ENGINE_ENTRYPOINT.md`
- `docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml`
- `docs/agent-system/engine-journal/input/TASK-0008-METH-CONSOLIDATION-C3-adoption-prompt-merge.md`
- `docs/agent-system/engine-journal/output/RESULT-0008-METH-CONSOLIDATION-C3-adoption-prompt-merge.md`
- `docs/agent-system/engine-journal/INDEX.md`

## Выполненные проверки

- Preflight: `git status`, `git fetch --all --prune`, `git switch developer`, `git pull --ff-only`, `git rev-parse developer/origin/developer`.
- Чтение RESULT-0004 §10, §3, §8, §4 как авторитетного scope.
- Inbound-карта обоих файлов через `git grep` до правок.
- Чтение SHORT_TARGET_ADOPTION_PROMPT и TARGET_REPOSITORY_ADOPTION_CHAT_PROMPT целиком для content-preservation.
- После правок: `git status --short` — только whitelist + journal; `git diff --check` — чисто; `git grep` старых имён — все вхождения объяснимы (stub, manifest comment, README объяснения, не-whitelist файлы через redirect, append-only история).

## Невыполненные проверки и причина

- Markdown/YAML lint — отдельный documented lint command не подтверждён.
- Docker/production checks — запрещены scope.
- Очистка ссылок в файлах вне whitelist (`TARGET_REPOSITORY_ADOPTION_GUIDE.md`, `STAGE_2_COMPLETION_CHECKLIST.md`, `NEW_PROJECT_ONBOARDING_GUIDE.md`, `RELEASE_READINESS.md`, `CURRENT_STATE.md`, `ADOPTION_GUIDE.md`) — вне whitelist; ссылки работают через redirect, очистка передаётся в PR-C4.

## Результат проверки запрещенных файлов

Файлы вне whitelist не изменялись. `.env` не читался. Append-only истории не переписывались.

## Результат проверки sensitive/private markers

Секреты не вводились и не печатались.

## Результат language policy

RESULT Russian-first; English только для technical identifiers, paths, filenames и literal terms. Канон `ADOPTION_PROMPT.md` сохраняет английский внутри copy/paste prompt дословно (это external user prompt с предсказуемой структурой).

## Принятые решения

- Канон = `templates/ADOPTION_PROMPT.md` (новый файл).
- **Stub для обоих** старых prompt-файлов (перекрыт stub-дефолт плана, который предусматривал stub только для самого ссылаемого).
- Обоснование stub'ов: ссылки в файлах вне whitelist + append-only истории; правка любого из них нарушила бы scope/append-only.
- Manifest: путь `ADOPTION_PROMPT.md` добавлен в `categories.generic.files`; прежний `TARGET_REPOSITORY_ADOPTION_CHAT_PROMPT.md` заменён, не сохранён как отдельная строка; YAML-комментарий поясняет про заглушки.
- `source/SOURCE_agent_system_index.md` не правился: после C1 он не содержит явных упоминаний прежних путей; reading-list-канон в README обновлён.

## Риски

- Файлы вне whitelist (особенно `TARGET_REPOSITORY_ADOPTION_GUIDE.md`, `STAGE_2_COMPLETION_CHECKLIST.md`, `NEW_PROJECT_ONBOARDING_GUIDE.md`, `RELEASE_READINESS.md`, `CURRENT_STATE.md`, `ADOPTION_GUIDE.md`) продолжают ссылаться на старые пути. Митигация: stub работает как 1-hop redirect; ссылки обновятся в PR-C4 (adoption guides merge) и в последующих docs-only правках.
- Внешние bookmark/чат-цитирования на прежние пути продолжают работать через stub. Митигация: stub явно указывает на канон и поясняет, что это redirect.

## Blockers

Нет.

## Закрытие после merge

Work PR URL: `https://github.com/MaximKolomeets/agent-system-development/pull/115`

Work PR status: `merged`

Work PR merge commit SHA: `ca7094528c4829b5eca221ae667dcfcb3796971c`

Work PR merged_at: `2026-06-14T21:12:09+07:00` (committer date merge commit; `gh` недоступен для GitHub `mergedAt`).

Release PR status: не применимо (перенос в `main` не выполнялся).

Release PR merge commit SHA: не применимо.

Release PR merged_at: не применимо.

Sync PR status: не применимо (sync `main -> developer` не выполнялся).

Sync PR merge commit SHA: не применимо.

Sync PR merged_at: не применимо.

RESULT closed after merge: yes

INDEX closed after merge: yes

No journal placeholders after merge: yes

Stale pre-merge status check: clean.

Closure source: local git history (`git log` / `git show`); `gh` недоступен.

Closure blockers: нет.

## Следующий рекомендуемый шаг

Пользователь создаёт PR `work/docs-maintainer-01/adoption-prompt-merge` → `developer`. После merge — closure 0008 (closure-only). Затем переходить к **PR-C5** (templates cleanup) по плану RESULT-0004 §10 (порядок: C1→C2→C3→**C5**→C4→C6; C6 уже выполнен раньше).

## Methodology feedback

Stub-стратегия для обоих файлов — пример того, как чёткие whitelist'ы и append-only правила вместе диктуют решение без архитекторского вмешательства. Архитекторское правило «delete если 0 ссылок» автоматически вылилось в «stub» при простом учёте scope и append-only истории — решение получилось дисциплинированным и журналируемым.
