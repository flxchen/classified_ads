from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime
from flask_login import login_required, current_user
from . import category, db
from .auth import voidCache
from .model import *

postAd = Blueprint('postAd',__name__)

@postAd.route("/choose-category")
@login_required
def choose():
    response = voidCache(render_template("choose-category.html",categories=category.categories))
    return response

@postAd.route("/post-ads/<category>/<subcategory>", methods=['GET','POST'])
@login_required
def post_ad(category,subcategory):
    response = voidCache(render_template("post_ad.html",category=category,subcategory=subcategory))
    if request.method == 'POST':
        subject = request.form.get('subject')
        city = request.form.get('city')
        state = request.form.get('state')
        address = request.form.get('address')
        zipCode = request.form.get('zip-code')
        body = request.form.get('body')
        photos = request.files.getlist('photo')
        phone = request.form.get('phone')
        for photo in photos:
            print(photo)
        if not address:
            address = None
        if not phone:
            phone = None
        email = request.form.get('email')
        postTime = datetime.now()        
        bedroom = request.form.get('bedroom')
        if not bedroom:
            bedroom = None
        bathroom = request.form.get('bathroom')
        if not bathroom:
            bathroom = None
        size = request.form.get('size')
        if not size:
            size = None
        type = request.form.get('Options')
        if not type:
            type = None
        rent = request.form.get('rent')
        if not rent:
            rent = None
        period = request.form.get('period')
        if not period:
            period = None
        price = request.form.get('price')
        if not price:
            price = None
        mileage = request.form.get('mileage')
        if not mileage:
            mileage = None
        brand = request.form.get('brand')
        if not brand:
            brand = None
        make = request.form.get('make')
        if not make:
            make = None
        model = request.form.get('model')
        if not model:
            model = None
        condition = request.form.get('condition')
        if not condition:
            condition = None
        industry = request.form.get('industry')
        if not industry:
            industry = None
        compensation = request.form.get('compensation')
        if not compensation:
            compensation = None
        userId = current_user.id
        if not userId:
            userId = None        
        
        if category == 'Housing':
            housingAd = HousingAd(subject=subject, city=city, state=state, address=address,
            zipcode=zipCode, body=body, contact_phone=phone,
            contact_email=email, post_time=postTime,rent=rent, rent_period=period, 
            type=type, bedroom=bedroom, bathroom = bathroom, size = size, 
            Ad_type=category, user_id=userId, subcategory=subcategory)
            db.session.add(housingAd)
            db.session.commit()
            ad_id=housingAd.id

        if category == 'For Sale':
            forSaleAd = ForSaleAd(subject=subject, city=city, state=state, address=address,
            zipcode=zipCode, body=body, contact_phone=phone,
            contact_email=email, post_time=postTime,price=price, mileage=mileage, make=make, brand=brand,
            model=model, condition = condition, Ad_type=category, user_id=userId, subcategory=subcategory)
            db.session.add(forSaleAd)
            db.session.commit()
            ad_id=forSaleAd.id
            
        if category == 'Jobs':
            jobAd = JobAd(subject=subject, city=city, state=state, address=address,
            zipcode=zipCode, body=body, contact_phone=phone,
            contact_email=email, post_time=postTime,industry=industry, compensation=compensation, 
            Ad_type=category, user_id=userId, subcategory=subcategory)
            db.session.add(jobAd)
            db.session.commit()
            ad_id=jobAd.id
        
        createPhoto(photos,ad_id)
        flash('post ad successfully!','success')
        return redirect(url_for('aux.payment'))
    return response

from flask import send_from_directory
@postAd.route('/app/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(Config.UPLOAD_FOLDER,filename)

from os import path, makedirs, getcwd
from config import Config
#create folder to store user uploaded photos
def createPhoto(photos,ad_id):
    uploads_folder = path.join(getcwd(),'app',Config.UPLOAD_FOLDER)
    if not path.exists(uploads_folder):
        makedirs(uploads_folder)
    if photos:
        for photo in photos:
            filename = photo.filename
            if photo and filename:
                    # Save the file to the upload folder
                    photo_url = path.join(uploads_folder, photo.filename)                    
                    photo.save(photo_url)
                    new_photo = Photo(filename = filename,ad_id=ad_id)
                    db.session.add(new_photo)
                    db.session.commit()

def photos_dict_to_list(photos_dict):
    return list(photos_dict.values())