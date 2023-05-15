from flask_jwt_extended import jwt_required
from db import get_collection
import json
from bson import json_util

# Admin Service
class AdminService():
    def __init__(self):
        self.collection = get_collection('users')

    @jwt_required()    
    def check_permission(self, username):
        try:
            admin = self.collection.find_one({'username': username, 'permission': True})
            if not admin:
                raise ValueError('Not perrmisson in this username!')
            return True
        except ValueError as e:
            raise ValueError(str(e),  exc_info=True) from e

    @jwt_required()
    def get_all_users(self):
        try:
            if not self.check_permission():
                raise ValueError ('You has not permission to use!')
            users = self.collection.find({}, projection={'_id':0})
            return {"user": json.loads(json_util.dumps(users))}
        except ValueError as e:
            raise ValueError(str(e),  exc_info=True) from e

 