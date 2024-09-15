"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secretkey"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


connect_db(app)

@app.route('/')
def home_page():
    """redirect to list of users (for now)"""
    return redirect('/users')

@app.route('/users')
def list_users():
    """list all userrs"""
    users = User.query.all()
    return render_template("users.html", users=users)

@app.route('/users/new')
def add_user():
    """show form to add a new user"""
    return render_template('new_user.html')

@app.route("/users/new", methods=["POST"])
def handle_form_submission():
    """process form data to add new user to databse"""
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    new_user  = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')
