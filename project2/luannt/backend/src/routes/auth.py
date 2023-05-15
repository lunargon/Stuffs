from flask import request, jsonify
from flask_restful import Resource
from src.services import Auth, Activate
from src.utils import logger

# Route for user sign in
class UsersSignin(Resource):
    def post(self):
        try:
            params = {
                "username": request.json.get("username", None),
                "password": request.json.get("password", None)
            }
            if not params["username"] or not params["password"]:
                raise ValueError("Invalid username or password")
            signed_in_user = Auth().signin(params)
            return signed_in_user, 200
        except ValueError as e:
            logger.exception(str(e), exc_info=True)
            return jsonify(str(e.__cause__)), 400
        except Exception as e:
            logger.exception(str(e), exc_info=True)
            return jsonify(str(e.__cause__)), 500

# Route for user sign up
class UsersSignup(Resource):
    def post(self):
        try:
            params = {
                "username": request.json.get("username", None),
                "email": request.json.get("email", None),
                "password": request.json.get("password", None)
            }
            if not params["username"] or not params["password"]:
                raise ValueError("Invalid username or password")
            signed_up_user = Auth().signup(params)
            return signed_up_user, 202  
        except ValueError as e:
            logger.exception(str(e), exc_info=True)
            return jsonify(str(e.__cause__)), 400
        except Exception as e:
            logger.exception(str(e), exc_info=True)
            return jsonify(str(e.__cause__)), 500
    
# Route for admin sign in
class AdminSignin(Resource):
    def post(self):
        try:
            params = {
                "username": request.json.get("username", None),
                "password": request.json.get("password", None)
            }
            if not params["username"] or not params["password"]:
                raise ValueError("Invalid username or password")
            signed_in_admin = Auth().signin(params)
            return signed_in_admin, 200
        except ValueError as e:
            logger.exception(str(e), exc_info=True)
            return jsonify(str(e.__cause__)), 400
        except Exception as e:
            logger.exception(str(e), exc_info=True)
            return jsonify(str(e.__cause__)), 500


# Route for activate user account
class ActivateUser(Resource):
    def post(self):
        try:
            params = {
                "email": request.json.get("email", None),
                "otp": request.json.get("otp", None)
            }
            if not params["otp"] or not params["email"]:
                raise ValueError("Invalid otp or email")
            activate_user = Activate().confirm_register(params)
            return activate_user, 201
        except ValueError as e:
            logger.exception(str(e), exc_info=True)
            return jsonify(str(e.__cause__)), 400
        except Exception as e:
            logger.exception(str(e), exc_info=True)
            return jsonify(str(e.__cause__)), 500