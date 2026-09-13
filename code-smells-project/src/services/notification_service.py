import logging

logger = logging.getLogger(__name__)


class NotificationService:
    """Serviço de notificação desacoplado dos controllers.

    Nesta base de exemplo apenas registra a intenção via logging; em produção
    seria integrado a e-mail/SMS/push reais.
    """

    def pedido_criado(self, pedido_id, usuario_id):
        logger.info("Notificação: pedido %s criado para usuário %s", pedido_id, usuario_id)

    def status_atualizado(self, pedido_id, status):
        if status == "aprovado":
            logger.info("Notificação: pedido %s aprovado — preparar envio", pedido_id)
        elif status == "cancelado":
            logger.info("Notificação: pedido %s cancelado — devolver estoque", pedido_id)


notification_service = NotificationService()
