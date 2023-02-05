from flask import Flask
from config import Config
from .api.routes import api
from .auth.routes import auth
from .site.routes import site
from .models import db as root_db, login_manager, ma
from flask_migrate import Migrate
from villagers.helpers import JSONEncoder
from flask_cors import CORS

app = Flask(__name__)

app.register_blueprint(api)
app.register_blueprint(auth)
app.register_blueprint(site)

app.config.from_object(Config)

root_db.init_app(app)
migrate = Migrate(app, root_db)

login_manager.init_app(app)
login_manager.login_view = 'auth.signin'

ma.init_app(app)
app.json_encoder = JSONEncoder

CORS(app)