from flask import Flask, Blueprint, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from config import Config


bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()

config = Config()

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "auth.login"


def create_app(config_name):

    app = Flask(__name__)
    app.config.from_object(config)
    config.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)
    db.init_app(app)

    # здесь выполняется подключение маршрутов и
    # нестандартных страниц с сообщениями об ошибках
    from .main import main as main_blueprint
    from .auth import auth as auth_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint)

    return app
