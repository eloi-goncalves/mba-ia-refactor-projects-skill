# Referência — Análise de Projeto (Fase 1)

Heurísticas para detectar linguagem, framework, banco de dados e mapear a
arquitetura atual, de forma agnóstica de tecnologia. **Não altere arquivos**;
apenas leia e infira.

## 1. Detecção de linguagem e gerenciador de pacotes

| Sinal (arquivo) | Linguagem / Ecossistema |
|-----------------|-------------------------|
| `requirements.txt`, `pyproject.toml`, `Pipfile`, `*.py` | Python (pip/poetry) |
| `package.json`, `*.js`, `*.ts` | Node.js (npm/yarn/pnpm) |
| `go.mod`, `*.go` | Go |
| `pom.xml`, `build.gradle`, `*.java` | Java |
| `composer.json`, `*.php` | PHP |
| `Gemfile`, `*.rb` | Ruby |

Conte os arquivos-fonte reais (exclua dependências: `node_modules/`, `.venv/`,
`dist/`, `build/`).

## 2. Detecção de framework (+ versão)

- **Python:** procure imports `from flask import ...` / `import flask` (Flask);
  `fastapi`, `django`, `flask_sqlalchemy`. Versão em `requirements.txt`/lockfile.
- **Node.js:** procure `require('express')` / `import express` (Express);
  `fastify`, `koa`, `@nestjs/*`. Versão em `package.json` → `dependencies`.
- Registre a versão exata quando disponível (ex.: `Flask 3.1.1`, `Express ^4.18.2`).

## 3. Detecção de banco de dados e camada de acesso

| Sinal | Banco / Acesso |
|-------|----------------|
| `sqlite3.connect(...)`, `require('sqlite3')`, `*.db` | SQLite (driver cru) |
| `flask_sqlalchemy`, `db.Model`, `SQLAlchemy(...)` | SQLAlchemy (ORM) |
| `psycopg2`, `pg`, `mysql2`, `mongoose` | Postgres / MySQL / MongoDB |
| `CREATE TABLE ...` no código | Schema definido em código |

Para descobrir **tabelas/entidades**: procure `CREATE TABLE <nome>`, classes
`db.Model` (`__tablename__`), ou nomes de tabela em queries `FROM <tabela>`.

## 4. Detecção do domínio da aplicação

Infira o domínio pelos nomes de rotas, tabelas e entidades:
- `produtos`, `pedidos`, `usuarios`, `itens_pedido` → E-commerce.
- `courses`, `enrollments`, `payments`, `checkout` → LMS / educação com pagamentos.
- `tasks`, `categories`, `users`, `priority`, `due_date` → Task Manager.

## 5. Mapeamento da arquitetura atual

Classifique o nível de organização:
- **Monolítica sem camadas:** tudo em poucos arquivos; rotas, regra de negócio e SQL
  misturados (ex.: um `models.py` com SQL + regra + formatação; uma `AppManager` com
  DB + rotas).
- **Parcialmente organizada:** já há pastas por responsabilidade (`models/`,
  `routes/`, `services/`), mas com vazamentos (regra na rota, dados sensíveis expostos).
- **MVC/camadas:** separação clara entre config, models, controllers, views/routes,
  middlewares e entry point.

Anote onde estão hoje: **config**, **entry point**, **rotas**, **acesso a dados** e
**regra de negócio** — isso guia a Fase 3.

## 6. Saída da Fase 1

Preencha e imprima:

```
Language:      <...>
Framework:     <... + versão>
Dependencies:  <deps relevantes>
Domain:        <...>
Architecture:  <monolítica | parcialmente organizada | camadas>
Source files:  <N> files analyzed
DB tables:     <lista>
```
