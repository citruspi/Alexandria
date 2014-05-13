from . import app, mongo
from alexandria.decorators import *
from flask import request, jsonify, url_for, session
from flask.ext.classy import FlaskView, route
import json
from bson import json_util
from bson.objectid import ObjectId
import bcrypt

class RegisterView(FlaskView):

    route_prefix = '/api/portal/'

    def post(self):

        if not app.config['ALLOW_REGISTRATION']:

            return jsonify(error='Registration is currently disabled.'), 403

        username = request.form.get('username')
        realname = request.form.get('realname')
        emailadd = request.form.get('emailadd')
        password = request.form.get('password')

        if (username and realname and emailadd and password):

            emailadd_ch = mongo.Users.find_one({'email_address': request.form.get('emailadd')})
            username_ch = mongo.Users.find_one({'username': request.form.get('username')})

            if (emailadd_ch or username_ch):

                if emailadd_ch:

                    return jsonify(error='The email address \'' + emailadd + '\' is already registered.'), 409

                if username_ch:

                    return jsonify(error='The username \'' + username + '\' is already registered.'), 409

            else:

                role = 1

                if mongo.Users.find_one() is None:

                    role = 0

                mongo.Users.insert({
                    'username' : username,
                    'realname' : realname,
                    'email_address' : emailadd,
                    'password' : bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()),
                    'role' : role,
                    'preferences' : {
                        'confirm' : True,
                        'authorized' : []
                    }
                })

                return jsonify(success='Registration completed successfully. You may now login.'), 201

        else:

            return jsonify(error='Please complete all fields in the form.'), 400

RegisterView.register(app)
