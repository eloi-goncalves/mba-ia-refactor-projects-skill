# Fase 2 — Criação da Skill `refactor-arch`

## 🎯 Objetivo
Construir a Agent Skill `refactor-arch` (arquivo `SKILL.md` + arquivos de referência em Markdown) que executa 3 fases sequenciais (Análise → Auditoria → Refatoração), cobre as 5 áreas de conhecimento obrigatórias e é **agnóstica de tecnologia** (Python/Flask e Node.js/Express). A skill é criada em `code-smells-project/.claude/skills/refactor-arch/`.

## ✅ Pré-condições
- Fase 1 concluída (você entende os anti-patterns reais dos 3 projetos).
- Claude CLI instalado (Fase 0).

## 🧠 Contexto necessário
- Leia [challenge.md](challenge.md) › "2. Criação da Skill" (áreas de conhecimento e requisitos da skill).
- **Nomes imutáveis:** skill = `refactor-arch`; arquivo principal = `SKILL.md`. Não renomeie.
- **Path (Claude Code):** `.claude/skills/refactor-arch/`.
- Mínimos obrigatórios (de [01-analise-do-desafio.md](01-analise-do-desafio.md), tabela R1–R10):
  - Catálogo com **≥ 8 anti-patterns** com severidade distribuída (CRITICAL/HIGH/MEDIUM/LOW).
  - Catálogo inclui **detecção de APIs deprecated** (com equivalente moderno).
  - Playbook com **≥ 8 transformações** com exemplos antes/depois.
  - **Fase 2 pausa e pede confirmação** antes de modificar arquivos.
  - **Fase 3 valida boot + endpoints**.

## 📋 Passo a passo
1. Crie a estrutura de pastas: `code-smells-project/.claude/skills/refactor-arch/`.
2. Crie o **`SKILL.md`** com frontmatter (nome `refactor-arch` + descrição de quando acionar) e o corpo descrevendo as **3 fases** e apontando para os arquivos de referência.
3. Crie os **arquivos de referência em Markdown** cobrindo as **5 áreas de conhecimento** (sugestão de organização abaixo — nomes/quantidade livres, desde que cubram as 5 áreas):
   - `reference/project-analysis.md` — **Análise de projeto**: heurísticas de detecção de linguagem, framework, banco e mapeamento de arquitetura (ex.: `requirements.txt`/`package.json`, imports Flask/Express, uso de `sqlite3`/SQLAlchemy).
   - `reference/anti-patterns.md` — **Catálogo**: ≥ 8 anti-patterns, cada um com sinais de detecção e severidade; **inclua uma seção de APIs deprecated**.
   - `reference/report-template.md` — **Template de relatório**: formato do relatório de auditoria da Fase 2 (cabeçalho, summary por severidade, findings com arquivo:linha, total).
   - `reference/mvc-guidelines.md` — **Guidelines de arquitetura**: responsabilidades de Models, Views/Routes, Controllers, config, middleware/error handler, entry point.
   - `reference/refactoring-playbook.md` — **Playbook**: ≥ 8 transformações com exemplo antes/depois, mapeadas aos anti-patterns.
4. Garanta **agnosticismo de tecnologia**: os arquivos de referência devem tratar Python/Flask **e** Node.js/Express (ex.: config → `config/settings.py` ou `src/config/index.js`; rotas → blueprints Flask ou routers Express).
5. Faça o `SKILL.md` **instruir explicitamente**: Fase 2 imprime o relatório e **pergunta** `Proceed with refactoring (Phase 3)? [y/n]`, só seguindo com confirmação; Fase 3 executa o boot e testa os endpoints ao final.
6. Revise os mínimos numéricos: conte os anti-patterns (≥ 8) e as transformações (≥ 8) e confirme a seção de APIs deprecated.

## 💻 Comandos (quando aplicável)
```bash
# Criar a estrutura da skill no Projeto 1 (fonte canônica da skill)
mkdir -p code-smells-project/.claude/skills/refactor-arch/reference

# Conferir os mínimos após escrever os arquivos de referência
grep -ciE '^\s*###?\s' code-smells-project/.claude/skills/refactor-arch/reference/anti-patterns.md
grep -ciE 'antes|before' code-smells-project/.claude/skills/refactor-arch/reference/refactoring-playbook.md
```
> A **criação do conteúdo** dos arquivos é feita por você (agente/humano) escrevendo Markdown; o Claude CLI só é invocado na Fase 3 para **executar** a skill.

## 🧩 Esqueleto sugerido do `SKILL.md`
```markdown
---
name: refactor-arch
description: Analisa, audita e refatora um projeto para o padrão MVC de forma agnóstica de tecnologia. Aciona quando o usuário pedir /refactor-arch ou refatoração arquitetural.
---

# refactor-arch

Refatoração arquitetural automatizada em 3 fases sequenciais.

## Fase 1 — Análise
Detecte linguagem, framework, banco e arquitetura seguindo `reference/project-analysis.md`.
Imprima o resumo (Language, Framework, Dependencies, Domain, Architecture, Source files, DB tables).

## Fase 2 — Auditoria
Cruze o código com `reference/anti-patterns.md` (inclui APIs deprecated).
Gere o relatório no formato de `reference/report-template.md` (findings com arquivo:linha, ordenados por severidade).
**PAUSE e pergunte:** "Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]". Só continue se confirmado.

## Fase 3 — Refatoração
Reestruture para MVC seguindo `reference/mvc-guidelines.md` e aplique `reference/refactoring-playbook.md`.
Ao final, **valide**: a aplicação inicia sem erros e os endpoints originais respondem. Imprima o checklist de validação.
```

## 📦 Artefatos produzidos
- `code-smells-project/.claude/skills/refactor-arch/SKILL.md`.
- Arquivos de referência em `code-smells-project/.claude/skills/refactor-arch/reference/` cobrindo as 5 áreas.

## 🔍 Validação / Definição de Pronto
- [ ] `SKILL.md` existe com o nome `refactor-arch` e descreve as 3 fases.
- [ ] As 5 áreas de conhecimento estão cobertas nos arquivos de referência.
- [ ] Catálogo com ≥ 8 anti-patterns e severidade distribuída.
- [ ] Catálogo inclui detecção de APIs deprecated com equivalente moderno.
- [ ] Playbook com ≥ 8 transformações com exemplos antes/depois.
- [ ] Fase 2 instrui pausa + confirmação; Fase 3 instrui validação de boot + endpoints.
- [ ] Conteúdo é agnóstico (cobre Flask e Express).

## ➡️ Próximo passo
- Prossiga para [docs/05-fase-3-execucao-nos-projetos.md](05-fase-3-execucao-nos-projetos.md).
