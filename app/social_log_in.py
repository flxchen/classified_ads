from flask_dance.contrib.facebook import make_facebook_blueprint, facebook
from flask_login import login_user
from flask import redirect, url_for, flash
from .model import User
from config import Config
from . import db

facebook_bp = make_facebook_blueprint(
    client_id = Config.FACEBOOK_CLIENT_ID,
    client_secret = Config.FACEBOOK_CLIENT_SECRET,
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