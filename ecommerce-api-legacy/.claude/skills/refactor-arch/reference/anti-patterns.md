# Referência — Catálogo de Anti-Patterns (Fase 2)

Catálogo agnóstico de tecnologia. Cada anti-pattern traz **sinais de detecção**
(acionáveis), **severidade** e o **encaminhamento** (veja o playbook para a
transformação). Use a escala de severidade abaixo.

## Escala de severidade

- **CRITICAL** — falha grave de arquitetura/segurança: credenciais hardcoded, SQL
  Injection, execução arbitrária, exposição de dados sensíveis, God Class que mistura
  DB + regra + roteamento.
- **HIGH** — violação forte de MVC/SOLID: regra de negócio pesada no controller,
  acoplamento sem injeção de dependência, estado global mutável, cripto insegura.
- **MEDIUM** — padronização, duplicação, performance moderada: N+1, validação ausente,
  middleware inadequado, integridade referencial frágil.
- **LOW** — legibilidade: nomes ruins, magic numbers, logging por `print`/`console.log`,
  tratamento de erro impreciso.

---

## Catálogo (≥ 8 anti-patterns)

### AP-01 — Hardcoded Credentials / Secrets — CRITICAL
Sinais: `SECRET_KEY = "..."`, `password = "..."`, chaves de API (`pk_live_...`,
`sk_...`), senha de DB/SMTP no código; segredo retornado por endpoint.
Detecção: regex por `secret|password|api[_-]?key|token|smtp` com literal atribuído.
→ Playbook T1 (extrair para config/env).

### AP-02 — SQL Injection (concatenação de string) — CRITICAL
Sinais: query montada com `+`/f-string/template usando entrada do usuário
(`"... WHERE id = " + str(id)`, `` `... ${x}` `` em SQL).
Detecção: `execute(` com concatenação/interpolação em vez de parâmetros `?`/`:x`.
→ Playbook T2 (parametrizar).

### AP-03 — God Class / God Module — CRITICAL (ou HIGH)
Sinais: um arquivo/classe que concentra DB + regra de negócio + roteamento +
formatação de múltiplos domínios (ex.: `AppManager`, `models.py` gigante).
Detecção: arquivo muito longo com responsabilidades heterogêneas.
→ Playbook T3 (separar em camadas).

### AP-04 — Endpoint de execução arbitrária / rota destrutiva sem auth — CRITICAL
Sinais: rota que executa SQL/comando vindo do body (`/admin/query`), ou que
apaga/reseta dados (`/admin/reset-db`, `DELETE` em massa) sem autenticação.
Detecção: `execute(<entrada do usuário>)`, `DELETE FROM` sem filtro/authz.
→ Playbook T13 (remover/proteger).

### AP-05 — Criptografia insegura / hashing fraco — HIGH (CRITICAL se senhas)
Sinais: `hashlib.md5`/`sha1` para senha, cripto caseira (loops de Base64), sem salt.
Detecção: `md5(`, `sha1(`, funções próprias de "hash".
→ Playbook T4 (bcrypt/argon2 ou `werkzeug.security`).

### AP-06 — Exposição de dados sensíveis — HIGH (CRITICAL conforme dado)
Sinais: senha/hash em resposta de API (`to_dict()` com `password`), número de cartão
ou chave de gateway em logs (`console.log(card)`).
Detecção: campos sensíveis em serialização/logs.
→ Playbook T5 (remover de serialização/logs).

### AP-07 — Estado global mutável / conexão singleton — HIGH
Sinais: variáveis globais mutáveis compartilhadas (`globalCache`, `totalRevenue`),
conexão de DB global reutilizada (`db_connection` module-level, `check_same_thread=False`).
Detecção: estado module-level alterado em runtime; singleton de conexão.
→ Playbook T6 (factory/DI/escopo por requisição).

### AP-08 — Fat Controller / regra de negócio na rota — HIGH
Sinais: cálculo de domínio, montagem de dados e orquestração dentro do handler da rota
(ex.: cálculo de `overdue`, enriquecimento com joins manuais na view).
Detecção: handlers longos com lógica além de I/O HTTP.
→ Playbook T7 (mover para service/model).

### AP-09 — Query N+1 — MEDIUM
Sinais: query dentro de loop (uma consulta por item/usuário), relatórios que iteram
e consultam repetidamente.
Detecção: `for ...: execute(...)` ou `.query...` dentro de laço.
→ Playbook T8 (join/eager loading/agregação).

### AP-10 — Validação de entrada ausente/duplicada — MEDIUM
Sinais: rotas que confiam no payload sem validar; regras de validação repetidas
(copiar/colar) entre create/update.
Detecção: acesso direto a campos do body sem checagem; blocos de validação duplicados.
→ Playbook T10 (validação centralizada/schema).

### AP-11 — Callback Hell / ausência de async-await — MEDIUM
Sinais: callbacks aninhados profundos (pirâmide), controle manual de contadores para
saber quando terminou (Node).
Detecção: `db.get(..., (err, x) => { db.get(..., () => { ... }) })` aninhado.
→ Playbook T9 (Promises/async-await).

### AP-12 — Integridade referencial frágil — MEDIUM
Sinais: `DELETE` que deixa registros órfãos (matrículas/pagamentos sem dono); ausência
de transação em operações multi-tabela.
Detecção: deleção/inserção multi-tabela sem cascata/transação.
→ Playbook T12 (transações/cascata).

### AP-13 — Logging por `print` / `console.log` — LOW
Sinais: `print(...)`/`console.log(...)` como log de aplicação, sem níveis.
→ Playbook T11 (logger estruturado).

### AP-14 — Magic numbers / magic strings — LOW
Sinais: listas de categorias/status hardcoded e repetidas, thresholds soltos
(`if faturamento > 10000`), regra por `cc.startsWith("4")`.
→ Playbook T? (extrair constantes/enums).

### AP-15 — Nomenclatura ruim / tratamento de erro impreciso — LOW
Sinais: nomes abreviados (`usr`, `eml`, `pwd`, `cc`), `except:` nu / `catch` vazio que
engole erros.
→ Renomear; capturar exceções específicas.

---

## Detecção de APIs deprecated (obrigatória)

Ao auditar, sinalize usos de APIs obsoletas e recomende o equivalente moderno:

| API deprecated / legada | Onde aparece | Equivalente moderno recomendado |
|-------------------------|--------------|--------------------------------|
| `datetime.datetime.utcnow()` | Python 3.12+ (deprecated) | `datetime.now(datetime.UTC)` (timezone-aware) |
| `Model.query` / `Query.get(id)` | SQLAlchemy 1.x legacy | API 2.0: `db.session.get(Model, id)` / `select()` |
| `hashlib.md5`/`sha1` para senha | Python | `bcrypt`, `argon2`, ou `werkzeug.security.generate_password_hash` |
| `new Buffer(...)` / `Buffer` cripto caseira | Node.js | `Buffer.from(...)`; para hash de senha `bcrypt`/`argon2` |
| `sqlite3.verbose()` + driver cru | Node.js | driver com Promises (`better-sqlite3`) ou ORM/`node:sqlite` |
| `app.run(debug=True)` em produção | Flask | `debug` via env; servidor WSGI (gunicorn) |
| `body-parser` avulso | Express 4.16+ | `express.json()` / `express.urlencoded()` nativos |
| callbacks de `sqlite3` | Node.js | versão baseada em Promise/`async-await` |

> Registre cada API deprecated como um finding (severidade conforme risco: segurança
> → HIGH/CRITICAL; apenas obsolescência → MEDIUM/LOW) com arquivo:linha e o equivalente.
