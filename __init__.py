from flask import Flask, redirect
from flask import request
from flask import jsonify
import matplotlib.pyplot as plt
import keras_ocr
from drug_named_entity_recognition import find_drugs
import requests
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import psycopg2

secret = "lolol"

# DONT TOUCH THE CODE IF YOURE READING THIS, IM STILL NOT DONE

pipeline = keras_ocr.pipeline.Pipeline()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://ubuntu:0912@localhost/hophacks"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = secret
login_manager = LoginManager()
login_manager.init_app(app)
db = SQLAlchemy(app)


class usertable(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)

    def get_id(self):
        return self.user_id


class userinfo(UserMixin, db.Model):
    info_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("usertable.user_id"), nullable=False)
    firstname = db.Column(db.String(32), nullable=False)
    lastname = db.Column(db.String(32), nullable=False)
    height = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    dateofbirth = db.Column(db.DateTime, nullable=False)


class userstaff(UserMixin, db.Model):
    staff_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("usertable.user_id"), nullable=False)
    nurse_id = db.Column(db.Integer, db.ForeignKey("usertable.user_id"), nullable=False)
    doctor_id = db.Column(
        db.Integer, db.ForeignKey("usertable.user_id"), nullable=False
    )


class userpwd(UserMixin, db.Model):
    pwd_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("usertable.user_id"), nullable=False)
    pwd = db.Column(db.String(128), nullable=False)


class prescription(UserMixin, db.Model):
    prescription_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("usertable.user_id"), nullable=False)
    nurse_id = db.Column(db.Integer, db.ForeignKey("usertable.user_id"), nullable=False)
    rxcuid = db.Column(db.Integer, nullable=False)
    drug_name = db.Column(db.String(64), nullable=False)
    drug_description = db.Column(db.String(512))
    drug_power = db.Column(db.Integer, nullable=False)
    drug_days = db.Column(db.String(16), nullable=False)
    drug_time = db.Column(db.String(16), nullable=False)
    expiry = db.Column(db.DateTime, nullable=False)


# Le login stuff
@login_manager.user_loader
def load_user(user_id):
    return usertable.query.get(int(user_id))


# POST for registering
@app.route("/register", methods=["POST"])
def register():
    name = request.args.get("name")
    pwd = request.args.get("password")
    firstname = request.args.get("first_name")
    lastname = request.args.get("last_name")
    height = request.args.get("height")
    weight = request.args.get("weight")
    date_of_birth = datetime.strptime(request.args.get("date_of_birth"), "%Y-%m-%d")
    nurse_id = request.args.get("nurse_id")
    doctor_id = request.args.get("doctor_id")
    user = usertable(name=name)
    db.session.add(user)
    db.session.commit()
    user = usertable.query.filter_by(name=name).first()
    user_id = user.user_id
    user_pwd = userpwd(user_id=user_id, pwd=pwd)
    user_info = userinfo(
        user_id=user_id,
        firstname=firstname,
        lastname=lastname,
        height=height,
        weight=weight,
        dateofbirth=date_of_birth,
    )
    user_staff = userstaff(user_id=user_id, nurse_id=nurse_id, doctor_id=doctor_id)
    db.session.add(user_pwd)
    db.session.add(user_info)
    db.session.add(user_staff)
    db.session.commit()
    return "successful"


# POST for logging in
@app.route("/login", methods=["POST"])
def login():
    name = request.args.get("name")
    pwd = request.args.get("password")
    user = usertable.query.filter_by(name=name).first()
    if user is None:
        return "User does not exist"
    userpwd_ = userpwd.query.filter_by(user_id=user.user_id).first()
    if userpwd_.pwd != pwd:
        return "Incorrect password"
    login_user(user)
    nurse_id = userstaff.query.filter_by(user_id=user.user_id).first().nurse_id
    return str(user.user_id) + "-" + str(nurse_id)


# POST for image recognition
@app.route("/scan_check", methods=["POST"])
def scan_check():
    file = request.files["Medicineimage"]

    prediction_groups = pipeline.recognize([file])

    s = []
    for predictions in prediction_groups:
        for x in predictions:
            s.append(x[0])

    try:
        rxuid = requests.get(
            "https://rxnav.nlm.nih.gov/REST/rxcui.json?name=" + s[0] + "&search=1"
        ).json()["idGroup"]["rxnormId"][0]
        return jsonify(find_drugs(s, is_ignore_case=True)[0][0]["name"], rxuid)
    except:
        return "No drug found"


# POST for manual input
@app.route("/manual_check", methods=["POST"])
def manual_check():
    drug = []
    drug.append(request.args.get("drug"))

    try:
        rxuid = requests.get(
            "https://rxnav.nlm.nih.gov/REST/rxcui.json?name=" + drug[0] + "&search=1"
        ).json()["idGroup"]["rxnormId"][0]
        return jsonify(find_drugs(drug, is_ignore_case=True)[0][0]["name"], rxuid)
    except:
        return "No drug found"


# GET for compatibility check
@app.route("/check_compatibility", methods=["GET"])
def check_compatibility():
    drug_id = request.args.get("drug")
    userid = int(request.args.get("userid"))
    # get all the current prescriptions from the prescription table using the user id
    medicines = prescription.query.filter_by(user_id=userid).all()

    incompatible = []
    for medicine in medicines:
        description = {'Interaction': '', 'Risk': ''}
        if medicine.rxcuid == drug_id:
            incompatible.append("Same drug.")

        else:
            medicine_id = medicine.rxcuid
            url = (
                "https://rxnav.nlm.nih.gov/REST/interaction/list.json?rxcuis="
                + str(drug_id)
                + "+"
                + str(medicine_id)
            )
            compatibility_data = requests.get(url).json()

            if "fullInteractionTypeGroup" not in compatibility_data.keys():
                description["Interaction"] = "No interaction found."
                description["Risk"] = "None/Unknown"
            else:
                description["Interaction"] =  compatibility_data["fullInteractionTypeGroup"][0][
                    "fullInteractionType"
                ][0]["interactionPair"][0]["description"]
                if (
                    compatibility_data["fullInteractionTypeGroup"][0][
                        "fullInteractionType"
                    ][0]["interactionPair"][0]["severity"]
                    != "N/A"
                ):
                    description['Risk'] = (
                        compatibility_data["fullInteractionTypeGroup"][0][
                            "fullInteractionType"
                        ][0]["interactionPair"][0]["severity"]
                    )
                else:
                    description['Risk'] = "Mild/Moderate"

            incompatible.append(description)

    if len(incompatible) == 0:
        return "Something went wrong :("
    else:
        return jsonify(incompatible)


# POST for adding a prescription
@app.route("/add", methods=["POST"])
def add():
    drug = request.args.get("drug")
    userid = request.args.get("userid")
    nurseid = request.args.get("nurseid")
    rxcuid = request.args.get("rxcuid")
    description = request.args.get("description")
    power = request.args.get("power")
    days = request.args.get("days")
    time = request.args.get("time")
    expiry = datetime.strptime(request.args.get("expiry"), "%Y-%m-%d")
    prescription_ = prescription(
        user_id=userid,
        nurse_id=nurseid,
        rxcuid=rxcuid,
        drug_name=drug,
        drug_description=description,
        drug_power=power,
        drug_days=days,
        drug_time=time,
        expiry=expiry,
    )
    db.session.add(prescription_)
    db.session.commit()
    return "true"


# POST for removing a prescription
@app.route("/remove", methods=["POST"])
def remove():
    prescription_id = request.args.get("prescription_id")
    prescription_ = prescription.query.filter_by(
        prescription_id=prescription_id
    ).first()
    db.session.delete(prescription_)
    db.session.commit()
    return "true"


# POST for getting the prescriptions
@app.route("/get", methods=["GET"])
def get_prescriptions():
    userid = request.args.get("userid")
    prescriptions = prescription.query.filter_by(user_id=userid).all()
    # for each prescription, get the drug name, description, power, days, time, expiry, rxcuid and prescription id then return as json
    prescription_list = []
    for prescription_ in prescriptions:
        prescription_list.append(
            {
                "drug": prescription_.drug_name,
                "description": prescription_.drug_description,
                "power": prescription_.drug_power,
                "days": prescription_.drug_days,
                "time": prescription_.drug_time,
                "expiry": prescription_.expiry,
                "rxcuid": prescription_.rxcuid,
                "prescription_id": prescription_.prescription_id,
            }
        )
    return jsonify(prescription_list)


# POST for updating the prescriptions
@app.route("/update", methods=["POST"])
def update():
    prescription_id = request.args.get("prescription_id")
    drug = request.args.get("drug")
    description = request.args.get("description")
    power = request.args.get("power")
    days = request.args.get("days")
    time = request.args.get("time")
    expiry = request.args.get("expiry")
    rxcuid = request.args.get("rxcuid")
    prescription_ = prescription.query.filter_by(
        prescription_id=prescription_id
    ).first()
    prescription_.drug_name = drug
    prescription_.drug_description = description
    prescription_.drug_power = power
    prescription_.drug_days = days
    prescription_.drug_time = time
    prescription_.expiry = expiry
    prescription_.rxcuid = rxcuid
    db.session.commit()
    return "true"


# POST for getting user info
@app.route("/get_user_info", methods=["GET"])
def get_user_info():
    userid = request.args.get("userid")
    info = userinfo.query.filter_by(user_id=userid).first()
    #turn info into json object without jsonify
    toret = {
        "firstname": info.firstname,
        "lastname": info.lastname,
        "height": info.height,
        "weight": info.weight,
        "dateofbirth": info.dateofbirth,
    }
    return jsonify(toret)
        
app.run(debug=True)
