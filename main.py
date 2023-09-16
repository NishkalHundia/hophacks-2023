import flask
import matplotlib.pyplot as plt
import keras_ocr

app = flask.Flask(__name__)
pipeline = keras_ocr.pipeline.Pipeline()

@app.route('/check', methods = ['GET', 'POST']) 
def index():
    if flask.request.method == 'POST':
        # Get the file from post request
        image = flask.request.files.get('medicineImage')
        prediction_groups = pipeline.recognize(image)
        for image, predictions in zip(image, prediction_groups):
            keras_ocr.tools.drawAnnotations(image=image, predictions=predictions)
            print(predictions)
            print("-----END-----")

        
    return None