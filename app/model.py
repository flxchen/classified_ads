from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash

#represents a registered user
class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)    
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    housing_ads = db.relationship('HousingAd',cascade='all, delete-orphan')
    for_sale_ads = db.relationship('ForSaleAd',cascade='all, delete-orphan')
    job_ads = db.relationship('JobAd',cascade='all, delete-orphan')
    payments = db.relationship('Payment',cascade='all, delete-orphan')
    def set_password(self, password):
        self.password_hash = generate_password_hash(password,'pbkdf2')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

#base ad with common fields
class Ad(db.Model):
    __tablename__ = 'ad'    
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    zipcode = db.Column(db.String(5), nullable=False)
    body = db.Column(db.Text, nullable=False)
    address = db.Column(db.String(100))
    contact_phone = db.Column(db.String(13))
    contact_email = db.Column(db.String(50), nullable=False)
    post_time = db.Column(db.DateTime,nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id',onupdate='CASCADE',ondelete='CASCADE'), nullable=False)    
    Ad_type = db.Column(db.String(50), nullable=False)
    subcategory = db.Column(db.String(50), nullable=False)
    photos = db.relationship('Photo',cascade='all, delete-orphan')
    __mapper_args__ = {
        'polymorphic_identity': 'ad',
        "polymorphic_on": Ad_type
    }

class HousingAd(Ad):
    __tablename__ = 'housing_ad'
    id = db.Column(db.Integer, db.ForeignKey('ad.id',onupdate='CASCADE',ondelete='CASCADE'), primary_key=True)
    bedroom = db.Column(db.Integer)
    bathroom = db.Column(db.Integer)
    size = db.Column(db.Float)
    rent = db.Column(db.Float)
    rent_period = db.Column(db.Enum('day', 'week', 'month'))    
    type = db.Column(db.Enum('apartment', 'house', 'condo', 'townhouse', 'other'))
    __mapper_args__ = {
        'polymorphic_identity': 'Housing',
    }

class ForSaleAd(Ad):
    __tablename__ = 'for_sale_ad'
    id = db.Column(db.Integer, db.ForeignKey('ad.id',onupdate='CASCADE',ondelete='CASCADE'), primary_key=True)
    price = db.Column(db.Float)
    mileage = db.Column(db.Float)
    brand = db.Column(db.String(50))
    make = db.Column(db.String(50))
    model = db.Column(db.String(50))
    condition = db.Column(db.Enum('new','used','deficiency'))
    __mapper_args__ = {
        'polymorphic_identity': 'For Sale',
    }

class JobAd(Ad):
    __tablename__ = 'job_ad'
    id = db.Column(db.Integer, db.ForeignKey('ad.id',onupdate='CASCADE',ondelete='CASCADE'), primary_key=True)
    industry = db.Column(db.String(50))
    compensation = db.Column(db.Float)
    __mapper_args__ = {
        'polymorphic_identity': 'Jobs',
    }

#user uploaded ads photos
class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    ad_id = db.Column(db.Integer, db.ForeignKey('ad.id',ondelete='CASCADE',onupdate='CASCADE'), nullable=False)
    
class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    card_number = db.Column(db.String(16), nullable=False)
    expiration_date = db.Column(db.String(5), nullable=False)#MM/YY
    cvv = db.Column(db.String(3), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id',ondelete='CASCADE',onupdate='CASCADE'), nullable=False)
