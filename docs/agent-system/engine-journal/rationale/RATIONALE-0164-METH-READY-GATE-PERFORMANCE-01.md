# RATIONALE-0164-METH-READY-GATE-PERFORMANCE-01

Связанный TASK file: `docs/agent-system/engine-journal/input/TASK-0164-METH-READY-GATE-PERFORMANCE-01.md`

Связанный RESULT file: `docs/agent-system/engine-journal/output/RESULT-0164-METH-READY-GATE-PERFORMANCE-01.md`

Номер sequence: 0164

Идентификатор задачи: METH-READY-GATE-PERFORMANCE-01

authoring_role: dev-implementer-01

actor_type: agent

Статус обоснования: finalized_for_review

raw_chain_of_thought_stored: no

## Решаемый вопрос

Как сократить время aggregate readiness gate на Windows Docker bind mount, сохранив полный набор проверок и их порядок.

## Контекст и evidence

Диагностика после PR #338 подтвердила корректный verdict `ready` при длительности около 232 секунд. Значительная доля времени относится к повторным одинаковым Git-подпроцессам в одном запуске.

## Ограничения и инварианты

Сохраняются secret scan, forbidden paths, journal, policy invariants, generated checks, EOL guard, ID references, Russian-first lint и остальные существующие gates. JSON stdout остаётся обратно совместимым и валидным.

## Рассмотренные варианты

1. Отключить дорогие проверки.
2. Добавить увеличение timeout без наблюдаемости.
3. Кэшировать повторяющиеся Git-результаты внутри процесса и писать этапы в stderr.

## Выбранный путь

Выбран вариант 3: кэш ограничен единственным запуском `check_task_ready.py`; progress выводится только в stderr перед крупными этапами.

## Причины выбора

Кэширование не меняет входные данные или verdict проверки, а исключает лишь повторный запуск идентичной Git-команды. Stderr logging даёт безопасную наблюдаемость и не нарушает контракт JSON stdout.

## Отклонённые альтернативы

Вариант 1 отклонён как ослабление safety gate. Вариант 2 не объясняет, на каком этапе выполняется gate, и не устраняет повторную работу.

## Компромиссы, последствия и риски

Кэш актуален только пока выполняется один процесс; это исключает перенос устаревших данных между запусками. Progress не является основанием обходить или прерывать gate.

## Предположения, неопределённости и confidence

Предполагается, что одинаковые Git-команды в read-only запуске имеют одинаковый результат. Confidence: high.

## Условия пересмотра или rollback triggers

Пересмотреть решение при доказанном расхождении cached и uncached verdict либо при изменении модели сборки изменённых файлов.

## Что явно не решалось

Не изменялись Docker, CI, политика timeout, порядок validators, внешние проекты и release-процесс.

## Связь с решениями

Решение уточняет Operational Fast Lane: 360-секундный timeout применяется как инфраструктурный бюджет для Windows Docker bind mount, а не как обход проверки.

## Изменения после review

Нет.
