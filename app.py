import os
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT


from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList
#in this case, Resource does the jsonifying here.
#reqparse parses the request we get from the user


app = Flask(__name__)

app.secret_key = 'frank'
#tells where the database is; that the database will be at the root folder of our project
#app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db" # we do this so that our .db file will be saved to Heroku postgres dyno instead of being cleared out everytime it exits
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db') #THE DATABASE URL IS GOING TO BE FOUND ON HEROKU CONFIG VARIABLE under settings;
#sqlite is passed as a second variable in case heroku not found
# #THIS WAS commented out to use for web api on Heroku
# #effect hte method below, run that method before the first request into this app
# #flask decorator
# #before the first request runs, itll create data.db unless they exist already
# @app.before_first_request
# def create_tables():
#     db.create_all() #when this runs, it'll create data.db and all the tables in the file unless they exist already


#this turns off the library tracker; turns off the flask sqlalchemy tracker and not the sqlalchemy trackers
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_AUTH_URL_RULE'] = '/login'
#app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds = 1800) #30 minutes
api = Api(app)

jwt = JWT(app, authenticate, identity)
#app.config['JWT_AUTH_USERNAME_KEY'] = 'email'
#authenticaktion key uses email instead of default username
#Expiration delta - token expiration time
#app config auth url rule changes the authentication from /auth to login
#jwt creates a new endpoint called /auth when we call auth, we end username and password
#for this example. we're going to use a list as a substitute for our database
#items = []; was used for the in-memory database


#Everytime you add a new Resource, you need to explicitly state it here.
#were getting the name variable from the URL
api.add_resource(Item, '/item/<string:name>') #ie http://127.0.0.1:5000/student/Rolf
api.add_resource(Store, '/store/<string:name>')
api.add_resource(UserRegister, '/register')
api.add_resource(StoreList,'/stores/')
api.add_resource(ItemList,'/items')
#the if statement is to ensure that if something imports app.py, the app.run method doesnt run again
if __name__ == '__main__':
    #this is here to prevent circular imports
    from database import db
    db.init_app(app)
    app.run(port=5000, debug=True)
#port is default; not needed but better to be explicit
#debug = True will tell your whats wrong on an html page
