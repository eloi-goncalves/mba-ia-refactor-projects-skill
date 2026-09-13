const logger = require('../utils/logger');

// Error handler centralizado (registrado por último no app).
// eslint-disable-next-line no-unused-vars
function errorHandler(err, req, res, next) {
  logger.error('Erro não tratado', { message: err.message });
  res.status(500).json({ error: 'Erro interno do servidor' });
}

module.exports = errorHandler;
