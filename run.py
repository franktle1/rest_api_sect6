from app import app
from db import db

db.init_app(app)
#this is help wsgi to define db and prevenet circulr imports
#we do this to prevent importing the resources themselves


#effect hte method below, run that method before the first request into this app
#flask decorator
#before the first request runs, itll create data.db unless they exist already
@app.before_first_request
def create_tables():
    db.create_all() #when this runs, it'll create data.db and all the tables in the file unless they exist already
