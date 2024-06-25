import alembic.config
import flask_injector
from flask import Flask
from flask_cors import CORS


from src.torpedo.errors import TorpedoException
from src.torpedo.web.config import Config
from src.torpedo.web.exception_handlers import handle_generic_exception
from src.torpedo.web.module import TorpedoModule
from src.torpedo.web.routes import auth, healthchecks, home


def create_app() -> Flask:
    # apply migrations
    alembic.config.main(argv=["--raiseerr", "upgrade", "head"])  # --raiserr raises stacktrace

    flask_app = Flask(__name__)
    CORS(flask_app)
    flask_app.config.from_object(Config)

    flask_app.register_blueprint(healthchecks.health)
    flask_app.register_blueprint(auth.auth)
    flask_app.register_blueprint(home.home)
    flask_app.register_error_handler(TorpedoException, handle_generic_exception)

    flask_injector.FlaskInjector(app=flask_app, modules=[TorpedoModule()])

    return flask_app
