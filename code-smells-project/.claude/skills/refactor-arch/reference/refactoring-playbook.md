# Referência — Playbook de Refatoração (Fase 3)

Transformações concretas, com exemplos **antes/depois**, mapeadas aos anti-patterns
do catálogo. Exemplos em Python/Flask e Node.js/Express para reforçar o agnosticismo.
Aplique a transformação correspondente a cada finding.

---

## T1 — Extrair configuração/segredos para config/env (AP-01)

**Antes (Flask)**
```python
app.config["SECRET_KEY"] = "minha-chave-super-secreta-123"
app.config["DEBUG"] = True
```
**Depois**
```python
# config/settings.py
import os
class Settings:
    SECRET_KEY = os.environ["SECRET_KEY"]
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
```
```python
# app.py
app.config.from_object("config.settings.Settings")
```

**Antes (Express)**
```js
const config = { dbPass: "senha_super_secreta_prod_123", paymentGatewayKey: "pk_live_..." };
```
**Depois**
```js
// src/config/index.js
module.exports = {
  dbPass: process.env.DB_PASS,
  paymentGatewayKey: process.env.PAYMENT_GATEWAY_KEY,
};
```

---

## T2 — Parametrizar queries SQL (AP-02)

**Antes**
```python
cursor.execute("SELECT * FROM usuarios WHERE email = '" + email + "' AND senha = '" + senha + "'")
```
**Depois**
```python
cursor.execute("SELECT * FROM usuarios WHERE email = ? AND senha = ?", (email, senha))
```
Nunca concatene entrada em SQL; use placeholders (`?`, `:nome`) ou o ORM.

---

## T3 — Quebrar God Class/Module em camadas (AP-03)

**Antes**
```python
# models.py: SQL + regra + formatação + 4 domínios em um arquivo
```
**Depois**
```
models/produto_model.py      # dados/persistência de produto
controllers/produto_controller.py  # fluxo/validação
views/produto_routes.py      # rota HTTP
```
Mova cada responsabilidade para sua camada (ver `mvc-guidelines.md`).

**Express — antes:** `AppManager` com DB + rotas + checkout.
**Depois:** `models/`, `controllers/checkoutController.js`, `routes/checkout.js`,
`services/paymentService.js`.

---

## T4 — Substituir hashing/cripto insegura (AP-05)

**Antes**
```python
self.password = hashlib.md5(pwd.encode()).hexdigest()
```
**Depois**
```python
from werkzeug.security import generate_password_hash, check_password_hash
self.password = generate_password_hash(pwd)      # pbkdf2/scrypt com salt
# check: check_password_hash(self.password, pwd)
```
**Node**
```js
const bcrypt = require('bcrypt');
const hash = await bcrypt.hash(pwd, 12); // substitui badCrypto()
```

---

## T5 — Remover dados sensíveis de respostas e logs (AP-06)

**Antes**
```python
def to_dict(self):
    return {"id": self.id, "email": self.email, "password": self.password}
```
**Depois**
```python
def to_dict(self):
    return {"id": self.id, "email": self.email}  # nunca expor hash de senha
```
**Node — antes:** `console.log(\`Processando cartão ${cc} na chave ${key}\`)`.
**Depois:** nunca logar PAN/segredo; logar apenas um id de transação mascarado.

---

## T6 — Eliminar estado global / conexão singleton (AP-07)

**Antes**
```python
db_connection = None
def get_db():
    global db_connection
    if db_connection is None:
        db_connection = sqlite3.connect(db_path, check_same_thread=False)
    return db_connection
```
**Depois**
```python
# conexão por requisição (Flask): flask.g + teardown
from flask import g
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DB_PATH"])
        g.db.row_factory = sqlite3.Row
    return g.db
```
**Node:** injete a instância de DB via construtor/parâmetro em vez de `globalCache`
module-level.

---

## T7 — Mover regra de negócio do controller/rota para service/model (AP-08)

**Antes (rota calcula overdue e enriquece dados)**
```python
@task_bp.route('/tasks')
def get_tasks():
    for t in Task.query.all():
        task_data['overdue'] = t.due_date and t.due_date < datetime.utcnow() and t.status not in ('done','cancelled')
        ...
```
**Depois**
```python
# models/task.py
class Task(db.Model):
    @property
    def is_overdue(self):
        return bool(self.due_date and self.due_date < now_utc() and self.status not in ("done","cancelled"))
# controller apenas orquestra; rota só faz I/O
```

---

## T8 — Corrigir N+1 (AP-09)

**Antes**
```python
for row in pedidos:
    itens = cursor.execute("SELECT * FROM itens_pedido WHERE pedido_id = " + str(row["id"]))
    for item in itens:
        prod = cursor.execute("SELECT nome FROM produtos WHERE id = " + str(item["produto_id"]))
```
**Depois**
```python
# uma query com JOIN
cursor.execute("""
  SELECT p.id, ip.produto_id, pr.nome, ip.quantidade
  FROM pedidos p
  JOIN itens_pedido ip ON ip.pedido_id = p.id
  JOIN produtos pr ON pr.id = ip.produto_id
""")
```
Com ORM: use `joinedload`/`selectinload` (SQLAlchemy) para carregar relações de uma vez.

---

## T9 — Substituir callback hell por async/await (AP-11)

**Antes (Express)**
```js
this.db.get(q1, [a], (e, r1) => {
  this.db.get(q2, [b], (e, r2) => {
    this.db.run(q3, [c], (e) => { res.json(...) });
  });
});
```
**Depois**
```js
const db = require('better-sqlite3')('app.db'); // ou wrapper com Promise
const r1 = db.prepare(q1).get(a);
const r2 = db.prepare(q2).get(b);
db.prepare(q3).run(c);
res.json(/* ... */);
```

---

## T10 — Centralizar validação de entrada (AP-10)

**Antes:** blocos de `if not data.get(...)` repetidos em create/update.
**Depois**
```python
# validação reutilizável (schema/função) chamada pelo controller
def validate_produto(data):
    errors = []
    if not data.get("nome"): errors.append("nome obrigatório")
    if data.get("preco", 0) < 0: errors.append("preço inválido")
    return errors
```
Ou use um schema (pydantic/marshmallow/JSON Schema) e valide num único ponto.

---

## T11 — Trocar print/console.log por logging estruturado (AP-13)

**Antes**
```python
print("Login bem-sucedido: " + email)
```
**Depois**
```python
import logging
logger = logging.getLogger(__name__)
logger.info("login ok", extra={"email": email})
```
**Node:** substitua `console.log` por um logger (`pino`/`winston`) com níveis.

---

## T12 — Garantir integridade referencial / transações (AP-12)

**Antes**
```js
this.db.run("DELETE FROM users WHERE id = ?", [id]); // deixa enrollments/payments órfãos
```
**Depois**
```js
// transação + cascata (ou ON DELETE CASCADE no schema)
db.transaction(() => {
  db.prepare("DELETE FROM payments WHERE enrollment_id IN (SELECT id FROM enrollments WHERE user_id=?)").run(id);
  db.prepare("DELETE FROM enrollments WHERE user_id=?").run(id);
  db.prepare("DELETE FROM users WHERE id=?").run(id);
})();
```

---

## T13 — Remover/proteger endpoints perigosos (AP-04)

**Antes**
```python
@app.route("/admin/query", methods=["POST"])
def executar_query():
    cursor.execute(request.get_json().get("sql", ""))  # SQL arbitrário
```
**Depois**
- **Remover** a rota de execução arbitrária; ou
- restringir a operações específicas + **autenticação/autorização** + parametrização.
- `/admin/reset-db` e deleções em massa: exigir authz e mover para tarefa administrativa.

---

## T14 — Centralizar error handling (transversal)

**Antes:** `try/except` repetido em cada função retornando 500 genérico; `except:` nu.
**Depois (Flask)**
```python
# middlewares/error_handler.py
def register_error_handlers(app):
    @app.errorhandler(Exception)
    def handle(e):
        logger.exception(e)
        return {"error": "internal error"}, 500
```
**Express**
```js
app.use((err, req, res, next) => { logger.error(err); res.status(500).json({ error: "internal error" }); });
```
Capture exceções específicas nas camadas; deixe o handler central cuidar do resto.

---

## Ordem de aplicação sugerida

1. Segurança CRITICAL primeiro: T1 (segredos), T2 (SQL Injection), T13 (rotas perigosas), T5 (dados sensíveis).
2. Estrutura: T3 (camadas), T6 (estado/conexão), T7 (regra fora da rota), T14 (erros).
3. Qualidade/performance: T4 (cripto), T8 (N+1), T9 (async), T10 (validação), T11 (logging), T12 (integridade).
4. Valide boot + endpoints após cada bloco relevante (ver `SKILL.md`, Fase 3).
