from decouple import config as env
from datetime import datetime

from flask import Flask
from flask_pymongo import PyMongo
from flask_login import LoginManager


# Flask App instance
app = Flask(__name__)

# Flask-Login Config

app.config["SECRET_KEY"] = env("SECRET_KEY")
app.config["SESSION_PROTECTION"] = "strong"

login_manager = LoginManager()
login_manager.setup_app(app)
login_manager.login_view = "login"

# MONGODB Config

db_user = env("MONGO_USERNAME", "root")
db_pass = env("MONGO_PASSWORD", "root")
db_host = env("MONGO_HOST", "localhost")
db_port = env("MONGO_PORT", 27017)
db_name = env("MONGO_DBNAME", "flaskapp")

MONGO_BASE_URI = f"mongodb://{db_user}:{db_pass}@{db_host}:{db_port}"

# Important to point to "admin" as authentication database
mongo = PyMongo(app, uri=f"{MONGO_BASE_URI}/{db_name}", authSource="admin")

stats = mongo.db.stats
stats.insert_one(
    {
        "event": "start-up",
        "timestamp": datetime.now(),
    }
)
