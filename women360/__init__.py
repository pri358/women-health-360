from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from women360 import config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'


def create_app(config_class=config.Config):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = config_class.SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = config_class.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from women360.home.routes import home
    from women360.users.routes import users
    from women360.menstruation.routes import menstruation
    from women360.healthMonitor.routes import healthMonitor
    from women360.errors.handlers import errors

    app.register_blueprint(home)
    app.register_blueprint(users)
    app.register_blueprint(menstruation)
    app.register_blueprint(healthMonitor)
    app.register_blueprint(errors)

    return app
