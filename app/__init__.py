from flask import Flask

from app.config import Config
from app.db_client import MongoDB, ES


app = Flask(__name__)
app.config.from_object(Config)

# MongoDB Client
mongo_client = MongoDB(
    host=app.config["MONGO_SERVER"], 
    db_name=app.config["INDEX"], 
    doc_name=app.config["INDEX"]
)

# Elasticsearch Client
elastic_client = ES(
    host=app.config["ES_SERVER"],
    user=app.config["ES_USER"],
    pwd=app.config["ES_PWD"],
    index_name=app.config["INDEX"],
)

from app import routes, commands