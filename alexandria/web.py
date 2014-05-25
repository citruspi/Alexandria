from alexandria import app, mongo
from decorators import *
from flask import render_template, send_from_directory

@app.route('/', methods=['GET'])
def index():

    return render_template('app.html')

@app.route('/download/<id>/<format>')
@authenticated
def download(id, format):

    book = mongo.Books.find({'id':id})[0]

    response = send_from_directory(app.config['LIB_DIR'], id+'.'+format)
    response.headers.add('Content-Disposition', 'attachment; filename="' + book['title'] + '.' + format + '"')

    return response

if __name__ == "__main__":

	  app.run()
