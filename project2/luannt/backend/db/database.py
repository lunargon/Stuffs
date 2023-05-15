from flask_pymongo import PyMongo
from flask_restful import abort
import certifi

mongo = PyMongo()
# Custom init_app with certifi
def init_app(app):
    try:
        app.config['MONGO_URI'] = 'mongodb+srv://luannt:hknB05Iml2QdMTOC@cluster0.v09ufpk.mongodb.net/store?retryWrites=true&w=majority'
        mongo.init_app(app, tlsCAFile=certifi.where())
    except Exception as e:
        raise Exception(str(e), exc_info=True) from e

# Get collectipn db
def get_collection(collection_name):
    try:
        return mongo.db[collection_name]
    except Exception as e:
        raise Exception(str(e), exc_info = True) from e

# Get data from collection by id
def get_document_by_id(collection_name, document_id):
    try:
        collection = get_collection(collection_name)
        document = collection.find_one({'id': document_id})
        if document is None:
            abort(404, message=f"{collection_name} document {document_id} not found")
        return document
    except Exception as e:
        raise Exception(str(e), exc_info = True) from e

# Get all data from collection
def get_documents(collection_name):
    try:
        collection = get_collection(collection_name)
        return list(collection.find())
    except Exception as e:
        raise Exception(str(e), exc_info = True) from e

# Create unique fields
def create_indexed(collection_name, key):
    try:
        get_collection(collection_name).create_indexes(key)
    except Exception as e:
        raise Exception(str(e), exc_info = True) from e

# insert data to collection
def insert_document(collection_name, document):
    try:
        collection = get_collection(collection_name)
        inserted_id = collection.insert_one(document).inserted_id
        return str(inserted_id)
    except Exception as e:
        raise Exception(str(e), exc_info = True) from e
        
# insert data to collection by id (not _id)
def update_document(collection_name, document_id, update_data):
    try:
        collection = get_collection(collection_name)
        result = collection.update_one({'id': document_id}, {'$set': update_data})
        if result.modified_count == 0:
            abort(404, message=f"{collection_name} document {document_id} not found")
    except Exception as e:
        raise Exception(str(e), exc_info = True) from e
    
# delete data to collection by id (not _id)
def delete_document(collection_name, document_id):
    try:
        collection = get_collection(collection_name)
        result = collection.delete_one({'id': document_id})
        if result.deleted_count == 0:
            abort(404, message=f"{collection_name} document {document_id} not found")
    except Exception as e:
        raise Exception(str(e), exc_info = True) from e