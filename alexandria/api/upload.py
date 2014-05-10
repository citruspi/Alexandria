from . import app, mongo
from alexandria.decorators import *
from flask import request, jsonify, url_for, session
from flask.ext.classy import FlaskView, route
import json
from bson import json_util
import requests

class UploadView(FlaskView):

    route_prefix = '/api/'

    @authenticated
    def search(self, query):

        results = requests.get('https://www.googleapis.com/books/v1/volumes?q='+query).json()

        return jsonify(results=results)

UploadView.register(app)
