// Relatório financeiro sem N+1: usa consultas agregadas com JOIN/GROUP BY.
class ReportController {
  constructor({ db }) {
    this.db = db;
  }

  financialReport = async (req, res, next) => {
    try {
      const revenues = await this.db.all(`
        SELECT c.id AS course_id, c.title AS course,
               COALESCE(SUM(CASE WHEN p.status = 'PAID' THEN p.amount ELSE 0 END), 0) AS revenue
        FROM courses c
        LEFT JOIN enrollments e ON e.course_id = c.id
        LEFT JOIN payments p ON p.enrollment_id = e.id
        GROUP BY c.id, c.title
      `);

      const students = await this.db.all(`
        SELECT c.id AS course_id, u.name AS student,
               COALESCE(p.amount, 0) AS paid
        FROM courses c
        JOIN enrollments e ON e.course_id = c.id
        JOIN users u ON u.id = e.user_id
        LEFT JOIN payments p ON p.enrollment_id = e.id
      `);

      const byCourse = new Map();
      revenues.forEach((r) => {
        byCourse.set(r.course_id, { course: r.course, revenue: r.revenue, students: [] });
      });
      students.forEach((s) => {
        const entry = byCourse.get(s.course_id);
        if (entry) entry.students.push({ student: s.student, paid: s.paid });
      });

      return res.json([...byCourse.values()]);
    } catch (err) {
      return next(err);
    }
  };
}

module.exports = ReportController;
