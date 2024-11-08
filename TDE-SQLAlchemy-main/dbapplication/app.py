from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SECRET_KEY'] = 'supersecretkey'  # Secret key for sessions and cookies
    
    db.init_app(app)

    from routes import register_routes
    register_routes(app, db)

    migrate = Migrate(app, db)

    return app
