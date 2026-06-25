# NEXT_STEPS

## Постоянный рабочий цикл (Standing Workflow Loop)

Повторяемый цикл methodology maintenance:

1. Сформулировать plan/task с точным scope, allowed files, checks, STOP conditions и branch guard.
2. Выполнить work PR из `work/<role>/<task>` в `developer`.
3. Провести review по head SHA и фактическому diff.
4. После merge оставить work-journal entry open/closure-pending, если действует batch-policy.
5. Повторять work/review/merge до завершения текущей серии.
6. Перед release выполнить pre-release batch-closure для всех merged-but-unclosed journal entries.
7. Выполнить release-gate: journal closed, `python docs/agent-system/tools/gen_file_map.py --check`, `python docs/agent-system/tools/gen_cloud_bundle.py --check` (content-oriented / EOL-safe), state-refresh для `CURRENT_STATE.md`/`NEXT_STEPS.md` с regenerated `docs/agent-system/cloud/**`.
8. Человек-архитектор мержит release PR `developer -> main`, затем ставит human-only annotated tag на release merge commit в `main`; после release выполняется sync `main -> developer`.
9. Повторить цикл от актуального `developer`.

## Текущий фокус (Current Focus)

Текущий фокус: release-prep к `v1.2.0`. Full audit и fix-серия P0-P4 выполнены; batch-closure и reviewer consistency-gate завершены, reviewer verdict — `READY for release-prep v1.2.0`. После merge текущего release-prep PR следующий шаг выполняется отдельной задачей: создать release PR `developer -> main` для `v1.2.0`. Дальше только человек-архитектор мержит release PR и ставит human-only annotated tag `v1.2.0` на release merge commit в `main`; затем engine выполняет sync `main -> developer`, после чего команда переходит к downstream adoption / verification dry run от актуального release pointer.

Точные task/PR факты не дублируются здесь как source of truth. Актуальный pointer: `docs/agent-system/engine-journal/INDEX.md`; latest release: GitHub `main`/tags и release/sync facts в journal.

## Опциональный backlog (на усмотрение архитектора)

- **Review journaling polish**: blocker по PR-C6.1 закрыт. `Journal trace: always` и `Report delivery` разведены; future polish допустим только как wording cleanup без blocker status.
- **Чистка redirect-заглушек** — выполнено (METH-BACKLOG-POLISH): 6 history-only заглушек удалены (`SHORT_TARGET_ADOPTION_PROMPT`, `REVIEW_TEMPLATE`, `NEW_PROJECT_BOOTSTRAP_PROMPT`, `PROJECT_CHAT_START_PROMPT_TEMPLATE`, `TARGET_REPOSITORY_ADOPTION_GUIDE`, `PROJECT_LIFECYCLE`); `templates/TARGET_REPOSITORY_ADOPTION_CHAT_PROMPT.md` оставлен заглушкой (внешние bookmark); живые ссылки перенаправлены на каноны; `ADOPTION_PROMPT.md` список «engine should find» обновлён на `ADOPTION_GUIDE.md`.
- **Optional polish**: отдельно можно рассмотреть vendor/public metadata hygiene и English wording там, где это не нарушает Russian-first policy; это не blocker для adoption.
- **Operating layer (`ASD-OPLAYER-001`, journal 0024)**: добавлены нейтральные контракты `ORCHESTRATOR_PROJECT_OPERATING_LAYER.md` и `CROSS_PROJECT_CONSOLIDATION_CONTRACT.md`, governance pack template расширен разделом «Три слоя управления». Опционально: при downstream adoption включать эти контракты в target governance pack как optional-файлы; реальные visibility-matrix и дайджесты держать в приватном control plane, не в публичном репозитории.
- **Future methodology simplification**: после `v1.2.0` отдельно рассмотреть lifecycle simplification, context handoff footer enforcement, GitHub PR state as authority, journal gate automation и adoption feedback loop automation. Это future backlog, не часть release-prep и не blocker для `v1.2.0`.

## Текущие операционные правила

1. Применять обновленный `ORCHESTRATOR_RESPONSE_STANDARD.md` и `ORCHESTRATOR_RESPONSE_TEMPLATE.md` при подготовке новых Engine-блоков.
2. Проверять Fast Lane -> Engine escalation при любой write-action recommendation.
3. Проверять русские пользовательские заголовки и описания в Engine-блоках.
4. Проверять Closure policy после сообщений о merge/release/sync: обычные work PR могут оставаться `merged; closure pending` до batch-closure перед release; release gate, audit/review consistency gate, adoption/source-update, завершение/пауза серии и явное closure-задание требуют per-task closure.
5. Если journal stale после merge в per-task exception или под release gate, создавать docs-only Engine-блок на closure cleanup вместо ответа `все закрыто`.
6. Использовать `CODE_REVIEW_TASK_TEMPLATE.md` для первого безопасного review target implementation repository только после проверки, что task явно содержит режим, объект проверки, allowed/forbidden files и правило сохранения отчета. Review-задачи всегда журналируют TASK+RESULT (`Journal trace: always`).
7. При следующем target repository dry run фиксировать methodology feedback без private data и с sanitization checkpoint.
8. Перед любым sync/checkout/switch/pull/merge применять `Repository sync / checkout guard`: root, remote, branch и `git status --short`; dirty tree → STOP.
9. Отдельной future task рассмотреть tags/releases для methodology versioning, если commit-based `methodology_reference` окажется недостаточным.
