#this will be similate teh dictionary
#we use _id because python has a keyword id, but self.id is okay
import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel
#importing ssqlite3 will enable interaction with sqlite3/database tools


'''this is a resource that adds users to the database; because the website allows users to register
and has an endpoint to do so; this method is a resource'''

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
    'username',
    type = str,
    required = True,
    help="username cannot be blank."
    )
    parser.add_argument(
    'password',
    type = str,
    required =True,
    help="password cannot be blank"
    )


    def post(self):
        data = UserRegister.parser.parse_args()
        #this checks for duplicate usernames
        if UserModel.find_by_username(data['username']) is not None:
            return {'message': 'Username already taken.'},400

        user = UserModel(**data) #unpacks data using kwargs - data['username'], data['password']
        user.save_to_db()


        return {'message': "User successfully created"},201




'''
#this will be similate teh dictionary
#we use _id because python has a keyword id, but self.id is okay
import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel
#importing ssqlite3 will enable interaction with sqlite3/database tools


#this is a resource that adds users to the database; because the website allows users to register
#and has an endpoint to do so; this method is a resource

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
    'username',
    type = str,
    required = True,
    help="username cannot be blank."
    )
    parser.add_argument(
    'password',
    type = str,
    required =True,
    help="password cannot be blank"
    )


    def post(self):
        data = UserRegister.parser.parse_args()
        #this checks for duplicate usernames
        if UserModel.find_by_username(data['username']) is not None:
            return {'message': 'Username already taken.'},400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "INSERT INTO users VALUES (NULL, ?,?)"
        cursor.execute(query, (data['username'], data['password'],)) #execute only accepts tuples

        connection.commit()
        connection.close()

        return {'message': "User successfully created"},201

'''
