from flask import Flask, redirect, request
import matplotlib.pyplot as plt
import keras_ocr
from drug_named_entity_recognition import find_drugs

pipeline = keras_ocr.pipeline.Pipeline()

def create_app():
    app = Flask(__name__)

    @app.route('/scan_check', methods = ['POST']) 
    def scan_check():
        image = Flask.request.files.get('medicineImage', '')
        prediction_groups = pipeline.recognize(image)
        s = []
        for predictions in prediction_groups:
            for x in predictions:
                s.append(x[0]) 

        try:
            return find_drugs(s, is_ignore_case=True)[0][0]['name']
        except:
            return "No drug found"

    @app.route('/manual_check', methods = ['POST'])
    def manual_check():
        drug = []
        drug.append(request.form.get('drug'))
        try:
            return find_drugs(drug, is_ignore_case=True)[0][0]['name']
        except:
            return "No drug found"
    
    @app.route('/drug_id', methods = ['POST'])
    def drug_id():
        drug = request.form.get('drug')
        return redirect('https://rxnav.nlm.nih.gov/REST/rxcui.json?name=' + drug + '&search=1')

    return app
