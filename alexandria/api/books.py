from . import app, mongo
from alexandria.decorators import *
from flask import request, jsonify, url_for, session
from flask.ext.classy import FlaskView, route
import json
from bson import json_util

class BooksView(FlaskView):

    route_prefix = '/api/'

    @authenticated
    def index(self):

        query = mongo.Books.find()

        books = json.loads(json_util.dumps(query, default=json_util.default))

        for book in books:

            book['id'] = book['_id']['$oid']
            book.pop('_id')

            book['owner'] = book['owner']['$oid']

        return jsonify(books=books)

    @authenticated
    def genre(self, id):

        query = mongo.Books.find({'genres':id})

        books = json.loads(json_util.dumps(query, default=json_util.default))

        for book in books:

            book['id'] = book['_id']['$oid']
            book.pop('_id')

            book['owner'] = book['owner']['$oid']

        return jsonify(books=books)


    @authenticated
    def author(self, id):

        query = mongo.Books.find({'authors':id})

        books = json.loads(json_util.dumps(query, default=json_util.default))

        for book in books:

            book['id'] = book['_id']['$oid']
            book.pop('_id')

            book['owner'] = book['owner']['$oid']

        return jsonify(books=books)


BooksView.register(app)
