from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from flask_migrate import Migrate
from flask_mail import Mail

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()

#login_manager.login_view = 'auth.py'
def create_app():
    app = Flask(__name__)
    #load configuration files
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    #create database models
    from .model import User
    with app.app_context():
        db.create_all()
    #register blueprint
    from .auth import auth
    from .social_log_in import facebook_bp
    from .view import view
    from .postAd import postAd
    from .account import account_bp
    from .auxiliary import aux
    app.register_blueprint(auth)
    app.register_blueprint(facebook_bp)
    app.register_blueprint(view)
    app.register_blueprint(account_bp)
    app.register_blueprint(postAd)
    app.register_blueprint(aux)

    login_manager.init_app(app)
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)    
    return app

