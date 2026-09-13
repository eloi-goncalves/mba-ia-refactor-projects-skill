# Fase 3 — Execução da Skill nos 3 Projetos (via Claude CLI)

## 🎯 Objetivo
Executar a skill `refactor-arch` via **Claude CLI** nos 3 projetos, validando as 3 fases em cada um, salvando os relatórios de auditoria em `reports/audit-project-{1,2,3}.md` e commitando o código refatorado. Provar que a skill é agnóstica de tecnologia (Flask e Express) e de nível de organização.

## ✅ Pré-condições
- Fase 2 concluída: skill criada em `code-smells-project/.claude/skills/refactor-arch/`.
- Fase 0: Claude CLI autenticado; dependências instaláveis (`pip`/`npm`).
- Pasta `reports/` existente na raiz.

## 🧠 Contexto necessário
- Leia [challenge.md](challenge.md) › "3. Execução da Skill" e "Validação" (checklist das 3 fases).
- **Regra:** a Fase 2 pausa e pede confirmação — revise o relatório antes de responder `y`.
- **Critérios de aceite (3/3):** Fase 1 detecta stack; Fase 2 ≥ 5 findings; Fase 2 ≥ 1 CRITICAL/HIGH; Fase 3 app funciona (boot + endpoints).
- Os dois projetos Flask usam porta 5000 — valide **um de cada vez**.
- A skill precisa existir **dentro de cada projeto** (`.claude/skills/refactor-arch/`); para os projetos 2 e 3, copie a pasta a partir do Projeto 1.

## 📋 Passo a passo

### Projeto 1 — `code-smells-project` (Python/Flask)
1. Entre no projeto: `cd code-smells-project`.
2. Invoque a skill: `claude "/refactor-arch"`.
3. Valide a **Fase 1**: stack detectada = Python + Flask; domínio = E-commerce; nº de arquivos condiz.
4. Valide a **Fase 2**: ≥ 5 findings com arquivo:linha, ordenados por severidade, incluindo ≥ 1 CRITICAL/HIGH; a skill **pede confirmação**.
5. Salve o relatório da Fase 2 em `reports/audit-project-1.md` (raiz).
6. Confirme com `y` e deixe a **Fase 3** rodar (estrutura MVC).
7. Valide boot + endpoints (veja "Comandos"). Depois **commit**.

### Projeto 2 — `ecommerce-api-legacy` (Node.js/Express)
1. Copie a skill do Projeto 1 para o Projeto 2 (comando na seção "Comandos").
2. Entre no projeto: `cd ../ecommerce-api-legacy`.
3. Invoque: `claude "/refactor-arch"`.
4. Valide as 3 fases (Fase 1 = Node.js + Express; Fase 2 ≥ 5 findings com ≥ 1 CRITICAL/HIGH e confirmação; Fase 3 = MVC).
5. Salve o relatório em `reports/audit-project-2.md`.
6. Valide boot + endpoints e **commit**.

### Projeto 3 — `task-manager-api` (Python/Flask, parcialmente organizado)
1. Copie a skill do Projeto 1 para o Projeto 3.
2. Entre no projeto: `cd ../task-manager-api`.
3. Invoque: `claude "/refactor-arch"`.
4. Valide: Fase 1 detecta Python/Flask e domínio **Task Manager**; Fase 2 acha problemas mesmo com organização parcial (≥ 5 findings, ≥ 1 CRITICAL/HIGH, pede confirmação); Fase 3 melhora a estrutura **sem quebrar** os endpoints.
5. Salve o relatório em `reports/audit-project-3.md`.
6. Valide boot + endpoints e **commit**.

### Iteração (2–4 rodadas)
- Se algum projeto ficar abaixo de 5 findings, sem CRITICAL/HIGH, ou a refatoração quebrar o boot/endpoints: **ajuste os arquivos de referência** da skill (catálogo/playbook/guidelines) e execute novamente. É normal precisar de 2–4 iterações. Após ajustar a skill no Projeto 1, **recopie** para os projetos 2 e 3.

## 💻 Comandos (quando aplicável)
```bash
# --- Projeto 1 ---
cd code-smells-project
claude "/refactor-arch"        # confirme 'y' após revisar o relatório
# Validar boot + endpoints (após refatoração):
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python app.py &      # sobe em http://localhost:5000
sleep 2
curl -s http://localhost:5000/health && curl -s http://localhost:5000/produtos
kill %1
cd ..

# --- Copiar a skill para o Projeto 2 (Linux) ---
mkdir -p ecommerce-api-legacy/.claude/skills
cp -r code-smells-project/.claude/skills/refactor-arch ecommerce-api-legacy/.claude/skills/

# --- Projeto 2 ---
cd ecommerce-api-legacy
claude "/refactor-arch"
npm install
npm start &                    # sobe conforme config.port
sleep 2
curl -s -X POST http://localhost:3000/api/checkout -H 'Content-Type: application/json' -d '{}' || true
kill %1
cd ..

# --- Copiar a skill para o Projeto 3 (Linux) ---
mkdir -p task-manager-api/.claude/skills
cp -r code-smells-project/.claude/skills/refactor-arch task-manager-api/.claude/skills/

# --- Projeto 3 ---
cd task-manager-api
claude "/refactor-arch"
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python app.py &      # sobe em http://localhost:5000
sleep 2
curl -s http://localhost:5000/health && curl -s http://localhost:5000/tasks
kill %1
cd ..
```
> Ajuste portas/rotas dos `curl` conforme a saída real de cada app após a refatoração. Rode os apps Flask um de cada vez (porta 5000).

## 🔎 Checklist de validação (aplicar por projeto)
```markdown
### Fase 1 — Análise
- [ ] Linguagem detectada corretamente
- [ ] Framework detectado corretamente
- [ ] Domínio da aplicação descrito corretamente
- [ ] Número de arquivos analisados condiz com a realidade

### Fase 2 — Auditoria
- [ ] Relatório segue o template dos arquivos de referência
- [ ] Cada finding tem arquivo e linhas exatos
- [ ] Findings ordenados por severidade (CRITICAL → LOW)
- [ ] Mínimo de 5 findings identificados
- [ ] Detecção de APIs deprecated incluída (se aplicável)
- [ ] Skill pausa e pede confirmação antes da Fase 3

### Fase 3 — Refatoração
- [ ] Estrutura de diretórios segue padrão MVC
- [ ] Configuração extraída para módulo de config (sem hardcoded)
- [ ] Models criados para abstrair dados
- [ ] Views/Routes separadas
- [ ] Controllers concentram o fluxo
- [ ] Error handling centralizado
- [ ] Entry point claro
- [ ] Aplicação inicia sem erros
- [ ] Endpoints originais respondem corretamente
```

## 📦 Artefatos produzidos
- `.claude/skills/refactor-arch/` copiada para os 3 projetos.
- Código refatorado (MVC) nos 3 projetos.
- `reports/audit-project-1.md`, `reports/audit-project-2.md`, `reports/audit-project-3.md`.
- Commits do código refatorado de cada projeto.

## 🔍 Validação / Definição de Pronto
- [ ] 3/3 projetos: Fase 1 detecta a stack corretamente.
- [ ] 3/3 projetos: Fase 2 com ≥ 5 findings e ≥ 1 CRITICAL/HIGH.
- [ ] 3/3 projetos: Fase 3 com app funcionando (boot + endpoints).
- [ ] 3 relatórios salvos em `reports/`.
- [ ] Código refatorado commitado nos 3 projetos.

## ➡️ Próximo passo
- Prossiga para [docs/06-fase-4-documentacao-e-entrega.md](06-fase-4-documentacao-e-entrega.md).
