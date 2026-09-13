const cryptoService = require('../services/cryptoService');

class UserModel {
  constructor(db) {
    this.db = db;
  }

  findByEmail(email) {
    return this.db.get('SELECT * FROM users WHERE email = ?', [email]);
  }

  async create(name, email, password) {
    const { lastID } = await this.db.run(
      'INSERT INTO users (name, email, pass) VALUES (?, ?, ?)',
      [name, email, cryptoService.hashPassword(password)]
    );
    return lastID;
  }

  delete(id) {
    return this.db.run('DELETE FROM users WHERE id = ?', [id]);
  }
}

module.exports = UserModel;
