// Serviço de pagamento isolado. Nunca loga o número do cartão (PAN) nem segredos.
// A regra de aprovação é um mock de exemplo; em produção chamaria o gateway real.
const APPROVED = 'PAID';
const DENIED = 'DENIED';

function maskCard(card) {
  const digits = String(card || '').replace(/\D/g, '');
  return digits.length >= 4 ? `****${digits.slice(-4)}` : '****';
}

function authorize(card) {
  const digits = String(card || '').replace(/\D/g, '');
  // Mock: cartões que começam com 4 são aprovados.
  return digits.startsWith('4') ? APPROVED : DENIED;
}

module.exports = { authorize, maskCard, APPROVED, DENIED };
