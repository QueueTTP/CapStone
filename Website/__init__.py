import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO
from dotenv import load_dotenv
import os

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()
socketio = SocketIO(async_mode='eventlet')


def create_app():
    
    global db
    
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    socketio.init_app(app)
    db = SQLAlchemy(app)
        
    migrate.init_app(app, db)
    
    from .routes import routes
    from .views import views
    
    app.register_blueprint(routes, url_prefix='/')
    app.register_blueprint(views, url_prefix='/')
    
    with app.app_context():
        try:
            # Check the add user function
            logging.info("with app.app_context():")

            logging.info(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")

            # Check database connection
            db.session.execute(text('SELECT 1'))
            logging.info("Database connection successful")
        except Exception as e:
            logging.error("Database connection failed: %s", e)


    return app
