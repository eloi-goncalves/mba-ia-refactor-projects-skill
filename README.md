# Refatoração Arquitetural Automatizada — Skill `refactor-arch`

Documentação da entrega do desafio de criação da skill `refactor-arch`, que analisa, audita e refatora projetos legados para o padrão **MVC** de forma agnóstica de tecnologia.

> O enunciado original do desafio está preservado em [docs/challenge.md](docs/challenge.md). O plano de execução por fases está em [docs/01-analise-do-desafio.md](docs/01-analise-do-desafio.md).

Projetos-alvo:

| # | Projeto | Stack | Domínio |
|---|---------|-------|---------|
| 1 | `code-smells-project/` | Python + Flask 3.1.1 + `sqlite3` cru | E-commerce (produtos, usuários, pedidos) |
| 2 | `ecommerce-api-legacy/` | Node.js + Express 4.18 + `sqlite3` | LMS com checkout (cursos, matrículas, pagamentos) |
| 3 | `task-manager-api/` | Python + Flask + SQLAlchemy | Task Manager (tasks, usuários, categorias) |

---

## A) Análise Manual

Análise manual do código dos 3 projetos. Cada finding tem severidade, arquivo:linha, anti-pattern, descrição, impacto e justificativa. Escala de severidade conforme [docs/challenge.md](docs/challenge.md) (CRITICAL / HIGH / MEDIUM / LOW).

### Projeto 1 — `code-smells-project` (Python/Flask — E-commerce)

Monólito sem separação de camadas: `app.py` (rotas + config), `controllers.py` (validação + orquestração), `models.py` (regra de negócio + SQL cru), `database.py` (conexão global + schema).

| Severidade | Arquivo:Linha | Anti-pattern | Descrição | Impacto | Justificativa |
|------------|---------------|--------------|-----------|---------|---------------|
| CRITICAL | [models.py:27](code-smells-project/models.py#L27) | SQL Injection | Queries montadas por concatenação de string com entrada do usuário (ex.: `"... WHERE id = " + str(id)`, `login`, `buscar_produtos`) | Permite injeção de SQL, vazamento/adulteração de dados | Entrada não parametrizada em SQL é falha grave de segurança |
| CRITICAL | [app.py:7](code-smells-project/app.py#L7) | Hardcoded Credentials | `SECRET_KEY = "minha-chave-super-secreta-123"` no código; ainda exposta no `/health` ([controllers.py:311](code-smells-project/controllers.py#L311)) | Segredo versionado e vazado via API | Credenciais no código violam segurança básica |
| CRITICAL | [app.py:60](code-smells-project/app.py#L60) | Endpoint de execução arbitrária | `/admin/query` executa SQL arbitrário do body; `/admin/reset-db` apaga todas as tabelas, ambos sem autenticação | RCE de SQL / destruição total de dados por qualquer um | Superfície de ataque catastrófica |
| HIGH | [models.py:1](code-smells-project/models.py#L1) | God Module / mistura de camadas | `models.py` concentra regra de negócio, SQL, cálculo de relatório e formatação de 4 domínios | Impossível testar isolado; qualquer mudança afeta tudo | Viola separação de responsabilidades (MVC/SOLID) |
| HIGH | [database.py:3](code-smells-project/database.py#L3) | Estado global / conexão singleton | Conexão única global (`db_connection`) com `check_same_thread=False` | Condições de corrida; acoplamento global | Estado global mutável dificulta manutenção e concorrência |
| MEDIUM | [models.py:139](code-smells-project/models.py#L139) | Query N+1 | `get_pedidos_usuario`/`get_todos_pedidos` fazem uma query por item e por produto dentro de loops | Degradação de performance conforme cresce o volume | Gargalo clássico de performance |
| MEDIUM | [controllers.py:186](code-smells-project/controllers.py#L186) | Efeito colateral no controller / notificações fake | `print("ENVIANDO EMAIL/SMS/PUSH...")` como "notificação"; regra de notificação no controller | Sem serviço real; lógica acoplada ao controller | Falta de camada de serviço; padronização |
| LOW | [controllers.py:8](code-smells-project/controllers.py#L8) | `print` como logging | Uso de `print` para log em vários pontos | Sem níveis/estrutura de log | Legibilidade/observabilidade ruins |
| LOW | [controllers.py:52](code-smells-project/controllers.py#L52) | Magic values / listas hardcoded | Categorias e status válidos hardcoded e repetidos entre create/update | Duplicação; manutenção propensa a erro | Magic values soltos pelo código |

### Projeto 2 — `ecommerce-api-legacy` (Node.js/Express — LMS/checkout)

`src/app.js` (entry), `src/AppManager.js` (God Class: DB + rotas + regras), `src/utils.js` (config + estado global + cripto caseira).

| Severidade | Arquivo:Linha | Anti-pattern | Descrição | Impacto | Justificativa |
|------------|---------------|--------------|-----------|---------|---------------|
| CRITICAL | [utils.js:1](ecommerce-api-legacy/src/utils.js#L1) | Hardcoded Credentials | `dbPass`, `paymentGatewayKey` (`pk_live_...`), `smtpUser` hardcoded no `config` | Vazamento de chave de produção do gateway de pagamento | Credenciais sensíveis versionadas |
| CRITICAL | [AppManager.js:66](ecommerce-api-legacy/src/AppManager.js#L66) | Log de dados sensíveis (PCI) | `console.log("Processando cartão ${cc} na chave ${config.paymentGatewayKey}")` loga número de cartão e chave | Violação de PCI-DSS; vazamento de cartão | Dados de pagamento nunca devem ser logados |
| HIGH | [AppManager.js:1](ecommerce-api-legacy/src/AppManager.js#L1) | God Class | `AppManager` acumula conexão de DB, criação de schema, rotas HTTP e regra de negócio de checkout | Impossível testar/evoluir; sem camadas | Viola MVC/SOLID por completo |
| HIGH | [utils.js:16](ecommerce-api-legacy/src/utils.js#L16) | Criptografia insegura | `badCrypto` faz "hash" caseiro com Base64 em loop | Senhas efetivamente sem proteção | Nunca implementar cripto própria; usar bcrypt/argon2 |
| HIGH | [utils.js:9](ecommerce-api-legacy/src/utils.js#L9) | Estado global mutável | `globalCache` e `totalRevenue` como estado global compartilhado | Efeitos colaterais imprevisíveis; não escala | Estado global mutável em toda a app |
| MEDIUM | [AppManager.js:91](ecommerce-api-legacy/src/AppManager.js#L91) | Query N+1 / callback hell | `/api/admin/financial-report` itera cursos → matrículas → users/payments com queries aninhadas | Performance ruim e código ilegível | N+1 clássico + pirâmide de callbacks |
| MEDIUM | [AppManager.js:132](ecommerce-api-legacy/src/AppManager.js#L132) | Integridade referencial / registros órfãos | `DELETE FROM users` deixa matrículas e pagamentos órfãos (a própria resposta admite) | Dados inconsistentes no banco | Falta de transação/cascata |
| LOW | [AppManager.js:29](ecommerce-api-legacy/src/AppManager.js#L29) | Nomenclatura ruim | Campos do body abreviados: `usr`, `eml`, `pwd`, `c_id`, `cc` | Baixa legibilidade | Nomes pouco descritivos |
| LOW | [AppManager.js:65](ecommerce-api-legacy/src/AppManager.js#L65) | Magic logic | Aprovação de pagamento por `cc.startsWith("4")` | Regra obscura embutida | Magic values / lógica frágil |

### Projeto 3 — `task-manager-api` (Python/Flask — Task Manager)

Parcialmente organizado (blueprints em `routes/`, `models/` SQLAlchemy, `services/`, `utils/`), mas com problemas de segurança e regra de negócio nas rotas.

| Severidade | Arquivo:Linha | Anti-pattern | Descrição | Impacto | Justificativa |
|------------|---------------|--------------|-----------|---------|---------------|
| CRITICAL | [models/user.py:28](task-manager-api/models/user.py#L28) | Hashing inseguro (MD5) | `set_password`/`check_password` usam `hashlib.md5` sem salt | Senhas quebráveis trivialmente | MD5 é deprecated para senhas; usar bcrypt/argon2 |
| HIGH | [models/user.py:16](task-manager-api/models/user.py#L16) | Exposição de senha | `User.to_dict()` inclui o hash `password`; retornado por `/users` e `/users/<id>` | Vazamento de credenciais na API | Dados sensíveis nunca em respostas |
| HIGH | [services/notification_service.py:9](task-manager-api/services/notification_service.py#L9) | Credenciais SMTP hardcoded | `email_password = 'senha123'` e usuário SMTP no código | Segredo versionado | Credenciais no código |
| MEDIUM | [routes/report_routes.py:53](task-manager-api/routes/report_routes.py#L53) | Query N+1 | `summary_report` itera usuários e consulta tasks por usuário em loop (idem `user_productivity`) | Performance degrada com volume | N+1 em relatórios |
| MEDIUM | [routes/task_routes.py:14](task-manager-api/routes/task_routes.py#L14) | Regra de negócio na rota (fat controller) | Cálculo de `overdue`, montagem de dict e enriquecimento com user/category dentro da rota | Duplicação e baixa testabilidade | Lógica deveria estar em model/serviço |
| MEDIUM | [app.py:12](task-manager-api/app.py#L12) | Config hardcoded / debug | `SECRET_KEY` hardcoded, `debug=True`, `host='0.0.0.0'` | Segredo exposto; debug em produção | Configuração deveria vir de ambiente |
| LOW | [routes/task_routes.py:61](task-manager-api/routes/task_routes.py#L61) | `except:` genérico | `except:` nu engole qualquer erro retornando 500 genérico | Mascara bugs; difícil depurar | Tratamento de erro impreciso |
| LOW | [routes/task_routes.py:16](task-manager-api/routes/task_routes.py#L16) | Serialização duplicada | Montagem manual de dict repetida em vários pontos em vez de reusar `to_dict()` | Duplicação de código | Padronização/legibilidade |

> Distribuição por projeto (mínimos do desafio ✅): cada projeto tem ≥ 5 findings, com ≥ 1 CRITICAL/HIGH, ≥ 2 MEDIUM e ≥ 2 LOW.

---

## B) Construção da Skill

A skill vive em [code-smells-project/.claude/skills/refactor-arch/](code-smells-project/.claude/skills/refactor-arch/SKILL.md) e é a fonte canônica (copiada para os demais projetos na Fase 3).

**Estrutura (SKILL.md + 5 arquivos de referência):**

| Arquivo | Área de conhecimento |
|---------|----------------------|
| [SKILL.md](code-smells-project/.claude/skills/refactor-arch/SKILL.md) | Orquestra as 3 fases; frontmatter (`name`/`description`) + instruções |
| [reference/project-analysis.md](code-smells-project/.claude/skills/refactor-arch/reference/project-analysis.md) | Análise de projeto (detecção de stack/DB/domínio) |
| [reference/anti-patterns.md](code-smells-project/.claude/skills/refactor-arch/reference/anti-patterns.md) | Catálogo de anti-patterns + APIs deprecated |
| [reference/report-template.md](code-smells-project/.claude/skills/refactor-arch/reference/report-template.md) | Template do relatório de auditoria |
| [reference/mvc-guidelines.md](code-smells-project/.claude/skills/refactor-arch/reference/mvc-guidelines.md) | Guidelines de arquitetura MVC |
| [reference/refactoring-playbook.md](code-smells-project/.claude/skills/refactor-arch/reference/refactoring-playbook.md) | Playbook de transformações antes/depois |

**Decisões de design:**

- **Conhecimento fora do prompt:** o `SKILL.md` é enxuto e apenas orquestra as fases; o conhecimento de domínio fica nos arquivos de referência, lidos sob demanda. Isso mantém o prompt principal curto e a skill fácil de evoluir.
- **3 fases com portões:** Fase 1 (análise, read-only) → Fase 2 (auditoria, read-only, **pausa e pede confirmação**) → Fase 3 (refatoração + validação de boot/endpoints). Nenhuma alteração de arquivo ocorre antes do `y`.
- **Catálogo (15 anti-patterns):** cobre as 4 severidades e foi derivado da Análise Manual real dos 3 projetos — SQL Injection, credenciais hardcoded, God Class, execução arbitrária (CRITICAL); cripto insegura, exposição de dados, estado global, fat controller (HIGH); N+1, validação ausente, callback hell, integridade referencial (MEDIUM); logging por `print`, magic values, nomenclatura/`except:` nu (LOW). Inclui uma seção dedicada de **APIs deprecated** (`datetime.utcnow()`, `Query.get()`/`Model.query` legado do SQLAlchemy 2.0, `md5`, `Buffer` caseiro, `body-parser` avulso etc.) com o equivalente moderno.
- **Playbook (14 transformações):** cada anti-pattern tem uma transformação antes/depois correspondente (T1–T14), com exemplos em Python/Flask **e** Node.js/Express.
- **Agnosticismo de tecnologia:** heurísticas de detecção por sinais (arquivos/imports) em vez de presumir a stack; guidelines e playbook trazem exemplos paralelos Flask/Express; a Fase 3 adapta-se ao nível de organização (monólito vs. parcialmente organizado).
- **Desafios previstos:** preservar o contrato dos endpoints na refatoração e validar boot sem quebrar rotas — endereçados por regras explícitas na Fase 3 e pelo checklist de validação.

## C) Resultados

### Resumo dos relatórios de auditoria (Fase 2)

| Projeto | Findings | CRITICAL | HIGH | MEDIUM | LOW | Relatório |
|---------|:---:|:---:|:---:|:---:|:---:|-----------|
| 1 — `code-smells-project` | 9 | 3 | 2 | 2 | 2 | [reports/audit-project-1.md](reports/audit-project-1.md) |
| 2 — `ecommerce-api-legacy` | 10 | 3 | 3 | 2 | 2 | [reports/audit-project-2.md](reports/audit-project-2.md) |
| 3 — `task-manager-api` | 8 | 1 | 2 | 3 | 2 | [reports/audit-project-3.md](reports/audit-project-3.md) |

### Antes / depois da estrutura

**Projeto 1 (Flask, monólito → MVC):**
```
ANTES: app.py + controllers.py + models.py + database.py (tudo misturado)
DEPOIS: app.py (composition root) + src/{config,database,models,controllers,services,views,middlewares}
```

**Projeto 2 (Express, God Class → MVC):**
```
ANTES: src/{app.js, AppManager.js (DB+rotas+regra), utils.js (config+estado global+badCrypto)}
DEPOIS: src/{config,database,models,controllers,routes,services,middlewares,utils} + app.js (composition root)
```

**Projeto 3 (Flask/SQLAlchemy, parcial → melhorado):**
```
ANTES: models/ + routes/ + services/ + utils/ (com MD5, senha exposta, N+1, regra na rota)
DEPOIS: + config/settings.py; hashing seguro; serializer no model (overdue/relações); N+1 corrigido; SMTP via env
```

### Checklist de validação por projeto

| Item | P1 | P2 | P3 |
|------|:--:|:--:|:--:|
| Fase 1 — linguagem/framework/domínio/arquivos corretos | ✅ | ✅ | ✅ |
| Fase 2 — template, arquivo:linha, ordenado, ≥ 5 findings, deprecated, confirmação | ✅ | ✅ | ✅ |
| Fase 3 — estrutura MVC, config sem hardcoded, models, views/rotas, controllers, erro central, entry point | ✅ | ✅ | ✅ |
| Fase 3 — **aplicação inicia sem erros** | ✅ | ⏳ pendente (npm) | ✅ |
| Fase 3 — **endpoints originais respondem** | ✅ | ⏳ pendente (npm) | ✅ |

> **Projeto 2:** o código foi refatorado para MVC e passou na verificação de sintaxe (`node --check`) em 17/17 arquivos, mas a validação de **boot + endpoints** depende de `npm install` (bloqueado por rede no ambiente atual). Ver [docs/08-pendencias.md](docs/08-pendencias.md).

### Logs das aplicações rodando (após refatoração)

**Projeto 1** — `GET /health`:
```json
{"counts":{"pedidos":0,"produtos":10,"usuarios":3},"database":"connected","status":"ok","versao":"1.0.0"}
```
`POST /login` (senha com hash) retorna 200; senha errada retorna 401; `GET /usuarios` não expõe `senha`.

**Projeto 3** — `GET /tasks` (com `overdue` e relações, sem N+1):
```json
[{"id":1,"title":"Primeira task","overdue":true,"user_name":"Joao","category_name":"Backend", ...}]
```
`GET /users` não expõe `password`; `GET /reports/summary` responde com estatísticas agregadas.

### Observações sobre stacks diferentes

- **Mesma skill, transformações adaptadas:** no monólito Flask (P1) a skill criou todas as camadas do zero; no Express (P2) quebrou a God Class e trocou callbacks por async/await; no Flask/SQLAlchemy já organizado (P3) fez melhorias cirúrgicas (segurança, N+1, serializer) sem reescrever.
- **Agnosticismo confirmado:** detecção de stack e catálogo/playbook funcionaram nas 3 bases com níveis de organização distintos.

## D) Como Executar

### Pré-requisitos
- **Claude CLI** instalado e autenticado (`claude --version`).
- **Python 3.x** + `pip`/`venv` (Projetos 1 e 3).
- **Node.js** + `npm` (Projeto 2).

### Executar a skill em cada projeto (Claude CLI)
```bash
# Projeto 1
cd code-smells-project
claude "/refactor-arch"

# Projeto 2 (a skill já está copiada em .claude/skills/refactor-arch/)
cd ../ecommerce-api-legacy
claude "/refactor-arch"

# Projeto 3 (idem)
cd ../task-manager-api
claude "/refactor-arch"
```
> A Fase 2 pausa e pede confirmação antes de qualquer alteração. Salve o relatório em `reports/audit-project-{1,2,3}.md`.

### Rodar e validar as aplicações refatoradas
```bash
# Projeto 1 (Flask)
cd code-smells-project && python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python app.py         # http://localhost:5000
curl -s localhost:5000/health

# Projeto 2 (Express) — requer acesso à rede para instalar deps
cd ../ecommerce-api-legacy && npm install && npm start   # http://localhost:3000

# Projeto 3 (Flask/SQLAlchemy)
cd ../task-manager-api && python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python app.py         # http://localhost:5000
curl -s localhost:5000/tasks
```
> Os dois apps Flask usam a porta 5000 — rode um de cada vez.

### Ordem de execução sugerida
1. Análise manual (seção A) → 2. Criar a skill (seção B) → 3. Executar nos 3 projetos → 4. Documentar/validar (seções C/D). Detalhes por fase em [docs/](docs/01-analise-do-desafio.md).
