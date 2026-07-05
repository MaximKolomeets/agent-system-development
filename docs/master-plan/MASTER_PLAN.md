# МАСТЕР-ПЛАН: универсальная агентная система разработки — от локального Docker до автономного Engine

Версия: 1.2.1 от 2026-07-04  
Статус: рабочий канон проекта  
Владелец: Максим Коломеец  
Расположение: `docs/master-plan/MASTER_PLAN.md` в репозитории `MaximKolomeets/agent-system-development`  
Предыдущее основание: v1.0 — OpenHands + DeepSeek + GitHub Actions; v1.1 — универсальная агентная платформа.  
Главное решение v1.2: **первый практический запуск делаем локально через Docker на компьютере Максима; автономные CI-контуры подключаем следующим слоем.**
Правки v1.2.1: маркеры КТ-1/КТ-5, цены DeepSeek и срок отключения старых имён моделей, уточнение переменных штатного резолвера, нейтральная формулировка B6, оговорка об условных этапах 8–9.

---

## 0. Как читать этот документ

Документ описывает проект в четырёх плоскостях:

1. **Сторона владельца** — зачем это нужно, сколько стоит, какие контрольные точки принимать.
2. **Сторона оператора** — как каждый день ставить задачи, проверять PR и не лезть в код без необходимости.
3. **Сторона исполнения** — какие конкретные шаги выполнить: команды, настройки, критерии «сделано».
4. **Сторона платформы** — как не привязаться к одному агенту, одной модели и одному CI.

Правила чтения:

1. Этапы обозначены «Этап 0 … Этап 9».
2. Каждый шаг имеет структуру: **Что делаем** → **Как делаем** → **Критерий “сделано”** → **Если не получилось**.
3. Команды в терминале можно копировать и вставлять.
4. Этапы выполняются по порядку. Для v1.2 важное изменение: сначала локальный Docker-пилот, потом автономный CI. Этапы 8 и 9 — условные: они включаются только при выполнении своих условий входа (Шаг 8.1 и Шаг 9.1), их можно не выполнять вовсе.
5. Прогресс отмечается в разделе 12 «Сводный чек-лист прогресса».
6. Merge всегда делает человек. Агент может писать код, открывать PR, комментировать, но не принимает изменения сам.

**Решение по репозиториям:** отдельный репозиторий `agents` не создаётся. Методология, мастер-план, правила агентов и адаптеры живут в `agent-system-development`. Боевые пилоты выполняются в целевых репозиториях, начиная с `MaximKolomeets/verification`.

---

## 1. Термины простым языком

| Термин | Что это значит |
|---|---|
| **Агент** | Программа с ИИ, которая сама выполняет задачу: читает код, пишет код, запускает проверки, готовит PR. |
| **Engine** | Роль исполнителя. Агент, который берёт задачу и доводит её до результата. |
| **Оркестратор** | Роль постановщика и архитектора. Помогает превратить разговор в проверяемую задачу. |
| **Reviewer** | Роль проверяющего. Смотрит PR после Engine и ищет ошибки. |
| **Agent Adapter** | Обёртка, которая знает, как запускать конкретного агента: OpenHands, Qwen Code, Codex, Claude Code и т.д. |
| **Model Adapter** | Обёртка, которая знает, как обратиться к конкретной модели или провайдеру: DeepSeek, OpenAI, Anthropic, Qwen, локальная модель. |
| **Model Profile** | Логическое имя модели: `model/cheap`, `model/strong`, `model/reviewer`, `model/local`. Задачи выбирают профиль, а не конкретную модель. |
| **LLM Hub / LLM Gateway** | Единая точка доступа к моделям. Агенты ходят в Hub, а не напрямую к провайдерам. Hub хранит реальные API-ключи, выдаёт виртуальные ключи, считает расходы и может переключать модели. |
| **Virtual key** | Внутренний ключ для агента. Он не равен настоящему ключу DeepSeek/OpenAI/Anthropic и может быть ограничен по бюджету, моделям и сроку жизни. |
| **CI Adapter** | Обёртка, которая знает, как запустить агентный job в конкретном CI: GitHub Actions, GitLab CI, Jenkins, GitVerse CI/CD, SourceCraft CI/CD. |
| **Runner / Worker** | Машина, на которой CI выполняет работу: cloud runner, self-hosted runner, VM, локальный компьютер. |
| **Dispatcher** | Слой, который принимает задачу и выбирает Agent Adapter, Model Profile и CI Adapter. В MVP роль Dispatcher выполняет человек/оркестратор + workflow. |
| **Task Manifest** | Машиночитаемое описание задачи: репозиторий, issue, целевая ветка, агент, модельный профиль, ограничения, критерии приёмки. |
| **OpenHands** | Первый Engine для MVP. Умеет работать локально через Docker и имеет resolver-контур issue → PR. |
| **Qwen Code** | CLI-агент для работы в терминале/CI. Рассматривается как второй Engine после OpenHands-пилота. |
| **Codex** | CLI/agent/review-инструмент OpenAI. В этом плане используется как возможный Reviewer или fallback Engine. |
| **Claude Code** | CLI/GitHub Actions агент Anthropic. Используется как возможный дорогой fallback/Reviewer. |
| **Docker** | Среда контейнеров. В v1.2 первый практический запуск OpenHands делаем именно через Docker на локальном компьютере. |
| **WSL2** | Подсистема Linux внутри Windows. Нужна, чтобы Docker/OpenHands стабильно работали на Windows. |
| **Репозиторий** | Папка проекта на GitHub/GitVerse/SourceCraft/GitLab с историей изменений. |
| **Issue / Task** | Карточка задачи. В нашей системе — основной способ дать задание Engine. |
| **PR / MR** | Pull Request / Merge Request: предложение изменений. Результат работы Engine. |
| **Ветка** | Отдельная линия изменений для одной задачи. |
| **`main` / `developer`** | `main` — стабильная версия. `developer` — сборочная ветка для проверенных изменений перед выпуском в `main`. |
| **Headless-режим** | Запуск агента без интерфейса: текстовая задача на входе, результат/PR на выходе. |
| **RAG / база знаний** | Накопление прошлых решений и правил, чтобы агент не повторял ошибки. В v1.2 полноценный RAG откладывается, начинаем с файлов правил. |

---

## 2. Цель проекта и что считается успехом

**Цель** — построить универсальный агентный конвейер разработки, где Максим формулирует задачу простым текстом, а система доводит её до готового PR через выбранного агента, выбранную модель и выбранный контур исполнения.

Целевой поток v1.2:

```text
Максим говорит с оркестратором
→ оркестратор формулирует issue/task manifest
→ Dispatcher выбирает Agent Adapter + Model Profile + Execution/CI Adapter
→ агент работает локально через Docker или в CI
→ агент создаёт ветку и PR/MR
→ независимый Reviewer или человек проверяет PR
→ Максим принимает решение о merge
```

**Ключевое отличие от v1.0:** OpenHands + DeepSeek + GitHub Actions — это первая реализация, а не архитектурная зависимость.

**Ключевое отличие от v1.1:** стартуем не с облачного CI, а с локального Docker-режима, чтобы быстро увидеть агентную работу, настройки модели, расходы и качество PR на своём компьютере.

Система должна позволять заменить:

1. агента: `OpenHands` → `Qwen Code` → `Codex` → `Claude Code` → другой агент;
2. модель: `DeepSeek` → `OpenAI` → `Anthropic` → `Qwen` → локальная модель;
3. доступ к моделям: прямой API-ключ в MVP → LLM Hub / virtual keys в production;
4. CI: `GitHub Actions` → `GitLab CI` → `Jenkins` → `GitVerse CI/CD` → `SourceCraft CI/CD`;
5. место исполнения: локальный Docker → GitHub-hosted runner → VM/self-hosted runner → отдельный agent server.

**Критерии успеха всего проекта:**

1. УС-1. Локальный Docker-пилот: OpenHands запускается на компьютере Максима, подключается к модели, меняет файлы в песочнице и запускает проверки.
2. УС-2. Автономный поток: задача проходит путь «issue → PR» без участия Максима между запуском и проверкой.
3. УС-3. OpenHands + DeepSeek V4 Flash работает как первый дешёвый Engine.
4. УС-4. Система имеет единый конфигурационный слой: смена агента, модели или CI не требует переписывать методологию.
5. УС-5. В production агенты получают не настоящие provider API keys, а virtual keys через LLM Hub или аналогичный gateway.
6. УС-6. Не менее 3 из 5 пилотных PR принимаются с первой или второй попытки.
7. УС-7. Merge любого PR выполняется только человеком.
8. УС-8. Опыт накапливается в единых агентных правилах, а не размазывается по разным инструментам.

---

## 3. Границы проекта

### 3.1. Делаем в версии 1.2

1. Запускаем первый практический MVP локально: Windows/WSL2 + Docker Desktop + OpenHands.
2. Подключаем модель DeepSeek напрямую для первых тестов.
3. Готовим архитектуру под LLM Hub, чтобы позже не передавать агентам настоящие API-секреты провайдеров.
4. Унифицируем систему под разные агенты через Agent Adapter.
5. Унифицируем систему под разные модели через Model Profile / Model Adapter.
6. Унифицируем систему под разные CI через CI Adapter: GitHub Actions, GitLab CI, Jenkins, GitVerse CI/CD, SourceCraft CI/CD.
7. Оставляем OpenHands первым Engine, потому что он быстрее всего приводит к результату.
8. Создаём единый канон правил `docs/agent-system/AGENT_RULES.md`.
9. Создаём адаптерные файлы: `AGENTS.md`, `.openhands/microagents/repo.md`, `QWEN.md`, `CLAUDE.md`.
10. Встраиваем lightweight solo-operator mode: один PR — одна задача, human merge, Git provider как источник правды.
11. Проводим пилот на `agent-sandbox`, затем на `verification`.

### 3.2. Не делаем в версии 1.2

1. Не строим сразу полноценную платформу с UI, очередью задач и своим сервером Dispatcher.
2. Не запускаем локальную LLM на GPU, пока нет жёсткого требования не отправлять код наружу.
3. Не даём агентам admin-доступ к репозиториям.
4. Не разрешаем агентам merge.
5. Не подключаем приватные данные клиентов в пилоте.
6. Не переносим всё сразу в GitVerse/SourceCraft — сначала доказываем контракт локально и в GitHub, затем добавляем новые CI.
7. Не покупаем VM до тех пор, пока локальный Docker и первый CI-пилот не покажут, какие ресурсы реально нужны.

---

## 3A. Архитектурные слои системы

Система строится слоями. Каждый слой можно заменить без переписывания всей методологии.

```text
[Разговор / Оркестратор]
        ↓
[Task Layer: Issue / Task Manifest]
        ↓
[Dispatcher]
        ↓
[Execution Adapter: Local Docker / CI Adapter / VM Runner]
        ↓
[Agent Adapter: OpenHands / Qwen Code / Codex / Claude Code]
        ↓
[LLM Hub / Model Adapter: DeepSeek / OpenAI / Anthropic / Qwen / Local]
        ↓
[Branch + Commit + PR/MR]
        ↓
[Reviewer Agent + Human Review]
        ↓
[Human Merge]
```

### 3A.1. Task Layer

Источник правды о задаче — не чат, а проверяемый объект:

```text
issue или task manifest + trigger + run log + branch + PR/MR
```

Разговор с оркестратором нужен, чтобы сделать задачу качественной. Но запуск должен оставлять след в Git provider / CI.

### 3A.2. Execution Layer

| Режим | Когда использовать | Статус в v1.2 |
|---|---|---|
| Local Docker | Первый запуск, обучение, ручной контроль | Основной стартовый режим |
| GitHub Actions | Первый автономный issue → PR | Второй слой после локального теста |
| GitLab CI | Альтернатива для GitLab-проектов | Адаптер проектируется, не MVP |
| Jenkins | Корпоративный/self-hosted контур | Адаптер проектируется, не MVP |
| GitVerse CI/CD | Российская Git/CI-платформа, self-hosted/cloud runners | Адаптер проектируется для полноты |
| SourceCraft CI/CD | Yandex SourceCraft, `.sourcecraft/ci.yaml`, workers | Адаптер проектируется для полноты |
| VM runner | Когда ноутбук жалко или нужны ресурсы | После локального/CI пилота |
| Agent server | Когда нужна очередь задач и несколько агентов | Отдельный будущий мини-проект |

### 3A.3. Agent Layer

Базовые роли:

| Роль | Первый выбор | Альтернативы |
|---|---|---|
| Engine | OpenHands | Qwen Code, Codex, Claude Code, GitHub Copilot coding agent |
| Reviewer | ChatGPT/Codex/Claude/human | Qwen review, статический анализатор, OpenHands Critic |
| Dispatcher | Оркестратор + workflow | GitHub Action, GitLab job, Jenkins pipeline, отдельный сервис |

Правило: **Engine пишет код, Reviewer проверяет, человек мержит.**

### 3A.4. Model Layer

Модель не должна быть зашита в workflow. Используются профили:

```text
model/cheap       → дешёвая модель для простых задач
model/strong      → сильная модель для сложных задач
model/reviewer    → модель для ревью
model/local       → локальная модель, если нельзя отправлять код наружу
```

В MVP профили могут указывать напрямую на DeepSeek. В production они должны указывать на LLM Hub.

### 3A.5. CI Layer

CI не должен содержать бизнес-логику проекта. CI только запускает стандартный контракт:

```text
trigger → checkout → install agent → configure LLM → run agent → run checks → create/update PR/MR → upload artifacts
```

---

## 4. Карта этапов

| Этап | Название | Результат этапа | Первый вариант | Следующий вариант |
|---|---|---|---|---|
| 0 | Локальный Docker-контур | Docker/WSL/git готовы | Windows + WSL2 + Docker Desktop | VM Docker host |
| 1 | Контур моделей | Есть рабочий ключ модели | DeepSeek напрямую | LLM Hub + virtual keys |
| 2 | Первый Agent Adapter | OpenHands работает локально | `openhands serve` через Docker | headless / resolver |
| 3 | Песочница | Первый PR от агента | `agent-sandbox` через UI | issue → PR |
| 4 | Автономный конвейер | Метка/комментарий запускает PR | GitHub Actions | GitLab/Jenkins/GitVerse/SourceCraft |
| 5 | Унификация правил | Единые правила для агентов | AGENT_RULES + OpenHands adapter | Qwen/Codex/Claude adapters |
| 6 | Пилот на `verification` | 5 боевых задач | OpenHands + DeepSeek | LLM Hub + fallback models |
| 7 | Накопление знаний | Правила растут после ошибок | Markdown rules | RAG позже |
| 8 | LLM Hub | Агенты не видят provider keys | LiteLLM локально/VM | Production gateway |
| 9 | VM / self-hosted | Ноутбук не нагружается | Не покупаем сразу | Hetzner/DO/Yandex/локальный мини-сервер |

---

# БЛОК A. СТОРОНА ВЛАДЕЛЬЦА: ЗАЧЕМ И СКОЛЬКО СТОИТ

## A1. Какую проблему решаем

Сейчас разработка держится на ручной оркестровке: надо собирать задачу, копировать контекст, следить за выполнением, вручную переносить результаты. Это медленно, плохо масштабируется и слабо накапливает опыт.

Целевое состояние:

```text
поговорил с оркестратором → получил issue/task manifest → агент сделал PR → reviewer проверил → Максим merge
```

Версия 1.2 специально начинает с локального Docker, потому что это самый быстрый способ:

1. увидеть, как агент реально работает;
2. проверить модель и расходы;
3. понять ограничения ноутбука;
4. не платить за VM заранее;
5. подготовить правила до автономного CI.

## A2. Бизнес-цели

1. БЦ-1. Снизить стоимость выполнения типовой задачи разработки минимум в 10 раз против дорогих ручных сессий.
2. БЦ-2. Убрать необходимость постоянного присутствия после перехода к issue → PR.
3. БЦ-3. Запускать несколько задач параллельно после перехода к CI/VM.
4. БЦ-4. Сохранить контроль качества: каждый PR проходит review и human merge.
5. БЦ-5. Не попасть в vendor lock-in: агент, модель и CI должны быть заменяемыми.
6. БЦ-6. Снизить риск утечки API-секретов через LLM Hub / virtual keys.

## A3. Экономика

### A3.1. MVP-экономика

Первый MVP:

```text
OpenHands локально через Docker
+ DeepSeek API напрямую
+ тестовый репозиторий agent-sandbox
+ ручной review
```

Цены DeepSeek API (проверено 2026-07-04 на официальном сайте):

| Модель | Вход (1 млн токенов) | Вход при кэш-попадании | Выход (1 млн токенов) |
|---|---|---|---|
| `deepseek-v4-flash` — `model/cheap` | $0.14 | $0.0028 | $0.28 |
| `deepseek-v4-pro` — `model/strong` | $0.435 | $0.003625 | $0.87 |

Обе модели: контекст 1 млн токенов, вывод до 384 тыс. токенов, поддержка tool calls. Новым аккаунтам DeepSeek начисляет 5 млн бесплатных токенов — хватит на этапы 0–3.

Ориентир себестоимости типовой задачи: 1–3 млн токенов входа (повторное чтение файлов дёшево за счёт кэша) и 0.1–0.3 млн выхода — **примерно $0.2–0.8 за задачу**. Бюджет всего проекта до конца пилота: $10–15. VM на старте не нужна.

### A3.2. Production-экономика

Production-контур:

```text
агенты → LLM Hub → разные провайдеры моделей
CI/VM → изолированный runner
usage/cost tracking → таблица метрик
```

Ключевая экономическая идея: сначала дешёвый `model/cheap`, потом fallback на `model/strong` только если первая попытка не справилась.

### A3.3. Решение по VM

VM не покупаем в начале. Сначала проверяем:

1. тянет ли ноутбук локальный Docker;
2. достаточно ли качества OpenHands + выбранной модели;
3. есть ли реальная потребность в фоновой работе без ноутбука;
4. сколько места и RAM нужно в типовых задачах.

Если после пилота нужна VM, минимальная конфигурация:

```text
OS: Ubuntu 24.04 LTS
CPU: 4 vCPU минимум, 8 vCPU комфортно
RAM: 8 GB минимум, 16 GB комфортно
Disk: 80 GB минимум, 160 GB комфортно
Docker: обязателен
SSH: только ключом
Пользователь: отдельный user agent
```

GPU не нужен, пока модели вызываются по API. GPU понадобится только для локальной LLM.

## A4. Контрольные точки владельца

| Точка | После этапа | Что лично проверить | Решение |
|---|---|---|---|
| КТ-1 | Этап 0 | Docker работает в WSL2; `docker run hello-world` проходит | Продолжать / чинить Docker |
| КТ-2 | Этап 2 | OpenHands открывается локально, отвечает через модель, видны расходы | Продолжать / чинить модель |
| КТ-3 | Этап 3 | В `agent-sandbox` появился первый PR от агента | Продолжать / улучшить задачу |
| КТ-4 | Этап 4 | Issue с trigger превращается в PR без ручной работы | Продолжать / чинить CI |
| КТ-5 | Этап 6 | 5 задач пилота: стоимость, время, качество | Масштабировать / менять профиль |
| КТ-6 | Этап 8 | LLM Hub выдаёт virtual key; агент не видит provider key | Перевести production на Hub |

---

# БЛОК B. СТОРОНА ОПЕРАТОРА: КАК РАБОТАТЬ КАЖДЫЙ ДЕНЬ

## B1. Ежедневный цикл после локального запуска

Локальный Docker-режим нужен для обучения и первых задач:

1. Открыть WSL/Ubuntu.
2. Перейти в папку проекта.
3. Запустить OpenHands через Docker-команду `openhands serve --mount-cwd`.
4. Открыть `http://localhost:3000`.
5. Дать агенту маленькую задачу.
6. Проверить diff, тесты, итог.
7. Если всё хорошо — сделать PR или попросить агента открыть PR.
8. Зафиксировать уроки в правилах агента.

## B2. Ежедневный цикл после перехода к автономному CI

1. Открыть Git provider → репозиторий → Issues/Tasks.
2. Создать задачу по шаблону.
3. Выбрать профиль: агент, модель, целевая ветка, CI.
4. Запустить Engine через label/comment/manual pipeline.
5. Заниматься своими делами.
6. Получить PR/MR.
7. Проверить PR по чек-листу.
8. Если PR хороший — merge. Если нет — комментарий агенту или закрытие PR.
9. Записать стоимость, время, попытку принятия.

## B3. Шаблон issue / task

Правило: одна issue — одна задача — один PR.

```markdown
## Что нужно сделать
[1–3 предложения простым языком: какой результат нужен]

## Где
[какие файлы или какая часть проекта затрагивается, если известно]

## Что должно получиться (критерии приёмки)
1. [проверяемый пункт]
2. [проверяемый пункт]

## Чего делать нельзя
- Не менять файлы вне описанной области
- Не удалять существующие тесты
- Не добавлять секреты в файлы, issue, PR или логи

## Профиль запуска
- Agent: openhands
- Model profile: model/cheap
- Target branch: developer
- PR mode: draft
```

Плохие задачи: «сделай красиво», «улучши всё», «перепиши проект», «разберись сам», задача без критериев приёмки.

## B4. Как проверять PR, не будучи программистом

1. Прочитать описание PR: совпадает ли с задачей?
2. Открыть `Files changed`: изменены только ожидаемые файлы?
3. Посмотреть проверки CI: зелёные или красные?
4. Проверить, что нет секретов, токенов, `.env`, лишних бинарников.
5. Попросить Reviewer: «проверь PR по issue и найди риски».
6. Если сомневаешься — не принимать. Написать замечание агенту.

## B5. Что делать, когда PR плохой

1. Мелкая правка: комментарий агенту в PR.
2. Агент ушёл не туда: закрыть PR, переписать issue точнее, запустить заново.
3. Ошибка повторяется: добавить правило в `docs/agent-system/AGENT_RULES.md` и адаптерный файл нужного агента.
4. Модель слабая: поднять `MODEL_PROFILE` с `model/cheap` на `model/strong`.
5. Агент не подходит: попробовать другой Agent Adapter.

## B6. Разговор → запуск агента

Целевой режим:

```text
Максим говорит с оркестратором обычным текстом
→ оркестратор превращает разговор в issue/task manifest
→ Максим подтверждает запуск (safe mode) или заранее разрешает fast mode
→ Dispatcher выбирает agent/model/ci
→ агент делает PR
```

Режимы:

```text
safe mode:
оркестратор готовит issue → Максим подтверждает → запускается агент

fast mode:
для низкорисковых docs-only задач оркестратор сразу создаёт issue + trigger
```

В v1.2 safe mode является режимом по умолчанию.

---

# БЛОК C. ИСПОЛНЕНИЕ: ЭТАПЫ И ШАГИ

## Этап 0. Локальный Docker-контур

Цель этапа — подготовить компьютер Максима так, чтобы OpenHands запускался локально через Docker и мог безопасно работать с тестовым репозиторием.

### Шаг 0.1. Зафиксировать стартовый режим

**Что делаем.** Принимаем решение: первый практический запуск — локальный Docker.

**Как делаем.**

1. Не покупаем VM до конца Этапа 3.
2. Не запускаем сразу GitHub/GitVerse/SourceCraft CI.
3. Сначала проверяем локально: Docker → OpenHands → модель → песочница → первый PR.

**Критерий “сделано”.** В `DECISION_LOG.md` добавлена запись: «v1.2: стартуем с локального Docker, CI/VM — после локального пилота».

**Если не получилось.** Если ноутбук явно не тянет Docker/OpenHands, перейти к Этапу 9 раньше.

### Шаг 0.2. Проверить WSL2

**Что делаем.** Убеждаемся, что на Windows включена подсистема Linux версии 2.

**Как делаем.** Открыть PowerShell и выполнить:

```powershell
wsl --version
wsl --list --verbose
```

Если WSL2 не установлен, PowerShell от имени администратора:

```powershell
wsl --install -d Ubuntu
```

После установки перезагрузить компьютер, открыть Ubuntu, задать пользователя и пароль.

**Критерий “сделано”.** `wsl --list --verbose` показывает Ubuntu с версией 2.

**Если не получилось.** Ошибка про виртуализацию → включить Intel VT-x / AMD SVM в BIOS/UEFI.

### Шаг 0.3. Установить Docker Desktop

**Что делаем.** Ставим Docker Desktop и включаем интеграцию с WSL2.

**Как делаем.**

1. Установить Docker Desktop для Windows.
2. Docker Desktop → Settings → General → включить `Use the WSL 2 based engine`.
3. Docker Desktop → Settings → Resources → WSL Integration → включить интеграцию с Ubuntu.
4. В Ubuntu выполнить:

```bash
docker run hello-world
```

**Критерий “сделано” (КТ-1).** Команда печатает `Hello from Docker!`.

**Если не получилось.**

- `docker: command not found` → перезапустить Docker Desktop и открыть новый терминал Ubuntu.
- `permission denied` → выполнить `sudo usermod -aG docker $USER`, выйти и зайти заново.
- Docker socket недоступен → проверить настройки Docker Desktop Advanced / WSL Integration.

### Шаг 0.4. Подготовить рабочую папку в WSL

**Что делаем.** Храним проекты в Linux-файловой системе WSL, а не в `/mnt/c`, чтобы Docker и git работали быстрее.

**Как делаем.** В Ubuntu:

```bash
mkdir -p ~/workspace
cd ~/workspace
```

**Критерий “сделано”.** Рабочая папка `~/workspace` существует.

**Если не получилось.** Проверить, что команды выполняются именно в Ubuntu, а не в PowerShell.

### Шаг 0.5. Проверить git и доступ к GitHub

**Что делаем.** Убеждаемся, что из Ubuntu виден GitHub-аккаунт.

**Как делаем.**

```bash
git --version
git ls-remote https://github.com/MaximKolomeets/agent-system-development.git HEAD
```

**Критерий “сделано”.** Команды проходят без ошибок.

**Если не получилось.** Для приватных репозиториев нужен fine-grained PAT. Минимальные права для bot/user-токена в будущем: `Contents`, `Issues`, `Pull requests`, при необходимости `Workflows`; без admin и без bypass branch protection.

### Шаг 0.6. Правило секретов на локальном компьютере

**Что делаем.** Заранее исключаем случайную утечку ключей.

**Как делаем.**

1. API-ключи хранить в менеджере паролей.
2. Не вставлять ключи в `.md`, issue, PR, README, код.
3. Если создаётся `.env`, сразу добавить `.env` в `.gitignore`.
4. В репозитории хранить только `.env.example` без реальных значений.
5. При любом подозрении на утечку — отозвать ключ и создать новый.

**Критерий “сделано”.** В каждом пилотном репозитории есть `.gitignore`, где запрещены `.env`, `.openhands/secrets*`, временные логи.

---

## Этап 1. Контур моделей: DeepSeek сейчас, LLM Hub позже

### Шаг 1.1. Создать API-ключ DeepSeek

**Что делаем.** Получаем первый ключ модели для локального MVP.

**Как делаем.**

1. Открыть `https://platform.deepseek.com`.
2. Зарегистрироваться / войти.
3. Проверить Billing / Usage.
4. Создать API key с именем `openhands-local-mvp`.
5. Сохранить ключ в менеджере паролей.

**Критерий “сделано”.** Ключ `sk-...` сохранён не в репозитории.

**Если не получилось.** Использовать другой провайдер модели, совместимый с OpenHands/LiteLLM, но не менять архитектуру.

### Шаг 1.2. Проверить ключ

**Что делаем.** Один тестовый запрос.

**Как делаем.** В Ubuntu:

```bash
export DEEPSEEK_API_KEY='sk-ВАШ_КЛЮЧ'

curl https://api.deepseek.com/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $DEEPSEEK_API_KEY" \
  -d '{"model":"deepseek-v4-flash","messages":[{"role":"user","content":"Ответь одним словом: работаешь?"}]}'
```

**Критерий “сделано”.** Пришёл JSON с ответом модели.

**Если не получилось.** 401 → ключ неверный; 402 → баланс/лимит; network error → проверить доступ из WSL.

**Примечание.** Использовать только новые имена моделей `deepseek-v4-flash` / `deepseek-v4-pro`: старые имена `deepseek-chat` и `deepseek-reasoner` отключаются 24.07.2026 и не должны встречаться в наших настройках.

### Шаг 1.3. Зафиксировать модельные профили

**Что делаем.** Не привязываем задачи к конкретным моделям.

**Как делаем.** Создать файл:

```text
docs/agent-system/model-profiles.md
```

Начальный вариант:

```markdown
# Model Profiles

| Profile | MVP model | Purpose |
|---|---|---|
| model/cheap | deepseek/deepseek-v4-flash | docs, простые bugfix, маленькие задачи |
| model/strong | deepseek/deepseek-v4-pro | сложные изменения, refactor, архитектура |
| model/reviewer | codex/claude/chatgpt по выбору | независимое ревью PR |
| model/local | local/qwen3-coder-or-other | код нельзя отправлять внешнему API |
```

**Критерий “сделано”.** В задачах используется `MODEL_PROFILE`, а не только жёсткое имя модели.

### Шаг 1.4. Прямой API — только MVP-режим

**Что делаем.** Фиксируем границу.

```text
MVP:
LLM_BASE_URL = https://api.deepseek.com
LLM_API_KEY = настоящий ключ DeepSeek
LLM_MODEL = deepseek/deepseek-v4-flash

Production:
LLM_BASE_URL = https://llm-hub.example.com/v1
LLM_API_KEY = virtual key
MODEL_PROFILE = model/cheap
```

**Критерий “сделано”.** В документе и адаптерах явно написано: provider key не раздаётся агентам в production.

---

## Этап 2. Первый Agent Adapter: OpenHands локально через Docker

OpenHands остаётся первым Agent Adapter, потому что быстрее всего приводит к практическому результату: локальный UI, Docker runtime, чтение/изменение файлов, запуск команд, PR-контур.

### Шаг 2.1. Установить `uv`

**Что делаем.** Ставим `uv`, через который удобно установить OpenHands CLI.

**Как делаем.** В Ubuntu:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc
uv --version
```

**Критерий “сделано”.** `uv --version` печатает версию.

**Если не получилось.** Закрыть и открыть Ubuntu, затем повторить `uv --version`.

### Шаг 2.2. Установить OpenHands

**Как делаем.**

```bash
uv tool install openhands --python 3.12
source ~/.bashrc
openhands --version || true
```

**Критерий “сделано”.** Команда `openhands` доступна.

**Если не получилось.** Проверить `~/.local/bin` в PATH или выполнить `source ~/.bashrc`.

### Шаг 2.3. Запустить OpenHands GUI через Docker

**Что делаем.** Запускаем локальный OpenHands. Команда `openhands serve` сама использует Docker: проверяет Docker, скачивает образы, поднимает GUI и открывает порт `3000`.

**Как делаем.**

```bash
cd ~/workspace
openhands serve
```

Открыть в браузере:

```text
http://localhost:3000
```

**Критерий “сделано”.** Открылся интерфейс OpenHands.

**Если не получилось.**

- Docker daemon not running → запустить Docker Desktop.
- Permission denied → проверить права Docker в WSL.
- Port 3000 busy → остановить конфликтующий процесс.

### Шаг 2.4. Запуск с доступом к текущему проекту

**Что делаем.** Даём OpenHands доступ только к конкретной папке проекта, а не ко всему диску.

**Как делаем.**

```bash
cd ~/workspace/agent-sandbox
openhands serve --mount-cwd
```

Внутри контейнера текущая папка будет доступна как `/workspace`.

**Критерий “сделано”.** Агент видит только выбранный проект.

**Если не получилось.** Проверить, что проект лежит в WSL (`~/workspace/...`), а не в `/mnt/c/...`.

### Шаг 2.5. Настроить LLM в OpenHands

**Что делаем.** Подключаем DeepSeek к OpenHands.

**Как делаем.** В интерфейсе OpenHands:

1. Settings → LLM.
2. Включить Advanced, если нужно.
3. Указать:

```text
Custom Model: deepseek/deepseek-v4-flash
Base URL: https://api.deepseek.com
API Key: sk-...
```

**Критерий “сделано”.** Настройки сохранены, тестовый запрос проходит.

**Если не получилось.** Проверить пробелы в ключе, модельное имя, Base URL.

### Шаг 2.6. Первый локальный разговор

**Как делаем.** В OpenHands создать новый разговор и дать задачу:

```text
Создай файл hello.py, который печатает текущую дату, запусти его и покажи результат.
Работай только в текущей папке /workspace.
```

**Критерий “сделано” (КТ-2).** Агент создал файл, запустил его и показал результат; в кабинете модели видно usage.

**Если не получилось.** Сделать задачу ещё меньше: «создай hello.txt с текстом test».

### Шаг 2.7. Остановить OpenHands

**Как делаем.** В терминале, где запущен `openhands serve`, нажать `Ctrl+C`.

**Критерий “сделано”.** Контейнеры остановлены, порт 3000 свободен.

---

## Этап 3. Первая задача в песочнице

### Шаг 3.1. Создать тестовый репозиторий

**Что делаем.** Создаём безопасную песочницу.

**Как делаем.**

1. GitHub → New repository.
2. Имя: `agent-sandbox`.
3. Видимость: Private.
4. Add README.
5. Clone в WSL:

```bash
cd ~/workspace
git clone https://github.com/MaximKolomeets/agent-sandbox.git
cd agent-sandbox
```

**Критерий “сделано”.** Репозиторий есть локально и на GitHub.

### Шаг 3.2. Запустить OpenHands на песочнице

```bash
cd ~/workspace/agent-sandbox
openhands serve --mount-cwd
```

Открыть `http://localhost:3000`.

**Критерий “сделано”.** Агент видит файлы `agent-sandbox`.

### Шаг 3.3. Дать агенту первую задачу

Скопировать в OpenHands:

```text
Работай только в текущем репозитории.
Создай файл calculator.py с функциями add, subtract, multiply, divide.
Добавь файл test_calculator.py с pytest-тестами для каждой функции, включая деление на ноль.
Запусти тесты и убедись, что все проходят.
Создай ветку work/engine/sandbox-01, закоммить изменения.
Если можешь открыть Pull Request в main — открой. Если не можешь, напиши точные команды, которые нужно выполнить вручную.
```

**Критерий “сделано” (КТ-3).** Есть ветка и изменения; тесты проходят; PR открыт агентом или подготовлены команды для PR.

**Если не получилось.** Упростить задачу: только `calculator.py`, без PR. Затем добавить тесты отдельной задачей.

### Шаг 3.4. Принять первый PR

**Как делаем.**

1. Открыть PR.
2. Проверить файлы.
3. Проверить тесты.
4. Merge только если всё понятно.
5. Записать стоимость и время.

**Критерий “сделано”.** Первый агентный PR принят или осознанно закрыт с выводами.

### Шаг 3.5. Записать уроки локального пилота

Создать/обновить:

```text
docs/agent-system/LOCAL_DOCKER_PILOT_NOTES.md
```

Записать:

1. что сработало;
2. что сломалось;
3. сколько стоило;
4. сколько заняло времени;
5. какие правила добавить агентам.

---

## Этап 4. Автономный конвейер issue → PR через CI Adapter

Этот этап начинается после локального Docker-пилота. Его цель — убрать необходимость держать OpenHands UI открытым и перейти к запуску через issue/label/comment/manual CI.

### Шаг 4.1. Общий контракт CI Adapter

Любой CI должен выполнять одинаковый контракт:

```text
1. trigger
2. checkout
3. install agent
4. load rules
5. configure LLM endpoint
6. run agent
7. run tests/checks
8. create or update PR/MR
9. upload logs/artifacts
10. comment result back to issue/PR/task
```

**Критерий “сделано”.** Все CI-адаптеры описываются через один контракт.

### Шаг 4.2. GitHub Actions Adapter — первый автономный вариант

**Что делаем.** Подключаем OpenHands resolver в `agent-sandbox`.

**Как делаем.**

1. Открыть официальный README OpenHands resolver.
2. Взять актуальный YAML оттуда.
3. Создать `.github/workflows/openhands-resolver.yml`.
4. Настроить repository settings:

```text
Settings → Actions → General → Workflow permissions:
- Read and write permissions
- Allow GitHub Actions to create and approve pull requests
```

5. Secrets:

```text
LLM_API_KEY      = DeepSeek key в MVP или virtual key LLM Hub в production
LLM_BASE_URL     = https://api.deepseek.com или LLM Hub endpoint
PAT_TOKEN        = bot/user token
PAT_USERNAME     = bot/user name
```

6. Variables:

```text
AGENT_ENGINE          = openhands
MODEL_PROFILE         = model/cheap
LLM_MODEL             = deepseek/deepseek-v4-flash
TARGET_BRANCH         = main для песочницы, developer для боевых проектов
AGENT_MAX_ITER        = 50
OPENHANDS_MAX_ITER    = 50
JOB_TIMEOUT_MINUTES   = 60
PR_MODE               = draft
```

7. Добавить label `fix-me`.

**Важно про переменные.** Штатный резолвер OpenHands читает только свои настройки: `LLM_MODEL`, `LLM_API_KEY`, `LLM_BASE_URL`, `OPENHANDS_MAX_ITER`, `OPENHANDS_MACRO`, `OPENHANDS_BASE_CONTAINER_IMAGE`, `TARGET_BRANCH`, `TARGET_RUNNER`, `PAT_TOKEN`, `PAT_USERNAME`. Переменные `AGENT_ENGINE`, `MODEL_PROFILE`, `PR_MODE`, `JOB_TIMEOUT_MINUTES`, `AGENT_MAX_ITER` — наша собственная конвенция для будущего Dispatcher и других CI Adapter; штатный резолвер их молча игнорирует. Ждать от `PR_MODE=draft` эффекта в штатном резолвере нельзя — поведение PR задаётся самим резолвером. Точный список поддерживаемых настроек сверять с README резолвера.

**Критерий “сделано”.** Issue с `fix-me` запускает action и создаёт PR.

**Если не получилось.** Проверить логи action, имена secrets/variables, permissions, баланс модели.

### Шаг 4.3. GitHub bot-user / PAT

**Правило.** Не использовать основной личный PAT Максима как постоянный ключ агента.

Production-вариант:

```text
User: maxim-agent-bot или machine-user
Scope: только нужные репозитории
Permissions:
- Contents: read/write
- Issues: read/write
- Pull requests: read/write
- Workflows: read/write, только если действительно нужно
Forbidden:
- Admin
- bypass branch protection
- secret management
- organization owner права
```

**Критерий “сделано”.** Агентный токен не может мержить в защищённые ветки и не имеет admin-прав.

### Шаг 4.4. GitHub branch protection

В боевых репозиториях включить защиту `main` и `developer`:

1. запрет прямого push;
2. merge только через PR;
3. required checks;
4. запрет force-push;
5. bot-user не имеет bypass.

**Критерий “сделано”.** Даже при ошибке агента он не может сломать стабильную ветку напрямую.

### Шаг 4.5. Первый автономный прогон

Создать issue:

```markdown
## Что нужно сделать
Добавить в calculator.py функцию power(a, b).

## Что должно получиться
1. Функция power(a, b) в calculator.py.
2. Тесты на неё в test_calculator.py, включая отрицательную степень.
3. Все тесты проходят.

## Чего делать нельзя
- Не менять существующие функции.
- Не удалять тесты.

## Профиль запуска
- Agent: openhands
- Model profile: model/cheap
- Target branch: main
```

Повесить label `fix-me`.

**Критерий “сделано” (КТ-4).** PR появился без ручного запуска OpenHands UI.

### Шаг 4.6. GitLab CI Adapter — будущая реализация

Стандартный контракт:

```text
Trigger: issue label/comment, MR event или manual pipeline с ISSUE_ID
Config file: .gitlab-ci.yml
Secrets: GitLab CI/CD variables в UI, не в .gitlab-ci.yml
Output: branch + merge request
Target branch: developer
```

Минимальная идея job:

```yaml
agent_engine:
  image: python:3.12
  variables:
    AGENT_ENGINE: "openhands"
    MODEL_PROFILE: "model/cheap"
  script:
    - pip install uv
    - uv tool install openhands --python 3.12
    - echo "Run agent adapter here"
  timeout: 1h
```

**Критерий “сделано”.** GitLab adapter doc создан, но не обязателен для MVP.

### Шаг 4.7. Jenkins Adapter — будущая реализация

Стандартный контракт:

```text
Trigger: webhook из GitHub/GitLab/GitVerse/SourceCraft или ручной build с ISSUE_ID
Config file: Jenkinsfile
Secrets: Jenkins Credentials + withCredentials, не Jenkinsfile
Output: branch + PR/MR через git provider API
```

Минимальная структура:

```groovy
pipeline {
  agent any
  options { timeout(time: 60, unit: 'MINUTES') }
  stages {
    stage('Checkout') { steps { checkout scm } }
    stage('Run Agent') {
      steps {
        withCredentials([string(credentialsId: 'llm-virtual-key', variable: 'LLM_API_KEY')]) {
          sh 'echo Run agent adapter here'
        }
      }
    }
  }
}
```

**Критерий “сделано”.** Jenkins adapter doc создан, но не обязателен для MVP.

### Шаг 4.8. GitVerse CI/CD Adapter — будущая реализация

**Зачем добавляем.** GitVerse — отдельная Git/CI-платформа. Для полноты архитектуры она должна вписываться в тот же CI Adapter contract.

**Факты адаптера:**

```text
Config path: .gitverse/workflows/*.yaml
Также GitVerse runner может обрабатывать workflow YAML из .github/workflows/.
Runner types: cloud / self-hosted / organization runners
Trigger: push, merge request, schedule, manual/other supported GitVerse events
Output: branch + request/merge request в GitVerse
```

**Важно.** По текущей документации GitVerse CI/CD поддерживает `workflow_dispatch` и частично `pull_request`, но `issues`, `issue_comment` и `label` перечислены как неподдерживаемые триггеры. Поэтому OpenHands-style `issue label fix-me → PR` нельзя считать нативным для GitVerse без дополнительного Dispatcher. Используем один из вариантов:

1. manual workflow с параметром `ISSUE_ID`;
2. webhook → внешний Dispatcher → GitVerse workflow;
3. push в специальную branch/task-manifest;
4. scheduled poller, который смотрит задачи с меткой через API.

Минимальная структура адаптера:

```yaml
name: agent-engine

on:
  push:
    branches: ["agent-tasks/**"]

jobs:
  run-agent:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run agent adapter
        run: |
          echo "AGENT_ENGINE=${AGENT_ENGINE:-openhands}"
          echo "Run OpenHands/Qwen/Codex adapter here"
```

**Критерий “сделано”.** Создан `docs/agent-system/adapters/ci-gitverse.md` с точным способом trigger для выбранного репозитория.

### Шаг 4.9. SourceCraft CI/CD Adapter — будущая реализация

**Зачем добавляем.** SourceCraft — отдельная платформа разработки с Git, PR, issues и CI/CD. Её CI хранится в `.sourcecraft/ci.yaml` и поддерживает workflows/tasks/cubes.

**Факты адаптера:**

```text
Config path: .sourcecraft/ci.yaml
Trigger: pull_request, push, schedule, manual run
Execution unit: workflow → task → cube
Secrets: SourceCraft secrets; sensitive данные не хранить в env
Дополнительно: SourceCraft CI/CD поддерживает GitHub Actions и GitLab pipeline syntax через cloud workers
Output: branch + pull request в SourceCraft
```

Минимальная структура адаптера:

```yaml
on:
  pull_request:
    - workflows: [agent-review]
      filter:
        target_branches: ["developer"]

workflows:
  agent-review:
    tasks:
      - name: run-agent-review
        cubes:
          - name: run-agent
            image: python:3.12
            script:
              - pip install uv
              - echo "Run agent adapter here"
```

**Важно.** Для полноценного `issue → PR` нужно выбрать trigger:

1. SourceCraft issue/label event, если доступен в выбранном окружении;
2. manual workflow с параметром задачи;
3. webhook в внешний Dispatcher;
4. task manifest в branch.

**Критерий “сделано”.** Создан `docs/agent-system/adapters/ci-sourcecraft.md` с выбранным trigger и способом хранения secrets.

### Шаг 4.10. CI Adapter matrix

| CI | Config file | Trigger MVP | Secrets | Output | Статус |
|---|---|---|---|---|---|
| GitHub Actions | `.github/workflows/*.yml` | issue label/comment через OpenHands resolver | GitHub Secrets | PR | Первый автономный вариант |
| GitLab CI | `.gitlab-ci.yml` | manual pipeline/MR/issue integration | CI/CD variables UI | MR | Будущий адаптер |
| Jenkins | `Jenkinsfile` | webhook/manual build | Jenkins Credentials | PR/MR | Будущий адаптер |
| GitVerse CI/CD | `.gitverse/workflows/*.yaml` | push/MR/manual/webhook/dispatcher | GitVerse secrets/variables | request/MR | Будущий адаптер |
| SourceCraft CI/CD | `.sourcecraft/ci.yaml` | pull_request/push/schedule/manual/webhook | SourceCraft secrets | PR | Будущий адаптер |

---

## Этап 5. Унификация правил, агентов и методологии

### Шаг 5.1. Зафиксировать lightweight solo-operator mode

**Сохраняем:**

1. одна задача → одна ветка → один PR/MR;
2. merge только человек;
3. секреты только в secrets/Hub/secret manager;
4. issue/task manifest должен иметь критерии приёмки;
5. Git provider и CI logs — источник правды о выполнении.

**Упрощаем:**

1. ручной TASK/RESULT журнал для конвейерных задач не ведём;
2. ветки агента могут называться по правилам resolver/CI;
3. самодостаточный Engine-блок заменяется issue/task manifest;
4. метрики берём из PR, CI logs, Usage/Billing.

**Критерий “сделано”.** Решение записано в `docs/agent-system/DECISION_LOG.md`.

### Шаг 5.2. Создать единый канон правил

Создать:

```text
docs/agent-system/AGENT_RULES.md
```

Начальный вариант:

```markdown
# AGENT_RULES.md

## Язык
- Комментарии в коде, описания PR и отчёты — на русском языке, если задача не требует другого.

## Безопасность
- Никогда не выводи и не сохраняй секреты.
- Не добавляй API-ключи в файлы, issue, PR, логи.
- Не меняй настройки CI/secrets без явного указания.
- Если видишь секрет в коде/логе — остановись и сообщи.

## Работа с кодом
- Одна задача — одна ветка — один PR.
- Не трогай файлы вне области задачи.
- Не удаляй тесты.
- Если тесты падают — чини причину, а не отключай тесты.
- Перед PR запусти доступные проверки.
- Делай минимальный diff.

## Git
- Не делай merge.
- Не делай force-push в защищённые ветки.
- Целевая ветка по умолчанию: developer, если в задаче не указано другое.

## Отчёт
- В PR опиши: что сделано, какие файлы изменены, какие проверки запускались, что не удалось проверить.
```

**Критерий “сделано”.** Файл создан и используется адаптерами.

### Шаг 5.3. Создать адаптерные файлы правил

`AGENTS.md`:

```markdown
# AGENTS.md

Следуй правилам из `docs/agent-system/AGENT_RULES.md`.
Особенно важно: не трогать лишние файлы, не выводить секреты, запускать проверки, не делать merge.
```

`.openhands/microagents/repo.md`:

```markdown
# OpenHands repository instructions

Перед выполнением задачи прочитай и соблюдай `docs/agent-system/AGENT_RULES.md`.
Если правило из задачи конфликтует с `AGENT_RULES.md`, явно укажи конфликт в PR и не обходи безопасность.
```

`QWEN.md`:

```markdown
# Qwen Code instructions

Следуй правилам из `docs/agent-system/AGENT_RULES.md`.
Для каждой задачи делай минимальные изменения и в конце дай отчёт: diff summary, tests, risks.
```

`CLAUDE.md`:

```markdown
# Claude Code instructions

Следуй правилам из `docs/agent-system/AGENT_RULES.md`.
Не меняй файлы вне области задачи без явного разрешения.
```

**Критерий “сделано”.** Каждый агент получает одни и те же правила через свой формат.

### Шаг 5.4. Создать документацию адаптеров

Создать папку:

```text
docs/agent-system/adapters/
```

Файлы:

```text
agent-openhands.md
agent-qwen-code.md
agent-codex.md
agent-claude-code.md
ci-github-actions.md
ci-gitlab.md
ci-jenkins.md
ci-gitverse.md
ci-sourcecraft.md
model-deepseek.md
model-openai.md
model-anthropic.md
model-qwen.md
model-local.md
llm-hub-litellm.md
```

**Критерий “сделано”.** Даже если реализован только OpenHands, все будущие места расширения видны.

### Шаг 5.5. Шаблон issue в репозиторий

Создать:

```text
.github/ISSUE_TEMPLATE/engine-task.md
```

Содержимое — шаблон из B3.

Для GitVerse/SourceCraft позже создать эквивалентные шаблоны задач в их формате.

---

## Этап 6. Пилот на реальном проекте `verification`

### Шаг 6.1. Подготовить `verification` к локальному Docker-пилоту

**Что делаем.** Сначала запускаем агент локально на клоне проекта, но работаем через ветку и PR.

**Как делаем.**

```bash
cd ~/workspace
git clone https://github.com/MaximKolomeets/verification.git
cd verification
git checkout developer
git pull
openhands serve --mount-cwd
```

**Критерий “сделано”.** OpenHands видит проект `verification`, но работает только с текущей папкой.

### Шаг 6.2. Выбрать 5 пилотных задач

Начинать с маленьких задач:

1. docs-only правка;
2. добавление небольшого теста;
3. исправление конкретной ошибки;
4. улучшение README/инструкции;
5. маленький refactor с тестами.

Не начинать с большой архитектуры.

### Шаг 6.3. Выполнить задачи

Для каждой задачи:

1. создать issue;
2. локально попросить OpenHands выполнить задачу в отдельной ветке;
3. открыть PR в `developer`;
4. проверить PR;
5. принять или вернуть на доработку;
6. записать метрики.

**Критерий “сделано”.** 5 задач прошли полный цикл.

### Шаг 6.4. Таблица метрик

| № | Задача / issue | Режим | Agent | Model profile | Время до PR | Стоимость | Попытка принятия | Комментарий |
|---|---|---|---|---|---|---|---|---|
| 1 | | local Docker | OpenHands | model/cheap | | | | |
| 2 | | local Docker | OpenHands | model/cheap | | | | |
| 3 | | local Docker | OpenHands | model/cheap | | | | |
| 4 | | local Docker | OpenHands | model/cheap | | | | |
| 5 | | local Docker | OpenHands | model/cheap | | | | |

**Критерий успеха пилота (КТ-5):** ≥3 из 5 PR приняты с 1–2 попытки; средняя стоимость ≤ $1; нет утечек секретов; нет merge агентом.

### Шаг 6.5. Решение по итогам

1. Успех → подключить GitHub Actions resolver.
2. Частичный успех → улучшить issue template и AGENT_RULES.
3. Модель слабая → `model/strong` для сложных задач.
4. Ноутбук тяжело тянет → Этап 9: VM/self-hosted runner.
5. Нужна защита ключей → Этап 8: LLM Hub.

---

## Этап 7. Накопление знаний

### Шаг 7.1. Цикл обучения после каждой задачи

После каждого плохого PR:

1. определить тип ошибки: постановка / правило проекта / слабая модель / неправильный агент / CI-проблема;
2. если ошибка постановки — улучшить issue template;
3. если ошибка правила — обновить `AGENT_RULES.md`;
4. если слабая модель — сменить `MODEL_PROFILE` на `model/strong`;
5. если неправильный агент — обновить матрицу выбора агента;
6. если CI-проблема — обновить CI Adapter.

### Шаг 7.2. Когда нужен RAG

Полноценный RAG не начинаем до выполнения условий:

1. есть минимум 20–30 завершённых issue/PR;
2. правила в `AGENT_RULES.md` стали длиннее 50 пунктов;
3. агент повторяет ошибки, хотя правила уже есть;
4. появилась потребность искать похожие прошлые задачи.

До этого — Markdown-файлы правил достаточно.

---

## Этап 8. LLM Hub / LLM Gateway

Этот этап нужен, чтобы агенты не получали настоящие API-секреты провайдеров.

### Шаг 8.1. Решение по LLM Hub

Рекомендуемый первый вариант: LiteLLM Proxy как self-hosted LLM Gateway.

Задачи Hub:

1. хранить настоящие provider keys;
2. выдавать агентам virtual keys;
3. ограничивать ключи по бюджету, моделям и сроку жизни;
4. вести usage/cost tracking;
5. поддерживать fallback: дешёвая модель → сильная модель;
6. давать единый OpenAI-compatible endpoint;
7. централизовать логирование и guardrails.

### Шаг 8.2. Минимальный контракт Hub

```text
Agents see:
- LLM_BASE_URL = https://llm-hub.example.com/v1
- LLM_API_KEY = sk-virtual-agent-repo-task
- MODEL_PROFILE = model/cheap

LLM Hub stores:
- DEEPSEEK_API_KEY
- OPENAI_API_KEY
- ANTHROPIC_API_KEY
- QWEN_API_KEY
- local/vLLM/Ollama endpoint, если есть
```

### Шаг 8.3. Локальный тест LLM Hub

Сначала можно поднять Hub локально через Docker Compose, но это **после** OpenHands local Docker MVP. Не смешивать два новых компонента в первом тесте.

Минимальный порядок:

1. OpenHands напрямую к DeepSeek работает.
2. Поднять LiteLLM Proxy локально.
3. Создать virtual key.
4. Переключить OpenHands:

```text
Base URL: http://localhost:4000/v1
API Key: sk-virtual-...
Custom Model: model/cheap или alias, настроенный в Hub
```

5. Повторить задачу из песочницы.

**Критерий “сделано” (КТ-6).** OpenHands работает через Hub; настоящий DeepSeek key не передан агенту.

### Шаг 8.4. Production-правила LLM Hub

1. Master key Hub не хранить в репозиториях.
2. Virtual key выдавать на repo/agent/task или на короткий срок.
3. Для каждого ключа ставить budget/rate limit.
4. Логи Hub не должны содержать секреты.
5. Доступ к UI Hub закрыть паролем/VPN/локальной сетью.
6. Для CI использовать только virtual key.

---

## Этап 9. VM / self-hosted runner / agent server

Этот этап включается только если локальный Docker или GitHub-hosted CI не хватает.

### Шаг 9.1. Когда нужна VM

VM нужна, если:

1. ноутбук перегружается;
2. агенту нужны долгие задачи;
3. хочется запускать задачи, пока компьютер выключен;
4. нужны большие Docker cache/disk;
5. нужно несколько параллельных агентов;
6. надо поднять LLM Hub постоянно.

### Шаг 9.2. Минимальная VM

```text
OS: Ubuntu 24.04 LTS
CPU: 4 vCPU минимум, 8 vCPU комфортно
RAM: 8 GB минимум, 16 GB комфортно
Disk: 80 GB минимум, 160 GB комфортно
Docker Engine: да
User: agent
SSH: key-only
Firewall: SSH + нужные private endpoints
Backups/snapshots: да
```

### Шаг 9.3. Self-hosted runner safety

1. Self-hosted runner только для private repos.
2. Не запускать недоверенные fork PR на self-hosted runner.
3. Отдельный runner group для agent jobs.
4. Отдельный bot-token с минимальными правами.
5. Чистить workspace после job.
6. Периодически пересоздавать VM.
7. Не хранить provider keys на диске VM; использовать Hub/secret manager.

### Шаг 9.4. VM как Docker host, а не “удалённый ноутбук”

Правильная роль VM:

```text
Git provider / CI trigger
→ self-hosted runner на VM
→ Docker job/agent
→ PR/MR
```

Неправильная роль VM:

```text
постоянно заходить руками по SSH и вручную запускать всё как на ноутбуке
```

---

# БЛОК D. УНИВЕРСАЛЬНАЯ КОНФИГУРАЦИЯ: AGENTS / MODELS / CI

## D1. Единые переменные системы

| Переменная | Пример | Где хранить | Зачем |
|---|---|---|---|
| `AGENT_ENGINE` | `openhands`, `qwen-code`, `codex` | variable | Какой агент выполняет задачу |
| `AGENT_ROLE` | `engine`, `reviewer` | variable | Роль запуска |
| `MODEL_PROFILE` | `model/cheap`, `model/strong` | variable | Логическое имя модели |
| `LLM_MODEL` | `deepseek/deepseek-v4-flash` | variable | Конкретная модель в MVP |
| `LLM_BASE_URL` | `https://api.deepseek.com` / Hub endpoint | secret/protected variable | Куда агент отправляет LLM-запросы |
| `LLM_API_KEY` | `sk-...` / `sk-virtual-...` | secret | Ключ модели или virtual key |
| `TARGET_BRANCH` | `developer` | variable | Куда открывать PR/MR |
| `AGENT_MAX_ITER` | `50` | variable | Ограничение шагов агента |
| `OPENHANDS_MAX_ITER` | `50` | variable | OpenHands-specific ограничение |
| `JOB_TIMEOUT_MINUTES` | `60` | variable | Ограничение времени job |
| `AGENT_RUNNER_LABEL` | `ubuntu-latest`, `agent-vm` | variable | Где запускать job |
| `PR_MODE` | `draft`, `ready` | variable | Draft или обычный PR |
| `TASK_ID` | `123` | variable/input | Issue/task номер |
| `TASK_MANIFEST_PATH` | `.agent/tasks/123.yaml` | variable/input | Путь к task manifest |

Правило: настоящие provider keys не должны попадать в agent workflow в production.

## D2. Task Manifest

Файл:

```text
.agent/tasks/<task-id>.yaml
```

Пример:

```yaml
task_id: 123
repo: MaximKolomeets/verification
source: github_issue
source_url: https://github.com/MaximKolomeets/verification/issues/123
agent:
  engine: openhands
  role: engine
model:
  profile: model/cheap
execution:
  mode: local-docker
  ci: none
  target_branch: developer
  pr_mode: draft
limits:
  max_iter: 50
  timeout_minutes: 60
acceptance:
  - Все тесты проходят
  - Изменены только файлы из области задачи
constraints:
  - Не удалять существующие тесты
  - Не добавлять секреты в файлы
```

## D3. Agent Adapter contract

Любой агент должен уметь выполнить общий контракт:

```text
input:
- repository
- issue/task manifest
- target branch
- acceptance criteria
- constraints
- model profile
- max iterations

work:
- прочитать правила проекта
- создать отдельную ветку
- внести изменения
- запустить проверки
- подготовить описание результата

output:
- branch
- PR/MR или инструкции для PR
- summary
- test report
- cost/usage metadata, если доступно
```

## D4. Model Adapter contract

Любой Model Adapter должен предоставить агенту:

```text
- base_url
- api_key или virtual key
- model name / alias
- context limit, если известно
- max output, если известно
- budget/rate limit, если используется Hub
```

## D5. CI Adapter contract

Любой CI Adapter должен описать:

```text
- config file path
- trigger types
- secret storage
- runner/worker types
- how to checkout repo
- how to pass task id / manifest
- how to call agent adapter
- how to create/update PR/MR
- where logs/artifacts live
- how timeout/concurrency are configured
```

## D6. Рекомендуемая структура файлов

```text
.agent/
  tasks/
    .gitkeep

docs/
  master-plan/
    MASTER_PLAN.md
  agent-system/
    AGENT_RULES.md
    DECISION_LOG.md
    LOCAL_DOCKER_PILOT_NOTES.md
    model-profiles.md
    adapters/
      agent-openhands.md
      agent-qwen-code.md
      agent-codex.md
      agent-claude-code.md
      ci-github-actions.md
      ci-gitlab.md
      ci-jenkins.md
      ci-gitverse.md
      ci-sourcecraft.md
      llm-hub-litellm.md

.github/
  ISSUE_TEMPLATE/
    engine-task.md
  workflows/
    openhands-resolver.yml

.openhands/
  microagents/
    repo.md

AGENTS.md
QWEN.md
CLAUDE.md
.env.example
.gitignore
```

---

## 10. Реестр требований

### Общие

1. FR-AG-01. Система должна выполнять задачу разработки от issue/task до PR/MR с минимальным участием человека между запуском и проверкой.
2. FR-AG-02. Первый MVP должен запускаться локально через Docker на компьютере Максима.
3. FR-AG-03. OpenHands является первым Agent Adapter, но не единственным допустимым.
4. FR-AG-04. Система должна поддерживать Agent Adapter abstraction.
5. FR-AG-05. Система должна поддерживать Model Adapter / Model Profile abstraction.
6. FR-AG-06. Система должна поддерживать CI Adapter abstraction.
7. FR-AG-07. Merge любого PR/MR должен выполняться только человеком.
8. FR-AG-08. Один PR/MR должен соответствовать одной задаче.

### Модели и LLM Hub

9. FR-AG-09. В MVP допускается прямой API-ключ модели в локальных настройках/OpenHands/GitHub Secrets.
10. FR-AG-10. Production-контур должен использовать LLM Hub или эквивалентный gateway.
11. FR-AG-11. Агенты в production должны получать virtual keys вместо настоящих provider API keys.
12. FR-AG-12. LLM Hub должен поддерживать учёт расходов минимум по ключу, агенту или репозиторию.
13. FR-AG-13. Смена модели должна требовать изменения профиля/переменной, а не переписывания методологии.

### Конвейер

14. FR-AG-14. Постановка задачи должна выполняться через issue/task manifest с критериями приёмки и ограничениями.
15. FR-AG-15. Запуск Engine должен выполняться через локальный Docker, label/comment, manual pipeline или webhook Dispatcher.
16. FR-AG-16. Результатом работы Engine должен быть PR/MR или подготовленная ветка с инструкцией для PR.
17. FR-AG-17. Доработка по замечаниям должна выполняться в том же PR/MR, если инструмент это поддерживает.
18. FR-AG-18. В репозиториях с веткой `developer` PR/MR агента должны идти в `developer`, а не в `main`.

### CI

19. FR-AG-19. GitHub Actions является первым автономным CI Adapter.
20. FR-AG-20. GitLab CI, Jenkins, GitVerse CI/CD и SourceCraft CI/CD должны быть описаны как совместимые адаптеры одного контракта.
21. FR-AG-21. Все agent jobs должны иметь ограничения по времени и числу шагов.
22. FR-AG-22. Секреты CI должны храниться только в механизме secrets/credentials соответствующего CI.
23. FR-AG-23. Agent jobs не должны иметь права auto-merge.

### Безопасность

24. FR-AG-24. Агент не должен иметь admin token, bypass branch protection или secret management права.
25. FR-AG-25. Self-hosted runners должны использоваться только для приватных репозиториев и с минимальными правами.
26. FR-AG-26. В систему должны быть встроены правила против утечки секретов.
27. FR-AG-27. Для задач выше docs-only должен применяться независимый Reviewer или human review.

### Знания

28. FR-AG-28. Должен существовать единый канон правил `docs/agent-system/AGENT_RULES.md`.
29. FR-AG-29. Конкретные агенты должны получать правила через адаптерные файлы.
30. FR-AG-30. Повторная ошибка одного типа должна приводить к обновлению правил или шаблона задачи.

---

## 11. Риски и что с ними делать

| № | Риск | Признак | Действие |
|---|---|---|---|
| Р-1 | Локальный Docker тяжело грузит ноутбук | тормозит система, Docker ест RAM/CPU | уменьшить задачи, закрыть лишнее, перейти к VM после Этапа 3 |
| Р-2 | Дешёвая модель не справляется | PR мимо задачи | дробить задачи, поднять `model/strong`, сменить агента |
| Р-3 | Агент зациклился | долго работает, много токенов | `AGENT_MAX_ITER`, timeout, ручная остановка |
| Р-4 | Утечка API-ключа | ключ в файле/логе/PR | немедленно отозвать ключ, включить virtual keys/Hub |
| Р-5 | Агент ломает чужие файлы | неожиданные изменения | не принимать PR, добавить ограничения в issue и AGENT_RULES |
| Р-6 | Vendor lock-in на OpenHands | смена агента ломает процесс | Agent Adapter contract |
| Р-7 | Vendor lock-in на DeepSeek | модель недоступна/подорожала | Model Profile + LLM Hub + fallback |
| Р-8 | Vendor lock-in на GitHub Actions | нужен GitVerse/SourceCraft/GitLab | CI Adapter contract |
| Р-9 | LLM Hub стал единой точкой отказа | все агенты не могут вызвать модель | direct fallback для MVP, backup config, мониторинг |
| Р-10 | Self-hosted runner скомпрометирован | странные процессы/файлы | private repos only, rebuild VM, rotate tokens, cleanup |
| Р-11 | Prompt injection | агент пытается нарушить правила | минимальные права, AGENT_RULES, human review, secret scanning |
| Р-12 | Разные агенты читают разные правила | OpenHands/Qwen/Codex ведут себя по-разному | единый AGENT_RULES + короткие адаптеры |
| Р-13 | CI-специфика расползлась | у GitHub/GitVerse/SourceCraft разные смыслы переменных | единые переменные + CI Adapter docs |
| Р-14 | Слишком раннее усложнение | много Hub/VM/CI, нет результата | сначала локальный Docker MVP, потом усложнение |
| Р-15 | Непроверенный trigger в GitVerse/SourceCraft | issue label не запускает agent job | использовать manual workflow/webhook/Dispatcher/task manifest |

---

## 12. Сводный чек-лист прогресса

### Этап 0. Локальный Docker-контур

- [ ] 0.1. Решение v1.2 зафиксировано: стартуем с локального Docker
- [ ] 0.2. WSL2 установлен и проверен
- [ ] 0.3. КТ-1: Docker Desktop работает (`docker run hello-world`)
- [ ] 0.4. Рабочая папка `~/workspace` создана в WSL
- [ ] 0.5. git видит GitHub
- [ ] 0.6. Правило секретов добавлено

### Этап 1. Контур моделей

- [ ] 1.1. DeepSeek API key создан и сохранён вне репозитория
- [ ] 1.2. Ключ проверен curl-запросом
- [ ] 1.3. Создан `docs/agent-system/model-profiles.md`
- [ ] 1.4. Зафиксировано: прямой API только MVP, production через Hub

### Этап 2. OpenHands локально

- [ ] 2.1. `uv` установлен
- [ ] 2.2. OpenHands установлен
- [ ] 2.3. `openhands serve` запускает GUI на `localhost:3000`
- [ ] 2.4. `openhands serve --mount-cwd` работает на папке проекта
- [ ] 2.5. DeepSeek подключён в OpenHands
- [ ] 2.6. КТ-2: первый локальный разговор выполнен
- [ ] 2.7. OpenHands корректно остановлен

### Этап 3. Песочница

- [ ] 3.1. `agent-sandbox` создан и склонирован
- [ ] 3.2. OpenHands запущен на песочнице
- [ ] 3.3. КТ-3: первый PR/ветка от агента
- [ ] 3.4. PR принят или закрыт с выводами
- [ ] 3.5. Создан `LOCAL_DOCKER_PILOT_NOTES.md`

### Этап 4. Автономный CI

- [ ] 4.1. CI Adapter contract зафиксирован
- [ ] 4.2. GitHub Actions OpenHands resolver установлен
- [ ] 4.3. bot-user/PAT настроен минимально
- [ ] 4.4. Branch protection включён
- [ ] 4.5. КТ-4: issue → PR без ручного OpenHands UI
- [ ] 4.6. GitLab adapter doc создан
- [ ] 4.7. Jenkins adapter doc создан
- [ ] 4.8. GitVerse adapter doc создан
- [ ] 4.9. SourceCraft adapter doc создан
- [ ] 4.10. CI Adapter matrix заполнена

### Этап 5. Унификация

- [ ] 5.1. lightweight solo-operator mode записан в DECISION_LOG
- [ ] 5.2. Создан `AGENT_RULES.md`
- [ ] 5.3. Созданы `AGENTS.md`, `.openhands/microagents/repo.md`, `QWEN.md`, `CLAUDE.md`
- [ ] 5.4. Созданы docs адаптеров
- [ ] 5.5. Issue template установлен

### Этап 6. Пилот `verification`

- [ ] 6.1. `verification` подготовлен к локальному Docker-пилоту
- [ ] 6.2. 5 задач выбраны
- [ ] 6.3. 5 задач выполнены
- [ ] 6.4. КТ-5: метрики заполнены, критерий успеха пилота проверен
- [ ] 6.5. Решение по итогам принято

### Этап 7. Знания

- [ ] 7.1. После плохих PR обновляются правила/шаблоны
- [ ] 7.2. Условия перехода к RAG зафиксированы

### Этап 8. LLM Hub

- [ ] 8.1. Принято решение по LiteLLM/Hub
- [ ] 8.2. Контракт Hub описан
- [ ] 8.3. КТ-6: OpenHands работает через virtual key
- [ ] 8.4. Production-правила Hub зафиксированы

### Этап 9. VM / self-hosted

- [ ] 9.1. Есть доказанная необходимость VM
- [ ] 9.2. Конфигурация VM выбрана
- [ ] 9.3. Self-hosted runner safety применён
- [ ] 9.4. VM используется как runner/Docker host, не как ручной ноутбук

---

## 13. Источники

Факты и внешние технические предпосылки проверены 2026-07-04.

1. OpenHands local setup: `https://docs.openhands.dev/openhands/usage/run-openhands/local-setup`
2. OpenHands GUI server: `https://docs.openhands.dev/openhands/usage/cli/gui-server`
3. OpenHands installation / Docker mode: `https://docs.openhands.dev/openhands/usage/cli/installation`
4. OpenHands troubleshooting: `https://docs.openhands.dev/openhands/usage/troubleshooting/troubleshooting`
5. OpenHands GitHub Action: `https://docs.openhands.dev/openhands/usage/run-openhands/github-action`
6. OpenHands Resolver README: `https://github.com/OpenHands/OpenHands/blob/main/openhands/resolver/README.md`
7. DeepSeek pricing/docs: `https://api-docs.deepseek.com/quick_start/pricing`
8. LiteLLM docs: `https://docs.litellm.ai/docs/`
9. LiteLLM Docker quick start: `https://docs.litellm.ai/docs/proxy/docker_quick_start`
10. LiteLLM deploy docs: `https://docs.litellm.ai/docs/proxy/deploy`
11. LiteLLM virtual keys: `https://docs.litellm.ai/docs/proxy/virtual_keys`
12. Qwen Code docs: `https://qwenlm.github.io/qwen-code-docs/`
13. Codex CLI: `https://developers.openai.com/codex/cli`
14. Codex AGENTS.md: `https://developers.openai.com/codex/guides/agents-md`
15. Codex GitHub review: `https://developers.openai.com/codex/integrations/github`
16. GitHub Actions workflow syntax: `https://docs.github.com/actions/using-workflows/workflow-syntax-for-github-actions`
17. GitHub Actions events: `https://docs.github.com/actions/using-workflows/events-that-trigger-workflows`
18. GitHub self-hosted runner security: `https://docs.github.com/actions/hosting-your-own-runners/adding-self-hosted-runners`
19. GitLab CI YAML: `https://docs.gitlab.com/ci/yaml/`
20. GitLab CI variables: `https://docs.gitlab.com/ci/variables/`
21. Jenkins Pipeline / Jenkinsfile: `https://www.jenkins.io/doc/book/pipeline/jenkinsfile/`
22. Jenkins Credentials Binding: `https://www.jenkins.io/doc/pipeline/steps/credentials-binding/`
23. GitVerse CI/CD docs: `https://gitverse.ru/docs/cicd/`
24. GitVerse workflow syntax: `https://gitverse.ru/docs/cicd/docs/workflow/`
25. GitVerse triggers: `https://gitverse.ru/docs/cicd/docs/triggers/`
26. GitVerse runners: `https://gitverse.ru/docs/cicd/docs/runners/`
27. GitVerse self-hosted runners: `https://gitverse.ru/docs/cicd/docs/runners/self-hosted/`
28. GitVerse organization runners: `https://gitverse.ru/docs/cicd/docs/runners/organization-runners/`
29. SourceCraft CI/CD concepts: `https://sourcecraft.dev/portal/docs/en/sourcecraft/concepts/ci-cd`
30. SourceCraft CI/CD configuration: `https://sourcecraft.dev/portal/docs/en/sourcecraft/operations/ci-cd`
31. SourceCraft environment variables and secrets guidance: `https://sourcecraft.dev/portal/docs/en/sourcecraft/operations/variables`
32. SourceCraft GitHub Actions support: `https://sourcecraft.dev/portal/docs/en/sourcecraft/operations/gh-actions`
33. SourceCraft GitLab pipelines support: `https://sourcecraft.dev/portal/docs/en/sourcecraft/concepts/gl-pipelines`
34. Методология проекта: `MaximKolomeets/agent-system-development` — README, CURRENT_STATE, NEXT_STEPS, DECISION_LOG.

---

## 14. Запись для `DECISION_LOG.md`

```markdown
## 2026-07-04 — v1.2: старт с локального Docker и расширение CI Adapter до GitVerse/SourceCraft

### Контекст
Версия 1.0 описывала MVP на OpenHands + DeepSeek + GitHub Actions. Версия 1.1 расширила архитектуру до Agent Adapter, Model Adapter, CI Adapter и LLM Hub. После уточнения цели принято решение сначала попробовать систему локально через Docker на компьютере Максима, а автономные CI-контуры подключать после локального подтверждения.

### Решение
1. Первый практический запуск выполняется локально: Windows/WSL2 + Docker Desktop + OpenHands.
2. OpenHands остаётся первым Agent Adapter.
3. DeepSeek напрямую используется только для MVP; production должен перейти на LLM Hub / virtual keys.
4. CI Adapter abstraction расширяется: GitHub Actions, GitLab CI, Jenkins, GitVerse CI/CD, SourceCraft CI/CD.
5. GitVerse и SourceCraft фиксируются как будущие CI Adapter, но не блокируют локальный MVP.
6. VM не покупается до завершения локального Docker-пилота и первой оценки ресурсов.
7. Merge остаётся только человеческим действием.

### Последствия
`MASTER_PLAN.md` обновляется до версии 1.2. Этапы перестроены так, чтобы сначала получить результат локально, затем автоматизировать issue → PR через CI, затем при необходимости добавить LLM Hub и VM/self-hosted runner.
```
