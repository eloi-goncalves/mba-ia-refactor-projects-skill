import logging

from flask import Flask
from flask_cors import CORS

from src.config.settings import Settings
from src.database.connection import close_db, init_db
from src.middlewares.error_handler import register_error_handlers
from src.views.routes import api


def create_app():
    """Composition root: cria e configura a aplicação Flask."""
    logging.basicConfig(level=logging.INFO)

    app = Flask(__name__)
    app.config.from_object(Settings)
    CORS(app)

    init_db(app)
    app.teardown_appcontext(close_db)

    app.register_blueprint(api)
    register_error_handlers(app)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host=Settings.HOST, port=Settings.PORT, debug=Settings.DEBUG)
