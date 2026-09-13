// Deleção de usuário com integridade referencial (sem registros órfãos).
class UserController {
  constructor({ db, userModel, enrollmentModel, paymentModel }) {
    this.db = db;
    this.userModel = userModel;
    this.enrollmentModel = enrollmentModel;
    this.paymentModel = paymentModel;
  }

  deleteUser = async (req, res, next) => {
    const { id } = req.params;
    try {
      await this.db.run('BEGIN TRANSACTION');
      await this.paymentModel.deleteByUser(id);
      await this.enrollmentModel.deleteByUser(id);
      await this.userModel.delete(id);
      await this.db.run('COMMIT');
      return res.json({ msg: 'Usuário e registros relacionados removidos' });
    } catch (err) {
      await this.db.run('ROLLBACK').catch(() => {});
      return next(err);
    }
  };
}

module.exports = UserController;
