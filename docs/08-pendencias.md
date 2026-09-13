# 08 — Plano de Pendências (o que faltou executar)

> Registro do que ficou pendente após a execução autônoma das Fases 0–4. Data: 2026-09-13.
> Referência de progresso completo: [07-relatorio-de-execucao.md](07-relatorio-de-execucao.md).

## Situação atual (resumo)

| Fase | Status |
|------|--------|
| Fase 0 — Setup | ✅ concluída (exceto `npm install` do P2) |
| Fase 1 — Análise manual | ✅ concluída (README seção A) |
| Fase 2 — Criação da skill | ✅ concluída (skill nos 3 projetos) |
| Fase 3 — Projeto 1 (`code-smells-project`) | ✅ refatorado + validado (boot + endpoints) |
| Fase 3 — Projeto 2 (`ecommerce-api-legacy`) | ⚠️ refatorado, **boot/endpoints pendentes** (rede) |
| Fase 3 — Projeto 3 (`task-manager-api`) | ✅ refatorado + validado (boot + endpoints) |
| Fase 4 — Documentação (README A/B/C/D) | ✅ concluída |
| Entrega — `git push` do fork | ⏳ pendente (aguarda autorização de push/rede) |

## Pendência 1 — Validação de boot do Projeto 2 (BLOQUEADA por rede) 🔴

**O que falta:** subir o app Node refatorado e confirmar que os endpoints respondem
(critério de aceite A4 para o Projeto 2).

**Causa:** `npm install` falha com erro de rede/proxy; `node_modules/` ausente. Sem
`express`/`sqlite3` instalados, a aplicação não roda.

**O código já está pronto:** refatoração MVC concluída e **sintaxe validada** em 17/17
arquivos (`node --check`). Falta apenas executar.

**Como concluir quando houver rede:**
```bash
cd ecommerce-api-legacy
# se houver proxy:
# npm config set proxy http://<host>:<porta>
# npm config set https-proxy http://<host>:<porta>
npm install
npm start                      # sobe em http://localhost:3000
# validar endpoints:
curl -s -X POST localhost:3000/api/checkout -H 'Content-Type: application/json' \
  -d '{"name":"Ana","email":"ana@x.com","password":"123","courseId":1,"card":"4111111111111111"}'
curl -s localhost:3000/api/admin/financial-report
curl -s -X DELETE localhost:3000/api/users/1
```
**Definição de pronto:** app inicia sem erros; `/api/checkout`, `/api/admin/financial-report`
e `/api/users/:id` respondem; atualizar a linha do P2 no checklist do README (seção C).

## Pendência 2 — Executar a skill via Claude CLI de fato (opcional) 🟡

**Contexto:** nesta execução a skill `refactor-arch` foi aplicada **seguindo o `SKILL.md`**
(equivalente a `claude "/refactor-arch"`), pois rodar um agente CLI aninhado de forma
autônoma no ambiente não era prático/seguro.

**O que falta (para fidelidade total ao enunciado):** rodar `claude "/refactor-arch"`
em cada projeto e confirmar que a saída bate com os relatórios em `reports/`.
```bash
cd code-smells-project && claude "/refactor-arch"
cd ../ecommerce-api-legacy && claude "/refactor-arch"
cd ../task-manager-api && claude "/refactor-arch"
```
**Definição de pronto:** as 3 execuções reproduzem Fase 1/2/3 conforme o `SKILL.md`.

## Pendência 3 — Entrega final (push do fork) 🟡

**O que falta:** enviar os commits ao repositório público (fork).
```bash
git push origin main
```
**Definição de pronto:** fork público atualizado com skill (3 projetos), código refatorado,
`reports/` (3 arquivos) e README A/B/C/D.

## Pendência 4 — Screenshots (opcional, item do README seção C) 🟢

**O que falta:** o desafio sugere "screenshots ou logs" das apps rodando. Foram incluídos
**logs** (curl) no README; screenshots são opcionais e podem ser anexados se desejado.

## Melhorias opcionais (não bloqueiam a entrega)

- Substituir por completo as APIs deprecated remanescentes no P3 (`datetime.utcnow()` nas
  colunas dos models e `Model.query`/`Query.get()` legados → API 2.0 do SQLAlchemy).
- Adicionar testes automatizados (pytest / node:test) para os endpoints refatorados.
- Extrair uma camada de `controllers` explícita no P3 (hoje a lógica foi movida para
  models/serializer; controllers dedicados aumentariam a aderência ao MVC).

## Ordem sugerida para concluir
1. Resolver rede → **Pendência 1** (validar P2).
2. **Pendência 3** (push do fork).
3. Opcionais: Pendência 2 (CLI), Pendência 4 (screenshots) e melhorias.
