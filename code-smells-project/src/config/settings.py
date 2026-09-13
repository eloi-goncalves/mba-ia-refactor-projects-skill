import os
import secrets


class Settings:
    """Configuração da aplicação carregada a partir do ambiente."""

    SECRET_KEY = os.getenv("SECRET_KEY") or secrets.token_hex(32)
    DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    DB_PATH = os.getenv("DB_PATH", "loja.db")
    HOST = os.getenv("HOST", "127.0.0.1")
    PORT = int(os.getenv("PORT", "5000"))
