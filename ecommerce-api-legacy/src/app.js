const express = require('express');

const config = require('./config');
const Database = require('./database/db');
const { initDb } = require('./database/schema');
const buildRoutes = require('./routes');
const errorHandler = require('./middlewares/errorHandler');
const logger = require('./utils/logger');

// Composition root: cria a conexão, inicializa o schema, monta o app e sobe o servidor.
async function main() {
  const db = new Database(config.dbPath);
  await initDb(db);

  const app = express();
  app.use(express.json());
  app.use('/', buildRoutes(db));
  app.use(errorHandler);

  app.listen(config.port, () => {
    logger.info('LMS API rodando', { port: config.port });
  });
}

main().catch((err) => {
  logger.error('Falha ao iniciar a aplicação', { message: err.message });
  process.exit(1);
});
