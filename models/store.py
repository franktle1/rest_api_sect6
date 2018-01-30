from database import db

class StoreModel(db.Model):
    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))
    items = db.relationship('ItemModel', lazy = 'dynamic') #this is a list of item models
    #the lazy = dynamic is so, until we actually call the json method, were not always going to look into the the tables
    #self.items whenever we access the json method unless we use .all
    #self.items does not raise a list of items. self.items is not a query builder
    #so that means, until we call the query, were not looking through the tables
    #trade off is, speed of creating a store vs speed of calling the json method
    #in this case, every time we call the json method, it'll be slower because we are accessing the taables
    #but making the stores are easier since it is lazy


    def __init__(self, name):
        self.name = name


    def json(self):
        return{'name':self.name, 'item': [item.json() for item in self.items.all()]}

    @classmethod
    def find_store_by_name(cls, name):
        return cls.query.filter_by(name = name).first()  #SELECT * FROM stores WHERE name = name LIMIT 1


    def save_to_db(self):
        db.session.add(self) #session is a collection of objects that we will write into the database
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
