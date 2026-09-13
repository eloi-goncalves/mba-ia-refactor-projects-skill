```
================================
ARCHITECTURE AUDIT REPORT
================================
Project: code-smells-project
Stack:   Python + Flask 3.1.1
Files:   4 analyzed | ~600 lines of code

## Summary
CRITICAL: 3 | HIGH: 2 | MEDIUM: 2 | LOW: 2
```

## Findings

### [CRITICAL] SQL Injection (concatenação de string)
File: models.py:27 (e 91, 106, 122, 136, 190, 227, 240, 375-386)
Description: Queries montadas por concatenação de entrada do usuário, ex.: `"SELECT * FROM produtos WHERE id = " + str(id)` e `login_usuario` concatenando `email`/`senha`; `buscar_produtos` concatena `termo`/`categoria` no `LIKE`.
Impact: Permite injeção de SQL — vazamento, adulteração ou destruição de dados.
Recommendation: Parametrizar todas as queries com placeholders `?` (playbook T2) ou usar ORM.

### [CRITICAL] Hardcoded Credentials
File: app.py:7 (exposto em controllers.py:311)
Description: `SECRET_KEY = "minha-chave-super-secreta-123"` no código e ainda retornado pelo endpoint `/health`.
Impact: Segredo versionado e vazado publicamente via API.
Recommendation: Ler segredo de variável de ambiente (playbook T1); nunca expor em respostas.

### [CRITICAL] Endpoint de execução arbitrária / rota destrutiva sem auth
File: app.py:48 (`/admin/reset-db`) e app.py:60 (`/admin/query`)
Description: `/admin/query` executa SQL arbitrário vindo do body; `/admin/reset-db` apaga todas as tabelas — ambos sem autenticação.
Impact: Execução arbitrária de SQL e destruição total dos dados por qualquer requisição.
Recommendation: Remover as rotas (playbook T13); operações administrativas só com authz e parametrização.

### [HIGH] God Module / mistura de camadas
File: models.py:1-386
Description: `models.py` concentra acesso a dados (SQL), regra de negócio (cálculo de pedido, relatório com regras de desconto) e formatação para 4 domínios.
Impact: Impossível testar em isolamento; qualquer mudança afeta tudo.
Recommendation: Separar em models por domínio + controllers/serviços (playbook T3).

### [HIGH] Estado global / conexão singleton
File: database.py:3-9
Description: Conexão global única (`db_connection`) reutilizada com `check_same_thread=False`.
Impact: Condições de corrida e acoplamento global; não escala com concorrência.
Recommendation: Conexão por requisição via `flask.g` + teardown (playbook T6).

### [MEDIUM] Query N+1
File: models.py:172-207 (`get_pedidos_usuario`) e models.py:209-247 (`get_todos_pedidos`)
Description: Para cada pedido, uma query por item; para cada item, outra query pelo nome do produto.
Impact: Degradação de performance proporcional ao volume de pedidos/itens.
Recommendation: Substituir por `JOIN`/consulta agregada (playbook T8).

### [MEDIUM] Efeito colateral no controller / notificações fake
File: controllers.py:186-190 (e 254-258)
Description: `print("ENVIANDO EMAIL/SMS/PUSH ...")` simulando notificação dentro do controller.
Impact: Ausência de camada de serviço; lógica de notificação acoplada ao HTTP.
Recommendation: Extrair para um serviço de notificação; controller apenas orquestra (playbook T7).

### [LOW] Logging por `print` e magic values
File: controllers.py:8 (print) e controllers.py:52 / models.py:361-367 (magic values)
Description: `print` como logging em vários pontos; listas de categorias/status e thresholds de desconto hardcoded e repetidos.
Impact: Observabilidade ruim; duplicação propensa a erro.
Recommendation: Logger estruturado (playbook T11) e extração de constantes/enums.

### [LOW] Nomenclatura genérica de erro
File: controllers.py (múltiplos `except Exception as e` retornando 500 genérico)
Description: Tratamento de erro repetido em cada handler.
Impact: Duplicação; respostas de erro inconsistentes.
Recommendation: Centralizar error handling em middleware (playbook T14).

```
================================
Total: 9 findings
================================

Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]
> y
```
