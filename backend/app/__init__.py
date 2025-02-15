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
    from app.models.trip import Trip
    from app.auth.routes import auth_bp
    from app.trips.routes import trips_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(trips_bp)
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    return app
