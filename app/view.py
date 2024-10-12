from flask import render_template,Blueprint, request
from .model import *

view = Blueprint('view',__name__)


@view.route("/view/<category>", methods=['GET', 'POST'])
@view.route("/view/<category>/<subcategory>", methods=['GET', 'POST'])
def view_category(category, subcategory=None):    
    categorySize = len(Ad.query.filter(Ad.Ad_type == category).all()) 
    if request.method == 'POST':
        keyword = request.form.get('search')
        if keyword:
            categorySize = len(Ad.query.filter(Ad.Ad_type == category).all())
            if subcategory:
                ads = Ad.query.filter(Ad.Ad_type == category, Ad.subcategory == subcategory).all()
            else:
                ads = Ad.query.filter(Ad.Ad_type == category).all()                
            ads = searchAds(ads,keyword)            
            ads, page, total_page = pagination(ads)
            return render_template("view.html",category=category, subcategory=subcategory, ads=ads, categorySize=categorySize, page=page,total_page=total_page)
        display_type = request.form.get('view')
        sort = request.form.get('sort')
        has_image = request.form.get('has_image')
        city = request.form.get('city')
        state = request.form.get('state')
        zipcode = request.form.get('zipcode')
        min_rent = request.form.get('min_rent')
        max_rent = request.form.get('max_rent')
        min_size = request.form.get('min_size')
        max_size = request.form.get('max_size')
        min_bedroom = request.form.get('min_bedroom')
        max_bedroom = request.form.get('max_bedroom')
        min_bathroom = request.form.get('min_bathroom')
        max_bathroom = request.form.get('max_bathroom')
        type = request.form.get('type')
        min_price = request.form.get('min_price')
        max_price = request.form.get('max_price')
        make = request.form.get('make')
        model = request.form.get('model')
        min_mileage = request.form.get('min_mileage')
        max_mileage = request.form.get('max_mileage')
        condition = request.form.get('condition')
        industry = request.form.get('industry')
        min_compensation = request.form.get('min_compensation')
        max_compensation = request.form.get('max_compensation')        
        if subcategory:
            ads = Ad.query.filter(Ad.Ad_type == category, Ad.subcategory == subcategory).all()
        else:
            ads = Ad.query.filter(Ad.Ad_type == category).all()        
        ads = filterAd(ads,sort, has_image, city, state, zipcode, min_rent, max_rent, min_size
        , max_size, min_bedroom, max_bedroom, min_bathroom, max_bathroom, type
        , min_price, max_price, make,model, min_mileage, max_mileage, condition, industry, min_compensation,max_compensation)        
        ads, page, total_page = pagination(ads)
        return render_template('view.html',category=category, subcategory=subcategory, display_type=display_type, ads=ads, categorySize=categorySize, page=page, total_page=total_page)
    if subcategory:
        ads = Ad.query.filter(Ad.Ad_type == category, Ad.subcategory == subcategory) \
                       .order_by(Ad.post_time.desc()).all()
    else:
        ads = Ad.query.filter(Ad.Ad_type == category) \
                       .order_by(Ad.post_time.desc()).all()
    ads,page,total_page = pagination(ads)
    return render_template("view.html",category=category, subcategory=subcategory, ads=ads, categorySize=categorySize,page=page,total_page=total_page)

def pagination(ads):
    if not ads:
        return ads, 1, 1
    page = request.args.get('page', default=1, type=int)
    ads_per_page = 100  # Set how many ads to display per page
    total_ads = len(ads)
    # Fetch the ads for the current page
    ads = get_ads_for_page(ads, page, ads_per_page)  #return ads based on page
    

    # Calculate total pages
    total_page = (total_ads + ads_per_page - 1) // ads_per_page
    return ads, page, total_page

def get_ads_for_page(ads, page, ads_per_page):
    """
    Function to get ads for a specific page from the adList.
    
    Parameters:
        adList (list): List of ads (assumed to be a list of ad objects or dictionaries).
        page (int): The page number to get ads for (defaults to 1).
        per_page (int): The number of ads per page (defaults to 10).
    
    Returns:
        list: A sublist of ads for the specified page.
    """
    if len(ads) == 1:
        return ads
    start = (page - 1) * ads_per_page  # Calculate the starting index
    end = start + ads_per_page  # Calculate the ending index
    
    # Return the slice of adList corresponding to the requested page
    return ads[start:end]

def searchAds(ads,search):
    if search:
        lower_case_term = search.lower()
        ads = [ad for ad in ads if (lower_case_term in ad.subject.lower() or lower_case_term in ad.city.lower() or
        lower_case_term in ad.state.lower() or lower_case_term in ad.zipcode or lower_case_term in ad.body.lower() or
        (ad.address and lower_case_term in ad.address.lower()) or (ad.contact_phone and lower_case_term in ad.contact_phone) or lower_case_term in ad.contact_email.lower()
        or (ad.Ad_type == 'For Sale' and ad.brand and lower_case_term in ad.brand.lower()) or (ad.Ad_type == 'For Sale ' and ad.make and lower_case_term in ad.make.lower()) or (ad.Ad_type == 'For Sale' and ad.model and lower_case_term in ad.model.lower()) or
        (ad.Ad_type == 'For Sale' and ad.condition and lower_case_term in ad.condition) or (ad.Ad_type == 'Job' and ad.industry and lower_case_term in ad.industry.lower()))]
    return ads

def filterAd(ads, sort, has_image, city, state, zipcode, min_rent, max_rent, min_size
        , max_size, min_bedroom, max_bedroom, min_bathroom, max_bathroom, type
        , min_price, max_price, make,model, min_mileage, max_mileage, condition, industry, min_compensation,max_compensation):    
    if has_image:
        ads = [ad for ad in ads if ad.photos]
    if sort == 'newest':
        ads = sorted(ads, key=lambda ad: ad.post_time, reverse=True)
    else:
        ads = sorted(ads, key=lambda ad: ad.post_time)    
    if city:
        ads = [ad for ad in ads if ad.city.lower() == city.lower()]    
    if state:
        ads = [ad for ad in ads if ad.state.lower() == state.lower()]
    if zipcode:
        ads = [ad for ad in ads if ad.zipcode == zipcode]
    if min_rent:
        min_rent = convert_str_to_float(min_rent)
        ads = [ad for ad in ads if ad.rent and ad.rent >= min_rent]        
    if max_rent:
        max_rent = convert_str_to_float(max_rent)
        ads = [ad for ad in ads if ad.rent and ad.rent <= max_rent]
    if min_size:
        min_size = convert_str_to_float(min_size)
        ads = [ad for ad in ads if ad.size and ad.size >= min_size]        
    if max_size:
        max_size = convert_str_to_float(max_size)
        ads = [ad for ad in ads if ad.size and ad.size <= max_size]
    if min_bedroom:
        min_bedroom = convert_str_to_float(min_bedroom)
        ads = [ad for ad in ads if ad.bedroom and ad.bedroom >= min_bedroom]
    if max_bedroom:
        max_bedroom = convert_str_to_float(max_bedroom)
        ads = [ad for ad in ads if ad.bedroom and ad.bedroom <= max_bedroom]
    if min_bathroom:
        min_bathroom = convert_str_to_float(min_bathroom)
        ads = [ad for ad in ads if ad.bathroom and ad.bathroom >= min_bathroom]
    if max_bathroom:
        max_bathroom = convert_str_to_float(max_bathroom)
        ads = [ad for ad in ads if ad.bathroom and ad.bathroom <= max_bathroom]
    if type:
        ads = [ad for ad in ads if ad.type and ad.type == type]
    if min_price:
        min_price = convert_str_to_float(min_price)
        ads = [ad for ad in ads if ad.price and ad.price >= min_price]
    if max_price:
        max_price = convert_str_to_float(max_price)
        ads = [ad for ad in ads if ad.price and ad.price <= max_price]
    if make:
        ads = [ad for ad in ads if ad.make and ad.make.lower() == make.lower()]
    if model:
        ads = [ad for ad in ads if ad.model and ad.model.lower() == model.lower()]
    if min_mileage:
        min_mileage = convert_str_to_float(min_mileage)
        ads = [ad for ad in ads if ad.mileage and ad.mileage >= min_mileage]
    if max_mileage:
        max_mileage = convert_str_to_float(max_mileage)
        ads = [ad for ad in ads if ad.mileage and ad.mileage <= max_mileage]
    if condition:
        ads = [ad for ad in ads if ad.condition and ad.condition == condition]
    if industry:
        ads = [ad for ad in ads if ad.industry and ad.industry.lower() == industry.lower()]
    if min_compensation:
        min_compensation = convert_str_to_float(min_compensation)
        ads = [ad for ad in ads if ad.compensation and ad.compensation >= min_compensation]
    if max_compensation:
        max_compensation = convert_str_to_float(max_compensation)
        ads = [ad for ad in ads if ad.compensation and ad.compensation <= max_compensation]
    
    return ads

@view.route("/viewAd/<subject>/<id>")
def viewAd(subject,id):
    ad = Ad.query.filter(Ad.id == id).first()
    user = User.query.filter(User.id == ad.user_id).first()    
    return render_template("view_ad.html", ad=ad, user=user)

def convert_str_to_float(s):
    try:
        return float(s)
    except ValueError:
        return None 