from decouple import config as env
from datetime import datetime

from flask import Flask
from flask_pymongo import PyMongo


app = Flask(__name__)

# MONGODB Config

db_user = env("MONGO_USERNAME", "root")
db_pass = env("MONGO_PASSWORD", "root")
db_host = env("MONGO_HOST", "localhost")
db_port = env("MONGO_PORT", 27017)
db_name = env("MONGO_DBNAME", "flaskapp")

app.config["MONGO_DBNAME"] = db_name
app.config["MONGO_URI"] = f"mongodb://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

# Important to point to the "admin" as authentication database
mongo = PyMongo(app, authSource="admin")

stats = mongo.db.stats
stats.insert_one(
    {
        "event": "start-up",
        "timestamp": datetime.now(),
    }
)
