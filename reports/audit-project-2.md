```
================================
ARCHITECTURE AUDIT REPORT
================================
Project: ecommerce-api-legacy
Stack:   Node.js + Express 4.18
Files:   3 analyzed | ~180 lines of code

## Summary
CRITICAL: 3 | HIGH: 3 | MEDIUM: 2 | LOW: 2
```

## Findings

### [CRITICAL] Hardcoded Credentials / Secrets
File: src/utils.js:1-7
Description: `config` com `dbPass = "senha_super_secreta_prod_123"`, `paymentGatewayKey = "pk_live_1234567890abcdef"` e `smtpUser` hardcoded.
Impact: Vazamento de chave de produção do gateway de pagamento e credenciais versionadas.
Recommendation: Ler segredos de variáveis de ambiente (playbook T1).

### [CRITICAL] Log de dados sensíveis (violação PCI)
File: src/AppManager.js:66
Description: `console.log("Processando cartão ${cc} na chave ${config.paymentGatewayKey}")` registra número do cartão e a chave do gateway.
Impact: Violação de PCI-DSS; exposição de dados de cartão e segredo em logs.
Recommendation: Nunca logar PAN/segredos; isolar a autorização em um serviço (playbook T5).

### [CRITICAL] God Class
File: src/AppManager.js:1-138
Description: `AppManager` acumula conexão de DB, criação de schema/seed, definição de rotas HTTP e regra de negócio de checkout/relatório.
Impact: Impossível testar/evoluir; nenhuma separação de responsabilidades.
Recommendation: Separar em config, database, models, controllers, routes, services (playbook T3).

### [HIGH] Criptografia insegura (hash caseiro)
File: src/utils.js:16-22
Description: `badCrypto` gera um "hash" concatenando Base64 em loop, sem salt nem KDF.
Impact: Senhas efetivamente sem proteção.
Recommendation: Usar KDF real (scrypt/bcrypt/argon2). Aqui: `crypto.scryptSync` com salt (playbook T4).

### [HIGH] Estado global mutável
File: src/utils.js:9-10
Description: `globalCache` e `totalRevenue` como estado global compartilhado do módulo.
Impact: Efeitos colaterais imprevisíveis; não escala com concorrência.
Recommendation: Encapsular estado; injetar dependências (playbook T6).

### [HIGH] Callback Hell / API baseada em callbacks
File: src/AppManager.js:37-88
Description: Checkout e relatório aninham múltiplos callbacks de `sqlite3` com controle manual de contadores.
Impact: Código ilegível e propenso a erros; difícil tratar erros.
Recommendation: Encapsular `sqlite3` com Promises e usar async/await (playbook T9).

### [MEDIUM] Query N+1
File: src/AppManager.js:79-116
Description: `/api/admin/financial-report` itera cursos → matrículas → e consulta users/payments individualmente por matrícula.
Impact: Performance ruim conforme cresce o número de matrículas.
Recommendation: Substituir por consultas agregadas com JOIN/GROUP BY (playbook T8).

### [MEDIUM] Integridade referencial / registros órfãos
File: src/AppManager.js:130-136
Description: `DELETE FROM users` deixa matrículas e pagamentos órfãos (a própria resposta admite).
Impact: Dados inconsistentes no banco.
Recommendation: Transação + deleção em cascata (playbook T12).

### [LOW] Nomenclatura ruim
File: src/AppManager.js:29-33
Description: Campos do body abreviados: `usr`, `eml`, `pwd`, `c_id`, `cc`.
Impact: Baixa legibilidade e manutenção.
Recommendation: Nomes descritivos (name, email, password, courseId, card).

### [LOW] Logging por console.log / magic logic
File: src/AppManager.js:65 (e utils.js:12)
Description: `console.log` como logging; aprovação de pagamento por `cc.startsWith("4")` (magic).
Impact: Observabilidade ruim; regra obscura embutida.
Recommendation: Logger estruturado (playbook T11); extrair regra para serviço de pagamento.

## Detecção de APIs deprecated
- `sqlite3` com API de callbacks (padrão legado). Equivalente moderno: wrapper baseado em Promise / `better-sqlite3` / `node:sqlite`. (Aplicado aqui via wrapper Promise, sem mudar a dependência.)

```
================================
Total: 10 findings
================================

Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]
> y
```
