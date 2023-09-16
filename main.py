import flask

app = flask.Flask(__name__)

@app.route('/check', methods = ['GET', 'POST']) 
def index():
    if flask.request.method == 'POST':
        # Get the file from post request
        image = flask.request.files.get('medicineImage')

        
    return None