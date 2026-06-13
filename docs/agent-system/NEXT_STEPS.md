# NEXT_STEPS

1. Завершить PR-3c: добавить vendor-neutral review-only workflow для code review / external review / consulting review.
2. После merge PR-3c использовать `CODE_REVIEW_TASK_TEMPLATE.md` для первого безопасного review target implementation repository.
3. Проверять, что новые target adoption tasks явно фиксируют lifecycle mode, selected branch model, наличие `developer` и запрет `fallback-to-main` для `standard developer workflow`.
4. Для existing repository adoption сохранять поддержку осознанного `main-only flow`, если это фактическая модель target implementation repository или отдельное решение пользователя.
5. По результатам target adoption dry run возвращать только нейтральный methodology feedback без private downstream data.
