from flask import Blueprint,render_template, request, flash, redirect, url_for, make_response
from flask_login import login_user, current_user, login_required, logout_user
from flask_dance.contrib.facebook import make_facebook_blueprint, facebook
from . import db
from .model import *

auth = Blueprint('auth', __name__)

@auth.route("/register",methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        flash('already logged in','info')
        return redirect(url_for('auth.home'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('new_password')
        
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash('Email address already exists.', 'danger')
        else:
            # Create new user            
            new_user = User(email=email, password_hash=password)            
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! You can now login.', 'success')
            return redirect(url_for('auth.log_in')) 
    return render_template("register.html")

@auth.route("/log-in",methods=['GET','POST'])
def log_in():
    if current_user.is_authenticated:
        flash('already logged in!', 'info')
        return redirect(url_for('auth.home'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        existing_user = User.query.filter_by(email=email).first()

        if existing_user and existing_user.check_password(password):
            login_user(existing_user)
            flash('Login successful!', 'success')
            return redirect(url_for('auth.home'))
        elif not existing_user:
            flash('account does not exit, please create an account first','danger')
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
    return voidCache(render_template("log-in.html"))

from . import category
@auth.route("/")
def home():
    return voidCache(render_template("index.html",categories=category.categories,current_user=current_user))

#prevent browser caching login required page
def voidCache(page):
    response = make_response(page)
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.log_in'))

@auth.route('/forget-password', methods=['GET', 'POST'])
def reset_password():
    if current_user.is_authenticated:
        flash('already logged in','info')
        return redirect(url_for('auth.home'))  # Redirect if the user is already logged in

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Check if the email exists in the database
        user = User.query.filter_by(email=email).first()

        if user:
            # Ensure the new password is different from the old one
            if user.check_password(password):
                flash('New password cannot be the same as the old password.', 'danger')
            else:
                # Update the password
                user.set_password(password)                       
                db.session.commit()
                flash('Password updated successfully!', 'success')
                return redirect(url_for('auth.log_in'))
        else:
            flash('User account does not exist. Please check your email.', 'danger')

    return render_template('forget-password.html')

facebook_bp = make_facebook_blueprint(
    client_id = '874238507715111',
    client_secret = '3f631f69cb6d72cd2f1241017f9c31a8',
    redirect_to = 'facebook_login',
    scope=['email']
)

@facebook_bp.route('/facebook/login')
def facebook_login():    
    if not facebook.authorized:        
        return redirect(url_for('facebook.login')) 
    resp = facebook.get('/me?fields=id,name,email')    
    if resp.ok:
        user_info = resp.json()
        email = user_info['email']        

        # Check if user already exists
        user = User.query.filter_by(email=email).first()
        if not user:
            # Create a new user if not exists
            user = User(email=email)
            db.session.add(user)
            db.session.commit()

        login_user(user)
        flash('Login successful!', 'success')
        return redirect(url_for('auth.home'))
    else:
        flash('Failed to fetch user information from Facebook.', 'danger')
        return redirect(url_for('auth.log_in'))