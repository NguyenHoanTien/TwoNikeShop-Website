import os
import urllib
import datetime
import logging

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext import db
from google.appengine.api import images

import jinja2
import webapp2

class Categories(ndb.Model):
    name = ndb.StringProperty()

class Product(ndb.Model):
    name = ndb.StringProperty()
    style = ndb.StringProperty()
    price = ndb.StringProperty()
    color = ndb.StringProperty()
    type = ndb.StringProperty()
    category = ndb.KeyProperty(kind=Categories)
    image = ndb.StringProperty()
    image1 = ndb.StringProperty()
    image2 = ndb.StringProperty()
    image3 = ndb.StringProperty()
    image4 = ndb.StringProperty()
    image5 = ndb.StringProperty()
    description = ndb.StringProperty(indexed =False)

class Login(ndb.Model):
    username = ndb.StringProperty()
    password = ndb.StringProperty()

#===============================================        ================================================================

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])

#===============================================        ================================================================

class MainPage(webapp2.RequestHandler):

    def get(self):

        category_query = Categories.query()
        categories = category_query.fetch()

        template_values = {
            'categories': categories,
        }

        template = JINJA_ENVIRONMENT.get_template('homepage.html')
        self.response.write(template.render(template_values))

#===============================================        ================================================================
class LoginPage(webapp2.RequestHandler):

    def get(self):

        category_query = Categories.query()
        categories = category_query.fetch()

        template_values = {
            'categories': categories,
        }

        template = JINJA_ENVIRONMENT.get_template('login.html')
        self.response.write(template.render(template_values))

    def post(self):
        login = Login()
        login.username = self.request.get("username")
        login.password = self.request.get("password")
        login.put()
        if login.username == "admin" and login.password == "ad123":
            self.redirect('/adminview')
        else:
            self.redirect('/login')

#===============================================        ================================================================
class RegisterPage(webapp2.RequestHandler):

    def get(self):

        category_query = Categories.query()
        categories = category_query.fetch()

        template_values = {
            'categories': categories,
        }

        template = JINJA_ENVIRONMENT.get_template('register.html')
        self.response.write(template.render(template_values))

#===============================================        ================================================================
class ContactPage(webapp2.RequestHandler):

    def get(self):

        category_query = Categories.query()
        categories = category_query.fetch()

        template_values = {
            'categories': categories,
        }

        template = JINJA_ENVIRONMENT.get_template('contact.html')
        self.response.write(template.render(template_values))

#===============================================        ================================================================
class TermPage(webapp2.RequestHandler):

    def get(self):

        category_query = Categories.query()
        categories = category_query.fetch()

        template_values = {
            'categories': categories,
        }

        template = JINJA_ENVIRONMENT.get_template('term.html')
        self.response.write(template.render(template_values))

#===============================================        ================================================================
class PrivacyPage(webapp2.RequestHandler):

    def get(self):

        category_query = Categories.query()
        categories = category_query.fetch()

        template_values = {
            'categories': categories,
        }

        template = JINJA_ENVIRONMENT.get_template('privacy.html')
        self.response.write(template.render(template_values))
#===============================================        ================================================================
class ProductAdd(webapp2.RequestHandler):
    def get(self):

        # get category
        category_query = Categories.query()
        categories = category_query.fetch()

        #get product
        product_query = Product.query()
        products = product_query.fetch()

        template_values = {
            'categories': categories,
            ' products': products,
            }

        template = JINJA_ENVIRONMENT.get_template('Addproduct.html')
        self.response.write(template.render(template_values))

    def post(self):
        # find category and set key
        category_name = self.request.get('category')
        category = Categories.query(Categories.name == category_name).get()

        product = Product()
        product.category = category.key
        product.name = self.request.get('name')
        product.style = self.request.get('style')
        product.color = self.request.get('color')
        product.price = self.request.get('price')
        product.type = self.request.get('type')
        product.image = self.request.get('image')
        product.image1 = self.request.get('image1')
        product.image2 = self.request.get('image2')
        product.image3 = self.request.get('image3')
        product.image4 = self.request.get('image4')
        product.image5 = self.request.get('image5')
        product.description = self.request.get('description')

        # store the data
        product.put()
        self.redirect('/adminview')

#===============================================        ================================================================
class AddCategory(webapp2.RequestHandler):
    def get(self):

        category_query = Categories.query()
        categories = category_query.fetch()

        template_values = {
            'categories': categories
        }

        template = JINJA_ENVIRONMENT.get_template('addcategory.html')
        self.response.write(template.render(template_values))

    def post(self):
        name = self.request.get('category')
        category_query = Categories.query()
        categories = category_query.fetch()
        store_flag = True
        for category1 in categories:
            if category1.name.lower() == name.lower():
                store_flag = False
        if store_flag:
            category = Categories()
            category.name = name
            category.put()
        self.redirect('/adminview')

#===============================================        ================================================================
class DeleteCategory(webapp2.RequestHandler):
    def get(self, id ):

        category = Categories.get_by_id(int(id))
        product = Product.get_by_id(int(id))

        category_query = Categories.query()
        categories = category_query.fetch()

        #get product
        product_query = Product.query()
        products = product_query.fetch()

        template_values = {
            'category': category,
            'product':product,
            'products':products,
            'categories': categories,
        }

        template = JINJA_ENVIRONMENT.get_template('deletecategory.html')
        self.response.write(template.render(template_values))

    def post(self, id):
        category = Categories.get_by_id(int(id))
        product_query = Product.query()
        products = product_query.fetch()

        for product in products:
            if product.category == category.key:
                product.key.delete()

        category.key.delete()
        self.redirect('/addcategory')

#===============================================        ================================================================
class EditCategory(webapp2.RequestHandler):
    def get(self, id ):

        category = Categories.get_by_id(int(id))

        category_query = Categories.query()
        categories = category_query.fetch()

        template_values = {
            'category': category,
            'categories': categories,
        }

        template = JINJA_ENVIRONMENT.get_template('editcategory.html')
        self.response.write(template.render(template_values))

    def post(self, id):
        name = self.request.get('category')
        category_query = Categories.query()
        categories = category_query.fetch()
        store_flag = True
        for category1 in categories:
            if category1.name.lower() == name.lower():
                store_flag = False

        if store_flag:
            category = Categories.get_by_id(int(id))
            category.name = name
            category.put()
        self.redirect('/addcategory')

#===============================================        ================================================================
class Category(webapp2.RequestHandler):
    def get(self, id ):

        category = Categories.get_by_id(int(id))

        category_query = Categories.query()
        categories = category_query.fetch()

        #get product
        product_query = Product.query()
        products = product_query.fetch()


        template_values = {
            'category': category,
            'products': products,
            'categories': categories,
        }

        template = JINJA_ENVIRONMENT.get_template('category.html')
        self.response.write(template.render(template_values))

#===============================================        ================================================================
class ProductDelete(webapp2.RequestHandler):
    def get(self, id):

        product = Product.get_by_id(int(id))

        template_values = {'product': product}
        template = JINJA_ENVIRONMENT.get_template('Deleteproduct.html')
        self.response.write(template.render(template_values))

    def post(self, id):
        product = Product.get_by_id(int(id))
        product.key.delete()
        self.redirect('/productDisplay')

#===============================================        ================================================================
class DetailPage(webapp2.RequestHandler):
    def get(self,id):


        category_query = Categories.query()
        categories = category_query.fetch()

        product = Product.get_by_id(int(id))

        template_values = {
            'product': product,
            'categories': categories,
        }
        template = JINJA_ENVIRONMENT.get_template('productDetail.html')
        self.response.write(template.render(template_values))

#===============================================        ================================================================
class ProductEdit(webapp2.RequestHandler):
    def get(self, id):
        template = JINJA_ENVIRONMENT.get_template('Editproduct.html')

        category_query = Categories.query()
        categories = category_query.fetch()

        product = Product.get_by_id(int(id))

        template_values = {'product': product, 'categories': categories,}
        self.response.write(template.render(template_values))

    def post(self, id):
        # find category and set key
        category_name = self.request.get('category')
        category = Categories.query(Categories.name == category_name).get()

        product = Product.get_by_id(int(id))

        product.category = category.key
        product.name = self.request.get('name')
        product.style = self.request.get('style')
        product.color = self.request.get('color')
        product.price = self.request.get('price')
        product.type = self.request.get('type')
        product.image = self.request.get('image')
        product.image1 = self.request.get('image1')
        product.image2 = self.request.get('image2')
        product.image3 = self.request.get('image3')
        product.image4 = self.request.get('image4')
        product.image5 = self.request.get('image5')
        product.description = self.request.get('description')
        product.put()

        self.redirect('/productDisplay')


#===============================================        ================================================================
class AdminView(webapp2.RequestHandler):
    def get(self):
        category_query = Categories.query()
        categories = category_query.fetch()

        #get product
        product_query = Product.query()
        products = product_query.fetch()

        template_values = {
            'categories': categories,
            'products':products,
        }

        template = JINJA_ENVIRONMENT.get_template('adminview.html')
        self.response.write(template.render(template_values))



#===============================================        ================================================================
class ProductDisplay (webapp2.RequestHandler):
    def get(self):
        category_query = Categories.query()
        categories = category_query.fetch()

        #get product
        product_query = Product.query()
        products = product_query.fetch()

        template_values = {
            'categories': categories,
            'products':products,
        }

        template = JINJA_ENVIRONMENT.get_template('productDisplay.html')
        self.response.write(template.render(template_values))

#===============================================        ================================================================

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/adminview', AdminView),
    ('/contact', ContactPage),
    ('/term', TermPage),
    ('/privacy', PrivacyPage),
    ('/productDisplay', ProductDisplay),
    ('/Addproduct', ProductAdd),
    (r'/Editproduct/(\w+)', ProductEdit),
    ('/login', LoginPage),
    ('/register', RegisterPage),
    (r'/Deleteproduct/(\w+)', ProductDelete),
    (r'/product/(\w+)', DetailPage),
    (r'/category/(\w+)',Category),
    (r'/deletecategory/(\w+)', DeleteCategory),
    (r'/editcategory/(\w+)',EditCategory),
    ('/addcategory', AddCategory),
    (r'/category/(\w+)',Category),
], debug =True)