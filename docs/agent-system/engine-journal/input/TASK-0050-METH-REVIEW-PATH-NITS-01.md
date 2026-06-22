# TASK-0050: METH-REVIEW-PATH-NITS-01

## Режим

Роль: docs-maintainer. Исполнитель: на усмотрение архитектора. Reasoning effort: средний. Branch-guard обязателен.

Batch-policy: открытые journal-записи не являются blocker; closure не подмешивать.

## Цель

Закрыть мелкие audit-ниты: снять читаемость `docs/agent-system/reviews/` как dead methodology-source path и русифицировать prose-заголовки в `WORKFLOW.md` по `LANGUAGE_POLICY`.

## Repo / ветки

- Репозиторий: `MaximKolomeets/agent-system-development`
- Каталог: `C:\neural\repos\agent-system-development`
- base: `developer`
- work: `work/docs-maintainer-01/review-path-nits-01`

## Preflight

1. Перед sync/checkout проверить repository root, remote, branch и `git status --short`; dirty tree -> STOP.
2. `git fetch --all --prune`
3. `git switch developer`
4. `git pull --ff-only origin developer`
5. `git switch -c work/docs-maintainer-01/review-path-nits-01`
6. `git rev-parse --abbrev-ref HEAD` должен вернуть work-ветку.
7. Sequence взять из `INDEX`; текущая запись: `0050`.

## Discovery

```powershell
rg -n "docs/agent-system/reviews/" docs/agent-system/templates/CODE_REVIEW_TASK_TEMPLATE.md docs/agent-system/templates/CODE_REVIEW_REPORT_TEMPLATE.md
rg -n "Review-only workflow|Anti-overengineering checkpoint|Lightweight solo-operator mode|Multi-agent governed mode" docs/agent-system/WORKFLOW.md
```

## Allowed files

- `docs/agent-system/templates/CODE_REVIEW_TASK_TEMPLATE.md`
- `docs/agent-system/templates/CODE_REVIEW_REPORT_TEMPLATE.md`
- `docs/agent-system/WORKFLOW.md`
- `docs/agent-system/cloud/**`
- journal 0050

`ENGINE_JOURNAL_CONTRACT.md` не трогать: его заголовки являются technical tokens по `LANGUAGE_POLICY`. `WORKFLOW.md` и review templates не входят в orchestrator cloud bundle, поэтому их контентные зеркала в cloud не появляются. `docs/agent-system/cloud/**` разрешён только для штатного INDEX-driven regen: `engine-journal/INDEX.md` входит в bundle и обновляет `cloud/ENGINE_JOURNAL_INDEX.md` (+ `cloud/README.md` freshness).

## Изменения

1. В review task/report templates уточнить, что `docs/agent-system/reviews/<task-id>-review.md` — target-local create-on-demand convention при `Report delivery: repository` или `chat+repository`, а не обязательный methodology-source каталог.
2. В `WORKFLOW.md` перевести prose-заголовки:
   - `Lightweight solo-operator mode`;
   - `Multi-agent governed mode`;
   - `Anti-overengineering checkpoint`;
   - `Review-only workflow`.
3. Технические tokens оставить только там, где они являются mode/field names или identifiers.

## Проверки

- `reviews/` путь уточнён и не читается как dead methodology-source path;
- prose-заголовки в `WORKFLOW.md` русифицированы;
- `python docs/agent-system/tools/gen_file_map.py --check` exit 0;
- `python docs/agent-system/tools/gen_cloud_bundle.py --check` exit 0;
- cloud bundle regenerated только для `INDEX -> ENGINE_JOURNAL_INDEX` и freshness README;
- diff только whitelist;
- `git diff --check`;
- branch guard.

## Journal + Source Delta + handoff

`RESULT-0050` должен содержать Source Delta и handoff: архитектору загрузить изменённые source/template файлы; cloud bundle regenerated только для journal INDEX mirror.

## Commit / PR

Commit:

```text
docs(agent-system): clarify reviews/ path in review templates + RU prose headings (audit nits)
```

Создать PR в `developer`.

## Передача

`fix-cycle завершён. reviewer — review; затем архитектор — merge; затем engine — pre-release BATCH-CLOSURE 0047…последний; затем release dev→main`.

## STOP

- HEAD не work-ветка;
- правка вне whitelist;
- неожиданно затронут bundle-файл;
- соблазн чистить history/vendor literals;
- любой обязательный check не проходит.
