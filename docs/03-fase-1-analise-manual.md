# Fase 1 — Análise Manual dos Projetos

## 🎯 Objetivo
Ler o código dos 3 projetos e documentar, para cada um, **no mínimo 5 problemas** (≥ 1 CRITICAL/HIGH, ≥ 2 MEDIUM, ≥ 2 LOW), consolidando os achados na seção **"Análise Manual"** do `README.md`. Esta análise é o insumo que define os padrões que a skill precisará detectar.

## ✅ Pré-condições
- Fase 0 concluída (ambiente pronto, `reports/` criado).
- Acesso de leitura ao código dos 3 projetos.

## 🧠 Contexto necessário
- Escala de severidade (de [challenge.md](challenge.md) › "Definição de Severidades"):
  - **CRITICAL:** falha grave de arquitetura/segurança (credenciais hardcoded, SQL Injection, God Class com DB+regra+rota).
  - **HIGH:** violação forte de MVC/SOLID (regra de negócio no controller, acoplamento sem DI, estado global mutável).
  - **MEDIUM:** duplicação, padronização, performance moderada (N+1, middleware inadequado, validação ausente).
  - **LOW:** legibilidade, nomes ruins, magic numbers.
- Pistas já mapeadas em [01-analise-do-desafio.md](01-analise-do-desafio.md) (use como ponto de partida, mas **verifique arquivo:linha** você mesmo):
  - **Projeto 1 (`code-smells-project`)**: `SECRET_KEY` hardcoded em `app.py`; `DEBUG=True`; rota `/admin/query` executando SQL arbitrário; `/admin/reset-db`; lógica/SQL misturados em `models.py`/`controllers.py`; SQLite via `sqlite3` cru (risco de SQL Injection por concatenação).
  - **Projeto 2 (`ecommerce-api-legacy`)**: God Class `AppManager` (DB + rotas + regras); senhas em texto puro; log do número de cartão + chave do gateway; `badCrypto` em `utils.js`; callbacks aninhados; SQLite `:memory:`.
  - **Projeto 3 (`task-manager-api`)**: `SECRET_KEY` hardcoded e `debug=True` em `app.py`; host `0.0.0.0`; regra de negócio dentro das rotas; possíveis N+1 nas queries de relatório; validações ausentes.

## 📋 Passo a passo
1. **Projeto 1 — `code-smells-project/`**: leia `app.py`, `controllers.py`, `models.py`, `database.py`. Registre ≥ 5 findings com arquivo:linha exatos, respeitando a distribuição (≥1 CRITICAL/HIGH, ≥2 MEDIUM, ≥2 LOW).
2. **Projeto 2 — `ecommerce-api-legacy/`**: leia `src/app.js`, `src/AppManager.js`, `src/utils.js`. Registre ≥ 5 findings com arquivo:linha exatos e a mesma distribuição.
3. **Projeto 3 — `task-manager-api/`**: leia `app.py`, `database.py`, `models/`, `routes/`, `services/`, `utils/`. Registre ≥ 5 findings, incluindo tanto problemas de código quanto oportunidades de melhoria arquitetural.
4. Para cada finding, preencha a **tabela de findings** (template abaixo). Seja específico no sinal de detecção (ex.: "query SQL concatenando `request.args` em `controllers.py:NN`").
5. Consolide as 3 tabelas na seção **"Análise Manual"** do `README.md` (uma subseção por projeto).
6. Revise a distribuição por projeto: confirme ≥ 1 CRITICAL/HIGH, ≥ 2 MEDIUM e ≥ 2 LOW em cada.

## 💻 Comandos (quando aplicável)
```bash
# Contagem aproximada de linhas por arquivo (ajuda a citar arquivo:linha)
wc -l code-smells-project/*.py
wc -l ecommerce-api-legacy/src/*.js
find task-manager-api -name '*.py' | xargs wc -l

# Busca por sinais comuns de anti-patterns
grep -rn "SECRET_KEY\|DEBUG\|debug=True" code-smells-project task-manager-api
grep -rn "password\|pass\|card\|crypto" ecommerce-api-legacy/src
```
> Esta fase é de **análise manual**; não é necessário rodar o Claude CLI aqui. A execução da skill ocorre na Fase 3.

## 📝 Template de tabela de findings (por projeto)
```markdown
### Projeto N — <nome> (<stack>)

| Severidade | Arquivo:Linha | Anti-pattern | Descrição | Impacto | Justificativa |
|------------|---------------|--------------|-----------|---------|---------------|
| CRITICAL   | arquivo.ext:LINHA | <nome> | <o que é> | <consequência> | <por que é relevante> |
| HIGH       | ... | ... | ... | ... | ... |
| MEDIUM     | ... | ... | ... | ... | ... |
| MEDIUM     | ... | ... | ... | ... | ... |
| LOW        | ... | ... | ... | ... | ... |
| LOW        | ... | ... | ... | ... | ... |
```

## 📦 Artefatos produzidos
- Seção **"Análise Manual"** preenchida no `README.md` (3 subseções, uma por projeto).

## 🔍 Validação / Definição de Pronto
- [ ] Projeto 1: ≥ 5 findings com ≥1 CRITICAL/HIGH, ≥2 MEDIUM, ≥2 LOW, cada um com arquivo:linha.
- [ ] Projeto 2: idem.
- [ ] Projeto 3: idem.
- [ ] Todos os findings estão na seção "Análise Manual" do `README.md`.
- [ ] Cada finding tem descrição, impacto e justificativa.

## ➡️ Próximo passo
- Prossiga para [docs/04-fase-2-criacao-da-skill.md](04-fase-2-criacao-da-skill.md).
