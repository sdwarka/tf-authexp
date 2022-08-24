from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from .models import User
from app import db
from app import login_manager
from . import auth

# route for displaying the login form
@auth.route('/login')
def login():
    return render_template('login.html')

# route that processes POSTed login data
@auth.route('/login', methods=['POST'])
def login_post():
    # first, get the POSTed data
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    # fetch the user from the database
    print(f'fetching {email} from db')
    user = User.query.filter_by(email=email).first()

    # check if user exists and passwords match
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again')
        return redirect(url_for('auth.login'))

    # login successful, show the profile page
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))

# route for displaying the signup form
@auth.route('/signup')
def signup():
    return render_template('signup.html')

# route that processes POSTed signup data
@auth.route('/signup', methods=['POST'])
def signup_post():
    # TODO: code to validate and add user to database

    # first, get the POSTed data
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    # check if the user already exists
    user = User.query.filter_by(email=email).first()

    # if user exists, redirect them to the signup page
    # so that they can try signing up with a different
    # email ID
    if user:
        flash(f'Email ID already exists')
        return redirect(url_for('auth.signup'))

    # create a new user with the form data
    # but first hash the password
    hash_pass =  generate_password_hash(password, method='sha256')
    new_user = User(email=email, name=name, password=hash_pass)

    # add the user to the db
    db.session.add(new_user)
    db.session.commit()

    flash(f'Signup successful')
    return redirect(url_for('auth.login'))

# route for logout
@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@login_manager.user_loader
def load_user(user_id):
    # since user_id is the primary key of the user table,
    # use it in the query for the user
    return User.query.get(int(user_id))


