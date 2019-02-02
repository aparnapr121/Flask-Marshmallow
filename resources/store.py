from flask_restful import Resource
from models.store import StoreModel

from schemas.store import StoreSchema

STORE__NOT_FOUND = "Store not found"
ERROR_INSERTING = "An error occurred while inserting the store."
STORE_DELETED = "Store deleted."
NAME_ALREADY_EXISTS = "A store with name '{}' already exists."

store_schema = StoreSchema()
store_list_schema = StoreSchema(many=True)

class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store_schema.dump(store)
        return {"message": STORE__NOT_FOUND}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {"message": NAME_ALREADY_EXISTS.format(name)}, 400

        store = StoreModel(name=name)
        try:
            store.save_to_db()
        except:
            return {"message": ERROR_INSERTING}, 500

        return store_schema.dump(store), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {"message": STORE_DELETED}


class StoreList(Resource):
    def get(self):
        return {"stores": store_list_schema.dump(StoreModel.find_all())}
