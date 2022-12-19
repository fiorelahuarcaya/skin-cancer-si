from flask import Flask, request
from json import dumps
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from prediccionMobile import predict
from mejora_de_imagen import mejorar_image

UPLOAD_FOLDER = 'images/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
dirname = os.path.dirname(__file__)

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config['DEBUG'] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
cors = CORS(app)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return dumps({"message": 'Bienvenido a OncoSalud'})


@app.route('/image/', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        return dumps({"message": 'No file part'})
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        return dumps({"message": 'No selected file'})
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(dirname, app.config['UPLOAD_FOLDER'] + filename))

        # Mejoramos la imagen
        mejorar_image(filename)
        result = predict(os.path.join(dirname, "static/" + filename))

        return dumps({"predict": result[0], "melanoma": result[1], "other": result[2]})
    return dumps({"message": 'File not allowed'})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3333)
