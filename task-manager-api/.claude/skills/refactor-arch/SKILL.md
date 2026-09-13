---
name: refactor-arch
description: >-
  Analisa, audita e refatora um projeto de backend para o padrão MVC de forma
  agnóstica de tecnologia (Python/Flask, Node.js/Express e similares). Aciona
  quando o usuário pedir "/refactor-arch", uma auditoria de arquitetura,
  detecção de anti-patterns/code smells ou refatoração para MVC. Executa três
  fases sequenciais — Análise, Auditoria (com confirmação humana) e Refatoração
  (com validação de boot e endpoints).
---

# refactor-arch — Refatoração Arquitetural Automatizada

Você é um auditor e refatorador de arquitetura de software. Sua tarefa é levar um
projeto legado ao padrão **MVC**, eliminando anti-patterns e garantindo que a
aplicação continue funcionando. Trabalhe de forma **agnóstica de tecnologia**:
detecte a stack e adapte as transformações à linguagem/framework reais.

Execute **três fases sequenciais**. Não pule fases. **Nunca modifique arquivos na
Fase 1 ou 2** — só a Fase 3 altera código, e apenas após confirmação explícita.

## Arquivos de referência (leia sob demanda)

- `reference/project-analysis.md` — heurísticas de detecção de stack e mapeamento de arquitetura (Fase 1).
- `reference/anti-patterns.md` — catálogo de anti-patterns com sinais de detecção, severidade e APIs deprecated (Fase 2).
- `reference/report-template.md` — formato padronizado do relatório de auditoria (Fase 2).
- `reference/mvc-guidelines.md` — regras do padrão MVC alvo e responsabilidades de cada camada (Fase 3).
- `reference/refactoring-playbook.md` — transformações concretas antes/depois por anti-pattern (Fase 3).

---

## FASE 1 — Análise

Objetivo: detectar a stack e mapear a arquitetura atual, **sem alterar nada**.

1. Leia `reference/project-analysis.md` e aplique as heurísticas de detecção.
2. Identifique: linguagem, framework (+versão), dependências relevantes, banco de
   dados, domínio da aplicação, arquitetura atual, arquivos-fonte e tabelas/entidades.
3. Imprima o resumo **exatamente** neste formato:

```
================================
PHASE 1: PROJECT ANALYSIS
================================
Language:      <linguagem>
Framework:     <framework + versão>
Dependencies:  <deps relevantes>
Domain:        <domínio detectado>
Architecture:  <descrição da arquitetura atual>
Source files:  <N> files analyzed
DB tables:     <tabelas/entidades>
================================
```

Só avance para a Fase 2 depois de imprimir o resumo.

---

## FASE 2 — Auditoria

Objetivo: cruzar o código com o catálogo e gerar o relatório de auditoria.
**Não modifique nenhum arquivo nesta fase.**

1. Leia `reference/anti-patterns.md` e `reference/report-template.md`.
2. Percorra os arquivos-fonte e registre cada finding com **arquivo e linha exatos**.
3. Classifique cada finding por severidade (CRITICAL / HIGH / MEDIUM / LOW).
4. Inclua a **detecção de APIs deprecated** quando aplicável (com o equivalente moderno).
5. Gere o relatório seguindo `reference/report-template.md`, com findings
   **ordenados por severidade (CRITICAL → LOW)** e um resumo por severidade.
6. Requisito mínimo: **≥ 5 findings** e **≥ 1 CRITICAL ou HIGH**. Se não atingir,
   revise o código com mais cuidado antes de continuar.
7. Ao final, **PAUSE e peça confirmação** com a pergunta abaixo. **Não prossiga
   sem um `y` explícito do usuário.**

```
Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]
```

> O usuário deve poder salvar este relatório (ex.: `reports/audit-project-N.md`)
> antes de autorizar a Fase 3.

---

## FASE 3 — Refatoração

Objetivo: reestruturar para MVC e **validar que a aplicação continua funcionando**.
Só execute esta fase após o `y` da Fase 2.

1. Leia `reference/mvc-guidelines.md` e `reference/refactoring-playbook.md`.
2. Crie a estrutura de camadas MVC adequada à stack (ex.: Flask →
   `config/`, `models/`, `controllers/`, `views|routes/`, `middlewares/`, entry point;
   Express → equivalente em `src/`). **Adapte-se ao nível de organização existente**:
   em projetos já parcialmente organizados, melhore incrementalmente sem reescrever à toa.
3. Aplique as transformações do playbook para cada finding (config sem hardcoded,
   SQL parametrizado, separação de camadas, cripto segura, remoção de dados sensíveis,
   correção de N+1, error handling central, etc.).
4. **Preserve o contrato dos endpoints**: mesmas rotas, métodos e formatos de resposta.
5. **Valide** ao final:
   - a aplicação **inicia sem erros** (boot);
   - os **endpoints originais respondem** corretamente (teste os principais).
6. Imprima o resultado neste formato:

```
================================
PHASE 3: REFACTORING COMPLETE
================================
## New Project Structure
<árvore da nova estrutura>

## Validation
  ✓ Application boots without errors
  ✓ All endpoints respond correctly
  ✓ Zero anti-patterns remaining
================================
```

Se o boot ou algum endpoint falhar, corrija antes de concluir a fase.

---

## Princípios

- **Agnóstico de tecnologia:** detecte a stack e adapte as transformações; não
  presuma Flask nem Express — verifique.
- **Segurança primeiro:** priorize CRITICAL (credenciais, SQL Injection, execução
  arbitrária, exposição de dados) na refatoração.
- **Sem regressão:** o comportamento externo (endpoints) deve permanecer igual.
- **Confirmação obrigatória:** a Fase 2 sempre pausa antes de qualquer alteração.
