import flask
from flask import Flask, render_template, url_for
# from flask import render_template
from flask import request
from flask import jsonify
from flask import send_from_directory
from flask import redirect
from flask import flash
import os.path

# import pandas as pd
# import time
# import pandas as pd
# import numpy as np
import datetime
import json

import numpy as np
from PIL import Image
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import time
import os

# Tensorflow imports
import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_datasets as tfds

from predict import process_image, prediction, get_label_names

# Call the prediction function to get the top k probabilities and corresponding labels
# probs, classes = prediction(img_path, my_model2, top_k)
# # Print the probabilities and class numbers to the console
# print(f'Proabilities: {probs}')
# print(f'Label Numbers: {classes}')


# # Call the get_label_names function with the JSON file with class names and the classes returned from prediction
# label_names = get_label_names(label_map.json, classes)
# # Print the class names to the console
# print(f'Label Names: {label_names}')

from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
# ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg'}
ALLOWED_EXTENSIONS = {'jpg','jpeg'}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'GET':
        return flask.render_template('index.html')
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            # flash('No file part')
            # return redirect(request.url)
            return flask.render_template('index.html', 
                                    noFile = True)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            # flash('No selected file')
            # return redirect(request.url)
            return flask.render_template('index.html', 
                                    noSelectedFile = True)
        if allowed_file(file.filename) == False:
            return flask.render_template('index.html', 
                                    noFile = True)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            top_k = str(request.form['month_day'])
            if top_k.isdigit() == False:
                return flask.render_template('index.html', 
                                    topKError = True)
            else:
                print(top_k)
                top_k = int(top_k)
                
                probs, classes = prediction(filename, 'my_model2', top_k)
                
            # Print the probabilities and class numbers to the console
                print(f'Proabilities: {probs}')
                print(probs[0])
                print(f'Label Numbers: {classes}')


                # Call the get_label_names function with the JSON file with class names and the classes returned from prediction
                label_names = get_label_names('label_map.json', classes)
                # Print the class names to the console
                print(f'Label Names: {label_names}')
                print(probs[0])
                print(classes[0])
                print(label_names[0])
                top_flower_name = label_names[0].title()
                top_prob = round(probs[0]*100,2)
                
                if top_k == 1:
                    return flask.render_template('index.html', 
                                            probs = probs,
                                            classes=classes,
                                            labelNames=label_names,
                                            topFlowerName = top_flower_name,
                                            onlyOneK = True,
                                            topProb = top_prob)
                else:
                    temp = 'temp'
                    return flask.render_template('index.html', 
                                            probs = probs,
                                            classes=classes,
                                            labelNames=label_names,
                                            temp=temp,
                                            topFlowerName = top_flower_name,
                                            topProb = top_prob)
            # return redirect(url_for('uploaded_file',
            #                         filename=filename))

    # return flask.render_template('index.html')
    # '''
    # <!doctype html>
    # <title>Upload new File</title>
    # <h1>Upload new File</h1>
    # <form method=post enctype=multipart/form-data>
    #   <input type=file name=file>
    #   <input type=submit value=Upload>
    # </form>
    # '''
from flask import send_from_directory

# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'],
#                                filename)
# if request.method =='GET':
#         top_k = int(top_k)
#         probs, classes = prediction(filename, 'my_model2', top_k)
#     # Print the probabilities and class numbers to the console
#         print(f'Proabilities: {probs}')
#         print(f'Label Numbers: {classes}')


#         # Call the get_label_names function with the JSON file with class names and the classes returned from prediction
#         label_names = get_label_names('label_map.json', classes)
#         # Print the class names to the console
#         print(f'Label Names: {label_names}')
#         return flask.render_template('index.html', 
#                                 probs = probs,
#                                 classes=classes,
#                                 labelNames=label_names)
#     if request.method =='POST':
#         # check if the post request has the file part
#         if 'file' not in request.files:
#             flash('No file part')
#             return redirect(request.url)
#         file = request.files['file']
#         # if user does not select file, browser also
#         # submit an empty part without filename
#         if file.filename == '':
#             flash('No selected file')
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             top_k = str(request.form['month_day'])
#             print(top_k)
#             return redirect(url_for('uploaded_file',
#                                     filename=filename,
#                                     top_k = top_k))
if __name__ == "__main__":
    app.run(debug=True) 