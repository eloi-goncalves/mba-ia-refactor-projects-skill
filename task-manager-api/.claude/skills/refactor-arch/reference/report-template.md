# Referência — Template do Relatório de Auditoria (Fase 2)

Formato padronizado da saída da Fase 2. O relatório deve ser autoexplicativo,
com resumo por severidade e findings **ordenados de CRITICAL → LOW**, cada um com
**arquivo e linhas exatos**. Este é o conteúdo salvo em `reports/audit-project-N.md`.

## Estrutura obrigatória

```
================================
ARCHITECTURE AUDIT REPORT
================================
Project: <nome-do-projeto>
Stack:   <linguagem + framework>
Files:   <N> analyzed | ~<linhas> lines of code

## Summary
CRITICAL: <n> | HIGH: <n> | MEDIUM: <n> | LOW: <n>

## Findings

### [CRITICAL] <Nome do anti-pattern>
File: <arquivo>:<linha ou intervalo>
Description: <o que é o problema, de forma concreta>
Impact: <consequência prática (segurança, manutenção, performance)>
Recommendation: <ação de correção; cite a transformação do playbook>

### [HIGH] <...>
File: <arquivo>:<linha>
Description: <...>
Impact: <...>
Recommendation: <...>

### [MEDIUM] <...>
...

### [LOW] <...>
...

================================
Total: <N> findings
================================

Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]
```

## Regras de preenchimento

1. **Ordenação:** sempre CRITICAL → HIGH → MEDIUM → LOW.
2. **Rastreabilidade:** todo finding tem `File: arquivo:linha` (use intervalo
   `arquivo:10-42` quando abranger um bloco).
3. **Contagem:** o `## Summary` deve bater com o número de findings listados e com o
   `Total`.
4. **APIs deprecated:** inclua os achados de API obsoleta como findings normais,
   citando o equivalente moderno na `Recommendation`.
5. **Mínimos:** ≥ 5 findings e ≥ 1 CRITICAL ou HIGH. Se não atingir, reanalise.
6. **Confirmação:** o relatório termina **sempre** com a pergunta de confirmação; a
   Fase 3 só começa após `y`.

## Exemplo (parcial)

```
### [CRITICAL] SQL Injection
File: models.py:27
Description: Query montada por concatenação: "SELECT * FROM produtos WHERE id = " + str(id).
Impact: Permite injeção de SQL e vazamento/adulteração de dados.
Recommendation: Parametrizar a query (placeholders ?), conforme playbook T2.
```
