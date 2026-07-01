# SUPERSEDED_BANNER

<!-- SUPERSEDED_BY: <file>; PR: <n>; DATE: <YYYY-MM-DD> -->
> Этот документ заменён: `<file>`; PR-источник: `#<n>`; дата: `<YYYY-MM-DD>`.

## Назначение

Использовать в начале документа, который нельзя удалить из-за inbound links,
append-only history, external bookmarks или audit continuity, но который больше
не является canonical source. Эти technical literals не заменяют видимую
Russian-first строку для читателя.

## Правило заполнения

- `<file>` — canonical replacement path или stable document identifier.
- `<n>` — номер PR, где replacement принят или superseded-решение зафиксировано.
- `<YYYY-MM-DD>` — дата принятия superseded-решения.
- Видимая строка обязательна: machine-readable HTML comment сам по себе скрыт в
  rendered Markdown и не должен быть единственным сигналом для читателя.

## Пример

```markdown
<!-- SUPERSEDED_BY: docs/agent-system/ADOPTION_GUIDE.md; PR: 115; DATE: 2026-06-14 -->
> Этот документ заменён: `docs/agent-system/ADOPTION_GUIDE.md`; PR-источник: `#115`; дата: `2026-06-14`.
```
