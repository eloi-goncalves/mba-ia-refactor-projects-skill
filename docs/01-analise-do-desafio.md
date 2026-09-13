# 01 — Análise do Desafio (destilação do ULTRATHINK)

> Documento-síntese do desafio descrito em [challenge.md](challenge.md). Serve de base para as fases 0 a 4. Autocontido: pode ser lido junto apenas com o `challenge.md`.

## 🎯 Objetivo da entrega (3–5 linhas)

Construir uma **Agent Skill** chamada `refactor-arch` (arquivo principal `SKILL.md` + arquivos de referência em Markdown) que, de forma **agnóstica de tecnologia**, execute 3 fases sequenciais em qualquer projeto: **(1) Análise** de stack/arquitetura, **(2) Auditoria** de anti-patterns por severidade com relatório e confirmação humana, e **(3) Refatoração** para o padrão **MVC** com validação de que a aplicação continua funcionando. A skill deve ser provada nos **3 projetos** do repositório (2 Python/Flask + 1 Node.js/Express), gerando 3 relatórios em `reports/` e documentando tudo no `README.md`.

## 📌 Requisitos obrigatórios e mínimos numéricos

| # | Requisito | Mínimo | Fonte (challenge.md) |
|---|-----------|--------|----------------------|
| R1 | Anti-patterns no catálogo, com severidade distribuída (CRITICAL/HIGH/MEDIUM/LOW) | **≥ 8** | "O catálogo de anti-patterns deve conter no mínimo 8 anti-patterns com severidade distribuída" |
| R2 | Detecção de **APIs deprecated** com equivalente moderno | obrigatória | "O catálogo deve incluir detecção de APIs deprecated" |
| R3 | Padrões de transformação no playbook, com exemplos antes/depois | **≥ 8** | "O playbook deve ter no mínimo 8 padrões de transformação com exemplos de código antes/depois" |
| R4 | Findings por projeto na auditoria | **≥ 5** | "A Fase 2 encontra >= 5 findings: OBRIGATÓRIO (3/3 projetos)" |
| R5 | Findings CRITICAL **ou** HIGH por projeto | **≥ 1** | "Fase 2 inclui pelo menos 1 CRITICAL ou HIGH: OBRIGATÓRIO (3/3 projetos)" |
| R6 | Análise manual por projeto | ≥ 5 problemas (**≥1 CRITICAL/HIGH, ≥2 MEDIUM, ≥2 LOW**) | "identificar e documentar no mínimo 5 problemas, incluindo pelo menos: 1 CRITICAL ou HIGH, 2 MEDIUM, 2 LOW" |
| R7 | Áreas de conhecimento nos arquivos de referência | **5** | "Os arquivos devem cobrir obrigatoriamente as seguintes áreas de conhecimento" |
| R8 | Fases sequenciais da skill | **3** | "implementar o SKILL.md com 3 fases sequenciais" |
| R9 | Fase 2 pausa e pede confirmação antes de modificar | obrigatória | "A Fase 2 deve pausar e pedir confirmação antes de modificar qualquer arquivo" |
| R10 | Fase 3 valida boot + endpoints | obrigatória | "A Fase 3 deve validar o resultado (boot da aplicação + endpoints funcionando)" |
| R11 | Relatórios de auditoria em `reports/` | **3** (`audit-project-{1,2,3}.md`) | "Relatórios de auditoria em reports/ (3 arquivos)" |
| R12 | Skill copiada para os 3 projetos | 3 cópias | "Skill completa em .claude/skills/refactor-arch/ (dentro dos 3 projetos)" |
| R13 | README com 4 seções | A, B, C, D | "README.md deve conter: A) Análise Manual, B) Construção da Skill, C) Resultados, D) Como Executar" |

### 5 áreas de conhecimento obrigatórias (R7)

1. **Análise de projeto** — heurísticas de detecção de linguagem, framework, banco e mapeamento de arquitetura.
2. **Catálogo de anti-patterns** — anti-patterns com sinais de detecção e severidade.
3. **Template de relatório** — formato padronizado da auditoria (Fase 2).
4. **Guidelines de arquitetura** — regras do MVC alvo (Models, Views/Routes, Controllers).
5. **Playbook de refatoração** — transformações concretas por anti-pattern, com exemplos.

## ✅ Critérios de aceite (devem ser verdadeiros em 3/3 projetos)

| # | Critério | Meta |
|---|----------|------|
| A1 | Fase 1 detecta a stack corretamente | 3/3 |
| A2 | Fase 2 encontra ≥ 5 findings | 3/3 |
| A3 | Fase 2 inclui ≥ 1 CRITICAL ou HIGH | 3/3 |
| A4 | Fase 3 — aplicação funciona após a refatoração (boot + endpoints) | 3/3 |

## 🗺️ Mapa dos 3 projetos (stack real detectada)

| Projeto | Stack real | Persistência | Arquivos-fonte | Entidades / Tabelas | Estado |
|---------|-----------|--------------|----------------|---------------------|--------|
| **1. `code-smells-project/`** | Python + **Flask 3.1.1** + `flask-cors 5.0.1` | SQLite `loja.db` via **`sqlite3` cru** | `app.py`, `controllers.py`, `models.py`, `database.py` | `produtos`, `usuarios`, `pedidos`, `itens_pedido` | Monolítico, sem camadas. `SECRET_KEY` hardcoded, `DEBUG=True`, rotas `/admin/reset-db` e `/admin/query` (SQL arbitrário) |
| **2. `ecommerce-api-legacy/`** | Node.js + **Express ^4.18.2** + `sqlite3 ^5.1.6` | SQLite **em memória** (`:memory:`) | `src/app.js`, `src/AppManager.js`, `src/utils.js` | `users`, `courses`, `enrollments`, `payments`, `audit_logs` | God Class `AppManager` (DB + rotas + regras). Domínio LMS/checkout. Senhas em texto puro, log de número de cartão, `badCrypto` |
| **3. `task-manager-api/`** | Python + **Flask** + **SQLAlchemy** + `flask-cors` | SQLite `tasks.db` via **ORM** | `app.py`, `database.py`, `seed.py`, `models/`, `routes/`, `services/`, `utils/` | `tasks`, `users`, `categories` | **Parcialmente organizado** (blueprints + models). Ainda com `SECRET_KEY` hardcoded, `debug=True`, host `0.0.0.0`, possíveis N+1 e regra de negócio nas rotas |

> Observação: os dois projetos Flask usam a **porta 5000** por padrão — devem ser executados/validados **um de cada vez** para evitar conflito de porta.

## ⚠️ Lacunas e riscos identificados

**Lacunas (o que ainda não existe):**
- Não há pasta `.claude/skills/refactor-arch/` em nenhum dos 3 projetos.
- Não há pasta `reports/` na raiz.
- O `README.md` da raiz atualmente contém o texto do desafio; precisará ser reescrito com as seções **A/B/C/D**.
- Não há a skill (`SKILL.md` + arquivos de referência) ainda.

**Riscos de execução:**
- **Claude CLI** precisa estar instalado e autenticado (`claude --version`). Sem isso, a Fase 3 do plano não roda.
- Dependências não instaladas: `pip install -r requirements.txt` (Flask) e `npm install` (Node) antes de validar boot.
- Validar boot **sem quebrar endpoints**: manter contrato de rotas e payloads originais após refatoração.
- Conflito de porta 5000 entre os dois projetos Flask (rodar sequencialmente ou trocar porta na validação).
- Projeto 3 já tem camadas — a Fase 3 deve **melhorar** sem regressão, não reescrever à força.
- Iteração esperada: 2–4 rodadas ajustando arquivos de referência até bater os mínimos (R4/R5).

## 🧭 Convenções adotadas

- **Numeração dos documentos de fase:** `docs/01` a `docs/06` (este índice + fases 0 a 4).
- **Nomes imutáveis:** skill = `refactor-arch`; arquivo principal = `SKILL.md`.
- **Execução da skill:** sempre via **Claude CLI** (`claude "/refactor-arch"`).
- **Idioma:** todos os documentos em pt-BR.

## 📚 Índice navegável (documentos de fase)

| Doc | Fase | Conteúdo |
|-----|------|----------|
| [02-fase-0-setup-e-prerequisitos.md](02-fase-0-setup-e-prerequisitos.md) | Fase 0 | Ambiente, Claude CLI, runtimes, estrutura `reports/` |
| [03-fase-1-analise-manual.md](03-fase-1-analise-manual.md) | Fase 1 | Análise manual dos 3 projetos → seção "Análise Manual" do README |
| [04-fase-2-criacao-da-skill.md](04-fase-2-criacao-da-skill.md) | Fase 2 | Construção da skill `refactor-arch` (SKILL.md + 5 áreas) |
| [05-fase-3-execucao-nos-projetos.md](05-fase-3-execucao-nos-projetos.md) | Fase 3 | Execução via Claude CLI nos 3 projetos + relatórios |
| [06-fase-4-documentacao-e-entrega.md](06-fase-4-documentacao-e-entrega.md) | Fase 4 | README A/B/C/D, conferência de aceite, entrega |

## ➡️ Próximo passo

Prossiga para [docs/02-fase-0-setup-e-prerequisitos.md](02-fase-0-setup-e-prerequisitos.md).
