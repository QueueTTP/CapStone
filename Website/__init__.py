from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO
from dotenv import load_dotenv
from sqlalchemy import text
import os

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()
socketio = SocketIO(async_mode='eventlet')


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    socketio.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    
    from .routes import routes
    from .views import views
    
    app.register_blueprint(routes, url_prefix='/')
    app.register_blueprint(views, url_prefix='/')


    return app
