# NEXT_STEPS

1. Использовать обновленный adoption prompt для следующих target implementation repositories.
2. Проверять, что новые target adoption tasks явно фиксируют lifecycle mode, selected branch model, наличие `developer` и запрет `fallback-to-main` для `standard developer workflow`.
3. Для existing repository adoption сохранять поддержку осознанного `main-only flow`, если это фактическая модель target repository или отдельное решение пользователя.
4. По результатам target adoption dry run возвращать только нейтральный methodology feedback без private downstream data.
