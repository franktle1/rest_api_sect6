import sqlite3
from database import db

class UserModel(db.Model):

    #variable
    __tablename__ = 'users'
    #what columns does the table contain; tell sqlalchemy that theres a column called id with those properties
    #IMPORTANT: these columns must share the same name as any UserModel object variables you want to include in the database

    id = db.Column(db.Integer, primary_key= True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        #autoincremented id so _id is unneeded
        self.username = username
        self.password = password

    #find a user by their username given a username
    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username = username).first()
        #first username = column in table, second is the argument passed into method
    #find a user by their username given a username
    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id = _id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()





'''
import sqlite3
from database import db

class UserModel(db.Model):

    #variable
    __tablename__ = 'users'
    #what columns does the table contain; tell sqlalchemy that theres a column called id with those properties
    #IMPORTANT: these columns must share the same name as any UserModel object variables you want to include in the database

    id = db.Column(db.Integer, primary_key= True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    #find a user by their username given a username
    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username =?"
        #parameters in cursor must always be a tuple, and a single tuple is (x,)/ comma is needed
        result = cursor.execute(query,(username,)) #has the cursor
        row = result.fetchone() #this will get the first row of that data setting; no rows will result in None
        #cls() will create a __init__ of the inheritor function and pass w/e params inside of it to create class variables?
        if row is not None:
            user = cls(*row) #*row unpacks the row list and represents positional arguments: row[0] = id, row[1] = username, row[2] = password
        else:
            user = None

        connection.close()
        return user
    #find a user by their username given a username
    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id =?"
        #parameters in cursor must always be a tuple, and a single tuple is (x,)/ comma is needed
        result = cursor.execute(query,(_id,)) #has the cursor
        row = result.fetchone() #this will get the first row of that data setting; no rows will result in None
        #cls() will create a __init__ of the inheritor function and pass w/e params inside of it to create class variables?
        if row is not None:
            user = cls(*row) #*row unpacks the row list and represents positional arguments: row[0] = id, row[1] = username, row[2] = password
        else:
            user = None
        connection.close()
        return user
'''
