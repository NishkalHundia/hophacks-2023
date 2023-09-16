from flask import Flask, redirect
from flask import request
import matplotlib.pyplot as plt
import keras_ocr
from drug_named_entity_recognition import find_drugs
import requests
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from PIL import Image

SECRET_KEY = "emergencymeeting"

#DONT TOUCH THE CODE IF YOURE READING THIS, IM STILL NOT DONE

pipeline = keras_ocr.pipeline.Pipeline()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/hophacks'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = SECRET_KEY
login_manager = LoginManager()
login_manager.init_app(app)
db = SQLAlchemy(app)

class usertable(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)

class userinfo(UserMixin, db.Model):
    info_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('usertable.user_id'), nullable=False)
    first_name = db.Column(db.String(32), nullable=False)
    last_name = db.Column(db.String(32), nullable=False)
    height = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    date_of_birth = db.Column(db.DateTime, nullable=False)

class userstaff(UserMixin, db.Model):
    staff_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('usertable.user_id'), nullable=False)
    nurse_id = db.Column(db.Integer, db.ForeignKey('usertable.user_id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('usertable.user_id'), nullable=False)

class userpwd(UserMixin, db.Model):
    pwd_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('usertable.user_id'), nullable=False)
    password = db.Column(db.String(128), nullable=False)

class prescription(UserMixin, db.Model):
    prescription_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('usertable.user_id'), nullable=False)
    nurse_id = db.Column(db.Integer, db.ForeignKey('usertable.user_id'), nullable=False)
    drug_name = db.Column(db.String(64), nullable=False)
    drug_description = db.Column(db.String(512))
    drug_power = db.Column(db.Integer, nullable=False)
    drug_days = db.Column(db.String(16), nullable=False)
    drug_time = db.Column(db.String(16), nullable=False)
    expiry = db.Column(db.DateTime, nullable=False)

#Le login stuff
@login_manager.user_loader
def load_user(user_id):
    return usertable.query.get(int(user_id))

# POST for registering
@app.route("/register", methods=["POST"])
def register():
    name = request.args.get("name")
    password = request.args.get("password")
    first_name = request.args.get("first_name")
    last_name = request.args.get("last_name")
    height = request.args.get("height")
    weight = request.args.get("weight")
    date_of_birth = request.args.get("date_of_birth")
    nurse_id = request.args.get("nurse_id")
    doctor_id = request.args.get("doctor_id")
    user = usertable(name=name)
    db.session.add(user)
    db.session.commit()
    user = usertable.query.filter_by(name=name).first()
    user_id = user.user_id
    userpwd = userpwd(user_id=user_id, password=password)
    userinfo = userinfo(user_id=user_id, first_name=first_name, last_name=last_name, height=height, weight=weight, date_of_birth=date_of_birth)
    userstaff = userstaff(user_id=user_id, nurse_id=nurse_id, doctor_id=doctor_id)
    db.session.add(userpwd)
    db.session.add(userinfo)
    db.session.add(userstaff)
    db.session.commit()
    return redirect("/login")

# POST for logging in
@app.route("/login", methods=["POST"])
def login():
    name = request.args.get("name")
    password = request.args.get("password")
    user = usertable.query.filter_by(name=name).first()
    if user is None:
        return "User does not exist"
    userpwd = userpwd.query.filter_by(user_id=user.user_id).first()
    if userpwd.password != password:
        return "Incorrect password"
    login_user(user)
    return str(user.user_id)

# POST for image recognition
@app.route("/scan_check", methods=["POST"])
def scan_check():
    file = request.files['image']
    img = Image.open(file.stream)
    plt.imshow(img)
    plt.show()

    img = keras_ocr.tools.read(img)
    prediction_groups = pipeline.recognize([img])

    s = []
    for predictions in prediction_groups:
        for x in predictions:
            s.append(x[0])

    try:
        return find_drugs(s, is_ignore_case=True)[0][0]["name"]
    except:
        return "No drug found"

# POST for manual input
@app.route("/manual_check", methods=["POST"])
def manual_check():

    drug = []
    drug.append(request.args.get("drug"))

    try:
        return find_drugs(drug, is_ignore_case=True)[0][0]["name"]
    except:
        return "No drug found"

@app.route("/check_compatibility", methods=["GET"])
def check_compatibility():
    drug = request.args.get("drug")
    #TODO: I fucking dont know how what why the fuck are we using flask bro

@app.route("/add", methods=["POST"])
def add():
    drug = request.args.get("drug")

# POST for getting the drug id, idk why is this here, seems useless to me
@app.route("/drug_id", methods=["POST"])
def drug_id():

    drug = request.args.get("drug")

    #return the rx number
    return requests.get("https://rxnav.nlm.nih.gov/REST/rxcui.json?name=" + drug + "&search=1").json()['idGroup']['rxnormId'][0]

app.run(debug=False)