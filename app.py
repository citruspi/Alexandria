from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for
import os
import shutil
import requests
from pymongo import MongoClient
from functools import wraps

app = Flask(__name__)
app.config.from_object('config.Debug')

client = MongoClient(app.config['MONGOHOST'], app.config['MONGOPORT'])
db = client[app.config['MONGODB']]

def not_even_one(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if db.Books.find_one() is None:
            return redirect(url_for('upload'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/library')
@not_even_one
def library():

    return render_template('library.html', books=db.Books.find())

@app.route('/download/<id>/<format>')
def download(id, format):

    book = db.Books.find({'id':id})[0]

    response = send_from_directory(app.config['LIB_DIR'], id+'.'+format)
    response.headers.add('Content-Disposition', 'attachment; filename="' + book['title'] + '.' + format + '"')

    return response

@app.route('/genre/<genre>')
@not_even_one
def bygenre(genre):

    books = db.Books.find({'genres':genre})

    return render_template('library.html', books=books)

@app.route('/author/<author>')
@not_even_one
def byauthor(author):

    books = db.Books.find({'authors':author})

    return render_template('library.html', books=books)

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):

    book = db.Books.find({"id": id})[0]

    if request.method == 'GET':

        return render_template('edit.html', book=book)

    elif request.method == 'POST':

        book['title'] = request.form.get('title')
        book['subtitle'] = request.form.get('subtitle')
        book['authors'] = request.form.get('authors').split(',')
        book['cover'] = request.form.get('cover')
        book['description'] = request.form.get('description')
        book['genres'] = request.form.getlist('genres')

        db.Books.update({'_id':book['_id']}, book, True)

        return ''

@app.route('/book/<id>')
def book(id):

    books = db.Books.find({"id": id})

    return render_template('book.html', book=books[0])

@app.route('/upload', methods=['GET', 'POST'])
def upload():

    if request.method == 'GET':

        return render_template('upload.html')

    elif request.method == 'POST':

        file = request.files['file']

        if file:

            filename = os.urandom(30).encode('hex') + '.' + file.filename.split('.')[-1]

            while os.path.isfile(os.path.join(app.config['TEMP_DIR'], filename)):

                filename = os.urandom(30).encode('hex')

            file.save(os.path.join(app.config['TEMP_DIR'], filename))

            return jsonify(filename=filename)

@app.route('/confirm/<filename>/<id>', methods=['POST'])
def confirm(filename, id):

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

    return ''

if __name__ == "__main__":

	  app.run()
