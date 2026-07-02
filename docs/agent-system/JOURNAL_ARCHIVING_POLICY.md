# JOURNAL_ARCHIVING_POLICY

## Назначение

Этот документ задает политику архивирования engine journal без потери истории и
без перегруза context bundle.

Проблема H15: `docs/agent-system/engine-journal/output/` растет вместе с каждой
задачей. Через несколько месяцев активный journal становится тяжелым для
контекста агента, хотя старая история все еще нужна для аудита и восстановления.

Решение: делить journal history на release-boundary эпохи и после release
переносить закрытые RESULT в archive, оставляя в active `INDEX.md` короткий
summary и ссылки на archive.

## Journal Epoch

`Journal Epoch` — интервал engine journal, закрытый конкретным release.

Именование epoch:

```text
vX.Y.Z
```

Граница epoch:

- начинается после предыдущего опубликованного release/snapshot;
- заканчивается после release `vX.Y.Z`, когда выполнены release PR, tag, sync PR
  и batch closure для входящих journal entries;
- фиксируется отдельным post-release archive PR.

Epoch не создается до публикации release. Если tag, release PR, sync PR или
closure facts неизвестны, archiving task пишет `STOP`.

## Что архивируется

Архивировать можно только finalized RESULT, которые:

- относятся к закрытому release epoch;
- имеют PR URL или explicit no-PR terminal state;
- не находятся в статусе `open`, `ready for review`, `closure pending`,
  `draft`, `blocked` или `STOP`;
- не нужны как active handoff для текущего release/review boundary;
- не содержат private data, secrets или forbidden values.

TASK files обычно остаются в `engine-journal/input/`, потому что они короткие и
нужны для source-of-truth trace. Если конкретный target repository хочет
архивировать TASK вместе с RESULT, это должно быть отдельным target-local
решением и не меняет default methodology policy.

## Archive path

Canonical archive path:

```text
docs/agent-system/engine-journal/archive/vX.Y.Z/
```

Файлы RESULT перемещаются через `git mv`:

```text
docs/agent-system/engine-journal/output/RESULT-0150-EXAMPLE.md
docs/agent-system/engine-journal/archive/vX.Y.Z/RESULT-0150-EXAMPLE.md
```

Archive PR должен также создать:

```text
docs/agent-system/engine-journal/archive/vX.Y.Z/INDEX.md
```

Archive `INDEX.md` хранит epoch summary и ссылки на archived RESULT files.

## Active INDEX после archive

После archive active `docs/agent-system/engine-journal/INDEX.md` не должен
держать полный список archived rows как контекст по умолчанию.

Active `INDEX.md` оставляет:

```text
## Archived Journal Epochs

| Epoch | Release tag | Seq range | Entries | Archive index | Notes |
| --- | --- | --- | --- | --- | --- |
| vX.Y.Z | vX.Y.Z | 0001-0150 | 150 | archive/vX.Y.Z/INDEX.md | closed and archived after release |
```

Для current epoch active `INDEX.md` продолжает хранить обычные rows.

Если reviewer или architect должен проверить старую запись, он открывает
archive index и конкретный archived RESULT вручную. Archive не грузится в
обычный context bundle.

## Context bundle rule

Archive files запрещено включать в `orchestrator_context_bundle`.

Default cloud bundle содержит active `engine-journal/INDEX.md`, где есть только
epoch summary и ссылки. Полные archived RESULT files остаются в GitHub history и
в `engine-journal/archive/vX.Y.Z/`, но не загружаются в cloud context по
умолчанию.

`gen_cloud_bundle.py` должен блокировать archive paths в bundle validation.

## Manifest and file map

`ADOPTION_TRANSFER_MANIFEST.yml` должен разделять:

- active journal scaffold/history;
- `journal_archive` как excluded-from-context archival surface.

`PROJECT_FILE_MAP.md` должен показывать `journal_archive`, но не считать archive
source-transferable content и не требовать копирования archive в target
repository.

## Target repositories

Target repository ведет собственные journal epochs.

Archive methodology repository не копируется в target repository. При adoption
переносится только scaffold journal и templates по
`ADOPTION_TRANSFER_MANIFEST.yml`.

Target-local archive может использовать тот же path pattern, но должен
архивировать только свою target-specific историю.

## STOP-условия archive task

Archive task должна остановиться, если:

- release `vX.Y.Z` не опубликован;
- release/sync facts неизвестны;
- batch closure не завершен;
- в epoch есть open или closure-pending RESULT;
- требуется удалить историю без `git mv`;
- archive path попадает в cloud bundle;
- archive содержит private data или forbidden values;
- задача пытается переписать pushed/merged history.

## Acceptance criteria

Archive считается корректным, если:

- archived RESULT доступны в `engine-journal/archive/vX.Y.Z/`;
- archive index содержит seq range, PR links и safe summary;
- active `INDEX.md` содержит epoch summary и ссылку на archive index;
- cloud bundle не содержит archive files;
- generated checks проходят;
- Git history сохраняет rename/move trace;
- RESULT archive task фиксирует actor, evidence и проверки.

## Передача

Следующий: methodology-architect-01/source-steward — после release `vX.Y.Z`
создать отдельный archive PR, если active journal стал слишком большим для
обычного context bundle.
