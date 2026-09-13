# Referência — Guidelines de Arquitetura MVC (Fase 3)

Regras do padrão MVC alvo. São **agnósticas de tecnologia**: o objetivo é separar
responsabilidades em camadas claras. Adapte os nomes de pasta à convenção da stack.

## Camadas e responsabilidades

### Config
- Centraliza configuração e **segredos vindos do ambiente** (nunca hardcoded).
- Ex.: `config/settings.py` (Flask) ou `src/config/index.js` (Express) lendo de
  variáveis de ambiente / `.env`.
- Contém: chaves, credenciais, flags (`debug`), host/porta, URL do banco.

### Models
- Representam **dados e regras de domínio** (entidades) e o **acesso a dados**.
- Encapsulam persistência: uma alteração de schema/consulta fica aqui, não na rota.
- Não conhecem HTTP (não usam `request`/`res`).
- Ex.: `models/produto_model.py`, `models/usuario_model.py`.

### Views / Routes
- Apenas **I/O HTTP**: recebem a requisição, chamam o controller e devolvem a resposta.
- Sem regra de negócio, sem SQL. Definem rota, método e (de)serialização.
- Ex.: `views/routes.py` (Flask blueprints) ou `src/routes/*.js` (Express routers).

### Controllers
- Concentram o **fluxo da aplicação**: orquestram validação → model/serviço → resposta.
- Traduzem entrada HTTP em chamadas de domínio e montam o retorno.
- Não contêm SQL cru nem detalhes de framework de persistência.
- Ex.: `controllers/produto_controller.py`, `controllers/pedido_controller.py`.

### Services (quando houver lógica de negócio significativa)
- Regras que cruzam múltiplos models ou integrações (pagamento, e-mail, relatórios).
- Ex.: `services/notification_service.py`, `services/checkout_service.py`.

### Middlewares
- Preocupações transversais: **error handling centralizado**, autenticação, logging,
  CORS. Ex.: `middlewares/error_handler.py` (Flask `errorhandler`) ou middleware Express.

### Entry point (composition root)
- Um ponto de entrada claro que **compõe** a aplicação: cria o app, carrega config,
  registra rotas e middlewares, inicializa o banco. Ex.: `app.py` / `src/app.js`.

## Regra de dependência

```
Views/Routes → Controllers → Services → Models → (Banco)
```

- As setas indicam a direção permitida das dependências (camadas de cima conhecem as
  de baixo, nunca o contrário).
- Config e middlewares são transversais.

## Estrutura alvo (exemplos)

**Flask**
```
src/
├── config/settings.py
├── models/
├── controllers/
├── views/ (ou routes/)
├── services/
├── middlewares/error_handler.py
└── app.py   # composition root
```

**Express**
```
src/
├── config/index.js
├── models/
├── controllers/
├── routes/
├── services/
├── middlewares/errorHandler.js
└── app.js   # composition root
```

## Critérios de "pronto" (MVC)

- [ ] Configuração fora do código (sem segredos hardcoded).
- [ ] Models abstraem dados; sem SQL cru nas rotas/controllers.
- [ ] Views/Routes só fazem I/O HTTP.
- [ ] Controllers concentram o fluxo.
- [ ] Error handling centralizado.
- [ ] Entry point claro (composition root).
- [ ] **Endpoints originais preservados** (mesmas rotas/métodos/respostas).

## Adaptação ao contexto

- **Monólito desestruturado:** crie todas as camadas do zero.
- **Parcialmente organizado:** aproveite o que existe (ex.: blueprints/models já
  presentes) e corrija os vazamentos (regra na rota, dados sensíveis, N+1) — não
  reescreva sem necessidade.
