# Fase 0 — Setup e Pré-requisitos

## 🎯 Objetivo
Preparar o ambiente para executar o desafio de ponta a ponta: garantir Claude CLI instalado e autenticado, runtimes (Python e Node.js) e Git disponíveis, confirmar que os 3 projetos estão presentes e criar a estrutura que ainda falta (`reports/`).

## ✅ Pré-condições
- Repositório clonado (fork de `https://github.com/devfullcycle/mba-ia-refactor-projects-skill`).
- Acesso a um terminal Linux com permissão para instalar pacotes.
- Conta habilitada para usar o **Claude CLI**.

## 🧠 Contexto necessário
- Leia [challenge.md](challenge.md) seções "Tecnologias obrigatórias", "Estrutura do repositório" e "Critérios de Aceite".
- Leia [01-analise-do-desafio.md](01-analise-do-desafio.md) (mapa dos projetos e lacunas).
- Stacks reais: Projeto 1 e 3 = Python/Flask; Projeto 2 = Node.js/Express. A skill é executada via **Claude CLI**.

## 📋 Passo a passo
1. Confirme que está na raiz do repositório e que os 3 projetos existem: `code-smells-project/`, `ecommerce-api-legacy/`, `task-manager-api/`.
2. Verifique o **Claude CLI**: rode `claude --version`. Se não existir, instale conforme a documentação oficial e autentique (`claude` / login).
3. Verifique o **Python 3.x** e **pip/venv**: `python3 --version` e `python3 -m venv --help`.
4. Verifique o **Node.js** e **npm**: `node --version` e `npm --version`.
5. Verifique o **Git**: `git --version` e confirme o remoto do fork com `git remote -v`.
6. Crie a pasta de relatórios na raiz: `mkdir -p reports`.
7. Confirme o caminho onde a skill será criada na Fase 2: `code-smells-project/.claude/skills/refactor-arch/` (será criada na Fase 2, não agora).
8. (Opcional, recomendado) Pré-instale dependências para agilizar a validação da Fase 3:
   - Projeto 1: `python3 -m venv code-smells-project/.venv && code-smells-project/.venv/bin/pip install -r code-smells-project/requirements.txt`
   - Projeto 3: `python3 -m venv task-manager-api/.venv && task-manager-api/.venv/bin/pip install -r task-manager-api/requirements.txt`
   - Projeto 2: `(cd ecommerce-api-legacy && npm install)`

## 💻 Comandos (quando aplicável)
```bash
# 1. Estar na raiz e conferir projetos
ls -d code-smells-project ecommerce-api-legacy task-manager-api

# 2. Claude CLI (execução da skill)
claude --version

# 3-5. Runtimes e ferramentas
python3 --version
node --version
npm --version
git --version
git remote -v

# 6. Estrutura que falta
mkdir -p reports
ls -la reports

# 8. (Opcional) Dependências
python3 -m venv code-smells-project/.venv
code-smells-project/.venv/bin/pip install -r code-smells-project/requirements.txt
python3 -m venv task-manager-api/.venv
task-manager-api/.venv/bin/pip install -r task-manager-api/requirements.txt
(cd ecommerce-api-legacy && npm install)
```

## 📦 Artefatos produzidos
- Pasta `reports/` criada na raiz.
- (Opcional) ambientes virtuais `*/.venv` e `ecommerce-api-legacy/node_modules/`.

## 🔍 Validação / Definição de Pronto
- [ ] `claude --version` responde (CLI instalado e autenticado).
- [ ] `python3 --version` e `node --version` respondem.
- [ ] `git --version` responde e o remoto do fork está configurado.
- [ ] Os 3 projetos estão presentes na raiz.
- [ ] Pasta `reports/` existe.

## ➡️ Próximo passo
- Prossiga para [docs/03-fase-1-analise-manual.md](03-fase-1-analise-manual.md).
