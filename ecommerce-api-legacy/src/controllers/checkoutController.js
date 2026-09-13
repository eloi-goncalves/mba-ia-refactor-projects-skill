const paymentService = require('../services/paymentService');
const logger = require('../utils/logger');

// Controller de checkout: orquestra o fluxo usando models e services.
class CheckoutController {
  constructor({ userModel, courseModel, enrollmentModel, paymentModel, auditModel }) {
    this.userModel = userModel;
    this.courseModel = courseModel;
    this.enrollmentModel = enrollmentModel;
    this.paymentModel = paymentModel;
    this.auditModel = auditModel;
  }

  checkout = async (req, res, next) => {
    try {
      const { name, email, password, courseId, card } = req.body;
      if (!name || !email || !courseId || !card) {
        return res.status(400).json({ error: 'Dados obrigatórios ausentes' });
      }

      const course = await this.courseModel.findActiveById(courseId);
      if (!course) return res.status(404).json({ error: 'Curso não encontrado' });

      let user = await this.userModel.findByEmail(email);
      const userId = user ? user.id : await this.userModel.create(name, email, password || '123456');

      // Autorização isolada; nunca logamos o número do cartão nem segredos.
      const status = paymentService.authorize(card);
      if (status === paymentService.DENIED) {
        logger.info('Pagamento recusado', { userId, card: paymentService.maskCard(card) });
        return res.status(400).json({ error: 'Pagamento recusado' });
      }

      const enrollmentId = await this.enrollmentModel.create(userId, courseId);
      await this.paymentModel.create(enrollmentId, course.price, status);
      await this.auditModel.log(`Checkout curso ${courseId} por ${userId}`);

      logger.info('Checkout concluído', { userId, courseId, card: paymentService.maskCard(card) });
      return res.status(200).json({ msg: 'Sucesso', enrollment_id: enrollmentId });
    } catch (err) {
      return next(err);
    }
  };
}

module.exports = CheckoutController;
