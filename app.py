from flask import Flask, render_template, request, jsonify
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

            filename = os.urandom(30).encode('hex')

            while os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], filename)):

                filename = os.urandom(30).encode('hex')

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            return jsonify(filename=filename)

if __name__ == "__main__":

	  app.run()
