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

        return redirect(url_for('index'))


@app.route('/logout')
def logout():

    session.pop('username', None)
    session.pop('role', None)
    session.pop('realname', None)

    return redirect(url_for('index'))

@app.route('/download/<id>/<format>')
@authenticated
def download(id, format):

    book = mongo.Books.find({'id':id})[0]

    response = send_from_directory(app.config['LIB_DIR'], id+'.'+format)
    response.headers.add('Content-Disposition', 'attachment; filename="' + book['title'] + '.' + format + '"')

    return response


@app.route('/upload')
@authenticated
@administrator
def upload():

    return render_template('upload.html')

if __name__ == "__main__":

	  app.run()
