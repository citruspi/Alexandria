from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)
app.config.from_object('config.Debug')

client = MongoClient(app.config['MONGO']['HOST'], app.config['MONGO']["PORT"])
mongo = client[app.config['MONGO']['DATABASE']]

import alexandria.web
import alexandria.api
