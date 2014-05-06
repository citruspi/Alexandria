from flask import Flask, render_template, request, jsonify, g, send_from_directory, redirect, url_for, session, flash
import os
import shutil
import requests
from pymongo import MongoClient
from functools import wraps
from flask.ext.openid import OpenID

app = Flask(__name__)
app.config.from_object('config.Debug')

oid = OpenID(app)

client = MongoClient(app.config['MONGOHOST'], app.config['MONGOPORT'])
db = client[app.config['MONGODB']]

@app.before_request
def before_request():

    g.user = None

    if 'openid' in session:
        g.user = db.Users.find_one({'openid': session['openid']})

def not_even_one(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if db.Books.find_one() is None:
            return redirect(url_for('upload'))
        return f(*args, **kwargs)
    return decorated_function

def is_administrator(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        user = db.Users.find_one({'openid': session['openid']})

        if user['role'] != 'Administrator':

            return redirect(url_for('library'))

        return f(*args, **kwargs)
    return decorated_function

def authenticated(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('login'))
        else:
            if db.Users.find_one() is not None:
                if db.Users.find_one({'email': g.user['email']}) is None:
                    return redirect(url_for('logout'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/', methods=['GET'])
def index():

    if g.user is not None:
        return redirect(url_for('library'))
    else:
        return render_template('login.html')


@app.route('/login')
@oid.loginhandler
def login():

    if g.user is not None:

        return redirect(url_for('library'))

    return oid.try_login('https://www.google.com/accounts/o8/id',
                             ask_for=['email', 'fullname'])

@app.route('/logout')
def logout():

    session.pop('openid', None)
    return redirect(url_for('index'))

@oid.after_login
def create_or_login(resp):


    if db.Settings.find_one():

        if resp.email not in db.Settings.find_one()['authorized']:

            return redirect(url_for('logout'))

    session['openid'] = resp.identity_url
    user = db.Users.find_one({'openid':resp.identity_url})
    if user is not None:
        g.user = user
    else:

        if db.Users.find_one() is None:

            db.Users.insert({
                'name': resp.fullname or resp.nickname,
                'email': resp.email,
                'openid': session['openid'],
                'role': 'Administrator'
            })

            db.Settings.insert({
                'authorized': [resp.email],
                'confirm': False
            })

        else:

            if resp.email in db.Settings.find_one()['authorized']:

                db.Users.insert({
                    'name': resp.fullname or resp.nickname,
                    'email': resp.email,
                    'openid': session['openid'],
                    'role': 'User'
                })

            else:

                redirect(url_for('logout'))

    return redirect(oid.get_next_url())

@app.route('/settings', methods=['GET', 'POST'])
@authenticated
@is_administrator
def settings():

    if request.method == 'GET':

        return render_template('settings.html', setting=db.Settings.find_one())

    elif request.method == 'POST':

        authorized = request.form.get('authorized').split('\r\n')

        setting = db.Settings.find_one()

        setting['authorized'] = []

        for auth in authorized:

            if auth != '':

                setting['authorized'].append(auth)

        if len(request.form.getlist('confirm')) > 0:

            setting['confirm'] = True

        else:

            setting['confirm'] = False

        db.Settings.update({'_id':setting['_id']}, setting, True)

        return ''

@app.route('/library', defaults={'page': 1})
@app.route('/library/<int:page>')
@authenticated
@not_even_one
def library(page):

    perpage = 10

    books = db.Books.find().skip((page-1)*perpage).limit(perpage)
    cap = db.Books.count() / perpage

    if db.Books.count() % perpage > 0:

        cap += 1

    return render_template('library.html', books=books, page=page, cap=cap)

@app.route('/download/<id>/<format>')
@authenticated
def download(id, format):

    book = db.Books.find({'id':id})[0]

    response = send_from_directory(app.config['LIB_DIR'], id+'.'+format)
    response.headers.add('Content-Disposition', 'attachment; filename="' + book['title'] + '.' + format + '"')

    return response

@app.route('/genre/<genre>', defaults={'page': 1})
@app.route('/genre/<genre>/<int:page>')
@authenticated
@not_even_one
def bygenre(genre, page):

    perpage = 10

    books = db.Books.find({'genres':genre}).skip((page-1)*perpage).limit(perpage)
    cap = db.Books.find({'genres':genre}).count() / perpage

    if db.Books.count() % perpage > 0:

        cap += 1

    return render_template('library.html', books=books, page=page, cap=cap)

@app.route('/author/<author>', defaults={'page': 1})
@app.route('/author/<author>/<int:page>')
@authenticated
@not_even_one
def byauthor(author, page):

    perpage = 10

    books = db.Books.find({'authors':author}).skip((page-1)*perpage).limit(perpage)
    cap = db.Books.find({'authors':author}).count() / perpage

    if db.Books.count() % perpage > 0:

        cap += 1

    return render_template('library.html', books=books, page=page, cap=cap)

@app.route('/edit/<id>', methods=['GET', 'POST'])
@authenticated
@is_administrator
def edit(id):

    book = db.Books.find({"id": id})[0]

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

        db.Books.update({'_id':book['_id']}, book, True)

        return ''

@app.route('/book/<id>')
@authenticated
def book(id):

    books = db.Books.find({"id": id})

    return render_template('book.html', book=books[0])

@app.route('/upload', methods=['GET', 'POST'])
@authenticated
@is_administrator
def upload():

    if request.method == 'GET':

        return render_template('upload.html', setting=db.Settings.find_one())

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
@is_administrator
def confirm(filename, id):

    query = db.Books.find_one({'id': id})

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

        db.Books.insert(book)

    else:

        if filename.split('.')[-1] in query['files']:

            return jsonify(error='The format \'' + filename.split('.')[-1] + '\' already exists.'), 409

        else:

            query['files'].append(filename.split('.')[-1])

            if os.path.isfile(os.path.join(app.config['TEMP_DIR'], filename)):

                shutil.move(os.path.join(app.config['TEMP_DIR'], filename), os.path.join(app.config['LIB_DIR'], query['id']+'.'+filename.split('.')[-1]))

            db.Books.update({'_id':query['_id']}, query, True)

    return ''

if __name__ == "__main__":

	  app.run()
