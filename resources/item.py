from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
#import sqlite3

from models.item import ItemModel

__tablename__ = 'items'

class Item(Resource):

    parser = reqparse.RequestParser() #instantiate the object
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help="This field cannot be left blank")
    parser.add_argument(
        'store_id',
        type=int,
        required=True,
        help="Every item needs a store id")

    @jwt_required() #needed to call the get method
    def get(self, name):
        item = ItemModel.find_item_by_name(name)
        if item is not None:
            return item.json()
        return {'message': "item doesnt exist in database"},404

    #adding an item to our item list
    def post(self,name):
        if ItemModel.find_item_by_name(name) is not None:
            return {'message': 'item: {} already exists'.format(name)}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'], data['store_id'])
        #theres a possibility that item is not inserted
        try:
            item.save_to_db()
        except:
            return {'message':'Could not insert {} into database.'.format(item['name'])}, 500 #500 is an internal server error
        return item.json(), 201 #201 is the code for something being created and its successful

    def delete(self, name):
        item = ItemModel.find_item_by_name(name)
        if item is None:
            return {'message':'Item {} does not exist in database'.format(name)},400
        elif item:
            item.delete_from_db()
        return {'message': 'Item removed'}

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_item_by_name(name)

        if item is None:
            item = ItemModel(name, data['price'], data['store_id']) #creates the new item
            #item = ItemModel(name, **data) #also acceptable because data is parsed with just price adn store id adn they are in teh right order
        else:
            item.price = data['price'] #because item is being called by an id; itll just update the price
            item.store_id = data['store_id']
        item.save_to_db()
        return item.json()

class ItemList(Resource):
    def get(self):
        #gets all the items, iterate through it, and return a json
        return {'items': [item.json() for item in ItemModel.query.all()]} #.all returns all the objects in the database
        #return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))} #returns the same thing
        #map would match the function x.json() to elements in ItemModel.queryall()

# from flask_restful import Resource, reqparse
# from flask_jwt import jwt_required
# import sqlite3
#
# from models.item import ItemModel
#
# __tablename__ = 'items'
#
# #api works with resources and every resource has to be classes
# #IMPORTANT: ALL METHODS MUST BE AN HTTP VERB LIKE GET POST DELETE ...
# class Item(Resource):
#     #name refers to name of the student
#     #reminder: filter(function as the condition,iterable list)
#     #since we expect only ONE Object to be found, next(X,Y) can be used on a filter object, and it grabs the first element found in the filter X, if nothing is found, defaults to Y
#     #if more than one, we can use list() on filter object
#     #{'item':item} Necessary to get a valid JSON representation; you can ommit 'is not None' in conditional statement in return
#     #no self.parser here; that means it only belongs the class itself, and can only be called using the class name 'Item' in Item.parser...
#     parser = reqparse.RequestParser() #instantiate the object
#     parser.add_argument(
#         'price',
#         type=float,
#         required=True,
#         help="This field cannot be left blank")
#     #the above code parses the request from the user, and updates only the price, if it is updating
#     #this is to prevent rewriting over items names, etc...
#     #making parser a class variable makes it easier to reuse and edit
#
#     @jwt_required() #needed to call the get method
#     def get(self, name):
#         item = ItemModel.find_item_by_name(name)
#         if item is not None:
#             return item.json()
#         return {'message': "item doesnt exist in database"},404
#
#         # was used for in-memory storage; switching to database
#         # item = next(filter(lambda x: x['name'] == name, items), None)
#         # return {'item': item}, 200 if item is not None else 404
#
#     #adding an item to our item list
#     def post(self,name):
#         #this checks if there are any duplicate items
#         #we self refers to Item since the method find item by name is a class method
#         if ItemModel.find_item_by_name(name) is not None:
#             return {'message': 'item: {} already exists'.format(name)}, 400
#         # in memory to database switch
#         # if next(filter(lambda x: x['name'] == name, items), None): # is not None: omitted because if it exists (true)
#         #     return {'message':'item with name {} already exists.'.format(name)}, 400
#
#         data = Item.parser.parse_args()
#         #data = request.get_json() WE can change this to request parsing
#         #we have to call Item because it is a class variable, and it doesnt have self
#         # item = {
#         #     'name': name,
#         #     'price':data['price']
#         #     }
#
#         item = ItemModel(name, data['price'] )
#         #theres a possibility that item is not inserted
#         try:
#             # ItemModel.insert(item)
#             item.insert()
#         except:
#             return {'message':'Could not insert {} into database.'.format(item['name'])}, 500 #500 is an internal server error
#
#         #items.append(item) switched because items was used for in-memory database; using outside database
#         return item.json(), 201 #201 is the code for something being created and its successful
#
#     def delete(self, name):
#         #global items                          #this makes sure items doesnt refer to itself in the line below
#         #items = list(filter(lambda x: x['name'] != name, items))
#         if ItemModel.find_item_by_name(name) is None:
#             return {'message':'Item {} does not exist in database'.format(name)},400
#
#         connection = sqlite3.connect('data.db')
#         cursor = connection.cursor()
#         query = "DELETE FROM items WHERE name=?"
#         cursor.execute(query,(name,))
#         connection.commit()
#         connection.close()
#         return {'message': 'Item removed'}
#
#     def put(self, name):
#         data = Item.parser.parse_args()
#         item = ItemModel.find_item_by_name(name)
#         #insert into database if it doesn't exist
#         #doesnt exist
#         #we changed the name so it doesnt get over written
#         # updated_item = {
#         #     'name':name,
#         #     'price':data['price']
#         # }
#         updated_item = ItemModel(name, data['price'])
#         if item is None:
#             try:
#                 #ItemModel.insert(updated_item)
#                 updated_item.insert()
#             except:
#                 return {'message': 'Error, failed to insert'}, 500
#         #does exist, so we update
#         else:
#             #item.update(data) #data is a dictionary; the update function either appends new data or overwrites existing data
#             try:
#                 # ItemModel.update(updated_item)
#                 updated_item.update()
#             except:
#                 return {'message': 'error, failed to update'}, 500
#         return updated_item.json()
#
# class ItemList(Resource):
#     def get(self):
#         connection = sqlite3.connect('data.db')
#         cursor = connection.cursor()
#         query = "SELECT * FROM items"
#         result = cursor.execute(query)
#         items = []
#         for row in result:
#             items.append({'name':row[0], 'price': row[1]})
#         connection.close()
#         return {'items': items}
