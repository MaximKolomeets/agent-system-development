# SECURITY_POLICY

- Не читать `.env` без отдельного разрешения.
- Не коммитить секреты.
- Не коммитить рабочие данные.
- Запрещенные директории: `.venv/`, `data/`, `runtime/`, `dist/`, `backups/`, `exports/`.
- Перед commit проверять staged files.
- При обнаружении секрета остановиться и сообщить пользователю.
- Для target repositories, где security/privacy risk выходит за простые
  forbidden-file rules, заводить target-local `THREAT_MODEL.md` на основе
  `docs/agent-system/templates/THREAT_MODEL_TEMPLATE.md`: угрозы связываются с
  controls, tests, CI-gates, severity и stage.

## Public repository security

- Считать весь контент public repository публичным.
- Не хранить секреты даже временно.
- Не хранить `.env`.
- Не хранить клиентские или персональные данные.
- Документационные слова `token`, `password`, `secret`, `credential` допустимы только без реальных значений.
- Если реальный секрет попал в историю Git, его нужно считать скомпрометированным и ротировать.

## Threat model

`SECURITY_POLICY.md` задает запреты и baseline controls. Threat model показывает
эти controls как проверяемую систему: `Угроза -> Контроль -> Тест -> CI-gate ->
severity -> этап`.

Target-local `THREAT_MODEL.md` не должен содержать реальные secrets, private data,
client data, private repository URL или internal code names. Если control matrix
принята в target repository, threat model ссылается на `CONTROL_MATRIX` ids; для
acceptance/spec controls используется цепочка из
`ACCEPTANCE_SPEC_COMPLETENESS_PATTERN.md`.
