from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
from flaskblog.config import Config

# ----------------- Extensions -----------------
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()
csrf = CSRFProtect()
# ---------------------------------------------

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # ---------------- Security Config ----------------
    app.config['SECRET_KEY'] = 'supersecretkey'         # Required for Flask-WTF sessions
    app.config['WTF_CSRF_ENABLED'] = True              # Enable CSRF protection
    app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'   # Protect cookies from cross-site requests
    # --------------------------------------------------

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)

    # Register blueprints
    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)

    return app
