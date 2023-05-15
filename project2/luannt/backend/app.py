from flask import Flask
from db.database import init_app
from src.utils import API_URL
from src.routes import ProductList, Product, UsersSignin, UsersSignup, AdminSignin, AdminPermission, ActivateUser, CartItemList, CartItem
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from src.utils import SECRET_KEY

# Config 
app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})
app.config["JWT_SECRET_KEY"] = SECRET_KEY
app.config["JWT_ALGORITHM"] = "HS256"
jwt = JWTManager(app)
api = Api(app)
init_app(app)

# Add api routes - Product 
api.add_resource(ProductList, f'{API_URL}/products')
api.add_resource(Product, f'{API_URL}/products/<int:id>')

# Add routes - Auth User
api.add_resource(UsersSignin, f'{API_URL}/user/signin')
api.add_resource(UsersSignup, f'{API_URL}/user/signup')
api.add_resource(ActivateUser, f'{API_URL}/user/activate')

# Add routes - Auth Admin
api.add_resource(AdminSignin, f'{API_URL}/admin/signin')
api.add_resource(AdminPermission, f'{API_URL}/admin/getuser')

# # Add routes - Cart
api.add_resource(CartItemList, f'{API_URL}/carts')
api.add_resource(CartItem, f'{API_URL}/carts/<int:item_id>')


if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = 8000, debug=True)
