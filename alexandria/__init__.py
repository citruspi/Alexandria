from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)
app.config.from_object('config.Debug')

client = MongoClient(app.config['MONGOHOST'], app.config['MONGOPORT'])
mongo = client[app.config['MONGODB']]

import alexandria.web
