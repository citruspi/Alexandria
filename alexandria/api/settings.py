from . import app, mongo
from alexandria.decorators import *
from flask import request, jsonify, url_for, session
from flask.ext.classy import FlaskView, route
import json
from bson import json_util
from bson.objectid import ObjectId
import bcrypt

class SettingsView(FlaskView):

    route_prefix = '/api/'

    @authenticated
    def get(self):

        query = mongo.Users.find_one({'username': session['username']})

        settings = json.loads(json_util.dumps(query, default=json_util.default))

        settings.pop('_id')
        settings.pop('password')
        settings.pop('role')

        return jsonify(settings=settings)

    @authenticated
    def post(self):

        account = mongo.Users.find_one({'username': session['username']})

        if request.form.get('realname'):

            account['realname'] = request.form.get('realname')

        if request.form.get('email_address'):

            account['email_address'] = request.form.get('emailadd')

        if request.form.get('password'):

            account['password'] = bcrypt.hashpw(request.form.get('password').encode('utf-8'), bcrypt.gensalt())

        mongo.Users.update({'_id':account['_id']}, account, True)

        return ''

SettingsView.register(app)
