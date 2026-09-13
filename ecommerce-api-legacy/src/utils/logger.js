// Logger simples e estruturado (substitui console.log espalhado).
// Nunca registre dados sensíveis (cartões, segredos, senhas).
function log(level, message, meta) {
  const entry = { level, message, timestamp: new Date().toISOString() };
  if (meta) entry.meta = meta;
  // eslint-disable-next-line no-console
  console[level === 'error' ? 'error' : 'log'](JSON.stringify(entry));
}

module.exports = {
  info: (message, meta) => log('info', message, meta),
  warn: (message, meta) => log('warn', message, meta),
  error: (message, meta) => log('error', message, meta),
};
