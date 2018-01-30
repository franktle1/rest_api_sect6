#when the clients don't use them directly, this is what the models contain
# users have access to get/put/post/delete but dont have access to the helper
# all these methods are helper methods
#import sqlite3
from database import db


class ItemModel(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')
    #this init method creates an item model, so the item it is dealing with is the item itself
    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id


    def json(self):
        return{'name':self.name, 'price':self.price}

    @classmethod
    def find_item_by_name(cls, name):
        #query object inherited from SQLAlchemy object in ItemModel
        return cls.query.filter_by(name = name).first()  #SELECT * FROM items WHERE name = name LIMIT 1

        #sqlAlchemy will do an update instead of an insert,
        # because if something was called using an id, it just rewrites it?
        #this method is good for updating and inserting data
    def save_to_db(self):
        db.session.add(self) #session is a collection of objects that we will write into the database
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()



    # def find_item_by_name(cls, name):
    #     connection = sqlite3.connect('data.db')
    #     cursor = connection.cursor()
    #     query = "SELECT * FROM items WHERE name = ?"
    #     result = cursor.execute(query,(name,))
    #     row = result.fetchone() #the item name should be unique so were only fetching one row
    #     connection.close()
    #     if row is not None:
    #         return cls(*row)
    #         #returns an object of type ItemModel instead of a dictionary
    #         #so it'll return ItemModel(row[0] or name, row[1] or price) and build an itemmodel object with new values
    #         #return cls(row[0], row[1])

##@classmethod def insert/update(cls, item): -> because the new itemmodel class already stores an item; we switched
##also updated the cursor execute to reflect the item object calling the init values
# def insert(self):
#     #this code will write it to the database
#     connection = sqlite3.connect('data.db')
#     cursor = connection.cursor()
#     query = "INSERT INTO items VALUES(?, ?)"
#     cursor.execute(query,(self.name, self.price,))
#     connection.commit()
#     connection.close()
# def update(self):
#     connection = sqlite3.connect('data.db')
#     cursor = connection.cursor()
#     query = "UPDATE items SET price = ? WHERE name = ?"
#     cursor.execute(query,(self.price, self.name,))
#     connection.commit()
#     connection.close()
