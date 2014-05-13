from . import app, mongo
from alexandria.decorators import *
from flask import request, jsonify, url_for, session
from flask.ext.classy import FlaskView, route
import json
from bson import json_util
from bson.objectid import ObjectId

class LoginView(FlaskView):

    route_prefix = '/api/'

    def post(self):

        return 'hello'

LoginView.register(app)
