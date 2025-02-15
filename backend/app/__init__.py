from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    CORS(app)
    db.init_app(app)
    login_manager.init_app(app)
    
    from app.models.user import User
    from app.auth.routes import auth_bp
    from app.routes.trip_routes import trip_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(trip_bp, url_prefix='/api')
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    return app
