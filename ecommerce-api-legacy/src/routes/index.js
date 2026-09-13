const express = require('express');

const UserModel = require('../models/userModel');
const CourseModel = require('../models/courseModel');
const EnrollmentModel = require('../models/enrollmentModel');
const PaymentModel = require('../models/paymentModel');
const AuditModel = require('../models/auditModel');

const CheckoutController = require('../controllers/checkoutController');
const ReportController = require('../controllers/reportController');
const UserController = require('../controllers/userController');

// Compõe models e controllers a partir da conexão e registra as rotas.
function buildRoutes(db) {
  const router = express.Router();

  const models = {
    userModel: new UserModel(db),
    courseModel: new CourseModel(db),
    enrollmentModel: new EnrollmentModel(db),
    paymentModel: new PaymentModel(db),
    auditModel: new AuditModel(db),
  };

  const checkoutController = new CheckoutController(models);
  const reportController = new ReportController({ db });
  const userController = new UserController({ db, ...models });

  router.post('/api/checkout', checkoutController.checkout);
  router.get('/api/admin/financial-report', reportController.financialReport);
  router.delete('/api/users/:id', userController.deleteUser);

  return router;
}

module.exports = buildRoutes;
