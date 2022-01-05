""" app module"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from config import Configuration
from container import ApplicationService

import os


app = Flask(__name__)
app.config.from_object(Configuration)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
# container = ApplicationService(os.environ["APPLICATION_ENV"])
