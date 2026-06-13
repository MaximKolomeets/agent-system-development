# NEW_PROJECT_CHECKLIST

Использовать перед началом нового проекта и перед первым PR.

- [ ] Repository created.
- [ ] Visibility chosen.
- [ ] `.gitignore` created.
- [ ] Forbidden paths protected.
- [ ] `main`/`developer` policy chosen.
- [ ] Для `standard developer workflow` ветка `developer` создана до первой рабочей ветки.
- [ ] Если `developer` отсутствовал, bootstrap creation явно разрешен и выполнен до `work/<role>/*`.
- [ ] Рабочий PR в `main` запрещен для `standard developer workflow`.
- [ ] Work branch namespace chosen.
- [ ] `docs/` folder created.
- [ ] First state files created.
- [ ] First templates created.
- [ ] Rulesets/branch protection checked.
- [ ] First PR planned.
- [ ] CI guardrails planned.
- [ ] Source/index policy defined.

## Notes

- Для public repository все материалы считаются публичными.
- Для private repository правила безопасности все равно фиксируются явно.
- Если rulesets/branch protection недоступны, контроль фиксируется процессом и manual review.
- Для нового пустого repository `main-only flow` нельзя применять молча, если выбран стандартный workflow с `developer`.
