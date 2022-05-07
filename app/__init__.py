from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy

from app.config import Config
from app.db_client import MongoDB, ES

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

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

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

db.create_all()

admin = Admin(app, name='microblog', template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session))

from app import routes