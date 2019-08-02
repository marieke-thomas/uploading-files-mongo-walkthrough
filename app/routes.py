# Uploading/Downloading Files Walkthrough
import os
from app import app
from flask import render_template, request, redirect, session, url_for

app.secret_key = b'y\xd7;\xc4\xd5\xdf\x1a\xc2\xb4\x91=q\x95\xdf\xa8\xba'

from flask_pymongo import PyMongo

# name of database
app.config['MONGO_DBNAME'] = 'database' 

# URI of database
# app.config['MONGO_URI'] = INSERT MONGO URI HERE (change username, password, and change "test" to database name)


mongo = PyMongo(app)


# INDEX

@app.route('/')
@app.route('/index')

def index():
    # connect to the database
    collection = mongo.db.events
    # pull data from database
    events = collection.find({}).sort("date", -1)
    # use data
    return render_template('index.html', events = events)


# CONNECT TO DB, ADD DATA

@app.route('/add')

def add():
    # connect to the database
    events = mongo.db.events
    # insert new data
    events.insert({"event":"Marieke's Birthday", "date":"2019-02-27"})
    # return a message to the user
    return "Event added"

@app.route('/events/new', methods=["GET","POST"])
def events_new():
    userdata = dict(request.form)
    print(userdata)
    events = mongo.db.events
    events.insert(userdata)
    return redirect('/')

@app.route('/name/<name>')
def name(name):
    # connect to the database
    collection = mongo.db.events
    # pull data from database
    events = collection.find({"user_name":name}).sort("date", -1)
    # use data
    return render_template('person.html', events = events)

# SIGN-UP:
@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method =="POST":
        # take in the info they gave us, check if username is taken, if username is available put into a database of users
        users = mongo.db.users
        existing_user = users.find_one({"username":request.form['username']})
        if existing_user is None:
            users.insert({"username":request.form['username'],"password":request.form['password']})
            return "Username successful"
        else:
            return "That username is taken. Try logging in, or try a different usename"
    else:
        return render_template('signup.html')

#Log In:
@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    # use the username to find the account
    existing_user = users.find_one({"username":request.form['username']})
    if existing_user:
        # check if the password is right
        if existing_user['password'] == request.form['password'] :
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        else:
            return "Your password doesn't match your username."
    else:
        return "There is no user with that username. Try making an account."
  
#   LOG OUT
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
