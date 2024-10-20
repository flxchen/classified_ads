from app import create_app
from flask_sitemap import Sitemap

app = create_app()
ext = Sitemap(app=app)

@ext.register_generator
def auth_pages():
    yield 'auth.register', {}
    yield 'auth.log_in', {}
    yield 'auth.home', {}
    yield 'auth.reset_password', {}
    yield 'auth.privacy', {}

@ext.register_generator
def aux_pages():
    yield 'aux.about', {}
    yield 'aux.contact', {}
    yield 'aux.payment', {}
    yield 'aux.about', {}

from app.category import categories
@ext.register_generator
def view_pages():
    for category, subcategories in categories.items():
        yield 'view.view_category',{'category':category}
        for subcategory in subcategories:
            yield 'view.view_category',{'category':category, 'subcategory':subcategory}

if __name__ == "__main__":
    host="192.168.50.151"
    port=5000
    debug = True
    app.run(host,port,debug)