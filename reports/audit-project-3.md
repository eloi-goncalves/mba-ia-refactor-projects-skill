```
================================
ARCHITECTURE AUDIT REPORT
================================
Project: task-manager-api
Stack:   Python + Flask + SQLAlchemy
Files:   ~12 analyzed | ~700 lines of code

## Summary
CRITICAL: 1 | HIGH: 2 | MEDIUM: 3 | LOW: 2
```

## Findings

### [CRITICAL] Hashing de senha inseguro (MD5, sem salt)
File: models/user.py:28-31
Description: `set_password`/`check_password` usam `hashlib.md5(pwd).hexdigest()` sem salt.
Impact: Senhas quebráveis trivialmente (rainbow tables); MD5 é impróprio para senhas.
Recommendation: Usar KDF com salt via `werkzeug.security.generate_password_hash`/`check_password_hash` (playbook T4).

### [HIGH] Exposição de senha na API
File: models/user.py:16-24
Description: `User.to_dict()` inclui o campo `password` (hash), retornado por `GET /users` e `GET /users/<id>`.
Impact: Vazamento de credenciais em respostas da API.
Recommendation: Remover `password` da serialização (playbook T5).

### [HIGH] Credenciais SMTP hardcoded
File: services/notification_service.py:9-10
Description: `email_user`/`email_password = 'senha123'` hardcoded no serviço.
Impact: Segredo versionado e exposto.
Recommendation: Carregar de variáveis de ambiente (playbook T1).

### [MEDIUM] Query N+1 nos relatórios
File: routes/report_routes.py:53-67 (e user_report)
Description: `summary_report` itera todos os usuários e, para cada um, consulta as tasks (`Task.query.filter_by(user_id=...)`).
Impact: Número de queries cresce com a quantidade de usuários.
Recommendation: Agregar com `GROUP BY`/`func.count` numa única query (playbook T8).

### [MEDIUM] Regra de negócio na rota (fat controller) + duplicação
File: routes/task_routes.py:14-63 (e get_task)
Description: Cálculo de `overdue`, montagem manual do dict e enriquecimento com user/category dentro da rota, duplicado em vários pontos.
Impact: Baixa testabilidade e duplicação de lógica.
Recommendation: Mover para o model (`Task.is_overdue`, serializer) e/ou controller (playbook T7).

### [MEDIUM] Configuração hardcoded / debug ligado
File: app.py:12-14 e app.py:32
Description: `SECRET_KEY` hardcoded, `debug=True` e `host='0.0.0.0'` fixos no código.
Impact: Segredo exposto; debug/binding inseguros em produção.
Recommendation: Carregar config de ambiente (playbook T1); `debug` via env.

### [LOW] `except:` genérico (bare except)
File: routes/task_routes.py:61 (e utils/helpers.py:parse_date)
Description: `except:` nu engole qualquer exceção e retorna 500 genérico.
Impact: Mascara bugs e dificulta o diagnóstico.
Recommendation: Capturar exceções específicas; deixar o handler central tratar o resto (playbook T14).

### [LOW] Serialização duplicada / não reuso de to_dict
File: routes/task_routes.py:16-60
Description: Montagem manual de dict repetida em vez de reusar `to_dict()`/serializer.
Impact: Duplicação de código e inconsistência.
Recommendation: Centralizar a serialização no model.

## Detecção de APIs deprecated
- `datetime.datetime.utcnow()` — usado amplamente (models e rotas); deprecated no Python 3.12+. Equivalente moderno: `datetime.now(datetime.UTC)` (timezone-aware).
- `Model.query` / `Query.get(id)` — estilo legado do SQLAlchemy 1.x. Equivalente 2.0: `db.session.get(Model, id)` / `db.session.execute(select(...))`.

```
================================
Total: 8 findings
================================

Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]
> y
```
