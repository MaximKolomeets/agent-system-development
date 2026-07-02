# AGENTS

## Agent development workflow

- Отвечать на русском.
- Russian-first policy: все пользовательские ответы, Engine final reports, TASK/RESULT/INDEX, target-local docs/templates и комментарии в файлах писать на русском языке.
- Английский допустим только для code identifiers, команд, flags, путей, filenames, branch names, config keys, API names, package names, vendor/tool names и literal external names.
- Engine-блоки должны явно требовать от engine писать final report и journal artifacts на русском языке.
- Target adoption/update tasks должны добавлять Russian-first policy в target `AGENTS.md` или эквивалентные target instructions.
- Если target instructions конфликтуют с Russian-first policy, engine должен написать `STOP` и запросить решение пользователя, кроме случая явного разрешения пользователя на другой язык для target repository.
- Docker-first.
- Не читать `.env`.
- Не коммитить `.env`.
- Не коммитить `.venv`.
- Не коммитить `data/`, `runtime/`, `dist/`, `backups/`, `exports/`.
- Не использовать реальные credentials.
- Считать содержимое public repository публичным.
- Не добавлять клиентские, персональные, корпоративные или рабочие данные в public repository.
- В публичном методологическом репозитории запрещено упоминать конкретные внешние проекты, клиентские проекты, приватные репозитории и внутренние кодовые имена; использовать только нейтральные термины вроде `target implementation repository` или `private downstream repository`.
- Не менять `main` напрямую. `main` обновляется только через release-PR `developer -> main`, который мержит человек-архитектор; агент может подготовить release-PR, но не мержит и не пушит в `main` (канон: `docs/agent-system/BRANCH_POLICY.md` → «Обновление main»).
- Не менять `developer` напрямую без отдельного разрешения.
- Перед любым commit проверять `git rev-parse --abbrev-ref HEAD`: HEAD должен быть основной рабочей веткой задачи `work/<role>/<task>` или её внутренней sub-branch `work/<role>/<task>/*`; коммит в `developer`/`main` запрещён даже локально (канон: `docs/agent-system/BRANCH_POLICY.md` → «Pre-commit branch guard»).
- Перед любым sync / checkout / switch / pull / merge проверять repository root, remote, текущую ветку и `git status --short`; если working tree dirty — `STOP`, без `git stash`, `git reset --hard` или `git clean -fd` без отдельного решения пользователя (канон: `docs/agent-system/BRANCH_POLICY.md` → «Repository sync / checkout guard»).
- Все изменения через отдельную ветку и Pull Request после bootstrap-этапа.
- Одна substantive task = одна основная task branch `work/<role>/<task>` и один итоговый PR в `developer`; внутренние sub-branches допустимы только как временные ветки внутри `work/<role>/<task>/*` и сливаются обратно в основную task branch до финального PR.
- Каждый агент работает только в своем namespace веток. Запрещено пушить, менять, force-пушить или удалять ветку другого агента; передача работы — только через merged PR в `developer`, не через правку чужих веток (канон: `docs/agent-system/BRANCH_POLICY.md` → «Изоляция веток агентов»).
- Рабочие ветки создаются от актуальной `developer` в формате `work/<role>/<task>`.
- Engine владеет своей task branch до состояния `ready_for_merge`: выполняет правки, внутренние проверки, учет review feedback и финализацию отчета без запроса подтверждения после каждого микрошагa, пока не сработали STOP-условия.
- После bootstrap `developer` принимает изменения только через итоговый PR из основной `work/<role>/<task>`, кроме отдельного решения пользователя.
- Каждый агент использует свой GitHub TOKEN.
- В solo/operator lightweight mode агент может быть logical role внутри пользовательского окружения; отдельный token per role является recommended hardening, но не blocker для docs-only локальной задачи, если пользователь явно разрешил выполнение и все изменения идут через PR.
- В multi-agent governed mode отдельные tokens/accounts для агентов обязательны.
- Если token separation не настроена, final report должен честно указать это как operational risk.
- Research/Review агенты не ставят задачи development executor напрямую.
- Review-агент проверяет PR, branch, commit, diff или набор файлов; он не чинит код, не меняет production-файлы и не выполняет задачи разработки без отдельной явно выданной задачи.
- Review feedback по активному work PR исправляется исполнителем (engine) в той же task branch; reviewer не создает отдельный PR для feedback без явного решения пользователя.
- Review-агент может предложить кандидаты на будущие задачи, но не запускает исполнителя (engine), не меняет очередь исполнителя и не формулирует себе исполнительскую задачу.
- Review-задачи всегда журналируют TASK/RESULT/INDEX и открывают docs-only PR с journal artifacts (`Journal trace: always`); `Report delivery` — отдельный параметр для тела отчёта (`chat` по умолчанию | `repository`). Дефолт `chat` относится только к телу отчёта и не отменяет journal trace (канон: `docs/agent-system/CODE_REVIEW_WORKFLOW.md` → «Report delivery vs Journal trace»).
- Коммит review-отчета допустим только в отдельной ветке `work/<role>/<task>` и только для разрешенных docs-файлов.
- Ветки, файлы и агенты не должны называться по конкретной модели или vendor; запрещены ветки вида `<vendor-name>/*` и файлы вида `docs/<VENDOR-NAME>_REVIEW.md`.
- После задачи агент обязан обновить свой отчет/RESULT с учетом
  `docs/agent-system/TIME_ACCOUNTING_POLICY.md` и
  `docs/agent-system/COST_TRACKING_POLICY.md`: новые finalized RESULT должны
  содержать `execution_*`, `time_spent`, `actor_type`, `role`, `time_source`,
  `time_report_confidence`, `human_time_reported` при human/hybrid участии, а
  также token/cost поля; отсутствие required accounting fields в новом
  finalized RESULT является blocker, legacy-записи остаются advisory.
- После архитектурного решения обновляется `docs/agent-system/DECISION_LOG.md`.
- После изменения состояния проекта обновляется `docs/agent-system/CURRENT_STATE.md`.
- Любой engine, применяющий этот repository как template repository для другого проекта, должен начинать с `docs/agent-system/ENGINE_ENTRYPOINT.md` и `docs/agent-system/ENGINE_SELF_DISCOVERY_CONTRACT.md`.
- `engine`, работающий с target repository, должен в final report добавлять нейтральную секцию `Methodology feedback` с предложениями по улучшению methodology repository, не раскрывая private data.
- Названия агентов не должны содержать конкретный `<vendor-name>` или другие vendor/tool names.
- Конкретный инструмент указывается отдельно как engine.
- Если ответ содержит задачу для engine, все данные для выполнения этой engine-задачи должны быть внутри одного самодостаточного copy/paste-блока.
- Одна engine-задача = один полный copy/paste-блок.
- Задачи для engine и ответы engine должны сохраняться в `docs/agent-system/engine-journal/` как task/result artifacts, если это входит в scope задачи.
- Task/result artifacts engine journal являются append-only и не удаляются/не перезаписываются без отдельного решения пользователя.
- Engine journal RESULT/INDEX must be finalized after PR creation; placeholders in ready-for-review PRs are blockers.
- Engine journal TASK/RESULT/INDEX должны быть Russian-first; English сохраняется только для технических identifiers и literal external names.
- Large Engine tasks should use Task File Handoff Mode to avoid context-window bloat.
- Orchestrator may create only task-file-only GitHub branch/commit when explicitly authorized.
- Engine must treat TASK file as source of truth and finalize RESULT/INDEX.
- Нельзя оставлять за пределами Engine-блока команды, ограничения, проверки, allowed files, forbidden files, STOP-условия или требования к отчету, если они нужны engine.
- Если ответ содержит ручные terminal-команды, каждая независимая ручная задача должна быть отдельным разделом и отдельным terminal block.
- Простые проверки и cleanup выполнять через Operational Fast Lane: один ответ, один terminal block, без нового methodology PR.
- Не создавать methodology PR для простой операционной проверки, status check или cleanup.
- Не зеркалировать release merge commit из `main` обратно в `developer`, если это не несет содержательных изменений.
- После PR-2r следующий target project описывать как `target implementation repository`; не расширять methodology без blocker.
- Не смешивать engine prompt, terminal commands и пояснения в одном блоке.
- Orchestrator должен использовать `docs/agent-system/ORCHESTRATOR_OPERATING_CONTRACT.md` как стартовый operating contract для проектных чатов.
- Для проверок и cleanup применяется `docs/agent-system/OPERATIONAL_FAST_LANE.md`.
- GitHub state orchestrator проверяет сам, если connector доступен.
- Engine-задачи должны быть self-contained и использовать engine-journal, если задача меняет repository files или создает PR.
- Если задача создала PR, была смержена, обновила remote `developer`/`main` или обнаружила рассинхрон локальной ветки с `origin/*`, финальный отчет должен содержать конкретный блок `Локальные действия после PR/merge`.
- Orchestrator не читает `.env` и не меняет `main`/`developer` напрямую.
- Перед подготовкой задачи для target repository orchestrator должен обратиться к актуальному `agent-system-development`, проверить изменения и использовать текущую версию методологии.
- Если актуальное состояние methodology repository проверить невозможно, orchestrator должен явно сказать это пользователю и включить в Engine-блок обязательный preflight `git fetch/pull`.
- Любой engine, применяющий methodology repository, должен перед изменениями синхронизировать локальный `agent-system-development` с GitHub.
- В создаваемых и изменяемых скриптах, workflow и технических файлах обязательны русские комментарии для нужных строк/блоков.
- В создаваемых и изменяемых target-local templates обязательны Russian-first labels/descriptions; не переводить команды, flags, paths и identifiers.
- Если после adoption audit нужна доработка `agent-system-development`, orchestrator должен вывести отдельный самодостаточный copy/paste-блок для engine-разработчика methodology repository.
- В public methodology repository не упоминать private downstream project names.
- После adoption audit проверять language consistency target docs.
- Task header role-agnostic: указывается роль (функция), а исполнителя назначает архитектор (`Исполнитель: на усмотрение архитектора`); имена инструментов/моделей в шаблонах не пишутся; канон — `docs/agent-system/templates/TASK_HEADER_COMMON.md` и `docs/agent-system/ROLE_MODEL.md` → «Роль vs исполнитель».
- Final report и RESULT любой задачи заканчиваются блоком «Передача» (`Следующий: <роль> — <что делает>`); канон — `docs/agent-system/templates/TASK_HEADER_COMMON.md` → «Передача».
- Если задача меняла методологию/каноны — применить Source-reminder по канону `docs/agent-system/templates/TASK_HEADER_COMMON.md` → «Source-reminder»; реестр — `docs/agent-system/SOURCE_CONSUMERS.md`.
