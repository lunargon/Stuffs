from flask import jsonify
from flask_restful import Resource
from src.services import AdminService
from src.utils import logger
from flask_jwt_extended import jwt_required

# Routes Add Admin permission
class AdminPermission(Resource):
    @jwt_required()
    def get():
        try:
            user = AdminService().get_all_users()
            return user, 200
        except ValueError as e:
            logger.exception(str(e), exc_info=True)
            return jsonify(str(e.__cause__)), 400
        except Exception as e:
            logger.exception(str(e), exc_info=True)
            return jsonify(str(e.__cause__)), 500