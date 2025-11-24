from flask import Flask
from app.config import Config
from flask_bootstrap import Bootstrap5

app = Flask(__name__)

bootstrap = Bootstrap5(app)

app.config.from_object(Config)

from app import routes