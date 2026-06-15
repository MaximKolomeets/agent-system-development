# DEVELOPMENT_TASK_TEMPLATE

## Общий header

Заполнить общий header по канону `docs/agent-system/templates/TASK_HEADER_COMMON.md`:

- Mandatory header (`Задача для <agent-name>: <task-id>` + блок рекомендуемого режима);
- Russian-first;
- Recommended Engine Mode;
- Verified Baseline;
- Copy/Paste Completeness Check;
- Project constitution check.

Ниже — секции, специфичные для задачи разработки.

## Task ID

Указать идентификатор задачи.

## Goal

Описать цель и ожидаемый результат.

## Base branch

Указать базовую ветку.

## Work branch

Указать рабочую ветку в разрешенном namespace.

## Разрешенные файлы

Перечислить файлы и директории, которые можно менять.

## Запрещенные файлы

Перечислить файлы и директории, которые нельзя читать или менять.

## Steps

Описать шаги выполнения.

## Checks

Описать проверки перед отчетом.

Если задача создает PR, release PR или sync PR, проверки должны включать проверку Post-merge Journal Closure для RESULT/INDEX.

## Ожидаемый отчет

Описать формат итогового отчета.

Отчет должен быть на русском языке и содержать language policy result.

Если PR был merged, отчет должен содержать статус PR после review (`PR status after review`), merge commit SHA, release PR URL/status/merge commit SHA при наличии, sync PR URL/status/merge commit SHA при наличии, `RESULT closed after merge`, `INDEX closed after merge` и проверку Post-merge Journal Closure.
