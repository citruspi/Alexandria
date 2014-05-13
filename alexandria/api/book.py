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

    @authenticated
    def post(self, id):

        book = mongo.Books.find({"id": id})[0]

        book['title'] = request.form.get('title')
        book['subtitle'] = request.form.get('subtitle')

        book['cover'] = request.form.get('cover')
        book['description'] = request.form.get('description')

        mongo.Books.update({'_id':book['_id']}, book, True)

        return ''

BookView.register(app)
