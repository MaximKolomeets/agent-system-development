# TASK-0089-METH-FULL-AUDIT-FRESH-01

Задача для reviewer: METH-FULL-AUDIT-FRESH-01
Роль: code-reviewer-01 (полный baseline-аудит)

Рекомендуемый режим исполнения:

Исполнитель: на усмотрение архитектора
Reasoning effort: высокий
Запуск: Local only
Режим: Agent
Время начала выполнения (execution_started_at) [measured/engine]: 2026-06-24T18:45:40+07:00
Время оркестрации, по факту (orchestration_time_reported) [reported/human, опционально]:
Почему: сквозной read-only аудит всей методологии на неизвестном оркестратору baseline; высокий reasoning, самостоятельная верификация состояния и строгий claim-протокол во избежание пересечений engine.

## Цель

Occasional сквозной read-only аудит ВСЕЙ методологии на актуальном `developer`. Подтвердить целостность/согласованность и найти все несоответствия/пробелы/риски перед downstream adoption. Включить в объём всё, что изменилось с прошлого полного аудита. Read-only по содержанию: контент не править, findings → рекомендованные fix-PR. Изменения только journal этой задачи + регенерация cloud. Journal trace: always; Report delivery: chat.

## Установленный baseline (engine, из git/gh)

- Repository: `MaximKolomeets/agent-system-development`.
- developer HEAD (claimed): `e6be18fbb4e92f41d328474fab0a9a33fdd06903`.
- main HEAD: `8c21a45bf189432afcdabfb164f85d175271df74` (release «Developer v1.1.0», PR #233 merged; sync #234 merged).
- developer на 10 коммитов впереди main (невыпущенный payload к следующему релизу: post-v1.1.0 работа 0086–0088 и т.д.).
- last seq в INDEX: `0088` → my_seq = `0089`.
- Прошлый полный аудит: seq `0074` (`METH-FULL-AUDIT-2026-06-23-02`); точка отсчёта inventory — commit `fa2184d97c084e4289d29298f3e1e3b433cd6977`.
- Теги: annotated `v1.1.0` → `8c21a45` (release merge commit на main). `v1.0.0` тег ОТСУТСТВУЕТ.
- Verification source: gh + local git. Verification date/time: 2026-06-24T18:47+07:00.

## Claim-протокол (выполнен)

- `git fetch --all --prune`; `git switch developer`; `git pull --ff-only`; HEAD == origin/developer (`e6be18f`).
- my_seq=0089 свободен: нет tracked/untracked TASK/RESULT-0089; нет открытых PR (`gh pr list --state open` пуст); нет ветки `work/code-reviewer-01/full-audit-fresh-01` локально/origin; чужие worktree (`.claude/*`) не держат my_seq/ветку и не трогаются.
- Рабочая ветка создана от `origin/developer`.

## Ослабленный preflight по closure

- Допустима одна terminal closed-at-creation складка. Фактически найдено 3 открытых substantive seq (0086/0087/0088 merged, но не closure-stamped) → зафиксировано как finding (см. RESULT), не hard-STOP: целостность журнала (seq/парность) не нарушена.

## Объём аудита (20 пунктов)

Governance 1–4; closure policy + producer-fix; целостность журнала; parity-гейты (sequential) + EOL-safe; Source Delta + handoff; Russian-first headings; перекрёстные ссылки; adoption ↔ manifest; безопасность; vendor-neutrality; полнота шаблонов; methodology_reference + tag; operating-layer + три слоя; state freshness; reviewer consistency-gate; execution-timestamps; релиз-тег; B-WIN fallback; terminal-fold канон; backlog-статус (F-17/F-18/F-06/F-10/terminal-fold + новые правки архитектора).

## Политика запуска --check

Sequential, напрямую (`python ... --check` по одному) — параллельный/обёрточный runner не использовать. Зависание параллельного runner >30s без живого процесса = не FAIL, повторить последовательно и зафиксировать.

## Разрешённые файлы

- `engine-journal/input/TASK-0089-METH-FULL-AUDIT-FRESH-01.md` (создать);
- `engine-journal/output/RESULT-0089-METH-FULL-AUDIT-FRESH-01.md` (создать);
- `engine-journal/INDEX.md` (строка);
- `docs/agent-system/cloud/**` (регенерация через `gen_cloud_bundle.py` ПОСЛЕ обновления INDEX).

## Запрещено

Контент методологии (read-only; findings → fix-PR); постановка/удаление тегов (human-only); main/developer напрямую; release; закрытие/мерж чужих PR; действия в `.claude/*`/чужих worktree; runtime/CI/secrets/.env/private data; force push; удаление/перезапись TASK/RESULT.

## STOP-условия

git-гарды; FF невозможен; HEAD != origin/developer; my_seq занят; ветка уже существует; разрыв сквозной закрытости сверх допустимого при серьёзности; невозможно получить commit SHA для methodology_reference; любой `--check` FAIL (sequential); задача потребовала бы править контент или ставить тег.

## Требования к финальному отчёту (русский)

Baseline; Фаза 0 inventory; статусы по 20 пунктам; backlog-статус; классификация blocker/major/minor/nit + fix-PR; результаты обоих `--check` + отметка про hang; tag-проверка; Source Delta; Source-reminder; строка «Архитектору — загрузить в контекст оркестратора: …»; подтверждения (incl execution timestamps present: yes); «Передача»; «Локальные действия после PR/merge».

Канон шапки и сквозных правил: `docs/agent-system/templates/TASK_HEADER_COMMON.md`.
