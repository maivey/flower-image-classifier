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

# try:
#     import Image
# except:
# import PIL
from PIL import Image
# import Pillow.Image
# from pillow import Image
# import PIL
# from PIL import Image
# 
# import Image
import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
import json
import time
import os

# Tensorflow imports
import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_datasets as tfds


# **** Place functions here from predict.py to avoid Heroku Error: **** 
# from predict import process_image, prediction, get_label_names
def process_image(image):
    '''
    The process_image function should take in an image (in the form of a NumPy array) and return an image in the form of a NumPy array with shape (224, 224, 3).
    '''
    # First, convert the image into a TensorFlow Tensor then resize it to the appropriate size using tf.image.resize
    image = tf.convert_to_tensor(image, dtype=tf.float32)
    image = tf.image.resize(image, (224,224))
    #Second, the pixel values of the input images are typically encoded as integers in the range 0-255, but the model expects the pixel values to be floats in the range 0-1. 
    # #Therefore, you'll also need to normalize the pixel values
    image /= 255

    image = image.numpy()
    return image
    
def prediction(image_path,model,top_k):
    import os
    model = 'my_model2'
    # model = '1587680462.h5'
    # export_path = os.path.join(os.getcwd(),model)
    # Load the model passed into the function
    # reloaded_keras_model = tf.keras.models.load_model(model, custom_objects={'KerasLayer':hub.KerasLayer})
    # reloaded_keras_model = tf.saved_model.load(export_path)
    reloaded_keras_model = tf.saved_model.load(model)

    # Process the image selected
    im = Image.open(image_path)
    test_image = np.asarray(im)
    processed_test_image = process_image(test_image)

    #The image returned by the process_image function is a NumPy array with shape (224, 224, 3) but the model expects the input images to be of shape (1, 224, 224, 3). This extra dimension represents the batch size.
    # Use  np.expand_dims() function to add the extra dimension.
    processed_test_image = np.expand_dims(processed_test_image, axis=0)

    # Create the model to get the probabilities by using the model and softmax layer as the input
    # probability_model = tf.keras.Sequential([reloaded_keras_model, 
                                          # tf.keras.layers.Softmax()])
    
    # Get the predictions by using the probability model to predict the input image 
    # predictions = probability_model.predict(processed_test_image)
    predictions = reloaded_keras_model(processed_test_image)
    predictions = np.array(predictions)
    # Get the index of the top 10 probabilities
    top_idxs = predictions[0].argsort()[-top_k:][::-1]
    
    # Get the top 10 probabilities
    top_probabilities = predictions[0][top_idxs]
    probs = top_probabilities
    
    # Get the labels (the index of the probabilities)
    labels_nums = [str(idx) for idx in top_idxs]
    classes = labels_nums
    return probs, classes


def get_label_names(json_file, labels):
    '''
    Given json_file that contains the label names for the label numbers, return the correct label names from array 'label'
    '''
    with open(json_file, 'r') as f:
        class_names = json.load(f)
    new_class_names = {}
    for key in class_names:
        new_class_names[int(key)-1]=class_names[key]
    label_names = [new_class_names[int(i)] for i in labels]
    return label_names
# **** End functions from predict.py  **** 


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
            print(filename)
            print(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Dont save file-- try if throw error
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            top_k = str(request.form['month_day'])
            if top_k.isdigit() == False:
                return flask.render_template('index.html', 
                                    topKError = True)
            else:
                print(top_k)
                top_k = int(top_k)
                
                # probs, classes = prediction(filename, 'my_model2', top_k)
                probs, classes = prediction(file_path, 'my_model2', top_k)
                
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
# from flask import send_from_directory
# @app.route('/my_model')
# def uploaded_file(filename):
#     return send_from_directory(filename)
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