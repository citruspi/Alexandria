from alexandria import app, mongo
from decorators import *
from flask import render_template, request, jsonify, g, send_from_directory, redirect, url_for, session, flash
import os
import shutil
import requests
from pymongo import MongoClient
from functools import wraps
import bcrypt
from bson.objectid import ObjectId

@app.route('/', methods=['GET'])
@authenticated
def index():

    return render_template('app.html')


@app.route('/portal')
def portal():

    if not session.get('username'):

        return render_template('portal.html')

    else:

        return render_template('index.html')


@app.route('/logout')
def logout():

    session.pop('username', None)
    session.pop('role', None)
    session.pop('realname', None)

    return redirect(url_for('index'))


@app.route('/preferences', methods=['GET', 'POST'])
@authenticated
@administrator
def settings():

    if request.method == 'GET':

        return render_template('preferences.html', preferences=mongo.Users.find_one({'username': session.get('username')})['preferences'])

    elif request.method == 'POST':

        user = mongo.Users.find_one({'username': session.get('username')})

        authorized = request.form.get('authorized').split('\r\n')

        user['preferences']['authorized'] = []

        for auth in authorized:

            if auth != '':

                user['preferences']['authorized'].append(auth)

        if len(request.form.getlist('confirm')) > 0:

            user['preferences']['confirm'] = True

        else:

            user['preferences']['confirm'] = False

        mongo.Users.update({'_id':user['_id']}, user, True)

        return ''


@app.route('/download/<id>/<format>')
@authenticated
def download(id, format):

    book = mongo.Books.find({'id':id})[0]

    response = send_from_directory(app.config['LIB_DIR'], id+'.'+format)
    response.headers.add('Content-Disposition', 'attachment; filename="' + book['title'] + '.' + format + '"')

    return response


@app.route('/edit/<id>', methods=['GET', 'POST'])
@authenticated
@administrator
def edit(id):

    book = mongo.Books.find({"id": id})[0]

    if request.method == 'GET':

        return render_template('edit.html', book=book)

    elif request.method == 'POST':

        book['title'] = request.form.get('title')
        book['subtitle'] = request.form.get('subtitle')

        authors = request.form.get('authors').split('\r\n')

        book['authors'] = []

        for author in authors:

            if author != '':

                book['authors'].append(author)

        book['cover'] = request.form.get('cover')
        book['description'] = request.form.get('description')
        book['genres'] = request.form.getlist('genres')

        mongo.Books.update({'_id':book['_id']}, book, True)

        return ''


@app.route('/upload')
@authenticated
@administrator
def upload():

    return render_template('upload.html')

if __name__ == "__main__":

	  app.run()
