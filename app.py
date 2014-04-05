from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config.from_object('config.Debug')

@app.route('/upload', methods=['GET', 'POST'])
def upload():

    if request.method == 'GET':

        return render_template('upload.html')

    elif request.method == 'POST':

        file = request.files['file']

        if file:

            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            return jsonify(filename=filename)


if __name__ == "__main__":

	  app.run()
