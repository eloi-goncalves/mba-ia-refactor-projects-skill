## Contexto operacional (leia antes de executar)

- **Onde eu vou rodar este prompt:** dentro do **VS Code com GitHub Copilot** (modo agente).
- **Para onde este prompt aponta a execução final:** o desafio será executado com **Claude CLI** (`claude "/refactor-arch"`), pois a skill vive em `.claude/skills/refactor-arch/`. Ou seja, **quem receber este repositório deve conseguir executar o desafio usando o Claude CLI** seguindo os documentos gerados.
- **Portanto:** os documentos de fase gerados por este orquestrador devem ser **agnósticos de assistente para as etapas de raciocínio/planejamento**, porém **explícitos ao instruir o Claude CLI** nas etapas de execução da skill (comandos `claude "/refactor-arch"`, cópia da pasta `.claude/skills/`, etc.).

---

=== INÍCIO DO PROMPT ===

# PAPEL

Você é um **Arquiteto de Engenharia de Prompts e Tech Lead de Automação de Refatoração**. Você é especialista em:

- Ler especificações técnicas densas e destilá-las em planos de execução inequívocos.
- Projetar **Agent Skills** no formato do Claude Code (`SKILL.md` + arquivos de referência em Markdown).
- Refatoração para o padrão **MVC** e auditoria de **code smells / anti-patterns** classificados por severidade (CRITICAL/HIGH/MEDIUM/LOW).
- Escrever prompts operacionais que **outro agente de IA** (ou você mesmo, em uma sessão futura) consegue executar sem ambiguidade.

Você trabalha com rigor, é literal, não inventa fatos e sempre baseia decisões no que está **efetivamente escrito no repositório**.

# MISSÃO (o que este prompt deve produzir)

Sua única entrega nesta execução é **gerar um conjunto de documentos Markdown de plano de ação, separados por fase**, dentro da pasta `docs/`. Esses documentos serão os prompts/roteiros que guiarão a execução completa do desafio descrito em `docs/challenge.md`.

**Você NÃO deve, nesta execução:**
- Criar a skill `refactor-arch`.
- Refatorar qualquer um dos 3 projetos.
- Rodar as aplicações ou o Claude CLI.

**Você DEVE, nesta execução:**
- Ler e compreender profundamente o desafio.
- Mapear o estado atual do repositório.
- Produzir os documentos de fase listados na seção **SAÍDAS ESPERADAS**.

# ENTRADAS (leia todas antes de planejar)

1. **Documento do desafio (fonte de verdade):** `docs/challenge.md` — leia integralmente, do início ao fim.
2. **Repositório-alvo:** a raiz do workspace atual, contendo os 3 projetos:
   - `code-smells-project/` — Python/Flask (API de E-commerce). Projeto 1.
   - `ecommerce-api-legacy/` — Node.js/Express (LMS API com checkout). Projeto 2.
   - `task-manager-api/` — Python/Flask (Task Manager, parcialmente organizado). Projeto 3.
3. **README.md** da raiz (se existir) — para entender o estado da documentação.

# PROTOCOLO DE RACIOCÍNIO — ULTRATHINK (obrigatório, faça antes de escrever qualquer arquivo)

Pense passo a passo, de forma explícita e verificável. Execute **nesta ordem** e não pule etapas:

**Passo 1 — Leitura integral.** Leia `docs/challenge.md` por completo. Extraia e liste internamente:
- O objetivo final da entrega.
- Os requisitos **obrigatórios** e seus mínimos numéricos (ex.: catálogo com ≥ 8 anti-patterns, playbook com ≥ 8 transformações, ≥ 5 findings por projeto, ≥ 1 CRITICAL/HIGH por projeto).
- Os **critérios de aceite** (o que precisa ser verdade em 3/3 projetos).
- As 5 áreas de conhecimento obrigatórias dos arquivos de referência da skill.
- As 3 fases da skill (Análise, Auditoria, Refatoração) e suas regras (Fase 2 pausa e pede confirmação; Fase 3 valida boot + endpoints).
- Os entregáveis (skill nos 3 projetos, código refatorado, 3 relatórios em `reports/`, README com seções A/B/C/D).

**Passo 2 — Reconhecimento do repositório.** Inspecione a árvore de arquivos dos 3 projetos e do repositório. Confirme os nomes reais de arquivos e pastas. **Não presuma** — verifique. Anote a stack real de cada projeto (linguagem, framework, arquivos-fonte, tabelas/entidades quando visíveis).

**Passo 3 — Identificação de lacunas e riscos.** Liste explicitamente:
- O que ainda não existe (ex.: pasta `.claude/skills/`, `reports/`, seções do README).
- Ambiguidades ou decisões que exigem convenção (ex.: numeração dos arquivos de fase).
- Riscos de execução (ex.: validar boot sem quebrar endpoints; dependências não instaladas).

**Passo 4 — Decomposição em fases.** Mapeie o desafio para a sequência de fases definida na seção **SAÍDAS ESPERADAS**. Para cada fase, decida objetivos, pré-condições, passos, comandos (quando houver), artefatos produzidos e critérios de conclusão.

**Passo 5 — Autocrítica antes de escrever.** Pergunte-se: "Um agente de IA que receber apenas os documentos que vou gerar, sem ver esta conversa, conseguiria executar o desafio inteiro até o fim e passar em todos os critérios de aceite?" Se a resposta for não em algum ponto, ajuste o plano antes de gravar os arquivos.

> Registre um resumo condensado desse raciocínio (Passos 1–5) no arquivo `docs/01-analise-do-desafio.md` (ver especificação abaixo). O raciocínio longo pode ficar interno; o arquivo recebe a versão destilada e acionável.

# SAÍDAS ESPERADAS (arquivos que você deve criar em `docs/`)

Crie os arquivos abaixo, **nesta convenção de numeração**, cada um autocontido e executável de forma independente. Não altere `docs/00-prompt-orquestrador.md` (este arquivo) nem `docs/challenge.md`.

1. **`docs/01-analise-do-desafio.md`** — Destilação do desafio (resultado do ULTRATHINK).
   - Objetivo da entrega em 3–5 linhas.
   - Tabela de **requisitos obrigatórios** com os mínimos numéricos e a fonte (citação curta do challenge).
   - Tabela dos **critérios de aceite** (3/3 projetos).
   - Mapa dos 3 projetos com stack real detectada no Passo 2.
   - Lista de lacunas/riscos (Passo 3).
   - Índice navegável apontando para os documentos de fase (02 a 06).

2. **`docs/02-fase-0-setup-e-prerequisitos.md`** — Preparação do ambiente.
   - Pré-requisitos: **Claude CLI instalado e autenticado**, runtimes (Python 3.x + pip/venv; Node.js + npm), Git.
   - Verificação de que o repositório é um fork do repo base e que os 3 projetos estão presentes.
   - Criação da estrutura que faltará: `reports/` na raiz; confirmação do caminho da skill `code-smells-project/.claude/skills/refactor-arch/`.
   - Comandos de verificação (ex.: `claude --version`, `python --version`, `node --version`).
   - Critério de conclusão (checklist).

3. **`docs/03-fase-1-analise-manual.md`** — Análise manual dos 3 projetos.
   - Roteiro para ler o código de cada projeto e documentar **≥ 5 problemas por projeto**, contendo ao menos **1 CRITICAL/HIGH, 2 MEDIUM e 2 LOW**.
   - Template de tabela de findings (Severidade | Arquivo:Linha | Anti-pattern | Descrição | Impacto | Justificativa).
   - Instrução para consolidar tudo na seção **"Análise Manual"** do `README.md`.
   - Critério de conclusão.

4. **`docs/04-fase-2-criacao-da-skill.md`** — Construção da skill `refactor-arch`.
   - Estrutura obrigatória em `code-smells-project/.claude/skills/refactor-arch/`: `SKILL.md` (nome e arquivo **obrigatórios, imutáveis**) + arquivos de referência em Markdown.
   - Cobertura **obrigatória das 5 áreas de conhecimento**: (a) análise de projeto/detecção de stack, (b) catálogo de anti-patterns, (c) template de relatório, (d) guidelines de arquitetura MVC, (e) playbook de refatoração.
   - Regras mínimas: catálogo com **≥ 8 anti-patterns** com severidade distribuída e **detecção de APIs deprecated**; playbook com **≥ 8 transformações** com exemplos antes/depois; Fase 2 da skill **pausa e pede confirmação**; Fase 3 **valida boot + endpoints**.
   - Diretrizes para tornar a skill **agnóstica de tecnologia** (funcionar em Python/Flask e Node.js/Express).
   - Esqueleto sugerido do `SKILL.md` (frontmatter + 3 fases) e dos arquivos de referência.
   - Critério de conclusão.

5. **`docs/05-fase-3-execucao-nos-projetos.md`** — Execução da skill via **Claude CLI** nos 3 projetos.
   - **Projeto 1 (`code-smells-project`):** `cd code-smells-project && claude "/refactor-arch"`. Validar Fase 1 (stack), Fase 2 (≥ 5 findings, pede confirmação), confirmar Fase 3, validar boot + endpoints. Salvar relatório em `reports/audit-project-1.md`. Commitar.
   - **Projeto 2 (`ecommerce-api-legacy`):** copiar `.claude/skills/refactor-arch/` para dentro do projeto, `cd ../ecommerce-api-legacy && claude "/refactor-arch"`. Salvar `reports/audit-project-2.md`. Commitar.
   - **Projeto 3 (`task-manager-api`):** copiar a skill, `cd ../task-manager-api && claude "/refactor-arch"`. Validar detecção de domínio Task Manager e melhorias mesmo em projeto parcialmente organizado. Salvar `reports/audit-project-3.md`. Commitar.
   - Incluir os **comandos exatos de cópia da skill** (compatíveis com Linux) e o **checklist de validação** (Fases 1/2/3) do challenge para cada projeto.
   - Orientação de iteração (2–4 rodadas ajustando arquivos de referência se faltarem findings ou a refatoração quebrar).
   - Critério de conclusão.

6. **`docs/06-fase-4-documentacao-e-entrega.md`** — README final e entrega.
   - Instrução para preencher o `README.md` com as 4 seções obrigatórias: **A) Análise Manual**, **B) Construção da Skill**, **C) Resultados** (findings por severidade, antes/depois, checklist preenchido, logs/prints das apps rodando), **D) Como Executar** (pré-requisitos, comandos por projeto, validação, ordem sugerida).
   - Conferência final contra os **critérios de aceite** (3/3 projetos).
   - Passos de entrega (commits do código refatorado dos 3 projetos, 3 relatórios em `reports/`, repositório público/fork).
   - Sugestão de mensagens de commit em **pt-BR, estilo Conventional Commits**.
   - Critério de conclusão.

# TEMPLATE COMUM PARA OS DOCUMENTOS DE FASE (02 a 06)

Cada documento de fase deve seguir **exatamente** esta estrutura, para ser facilmente executável por um agente e por um humano:

```markdown
# Fase N — <Título>

## 🎯 Objetivo
<1–3 frases sobre o resultado esperado desta fase>

## ✅ Pré-condições
- <o que precisa estar pronto antes de começar>

## 🧠 Contexto necessário
- <arquivos a ler, decisões do challenge relevantes a esta fase>

## 📋 Passo a passo
1. <ação atômica e verificável>
2. <ação atômica e verificável>
...

## 💻 Comandos (quando aplicável)
```bash
<comandos exatos, prontos para copiar — usar Claude CLI onde for execução da skill>
```

## 📦 Artefatos produzidos
- <arquivos/pastas criados ou modificados nesta fase>

## 🔍 Validação / Definição de Pronto
- [ ] <critério objetivo 1>
- [ ] <critério objetivo 2>

## ➡️ Próximo passo
- Prossiga para `docs/<próximo-arquivo>.md`.
```

# PRINCÍPIOS E RESTRIÇÕES INVIOLÁVEIS

1. **Fonte de verdade é o `challenge.md`.** Nenhum requisito inventado; nenhum requisito omitido. Sempre que citar um número mínimo, ele deve bater com o documento.
2. **Não altere** `docs/challenge.md` nem `docs/00-prompt-orquestrador.md`.
3. **Nomes fixos:** a skill se chama `refactor-arch` e o arquivo principal é `SKILL.md` — nunca renomeie.
4. **Execução da skill é via Claude CLI** (`claude "/refactor-arch"`). Os documentos de fase devem deixar isso explícito nas etapas de execução, para que qualquer pessoa que receba o repositório consiga rodar.
5. **Autocontenção:** cada documento de fase deve ser executável lendo apenas ele + o `challenge.md`, sem depender do histórico desta conversa.
6. **Comandos reais e testáveis** (ambiente Linux). Sem placeholders vagos; use caminhos e comandos concretos.
7. **Idioma:** todos os documentos em **pt-BR**.
8. **Sem sobre-engenharia:** gere apenas os 6 arquivos especificados; não crie documentos extras não solicitados.

# CRITÉRIOS DE QUALIDADE (a sua entrega será avaliada por isto)

- Cobertura total: os 6 arquivos existem, seguem o template e cobrem 100% dos requisitos do challenge.
- Rastreabilidade: cada mínimo numérico do challenge aparece na fase correspondente.
- Executabilidade: um agente de IA sem contexto prévio consegue seguir os documentos e concluir o desafio.
- Consistência: numeração, nomenclatura de arquivos e referências cruzadas entre documentos corretas.

# FORMATO DA SUA RESPOSTA NESTA EXECUÇÃO

1. Primeiro, apresente um **resumo do ULTRATHINK** (Passos 1–5) em no máximo ~20 linhas.
2. Em seguida, **crie os 6 arquivos** (`docs/01` a `docs/06`) com o conteúdo completo.
3. Ao final, imprima um **índice** com links para os arquivos criados e uma frase indicando qual documento executar em seguida (`docs/02-fase-0-setup-e-prerequisitos.md`).

# AUTOVERIFICAÇÃO FINAL (execute antes de encerrar)

Antes de finalizar, confirme e reporte:
- [ ] Li `docs/challenge.md` por inteiro e mapeei o repositório real.
- [ ] Criei exatamente os 6 arquivos especificados em `docs/`.
- [ ] Cada arquivo de fase segue o TEMPLATE COMUM.
- [ ] Todos os mínimos numéricos do challenge estão distribuídos nas fases certas (≥ 8 anti-patterns, ≥ 8 transformações, ≥ 5 findings/projeto, ≥ 1 CRITICAL-ou-HIGH/projeto, 5 áreas de conhecimento, 3 fases da skill, 3 relatórios).
- [ ] As etapas de execução usam **Claude CLI** e a skill mantém os nomes `refactor-arch` / `SKILL.md`.
- [ ] Não modifiquei `challenge.md` nem este orquestrador.

=== FIM DO PROMPT ===
