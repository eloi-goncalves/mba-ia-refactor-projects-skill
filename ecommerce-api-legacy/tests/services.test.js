const test = require('node:test');
const assert = require('node:assert');

const cryptoService = require('../src/services/cryptoService');
const paymentService = require('../src/services/paymentService');

test('cryptoService: hash e verificação de senha (scrypt + salt)', () => {
  const hash = cryptoService.hashPassword('secret');
  assert.ok(hash.includes(':'), 'hash deve conter salt:hash');
  assert.notStrictEqual(hash, cryptoService.hashPassword('secret'), 'salt aleatório por hash');
  assert.strictEqual(cryptoService.verifyPassword('secret', hash), true);
  assert.strictEqual(cryptoService.verifyPassword('wrong', hash), false);
});

test('paymentService: autorização por bandeira do cartão', () => {
  assert.strictEqual(paymentService.authorize('4111111111111111'), 'PAID');
  assert.strictEqual(paymentService.authorize('5111111111111111'), 'DENIED');
});

test('paymentService: cartão é mascarado (não expõe PAN)', () => {
  assert.strictEqual(paymentService.maskCard('4111111111111111'), '****1111');
  assert.strictEqual(paymentService.maskCard(''), '****');
});
