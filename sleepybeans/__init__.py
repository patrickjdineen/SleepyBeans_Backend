import os
from flask import Flask
from config import Config
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from sleepybeans import routes, models