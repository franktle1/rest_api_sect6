from flask_restful import Resource, reqparse

from models.store import StoreModel

class Store(Resource):
    #get post delete
    def get(self,name):
        store = StoreModel.find_store_by_name(name)
        if store:
            return store.json()
        else:
            return {'message': 'Store does not exist in our database.'}, 404

    def post(self,name):
        if StoreModel.find_store_by_name(name):
            return {'message': 'The store {} already exists.'.format(name)}, 400
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message': 'Error: Failed to save store to database.'}, 500
        return store.json(), 201

    def delete(self,name):
        store = StoreModel.find_store_by_name(name)
        if store is None:
            return {'message': 'Store does not exist.'}
        else:
            store.delete_from_db()
        return {'message': 'Store {} successfully deleted'.format(name)}

class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}
