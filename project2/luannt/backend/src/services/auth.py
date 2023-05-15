from flask_bcrypt import generate_password_hash, check_password_hash
from db.database import get_collection, create_indexed, insert_document
from flask_jwt_extended import create_access_token
from pytz import timezone
from src.utils import generateOTP
from src.models import UserModel
from src.services.mail import Mailsender
from datetime import datetime
from pymongo import IndexModel
import re

class JWTtoken():
    # generate token to access
    def generate_token(self, params):
        user = {
            "username": params["username"],
        }
        identity = {
            "username": user["username"],
        }
        access_token = create_access_token(identity)
        return {
            "username": user["username"],
            "access_token": access_token,
        }

# Class to auth
class Auth():
    def __init__(self):
        username_idx = IndexModel(
            [('username', 1)],
            unique=True
        )
        email_idx = IndexModel(
            [('email', 1)],
            unique=True
        )
        phone_idx = IndexModel(
            [('phone', 1)],
            unique=True,
            partialFilterExpression={
                'phone': {'$type': 'string'}
            }
        )
        otp_idx = IndexModel(
            [('created_at', 1)],
            expireAfterSeconds= 180
        )
        create_indexed(collection_name = 'users', key=[username_idx, email_idx, phone_idx])
        create_indexed(collection_name= 'otps', key=[otp_idx])

    #  service user signin
    def signin(self, params):
        try: 
            coming_user = {
                "username": params["username"],
                "password": params["password"],
            }
            user = get_collection("users").find_one({"username": coming_user["username"]})
            if not user:
                raise ValueError("Not found user!")
            if not check_password_hash(user["password"], coming_user["password"]):
                raise ValueError("Password is invalid!")
            return JWTtoken().generate_token(
                {
                    "username": user["username"],
                    "email": user["email"]
                }
            )
        except ValueError as e:
            raise ValueError(str(e),  exc_info=True) from e
        except Exception as e:
            raise Exception(str(e),  exc_info=True) from e
    
    # service admin signin
    def admin_signin(self, params):
        try:
            coming_user = {
                "username": params["username"],
                "password": params["password"],
            }
            user = get_collection("users").find_one({"username": coming_user["username"]})
            if not user:
                raise ValueError("Not found user!")
            if not check_password_hash(user["password"], coming_user["password"]):
                raise ValueError("Password is invalid!")
            return JWTtoken().generate_token(
                {
                    "username": user["username"],
                    "email": user["email"]
                }
            )
        except ValueError as e:
            raise ValueError(str(e), exc_info=True) from e
        except Exception as e:
            raise Exception(str(e), exc_info=True) from e
    
    # service user signup
    def signup(self, params):
        try:
            new_user = {
                "username": params["username"],
                "email": params["email"],
                "password": params["password"],
                "otp" : generateOTP(),
                "created_at": datetime.utcnow()
            }
            if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", new_user["email"]):
                raise ValueError("Email address is invalid!")
            hashed_password = generate_password_hash(new_user["password"])
            new_user["password"] = hashed_password
            check = get_collection("users").find_one({"username": new_user["username"], "email": new_user["email"]})
            if check:
                raise ValueError("User or email is already sign up !")
            insert_document('otps', new_user)
            Mailsender().send_otp("Confirm account", new_user["email"], new_user["otp"])
            return {
                    "username": new_user["username"],
                    "email": new_user["email"]
                }
        except ValueError as e:
            raise ValueError(str(e), exc_info=True) from e
        except Exception as e:
            raise Exception(str(e), exc_info=True) from e

# Class activate account
class Activate():
    def __init__(self):
        self.collection = get_collection("otps")

    # Service activate account
    def confirm_register(self, confirm_otp):
        try:
            OTPs = self.collection.find({'email': confirm_otp['email']},projection={'created_at':0})
            OTPs = list(OTPs)
            if OTPs == []:
                raise ValueError('Email is invalid or OTP was expired!')

            otp_user = OTPs[-1]
            if otp_user['otp'] == confirm_otp['otp']:
                user = UserModel(**otp_user,created_at=datetime.now(timezone('Asia/Ho_Chi_Minh')).strftime("%Y-%m-%d %H:%M:%S"))
                insert_document("users", user.dict())
            else:
                raise ValueError('OTP invalid!')
            return {
                "message": "Activate account success!"
            }
        except ValueError as e:
            raise ValueError(str(e), exc_info=True) from e
        except Exception as e:
            raise Exception(str(e), exc_info=True) from e