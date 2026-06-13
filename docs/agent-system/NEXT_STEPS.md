# NEXT_STEPS

1. Завершить PR-3a: закрепить bootstrap gate для нового repository со стандартной схемой `main -> developer -> work/<role>/*`.
2. После merge PR-3a в `developer` использовать обновленный adoption prompt для следующих target implementation repositories.
3. Проверять, что новые target adoption tasks явно фиксируют lifecycle mode, selected branch model, наличие `developer` и запрет `fallback-to-main` для `standard developer workflow`.
4. Для existing repository adoption сохранять поддержку осознанного `main-only flow`, если это фактическая модель target repository или отдельное решение пользователя.
5. По результатам target adoption dry run возвращать только нейтральный methodology feedback без private downstream data.
