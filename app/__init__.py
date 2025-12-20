from flask import Flask
from app.config import Config
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
app = Flask(__name__)

bootstrap = Bootstrap5(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Пожалуйста, выполните вход, чтобы получить доступ к странице"
login_manager.login_message_category = "warning"

app.config.from_object(Config)

from app import routes