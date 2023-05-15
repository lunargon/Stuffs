from flask import jsonify
from flask_restful import Resource, reqparse
from db import get_collection
import json
from bson import json_util
from src.utils import logger
from flask_jwt_extended import jwt_required


# Get cart list 
class CartItemList(Resource):
    def __init__(self):
        # cart item parser
        self.cart_item_parser = reqparse.RequestParser()
        self.cart_item_parser.add_argument("product_id", type=int, required=True)
        self.cart_item_parser.add_argument("quantity", type=int, default=1)
        self.collection = get_collection('carts')

    @jwt_required()
    def get(self): 
        try:
            cart_items = self.collection.find(projection = {'_id':0})
            if cart_items is None:
                    raise Exception('Cart is error!')
            return json.loads(json_util.dumps(cart_items)), 200
        except Exception as e:
            logger.exception(str(e), exc_info=True)
            return jsonify(str(e.__cause__)), 404
        
    @jwt_required()
    def post(self):
        try: 
            param = {}
            cart_item = self.collection.insert_many(param)
            return json.loads(json_util.dumps(cart_item)), 201
        except Exception as e:
            logger.exception(str(e), exc_info=True)
            return jsonify(str(e.__cause__)), 500


class CartItem(Resource):
    def __init__(self):
        # cart item parser
        self.cart_item_parser = reqparse.RequestParser()
        self.cart_item_parser.add_argument("product_id", type=int, required=True)
        self.cart_item_parser.add_argument("quantity", type=int, default=1)
        self.collection = get_collection('carts')

    # Get item cart
    @jwt_required()
    def get(self, item_id):
        try:
            cart_item = self.collection.find({'id': item_id})
            if cart_item:
                return json.loads(json_util.dumps(cart_item)), 200
        except Exception as e:
            logger.exception(str(e), exc_info=True)
            return jsonify(str(e.__cause__)), 404

    # Update item cart
    @jwt_required()
    def put(self, item_id):
        try:
            cart_item = self.collection.find({'id': item_id})
            params = {}
            if cart_item:
                cart_item = self.collection.update_one({'id': item_id}, {'$set': params})
                return json.loads(json_util.dumps(cart_item)), 200
        except Exception as e:
            logger.exception(str(e), exc_info=True)
            return jsonify(str(e.__cause__)), 404

    # Delete item cart
    @jwt_required()
    def delete(self, item_id):
        try:
            cart_item = self.collection.find({'id': item_id})
            if cart_item:
                cart_item = self.collection.delete_one({'id': item_id})
                return json.loads(json_util.dumps(cart_item)), 204
        except Exception as e:
            logger.exception(str(e), exc_info=True)
            return jsonify(str(e.__cause__)), 404