
import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
import main
import tools
import random

app = Flask(__name__)

# Run API
# ----------------------
# $ export FLASK_APP=mainAPI.py
# $ flash run

UPLOAD_FOLDER = 'resultado/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
  return 'Server Works!'
  

@app.route('/processimage', methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        hash = random.getrandbits(128)
        directory = "ProcessDirectory_" + str(hash) + "/"
        
        if not os.path.exists(directory):
          os.makedirs(directory)

        f.save(directory + f.filename)
        
        analises = main.execute(directory, 'layouts/lab_setrem.json', 'default', '', False)

        tools.removeTemporaryFiles(directory)

        return analises

    return 'Upload success'