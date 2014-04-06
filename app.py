from flask import Flask, render_template, request, jsonify
import os
import shutil
import requests
from pymongo import MongoClient
import pprint

app = Flask(__name__)
app.config.from_object('config.Debug')

client = MongoClient(app.config['MONGOHOST'], app.config['MONGOPORT'])
db = client[app.config['MONGODB']]

@app.route('/library')
def library():

    return render_template('library.html')

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

    if 'categories' in r['volumeInfo']:

        book['categories'] = r['volumeInfo']['categories']

    else:

        book['categories'] = ['Uncategorized']

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


    book['files'] = {
        filename.split('.')[-1]: True
    }

    db.Books.insert(book)

    if not db.Genres.find_one():

        genre_count = {}

        for genre in book['categories']:

            genre_count[genre] = 1

        db.Genres.insert(genre_count)

    else:

        genre_count = db.Genres.find_one()

        for genre in book['categories']:

            if genre in genre_count:

                genre_count[genre] = genre_count[genre] + 1

            else:

                genre_count[genre] = 1

        db.Genres.update({'_id':genre_count['_id']}, genre_count, True)


    return ''

if __name__ == "__main__":

	  app.run()
