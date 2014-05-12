from . import app, mongo
from alexandria.decorators import *
from flask import request, jsonify, url_for, session
from flask.ext.classy import FlaskView, route
import json
from bson import json_util
import requests
import os

class UploadView(FlaskView):

    route_prefix = '/api/'

    @authenticated
    def search(self, query):

        results = requests.get('https://www.googleapis.com/books/v1/volumes?q='+query).json()

        return jsonify(results=results)

    @authenticated
    def post(self):

        file = request.files['file']

        book = mongo.Books.find_one({'isbn-13': request.form.get('isbn-13')})

        if book:

            if file.filename.split('.')[-1] in book['formats']:

                return jsonify(error='Duplicate file format!'), 409

            else:

                book['formats'].append(file.filename.split('.')[-1])

                file.save(os.path.join(app.config['LIB_DIR'], book['id'] + '.' + file.filename.split('.')[-1]))

                mongo.Books.update({'_id':book['_id']}, book, True)

                return '', 200

        book = mongo.Books.find_one({'isbn-10': request.form.get('isbn-10')})

        if book:

            if file.filename.split('.')[-1] in book['formats']:

                return jsonify(error='Duplicate file format!'), 409

            else:

                book['formats'].append(file.filename.split('.')[-1])

                file.save(os.path.join(app.config['LIB_DIR'], book['id'] + '.' + file.filename.split('.')[-1]))

                mongo.Books.update({'_id':book['_id']}, book, True)

                return '', 200

        user = mongo.Users.find_one({'username': session.get('username')})

        book = {
            'title': request.form.get('title'),
            'subtitle': request.form.get('subtitle'),
            'isbn-10': request.form.get('isbn-10'),
            'isbn-13': request.form.get('isbn-13'),
            'isbn-10': request.form.get('isbn-10'),
            'publisher': request.form.get('publisher'),
            'publishedDate': request.form.get('datepublished'),
            'cover': request.form.get('cover'),
            'description': request.form.get('description'),
            'genres': filter(None, request.form.get('genres').split(',')),
            'authors': request.form.get('authors').split(','),
            'owner': str(user['_id']),
            'formats': [file.filename.split('.')[-1]]
        }

        id = mongo.Books.insert(book);

        book['id'] = str(id)

        mongo.Books.update({'_id':id}, book, True)

        file.save(os.path.join(app.config['LIB_DIR'], str(id) + '.' + file.filename.split('.')[-1]))

        return '', 200

UploadView.register(app)
