from db.database import get_collection
from flask import jsonify
from flask_restful import Resource, reqparse
from bson import json_util
from src.utils import redis_client, cache_data, logger
import re
import json
from copy import copy

# Route for get product by id
class Product(Resource):
    def __init__(self):
        self.collection = get_collection('products')

    def get(self, id):
        try:
            product = self.collection.find_one({'id':id})
            if product is None:
                raise Exception(f'Product with ID {id} not found')
            return json.loads(json_util.dumps(product)), 200
        except ValueError as e:
            logger.exception(str(e), exc_info=True)
            return jsonify(str(e.__cause__)), 400
        except Exception as e:
            logger.exception(str(e), exc_info=True)
            return jsonify(str(e.__cause__)), 404

# Route for get all products
class ProductList(Resource):
    def __init__(self):
        self.collection = get_collection('products')
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('page', type = int, default = 1, location = 'args')
        self.parser.add_argument('page_size', type = int, default = 30, location = 'args')
        self.parser.add_argument('sort', type = str, default  ='default', location = 'args')
        self.parser.add_argument('brands', type = str, default = None, location = 'args')
        self.parser.add_argument('sellers', type = str, default = None, location = 'args')
        self.parser.add_argument('colors', type = str, default = None, location = 'args')
        self.parser.add_argument('price', type = str, default = None, location = 'args')
        self.parser.add_argument('category', type = str, default = None, location = 'args')

    # GET method to get product
    def get(self):
        try:
            args = self.parser.parse_args()

            # Get params page and page_size
            page = args['page']
            page_size = args['page_size']

            # Set cache key
            cache_key = f"{args['page']}:{args['page_size']}:sort:{args.get('sort')}:brands:{args.get('brands')}:sellers:{args.get('sellers')}:colors:{args.get('colors')}:price:{args.get('price')}:category{args.get('category')}"

            # Check cache
            cached_data = redis_client.get(cache_key)
            if cached_data:
                return json.loads(cached_data), 200
            
            offset = (page - 1) * page_size
            sort_query = self._get_sort_query(args['sort'])
            filter_query = self._get_filter_query()

            # temp to get data to cache if not will return empty list
            temp = self.collection.find(filter_query, projection={'_id':0}).skip(offset).limit(page_size).sort(sort_query)
            products = copy(temp)

            # cache data to redis
            cache_data(redis_client, cache_key, temp)
            return {'products': json.loads(json_util.dumps(products)), 'total_count': self.collection.count_documents({})}, 200
        except ValueError as e:
            logger.exception(str(e), exc_info=True)
            return jsonify(str(e.__cause__)), 400
        except Exception as e:
            logger.exception(str(e), exc_info=True)
            return jsonify(str(e.__cause__)), 404

    # Private function: for get sort option
    def _get_sort_query(self, option):
        # mapping option
        sort_map = {
            'default': [('name', 1)],
            'top_seller': [('quantity_sold', -1)],
            'newest': [('day_ago_created', 1)],
            'price_asc': [('price', 1)],
            'price_desc': [('price', -1)]
        }
        return sort_map.get(option, [('name', 1)])

    # Private function: for get filter option
    def _get_filter_query(self):
        try:
            query = {}
            args = self.parser.parse_args()

            # get params
            brands = args['brands']
            sellers = args['sellers']
            colors = args['colors']
            price = args['price']
            category = args['category']

            # add filter to query
            if brands:
                query['brand_id'] = {
                '$in': [int(br_id) for br_id in brands.split(',')]
                }
            if sellers:
                query['seller_id'] = {
                    '$in': [int(seller_id) for seller_id in sellers.split(',')]
                }
            if colors:
                query['color_options.label'] = {
                    '$in': [re.compile(f'{color}', re.IGNORECASE) for color in colors.split(',')]
                }
            if category:
                query['category_id'] = int(category)
            if price:
                min_price = price.split(',')[0]
                max_price = price.split(',')[1]
                query['price'] = {
                    '$gte': int(min_price),
                    '$lt': int(max_price)
            }
            return query
        except ValueError as e:
            raise ValueError(str(e), exc_info=True) from e