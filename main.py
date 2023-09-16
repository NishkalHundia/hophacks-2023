import flask
import matplotlib.pyplot as plt
import keras_ocr
from drug_named_entity_recognition import find_drugs

app = flask.Flask(__name__)
pipeline = keras_ocr.pipeline.Pipeline()

@app.route('/check', methods = ['GET', 'POST']) 
def index():
    if flask.request.method == 'POST':
        # Get the file from post request
        image = flask.request.files.get('medicineImage')
        prediction_groups = pipeline.recognize(image)
        s = []
        for predictions in prediction_groups:
            for x in predictions:
                s.append(x[0]) 

            
        return find_drugs(s, is_ignore_case=True)[0][0]['name']

    return 0