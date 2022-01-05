from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from bookaholic.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
# decorater login_required, where the login route is located
login_manager.login_view = 'users.login'
#decorater how the error should be displayed 
login_manager.login_message_category = 'info' 
#after logged in directly to the page we were trying to access rather than home page
mail = Mail()


def create_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    #to pass the app to all those extension
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from bookaholic.posts.routes import pos
    from bookaholic.users.routes import users
    from bookaholic.main.routes import main
    from bookaholic.errors.handlers import errors

    app.register_blueprint(pos)
    app.register_blueprint(users)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app 