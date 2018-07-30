from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import config


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    return app

def create_db():
    app = create_app()
    db = SQLAlchemy(app=app)
    db.init_app(app)
    return db