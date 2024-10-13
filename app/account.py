from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from . import db
from .auth import voidCache
from .model import *
from .category import categories

account_bp = Blueprint('account_bp',__name__)

@account_bp.route("/account")
@login_required
def account():    
    response = voidCache(render_template("account.html",current_user=current_user))
    return response

@account_bp.route("/update_password", methods=['GET','POST'])
@login_required
def update_password():
    response = voidCache(render_template('account.html'))
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        password = request.form.get('new_password')        
        if not current_user.check_password(current_password):
            flash('You entered the wrong password.','danger')
            return redirect(url_for('account_bp.account'))
        else:
            if current_user.check_password(password):
                flash('New password cannot be the same as the old password.', 'danger')
                return redirect(url_for('account_bp.account'))
            else:
                # Update the password
                current_user.set_password(password)                       
                db.session.commit()
                flash('Password updated successfully!', 'success')
                return redirect(url_for('auth.logout'))
    return response

@account_bp.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    if current_user.is_authenticated:
        user_to_delete = User.query.get(current_user.id)        
        if user_to_delete:
            deletePhoto(current_user.id)
            db.session.delete(user_to_delete)
            db.session.commit()
            flash('Your account has been deleted successfully.', 'success')
        else:
            flash('User not found.', 'danger')
    else:
        flash('You need to be logged in to delete your account.', 'danger')

    return redirect(url_for('auth.home'))

@account_bp.route("/show_post", methods=['GET','POST'])
@login_required
def showPost():
    if current_user.is_authenticated:
        ads = Ad.query.filter(Ad.user_id == current_user.id) \
                       .order_by(Ad.post_time.desc()).all()
        if request.method == 'POST':
            sort = request.form.get('sort')
            search = request.form.get('search')
            category = request.form.get('category')
            subcategory = request.form.get('subcategory')
            ads = filterMyAd(ads,sort,search,category,subcategory)
        return voidCache(render_template('my_ads.html',ads=ads,categories=categories))
    else:
        flash('You need to log in to view your posted ads.', 'danger')
        return redirect('auth.login')

@account_bp.route("/delete_post/<ad_id>",methods=['POST'])
@login_required
def deletePost(ad_id):
    ad = Ad.query.filter_by(id=ad_id).first()    
    if current_user.is_authenticated:
        deleteAdPhoto(ad.photos)
        db.session.delete(ad)
        db.session.commit()
        if ad:
            flash('Your ad has been deleted successfully.', 'success')            
        else:
            flash('Ad not found.', 'danger')
        return redirect(url_for('account_bp.showPost'))
    else:
        flash('You need to be logged in to delete ad.', 'danger')
        return redirect('auth.log_in')
    
@account_bp.route("/edit_post/<ad_id>",methods=['POST','GET'])
@login_required
def editPost(ad_id):
    ad = Ad.query.filter_by(id=ad_id).first()
    category = ad.Ad_type
    subcategory = ad.subcategory
    from .postAd import post_ad
    if request.method == 'POST':
        post_ad(category,subcategory)        
    return voidCache(render_template('post_ad.html',ad=ad, category=category, subcategory=subcategory))

def filterMyAd(ads,sort,search,category,subcategory):
    if sort == 'newest':
        ads = sorted(ads, key=lambda ad: ad.post_time, reverse=True)
    else:
        ads = sorted(ads, key=lambda ad: ad.post_time)
    if category:
        ads = [ad for ad in ads if ad.Ad_type == category]
    if subcategory:
        ads = [ad for ad in ads if ad.subcategory == subcategory]
    if search:
        lower_case_term = search.lower()
        ads = [ad for ad in ads if (lower_case_term in ad.subject.lower() or lower_case_term in ad.city.lower() or
        lower_case_term in ad.state.lower() or lower_case_term in ad.zipcode or lower_case_term in ad.body.lower() or
        (ad.address and lower_case_term in ad.address.lower()) or (ad.contact_phone and lower_case_term in ad.contact_phone) or lower_case_term in ad.contact_email.lower()
        or (ad.Ad_type == 'For Sale' and ad.brand and lower_case_term in ad.brand.lower()) or (ad.Ad_type == 'For Sale ' and ad.make and lower_case_term in ad.make.lower()) or (ad.Ad_type == 'For Sale' and ad.model and lower_case_term in ad.model.lower()) or
        (ad.Ad_type == 'For Sale' and ad.condition and lower_case_term in ad.condition) or (ad.Ad_type == 'Job' and ad.industry and lower_case_term in ad.industry.lower()))]
    return ads

from os import path, remove, getcwd
from config import Config
def deletePhoto(userId):
    ads = Ad.query.filter_by(user_id=userId).all()
    for ad in ads:
        photos = ad.photos
        for photo in photos:
            photo_path = path.join(getcwd(), 'app', Config.UPLOAD_FOLDER, photo.filename)
            if path.exists(photo_path):
                remove(photo_path)  # Remove the photo file from the filesystem
            db.session.delete(photo)            
            db.session.commit()

def deleteAdPhoto(photos):
    if photos:
        for photo in photos:
            photo_path = path.join(getcwd(), 'app', Config.UPLOAD_FOLDER, photo.filename)
            if path.exists(photo_path):
                remove(photo_path)
            db.session.delete(photo)            
            db.session.commit()