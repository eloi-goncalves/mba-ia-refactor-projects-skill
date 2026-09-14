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
| Fase 3 — Projeto 2 (`ecommerce-api-legacy`) | ✅ refatorado + validado (boot + endpoints, 2026-09-14) |
| Fase 3 — Projeto 3 (`task-manager-api`) | ✅ refatorado + validado (boot + endpoints) |
| Fase 4 — Documentação (README A/B/C/D) | ✅ concluída |
| Entrega — `git push` do fork | ✅ concluída |

## Pendência 1 — Validação de boot do Projeto 2 ✅ CONCLUÍDA (2026-09-14)

**Resolvida:** após `npm install`, o app subiu na porta 3000 e os 3 endpoints foram validados:
- `POST /api/checkout` — aprova cartão `4xxx` (200), recusa `5xxx` (400).
- `GET /api/admin/financial-report` — receita por curso via consultas agregadas (sem N+1).
- `DELETE /api/users/:id` — remove registros relacionados (sem órfãos).
- Cartão **mascarado** (`****1111`) nos logs; nenhum PAN/segredo exposto.

Critério A4 do Projeto 2: ✅. **Todos os critérios de aceite agora estão em 3/3.**

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

## Pendência 3 — Entrega final (push do fork) ✅ CONCLUÍDA

Commits enviados ao fork público com `git push origin main` (skill nos 3 projetos,
código refatorado, `reports/` e README A/B/C/D).

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
1. ~~Resolver rede → **Pendência 1** (validar P2)~~ ✅ concluído.
2. ~~**Pendência 3** (push do fork)~~ ✅ concluído.
3. Opcionais: Pendência 2 (CLI), Pendência 4 (screenshots) e melhorias.
