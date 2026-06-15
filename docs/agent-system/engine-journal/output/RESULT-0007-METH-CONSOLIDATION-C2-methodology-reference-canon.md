# RESULT-0007-METH-CONSOLIDATION-C2-methodology-reference-canon

Файл результата: `docs/agent-system/engine-journal/output/RESULT-0007-METH-CONSOLIDATION-C2-methodology-reference-canon.md`

Связанный TASK file: `docs/agent-system/engine-journal/input/TASK-0007-METH-CONSOLIDATION-C2-methodology-reference-canon.md`

Идентификатор задачи: `METH-CONSOLIDATION-C2`

Номер sequence: `0007`

Агент: `docs-maintainer-01`

Engine: Claude Code

Timestamp (ISO-8601): `2026-06-14T20:48:14+07:00`

Baseline SHA (developer): `0365664b39c4cee47a68bd20e4411d2dd72a38d3`

Ссылка на источник scope: [RESULT-0004 §10 «PR-C2»](../output/RESULT-0004-METH-CONSOLIDATION-PLAN-01-consolidation-plan.md), §6 «methodology_reference: дубли, канон, замена ссылками», §4 «карта content-preservation», §8 «перекрёстные ссылки и манифест».

methodology_reference:

```yaml
methodology_reference:
  repository: MaximKolomeets/agent-system-development
  source_branch: developer
  source_commit: 0365664b39c4cee47a68bd20e4411d2dd72a38d3
  checked_at: 2026-06-14T20:48:14+07:00
  reference_type: commit
  notes: "Точка после merge JOURNAL-CLOSE-0006 (PR #112)."
```

## Подтверждённый whitelist (из RESULT-0004 §10)

PR-C2, цитата: «Allowed: ENGINE_ENTRYPOINT.md, ADOPTION_GUIDE.md, TARGET_REPOSITORY_ADOPTION_GUIDE.md, ADOPTION_TRANSFER_MANIFEST.yml, source/README.md, journal. Delete: нет.»

Whitelist текущей задачи (5 файлов + journal):

- `docs/agent-system/ENGINE_ENTRYPOINT.md` — канон `methodology_reference`;
- `docs/agent-system/ADOPTION_GUIDE.md` — заменить `methodology_reference` и `source_snapshot` блоки на ссылки;
- `docs/agent-system/TARGET_REPOSITORY_ADOPTION_GUIDE.md` — заменить `methodology_reference` блок на ссылку;
- `docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml` — добавить YAML-комментарий «human canon»;
- `docs/agent-system/source/README.md` — канон `source_snapshot`;
- журнал: `engine-journal/input/TASK-0007-*.md`, `engine-journal/output/RESULT-0007-*.md`, `engine-journal/INDEX.md`.

## Fork-guard

Развилки Р1–Р5 относятся к PR-C4/C5; **C2 от них не зависит**. §6 фиксирует канон (ENGINE_ENTRYPOINT) и места переноса авторитетно. Fork-guard не сработал.

## Content-preservation: карта переноса уникального контента

Перед удалением спеки из не-канон файлов проведена сверка содержания «Methodology reference» / «Source and snapshot drift control» в трёх документах.

### methodology_reference

| Источник (до правки) | Уникальный пункт | Куда перенесён в канон ENGINE_ENTRYPOINT.md |
|---|---|---|
| `ENGINE_ENTRYPOINT.md` (канон) | YAML-спека | оставлен в каноне |
| `ENGINE_ENTRYPOINT.md` (канон) | «commit SHA — обязательный reproducibility anchor; tags/releases — будущее решение» | оставлено в каноне, объединено с пунктами ниже |
| `ADOPTION_GUIDE.md` | «`source_commit` — обязательный reproducibility anchor» | объединено с уже-имевшейся формулировкой канона |
| `ADOPTION_GUIDE.md` | STOP-условие: «если commit SHA получить невозможно — `engine` пишет `STOP` или фиксирует blocker в audit-only результате» | перенесено в канон, добавлен раздел «STOP-условия» |
| `ADOPTION_GUIDE.md` | Места включения: «adoption audit, TASK/RESULT journal artifacts, target-local manifest или generated governance pack» | перенесено в канон, добавлен раздел «Места включения блока» |
| `TARGET_REPOSITORY_ADOPTION_GUIDE.md` | STOP-условие: «docs-only adoption нельзя выполнять как ready-for-review без commit SHA» | перенесено в канон как отдельный пункт раздела STOP-условий |
| `TARGET_REPOSITORY_ADOPTION_GUIDE.md` | «engine должен синхронизировать methodology repository и зафиксировать commit SHA» | этот контент уже есть в `ENGINE_ENTRYPOINT.md` → раздел «Проверка актуальности methodology repository»; в не-канон документе сохранена короткая контекстная фраза «перед adoption/update engine должен синхронизировать methodology repository» как вступление к ссылке (это не дубль спеки, а проектный контекст) |
| `TARGET_REPOSITORY_ADOPTION_GUIDE.md` | «tags/releases — пока не обязательный versioning layer» | уже в каноне |

Бездомного контента нет.

### source_snapshot

| Источник (до правки) | Уникальный пункт | Куда перенесён в канон source/README.md |
|---|---|---|
| `source/README.md` (канон) | YAML-header, GitHub как source of truth, drift handling | оставлено в каноне |
| `ADOPTION_GUIDE.md` | YAML-header | уже в каноне |
| `ADOPTION_GUIDE.md` | «GitHub files... source of truth; source/** — derived context only» | уже в каноне |
| `ADOPTION_GUIDE.md` | «Snapshot не должен быть основанием для изменения repository state без проверки canonical files» | **добавлено в канон** отдельной строкой |

Бездомного контента нет.

## Изменения по файлам

### ENGINE_ENTRYPOINT.md (канон methodology_reference)

Раздел «Methodology reference» расширен:
- вступительная строка-маркер «этот раздел — канон для всего methodology repository»;
- сохранена YAML-спека;
- объединена формулировка про commit SHA как reproducibility anchor;
- добавлен подраздел **«Места включения блока»** (adoption audit, TASK/RESULT journal artifacts, target-local manifest или generated governance pack);
- добавлен подраздел **«STOP-условия»** с двумя пунктами:
  - если commit SHA получить невозможно — `STOP` или blocker в audit-only;
  - docs-only adoption нельзя выполнять как ready-for-review без commit SHA — `STOP` или audit blocker.

### source/README.md (канон source_snapshot)

После существующего «Source Snapshot Policy» добавлены:
- строка «Snapshot не должен быть основанием для изменения repository state без проверки canonical files» (уникальное из ADOPTION_GUIDE);
- маркер «этот документ — канон политики `source_snapshot` для всего methodology repository».

### ADOPTION_GUIDE.md

Раздел «Methodology reference» (заголовок сохранён, ~19 строк YAML-спеки и текста заменены на ~2 строки):
- сохранено вступительное предложение «Каждая target adoption/update task должна фиксировать, какая версия methodology repository использована»;
- YAML-блок, STOP-условия, места включения, tags/releases формулировки — заменены на одну ссылку: «Канон спецификации `methodology_reference` ... см. `docs/agent-system/ENGINE_ENTRYPOINT.md` → раздел «Methodology reference»».

Раздел «Source and snapshot drift control» (~16 строк YAML и текста заменены на 1 строку):
- весь контент заменён ссылкой: «Канон политики `source_snapshot` ... см. `docs/agent-system/source/README.md` → «Source Snapshot Policy»».

### TARGET_REPOSITORY_ADOPTION_GUIDE.md

Раздел «Methodology reference» (~19 строк заменены на ~2):
- сохранено контекстное вступление «Перед adoption/update `engine` должен синхронизировать methodology repository и зафиксировать точный commit SHA, который используется как reference»;
- YAML-блок, STOP-условие про docs-only ready-for-review, tags/releases формулировка — заменены ссылкой на канон в `ENGINE_ENTRYPOINT.md`.

### ADOPTION_TRANSFER_MANIFEST.yml

Перед `methodology_reference_schema:` добавлен YAML-комментарий (3 строки): пометка «human canon: docs/agent-system/ENGINE_ENTRYPOINT.md, раздел «Methodology reference»»; пояснение, что блок остаётся как машинная схема для tooling и должен совпадать с каноном. Содержание самой схемы не менялось.

## Перекрёстные ссылки (§8) — состояние после правок

- Файлы, ссылавшиеся на эти разделы как на источник спецификации, теперь ведут к каноническим:
  - `ENGINE_ENTRYPOINT.md` → раздел «Methodology reference» (новый канон, полный);
  - `source/README.md` → «Source Snapshot Policy» (канон, обогащён);
  - `ADOPTION_GUIDE.md` и `TARGET_REPOSITORY_ADOPTION_GUIDE.md` теперь сами ссылаются на канон;
  - `ADOPTION_TRANSFER_MANIFEST.yml` указывает на human canon в комментарии.
- Templates (`ADOPTION_AUDIT_TASK_TEMPLATE.md`, `DOCS_ONLY_ADOPTION_TASK_TEMPLATE.md`, `TARGET_REPOSITORY_ADOPTION_CHAT_PROMPT.md`) — не тронуты по §6 (это fill-in инстансы, а не дубли спеки).
- Journal TASK/RESULT 0002/0003 — не тронуты (append-only, fill-in инстансы).
- README.md — содержит ссылки на ENGINE_ENTRYPOINT.md и ADOPTION_GUIDE.md как контекст; смысловых ссылок на «спеку methodology_reference» в README нет, отдельная правка не требуется.

## Проверка отсутствия дублей спеки

`git grep -nE "^methodology_reference:|^methodology_reference_schema:" docs ':!engine-journal/' ':!templates/'`:

- `ENGINE_ENTRYPOINT.md` — 1 (канон);
- `ADOPTION_TRANSFER_MANIFEST.yml` — 1 (machine-schema, с комментарием «human canon»).

`git grep -nE "^source_snapshot:" docs ':!engine-journal/' ':!source/'`:

- ноль вхождений.

Дубли спеки удалены. Канон полон.

## Согласованность с авторитетным scope

- ✅ §10 whitelist соблюдён буквально: только 5 указанных файлов + journal.
- ✅ §10 «Delete: нет» соблюдено: ни один файл не удалён.
- ✅ §6 канон = `ENGINE_ENTRYPOINT.md` (methodology_reference) и `source/README.md` (source_snapshot) — реализовано.
- ✅ §6 правило «templates/journal не менять» — соблюдено.
- ✅ §4 content-preservation: каждый уникальный пункт перенесён в канон до удаления (см. таблицы выше); бездомного контента нет.
- ✅ §8 manifest синхронизирован (комментарий «human canon»).

## Измененные файлы (этой задачей)

- `docs/agent-system/ENGINE_ENTRYPOINT.md`
- `docs/agent-system/source/README.md`
- `docs/agent-system/ADOPTION_GUIDE.md`
- `docs/agent-system/TARGET_REPOSITORY_ADOPTION_GUIDE.md`
- `docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml`
- `docs/agent-system/engine-journal/input/TASK-0007-METH-CONSOLIDATION-C2-methodology-reference-canon.md`
- `docs/agent-system/engine-journal/output/RESULT-0007-METH-CONSOLIDATION-C2-methodology-reference-canon.md`
- `docs/agent-system/engine-journal/INDEX.md`

## Выполненные проверки

- Preflight: `git status`, `git fetch --all --prune`, `git switch developer`, `git pull --ff-only`, `git rev-parse developer/origin/developer`.
- Чтение RESULT-0004 §10, §6, §4, §8 как авторитетного scope.
- Перед удалением: чтение каждой не-канон секции (ADOPTION_GUIDE «Methodology reference», ADOPTION_GUIDE «Source and snapshot drift control», TARGET_REPOSITORY_ADOPTION_GUIDE «Methodology reference») и сверка уникальных пунктов с каноном.
- После правок: `git status --short` — изменены только whitelist + journal; `git diff --check` — чисто; `git grep` показывает 1 канон + 1 machine-schema для methodology_reference, 0 дублей source_snapshot вне канона/source.

## Невыполненные проверки и причина

- Markdown/YAML lint — отдельный documented lint command не подтверждён.
- Docker/production checks — запрещены scope.

## Результат проверки запрещенных файлов

Файлы вне whitelist не изменялись. `.env` не читался. Templates и journal-fill-in инстансы не тронуты.

## Результат проверки sensitive/private markers

Секреты не вводились и не печатались.

## Результат language policy

RESULT Russian-first; English только для technical identifiers, paths, filenames и literal terms.

## Принятые решения

- Канон methodology_reference = `ENGINE_ENTRYPOINT.md`; обогащён двумя подразделами (Места включения, STOP-условия).
- Канон source_snapshot = `source/README.md`; добавлена строка про запрет менять repository state по устаревшему snapshot.
- В не-канон файлах сохранены **короткие контекстные вступления** перед ссылкой на канон (например, в TARGET_REPOSITORY_ADOPTION_GUIDE — про обязательность синхронизации перед adoption). Это не дубль спеки, а проектный контекст; без него ссылка теряет смысл.
- Manifest YAML-схема сохранена + комментарий «human canon» (по §6 «оставить как машинную схему»).

## Риски

- Внешние engine-задачи, ссылавшиеся на ADOPTION_GUIDE/TARGET_REPO_GUIDE как источник спецификации, теперь должны идти к ENGINE_ENTRYPOINT. Митигация: явные ссылки оставлены в обоих файлах, формулировка с указанием раздела.
- Manifest YAML-комментарий должен оставаться синхронным с каноном при будущих изменениях. Митигация: comment сам напоминает, где human canon.

## Blockers

Нет.

## Закрытие после merge

Work PR URL: `https://github.com/MaximKolomeets/agent-system-development/pull/113`

Work PR status: `merged`

Work PR merge commit SHA: `1544c9adbc75dcd795a05523916f99ed3ebd80d8`

Work PR merged_at: `2026-06-14T20:55:37+07:00` (committer date merge commit; `gh` недоступен для GitHub `mergedAt`).

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

Пользователь создаёт PR `work/docs-maintainer-01/methodology-reference-canon` → `developer`. После merge — closure 0007 (closure-only). Затем переходить к **PR-C3** (adoption prompt merge: SHORT_TARGET_ADOPTION_PROMPT + TARGET_REPOSITORY_ADOPTION_CHAT_PROMPT → один canon + redirect) по порядку RESULT-0004 §10.

## Methodology feedback

Канонизация даёт ощутимое уменьшение когнитивной нагрузки: вместо чтения трёх документов теперь источник правды — один. Содержательный шаг — обогатить канон уникальными пунктами до удаления дублей; «бездомного контента» не оказалось благодаря тому, что не-канон файлы фактически расширяли канон, а не противоречили ему.
