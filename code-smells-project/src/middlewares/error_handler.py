import logging

from flask import jsonify

logger = logging.getLogger(__name__)


def register_error_handlers(app):
    """Registra handlers de erro centralizados."""

    @app.errorhandler(404)
    def not_found(_error):
        return jsonify({"erro": "Recurso não encontrado", "sucesso": False}), 404

    @app.errorhandler(400)
    def bad_request(_error):
        return jsonify({"erro": "Requisição inválida", "sucesso": False}), 400

    @app.errorhandler(Exception)
    def handle_unexpected(error):
        logger.exception("Erro não tratado: %s", error)
        return jsonify({"erro": "Erro interno do servidor", "sucesso": False}), 500
