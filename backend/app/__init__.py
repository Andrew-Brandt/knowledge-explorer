import logging
import os


from flask import Flask, jsonify
from flask_caching import Cache
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager






db = SQLAlchemy()
migrate = Migrate()
cache = Cache()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # 🔐 Core App Config
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret")

    # 🔗 Database Config (Postgres or SQLite via .env)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL",
        "sqlite:///instance/app.db"  # fallback if DATABASE_URL is not set
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # 🔁 Redis Caching Config (optional fallback safe)
    app.config["CACHE_TYPE"] = "RedisCache"
    app.config["CACHE_REDIS_URL"] = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    app.config["CACHE_DEFAULT_TIMEOUT"] = int(os.getenv("CACHE_DEFAULT_TIMEOUT", 86400))

    # 👥 User session/login
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to access this page."
    login_manager.init_app(app)

    # 🌐 CORS
    CORS(app, supports_credentials=True)

    # 📦 Init Services
    os.makedirs("logs", exist_ok=True)
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler("logs/app.log"),
            logging.StreamHandler()
        ]
    )

    cache.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    register_blueprints(app)

    return app

@login_manager.user_loader
def load_user(user_id):
    from app.database import get_user_by_id
    return get_user_by_id(user_id)


@login_manager.unauthorized_handler
def unauthorized():
    return jsonify({"error": "Unauthorized"}), 401


def register_blueprints(app):
    from app.routes import main
    # from app.auth import auth
    # from app.admin import admin_bp



    app.register_blueprint(main)
    # app.register_blueprint(auth)
    # app.register_blueprint(admin_bp)