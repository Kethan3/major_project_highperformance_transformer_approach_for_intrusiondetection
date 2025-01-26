import numpy as np
from flask import Flask, request, jsonify, render_template, abort
import joblib
import sqlite3

import numpy as np
import pandas as pd
from sklearn import metrics
import warnings
import pickle
import pandas as pd
import numpy as np
import pickle
import sqlite3
import random
import json

import smtplib
from email.message import EmailMessage
from datetime import datetime

warnings.filterwarnings('ignore')


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/about")
def about():
    return render_template("about.html")


@app.route('/home1')
def home1():
    return render_template('home1.html')


@app.route('/logon')
def logon():
    return render_template('signup.html')


@app.route('/login')
def login():
    return render_template('signin.html')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route("/signup")
def signup():
    global otp, username, name, email, number, password
    username = request.args.get('user', '')
    name = request.args.get('name', '')
    email = request.args.get('email', '')
    number = request.args.get('mobile', '')
    password = request.args.get('password', '')
    otp = random.randint(1000, 5000)
    print(otp)
    msg = EmailMessage()
    msg.set_content("Your OTP is : " + str(otp))
    msg['Subject'] = 'OTP'
    msg['From'] = "evotingotp4@gmail.com"
    msg['To'] = email

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("evotingotp4@gmail.com", "xowpojqyiygprhgr")
    s.send_message(msg)
    s.quit()
    return render_template("val.html")


@app.route('/predict_lo', methods=['POST'])
def predict_lo():
    global otp, username, name, email, number, password
    if request.method == 'POST':
        message = request.form['message']
        print(message)
        if int(message) == otp:
            print("TRUE")
            con = sqlite3.connect('signup.db')
            cur = con.cursor()
            cur.execute("insert into `info` (`user`,`email`, `password`,`mobile`,`name`) VALUES (?, ?, ?, ?, ?)", (username, email, password, number, name))
            con.commit()
            con.close()
            return render_template("signin.html")
    return render_template("signup.html")


@app.route("/signin")
def signin():

    mail1 = request.args.get('user', '')
    password1 = request.args.get('password', '')
    con = sqlite3.connect('signup.db')
    cur = con.cursor()
    cur.execute("select `user`, `password` from info where `user` = ? AND `password` = ?", (mail1, password1,))
    data = cur.fetchone()

    if data == None:
        return render_template("signin.html")

    elif mail1 == str(data[0]) and password1 == str(data[1]):
        return render_template("home.html")
    else:
        return render_template("signin.html")


@app.route("/add", methods=['POST'])
def add_packet():
    request_data = request.get_json()
    with open("./test/output2.txt", "a") as f:
        f.write(json.dumps(request_data['data']) + "\n")
    return render_template("CIC-IDS-2017.html")


@app.route("/notebook1")
def notebook1():
    return render_template("CIC-IDS-2017.html")


@app.route("/notebook2")
def notebook2():
    return render_template("CIC-IDS-2019.html")


@app.route('/predict', methods=['POST'])
def predict():
    int_features = [float(x) for x in request.form.values()]
    print(int_features, len(int_features))
    final4 = [np.array(int_features)]
    model = joblib.load('model_cicids2017.sav')

    predict = model.predict(final4)

    return render_template('prediction.html', prediction=predict)


@app.route('/predict1', methods=['POST'])
def predict1():
    int_features = [float(x) for x in request.form.values()]
    print(int_features, len(int_features))
    final4 = [np.array(int_features)]
    model = joblib.load('model_cicids2019.sav')

    predict = model.predict(final4)

    return render_template('prediction1.html', prediction=predict)


def readFile(year):
    with open("./test/output2.txt", 'r') as f:
        lines = f.readlines()
    lines = lines[::-1]
    for line in lines:
        try:
            data = json.loads(line)
            if data[0] == year:
                return data
        except Exception as e:
            pass
    return None


@app.route('/populate2017')
def populate2017():
    data = readFile("2017")
    if data == None:
        abort(400)
    return jsonify({
        'data': data[1],
    })


@app.route('/populate2019')
def populate2019():
    data = readFile("2019")
    if data == None:
        abort(400)
    return jsonify({
        'data': data[1],
    })


if __name__ == "__main__":
    app.run(host="192.168.1.3", debug=False)

# 192.168.223.82