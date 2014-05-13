from . import app, mongo
from alexandria.decorators import *
from flask import request, jsonify, url_for, session
from flask.ext.classy import FlaskView, route
import json
from bson import json_util
from bson.objectid import ObjectId
import bcrypt

class LoginView(FlaskView):

    route_prefix = '/api/portal/'

    def post(self):

        username = request.form.get('username')
        password = request.form.get('password')

        if (username and password):

            user = mongo.Users.find_one({'username': username})

            if user:

                if bcrypt.hashpw(password.encode('utf-8'), user['password'].encode('utf-8')) == user['password']:

                    session['username'] = username
            	    session['role'] = user['role']
                    session['realname'] = user['realname']

                    return jsonify(success='The user \'' + username + '\' was successfully logged in.'), 200

                else:

                    return jsonify(error='The username and password did not match.'), 403

            else:

                return jsonify(error='The username \'' + username + '\' is not registered.'), 403

        else:

            return jsonify(error='Please complete all fields in the form.'), 400

LoginView.register(app)
