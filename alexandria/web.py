from alexandria import app, mongo
from flask import render_template, request, jsonify, g, send_from_directory, redirect, url_for, session, flash
import os
import shutil
import requests
from pymongo import MongoClient
from functools import wraps
import bcrypt

def not_even_one(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if mongo.Books.find_one() is None:
            return redirect(url_for('upload'))
        return f(*args, **kwargs)
    return decorated_function

def authenticated(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):

        if not session.get('username'):

            return redirect(url_for('portal'))

        return f(*args, **kwargs)
    return decorated_function

def administrator(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        user = mongo.Users.find_one({'username': session.get('username')})

        if user['role'] != 0:

            return redirect(url_for('index'))

        return f(*args, **kwargs)
    return decorated_function

@app.route('/', methods=['GET'])
def index():

    if session.get('username'):

        return redirect(url_for('library'))

    else:

        return redirect(url_for('portal'))

@app.route('/portal')
def portal():

    if not session.get('username'):

        return render_template('portal.html')

    else:

        return render_template('index.html')

@app.route('/portal/register', methods=['POST'])
def register():

    if (request.form.get('username') and
        request.form.get('realname') and
        request.form.get('emailadd') and
        request.form.get('password')):

        emailadd = mongo.Users.find_one({'email_address': request.form.get('emailadd')})
        username = mongo.Users.find_one({'username': request.form.get('username')})

        if (emailadd is None) and (username is None):

            role = 1

            if mongo.Users.find_one() is None:

                role = 0

            mongo.Users.insert({
                'username' : request.form.get('username'),
                'realname' : request.form.get('realname'),
                'email_address' : request.form.get('emailadd'),
                'password' : bcrypt.hashpw(request.form.get('password').encode('utf-8'), bcrypt.gensalt()),
                'role' : role,
                'preferences' : {
                    'confirm' : True,
                    'authorized' : []
                }
            })

            return 'Registration completed successfully.'

        else:

            if emailadd is not None:

                return 'Email address already registered.'

            elif username is not None:

                return 'Username is already registered.'

    else:

        return 'Please fill out all the fields.'

@app.route('/portal/login', methods=['POST'])
def login():

    if (request.form.get('username') and
        request.form.get('password')):

        query = mongo.Users.find_one({'username': request.form.get('username')})

        if query is not None:

            if bcrypt.hashpw(request.form.get('password').encode('utf-8'), query['password'].encode('utf8')) == query['password']:

                session['username'] = request.form.get('username')
                session['role'] = query['role']
                session['realname'] = query['realname']

                return redirect(url_for('index'))

            else:

                return 'Incorrect login.'

        else:

            return 'Username not registered.'

    else:

        return 'Please fill out all the fields.'


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

@app.route('/library', defaults={'page': 1})
@app.route('/library/<int:page>')
@authenticated
@not_even_one
def library(page):

    perpage = 10

    books = mongo.Books.find().skip((page-1)*perpage).limit(perpage)
    cap = mongo.Books.count() / perpage

    if mongo.Books.count() % perpage > 0:

        cap += 1

    return render_template('library.html', books=books, page=page, cap=cap)

@app.route('/download/<id>/<format>')
@authenticated
def download(id, format):

    book = mongo.Books.find({'id':id})[0]

    response = send_from_directory(app.config['LIB_DIR'], id+'.'+format)
    response.headers.add('Content-Disposition', 'attachment; filename="' + book['title'] + '.' + format + '"')

    return response

@app.route('/genre/<genre>', defaults={'page': 1})
@app.route('/genre/<genre>/<int:page>')
@authenticated
@not_even_one
def bygenre(genre, page):

    perpage = 10

    books = mongo.Books.find({'genres':genre}).skip((page-1)*perpage).limit(perpage)
    cap = mongo.Books.find({'genres':genre}).count() / perpage

    if mongo.Books.count() % perpage > 0:

        cap += 1

    return render_template('library.html', books=books, page=page, cap=cap)

@app.route('/author/<author>', defaults={'page': 1})
@app.route('/author/<author>/<int:page>')
@authenticated
@not_even_one
def byauthor(author, page):

    perpage = 10

    books = mongo.Books.find({'authors':author}).skip((page-1)*perpage).limit(perpage)
    cap = mongo.Books.find({'authors':author}).count() / perpage

    if mongo.Books.count() % perpage > 0:

        cap += 1

    return render_template('library.html', books=books, page=page, cap=cap)

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

@app.route('/book/<id>')
@authenticated
def book(id):

    books = mongo.Books.find({"id": id})

    return render_template('book.html', book=books[0])

@app.route('/upload', methods=['GET', 'POST'])
@authenticated
@administrator
def upload():

    if request.method == 'GET':

        return render_template('upload.html', setting=mongo.Settings.find_one())

    elif request.method == 'POST':

        file = request.files['file']

        if file:

            filename = os.urandom(30).encode('hex') + '.' + file.filename.split('.')[-1]

            while os.path.isfile(os.path.join(app.config['TEMP_DIR'], filename)):

                filename = os.urandom(30).encode('hex')

            file.save(os.path.join(app.config['TEMP_DIR'], filename))

            return jsonify(filename=filename)

@app.route('/confirm/<filename>/<id>', methods=['POST'])
@authenticated
@administrator
def confirm(filename, id):

    query = mongo.Books.find_one({'id': id})

    if query is None:

        r = requests.get('https://www.googleapis.com/books/v1/volumes/'+id).json()

        if os.path.isfile(os.path.join(app.config['TEMP_DIR'], filename)):

            shutil.move(os.path.join(app.config['TEMP_DIR'], filename), os.path.join(app.config['LIB_DIR'], r['id']+'.'+filename.split('.')[-1]))

        book = {}

        book['id'] = r['id']

        if 'title' in r['volumeInfo']:

            book['title'] = r['volumeInfo']['title']

        if 'subtitle' in r['volumeInfo']:

            book['subtitle'] = r['volumeInfo']['subtitle']

        if 'authors' in r['volumeInfo']:

            book['authors'] = r['volumeInfo']['authors']

        if 'publisher' in r['volumeInfo']:

            book['publisher'] = r['volumeInfo']['publisher']

        if 'publishedDate' in r['volumeInfo']:

            book['publishedDate'] = r['volumeInfo']['publishedDate']

        if 'description' in r['volumeInfo']:

            book['description'] = r['volumeInfo']['description']

        if 'averageRating' in r['volumeInfo']:

            book['averageRating'] = r['volumeInfo']['averageRating']

        if 'ratingsCount' in r['volumeInfo']:

            book['ratingsCount'] = r['volumeInfo']['ratingsCount']

        if 'language' in r['volumeInfo']:

            book['language'] = r['volumeInfo']['language']

        book['identifiers'] = []

        if 'industryIdentifiers' in r['volumeInfo']:

            for identifier in r['volumeInfo']['industryIdentifiers']:

                book['identifiers'].append({
                    'type': identifier['type'],
                    'identifier': identifier['identifier']
                })

        book['identifiers'].append({
            'type': 'GOOGLE',
            'identifier': r['id']
        })

        if 'imageLinks' in r['volumeInfo']:

            if 'extraLarge' in r['volumeInfo']['imageLinks']:

                book['cover'] = r['volumeInfo']['imageLinks']['extraLarge']

            elif 'large' in r['volumeInfo']['imageLinks']:

                book['cover'] = r['volumeInfo']['imageLinks']['large']

            elif 'medium' in r['volumeInfo']['imageLinks']:

                book['cover'] = r['volumeInfo']['imageLinks']['medium']

            elif 'small' in r['volumeInfo']['imageLinks']:

                book['cover'] = r['volumeInfo']['imageLinks']['small']

            elif 'thumbnail' in r['volumeInfo']['imageLinks']:

                book['cover'] = r['volumeInfo']['imageLinks']['thumbnail']

            elif 'thumbnail' in r['volumeInfo']['imageLinks']:

                book['cover'] = r['volumeInfo']['imageLinks']['smallThumbnail']

            else:

                book['cover'] = ''

        book['files'] = []

        book['files'].append(filename.split('.')[-1])

        book['genres'] = []

        if len(request.form.getlist('genres')) == 0:

            book['genres'].append('Uncategorized')

        else:

            for genre in request.form.getlist('genres'):

                book['genres'].append(genre)

        mongo.Books.insert(book)

    else:

        if filename.split('.')[-1] in query['files']:

            return jsonify(error='The format \'' + filename.split('.')[-1] + '\' already exists.'), 409

        else:

            query['files'].append(filename.split('.')[-1])

            if os.path.isfile(os.path.join(app.config['TEMP_DIR'], filename)):

                shutil.move(os.path.join(app.config['TEMP_DIR'], filename), os.path.join(app.config['LIB_DIR'], query['id']+'.'+filename.split('.')[-1]))

            mongo.Books.update({'_id':query['_id']}, query, True)

    return ''

if __name__ == "__main__":

	  app.run()
