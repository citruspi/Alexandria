from . import app, mongo
from alexandria.decorators import *
from flask import request, jsonify, url_for, session
from flask.ext.classy import FlaskView, route
import json
from bson import json_util
from bson.objectid import ObjectId

class BookView(FlaskView):

    route_prefix = '/api/'

    @authenticated
    def get(self, id):

        query = mongo.Books.find_one({'_id': ObjectId(id)})

        book = json.loads(json_util.dumps(query, default=json_util.default))
        book.pop('_id')

        return jsonify(book=book)


BookView.register(app)
