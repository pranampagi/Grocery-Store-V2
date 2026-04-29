from flask_restful import Resource, Api, reqparse, fields, marshal, marshal_with
from flask_security import auth_required, roles_required, current_user, roles_accepted
from sqlalchemy import or_
from sqlalchemy.orm import joinedload
from flask import request
from .models import db, User, Product, Category, Cart, CartItem, Order, OrderItem
from datetime import datetime
from .data import cache



api = Api(prefix='/api')




# USER API



user_parser = reqparse.RequestParser()

user_parser.add_argument('name', type=str, required=True, help='Name cannot be blank')
user_parser.add_argument('username', type=str, required=True, help='Username cannot be blank')
user_parser.add_argument('email', type=str, required=True, help='Email cannot be blank')
user_parser.add_argument('password', type=str, required=True, help='Password cannot be blank')

    

user_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'username': fields.String,
    'email': fields.String,
    'active': fields.Boolean,
    'roles': fields.List(fields.Nested({
        'id': fields.Integer,
        'name': fields.String,
        'description': fields.String
    }))
}


# Resource for User
class UserApi(Resource):
    @marshal_with(user_fields)
    @auth_required("token")
    @roles_required('Admin')
    @cache.memoize(timeout=30)
    def get(self):
        users = User.query.all()
        return users, 200


class Creator(fields.Raw):
    def format(self, user):
        return user.name
    



# CATEGORY API
    





category_parser = reqparse.RequestParser()

category_parser.add_argument('name', type=str, required=True, help='Name cannot be blank')
category_parser.add_argument('description', type=str, required=True, help='Description cannot be blank')

category_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'creator': Creator,
    'active': fields.Boolean,
    'delete': fields.Boolean,
    'products': fields.List(fields.Nested({
        'id': fields.Integer,
        'name': fields.String,
        'price': fields.Float,
        'quantity': fields.Integer,
        'manufacture_date': fields.DateTime(dt_format='iso8601'),
        'delete': fields.Boolean,
    }))
}


# Resource for Category
class CategoryApi(Resource):
    @marshal_with(category_fields)
    @auth_required("token")
    @roles_accepted('Admin', 'Storemanager')
    def get(self, category_id):
        category = Category.query.get(category_id)
        return category, 200
    
    
    @marshal_with(category_fields)
    @auth_required("token")
    @roles_accepted('Admin', 'Storemanager')
    def put(self, category_id):
        args = category_parser.parse_args()
        category = Category.query.get(category_id)
        category.name = args['name']
        category.description = args['description']

        if current_user.has_role('Admin'):
            category.active = True
        elif current_user.has_role('Storemanager'):
            category.active = False
        db.session.commit()
        return category, 200
    
    
    @auth_required("token")
    @roles_accepted('Admin', 'Storemanager')
    def delete(self, category_id):
        category = Category.query.get(category_id)

        if not category:
            return {"message": "Category does not exist"}, 404
        
        if current_user.has_role('Admin'):
            db.session.delete(category)
            db.session.commit()
            return {"message": "Category Deleted"}, 200
        elif current_user.has_role('Storemanager'):
            category.delete = True
            db.session.commit()
            return {"message": "Category Requested for Deletion"}, 200
    

class CategoryListApi(Resource):
    @marshal_with(category_fields)
    @cache.memoize(timeout=30)
    def get(self):
        categories = Category.query.options(joinedload(Category.products)).all()
        return categories, 200
    
    @marshal_with(category_fields)
    @auth_required("token")
    @roles_accepted('Admin', 'Storemanager')
    def post(self):
        args = category_parser.parse_args()
        name = args.get('name')
        description = args.get('description')

        category = Category.query.filter_by(name=name).first()

        if category:
            return {"message": "Category already exists"}, 404
        
        category = Category(name=name, description=description, creator_id=current_user.id, delete=False)

        if current_user.has_role('Admin'):
            category.active = True
        elif current_user.has_role('Storemanager'):
            category.active = False
        db.session.add(category)
        db.session.commit()
        return category, 201





# PRODUCT API
    


    

    
product_parser = reqparse.RequestParser()

product_parser.add_argument('name', type=str, required=True, help='Name cannot be blank')
product_parser.add_argument('price', type=float, required=True, help='Price cannot be blank')
product_parser.add_argument('category_id', type=int, required=True, help='Category ID cannot be blank')
product_parser.add_argument('quantity', type=int, required=True, help='Quantity cannot be blank')
product_parser.add_argument('manufacture_date', type=str, required=True, help='Manufacture Date cannot be blank')


product_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'price': fields.Float,
    'creator': Creator,
    'category_id': fields.Integer,
    'category': fields.Nested(category_fields),
    'quantity': fields.Integer,
    'manufacture_date': fields.DateTime(dt_format='iso8601'),
    'delete': fields.Boolean,
}


# Resource for Product
    

class ProductApi(Resource):
    @marshal_with(product_fields)
    @auth_required("token")
    @roles_required('Storemanager')
    def get(self, product_id):
        product = Product.query.get(product_id)
        return product, 200
    
    
    @marshal_with(product_fields)
    @auth_required("token")
    @roles_required('Storemanager')
    def put(self, product_id):
        args = product_parser.parse_args()
        product = Product.query.get(product_id)
        product.name = args['name']
        product.category_id = args['category_id']
        product.price = args['price']

        product.quantity = args['quantity']
        product.manufacture_date = datetime.strptime(args['manufacture_date'], '%Y-%m-%d').date()
        db.session.commit()
        return product, 200
    
    
    @auth_required("token")
    @roles_accepted('Admin', 'Storemanager')
    def delete(self, product_id):
        product = Product.query.get(product_id)
        
        if not product:
            return {"message": "Product does not exist"}, 404
        
        if current_user.has_role('Storemanager'):
            product.delete = True
            db.session.commit()
            return {"message": "Product Requested for Deletion"}, 200
        elif current_user.has_role('Admin') and product.delete:
            db.session.delete(product)
            db.session.commit()
            return {"message": "Product Deleted"}, 200
            
        return {"message": "Product Not eligible for deletion"}, 400
    


class ProductListApi(Resource):
    @marshal_with(product_fields)
    @auth_required("token")
    @roles_accepted('Admin', 'Storemanager')
    @cache.memoize(timeout=30)
    def get(self):
        products = Product.query.options(joinedload(Product.category)).all()
        return products, 200
    
    @marshal_with(product_fields)
    @auth_required("token")
    @roles_required('Storemanager')
    def post(self):
        args = product_parser.parse_args()
        name = args.get('name')
        price = args.get('price')
        category_id = args.get('category_id')
        quantity = args.get('quantity')
        manufacture_date = args.get('manufacture_date')

        if not name or not price or not quantity or not manufacture_date:
            return {"message": "All fields are required"}, 400
        #convert manufacture_date to datetime object
        manufacture_date = datetime.strptime(manufacture_date, '%Y-%m-%d').date()

        product = Product.query.filter_by(name=name).first()

        if product:
            return {"message": "Product already exists"}, 404
        
        product = Product(name=name, price=price, quantity=quantity, manufacture_date=manufacture_date, creator_id=current_user._get_current_object().id, category_id=category_id, delete=False, sold_quantity=0)
        db.session.add(product)
        db.session.commit()
        return product, 201
    





# CART ITEM API
    


cart_item_parser = reqparse.RequestParser()

cart_item_parser.add_argument('product_id', type=int, required=True, help='Product ID cannot be blank')
cart_item_parser.add_argument('quantity', type=int, required=True, help='Quantity cannot be blank')


cart_item_fields = {
    'id': fields.Integer,
    'cart_id': fields.Integer,
    'product_id': fields.Integer,
    'name': fields.String,
    'price': fields.Float,
    'category': fields.String,
    'quantity': fields.Integer,
    'manufacture_date': fields.DateTime(dt_format='iso8601'),
}


# Resource for Cart Item


class AddCartItemApi(Resource):
    @auth_required("token")
    @roles_required('Customer')
    def post(self):
        args = cart_item_parser.parse_args()
        product_id = args.get('product_id')
        quantity = args.get('quantity')
        cart = Cart.query.filter_by(user_id=current_user.id).first()    
        product = Product.query.get(product_id)
        manufacturer_date = product.manufacture_date
        if not product:
            return {"message": "Product does not exist"}, 404
        if product.quantity < quantity:
            return {"message": "Product quantity not available"}, 400
        cart_item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
        if cart_item:
            cart_item.quantity = cart_item.quantity + quantity
        else:
            cart_item = CartItem(cart_id=cart.id, product_id=product_id, name=product.name, price=product.price, category=product.category.name, quantity=quantity, manufacture_date=manufacturer_date)
            db.session.add(cart_item)
        db.session.commit()
        return marshal(cart_item, cart_item_fields), 201


class CartItemApi(Resource):
    @marshal_with(cart_item_fields)
    @auth_required("token")
    @roles_required('Customer')
    @cache.cached(timeout=30)
    def get(self, cart_item_id):
        cart_item = CartItem.query.get(cart_item_id)
        return cart_item, 200
    
    
    @marshal_with(cart_item_fields)
    @auth_required("token")
    @roles_required('Customer')
    def put(self, cart_item_id):
        args = cart_item_parser.parse_args()
        quantity = args.get('quantity')
        cart_item = CartItem.query.get(cart_item_id)
        product = Product.query.get(cart_item.product_id)
        
        if quantity > product.quantity:
            return {"message": "Product quantity not available"}, 400
        if quantity <= 0:
            return {"message": "Quantity must be greater than 0"}, 400
        
        cart_item.quantity = quantity
        db.session.commit()
        return {"message": "Cart Item Updated"}, 200
    
    
    @auth_required("token")
    @roles_required('Customer')
    def delete(self, cart_item_id):
        cart_item = CartItem.query.get(cart_item_id)
        db.session.delete(cart_item)
        db.session.commit()
        return {"message": "Cart Item Deleted"}, 200



# CART API
    

cart_parser = reqparse.RequestParser()

cart_parser.add_argument('cart_items', type=list, required=True, help='Cart Items cannot be blank')


cart_fields = {
    'id': fields.Integer,
    'user_id': fields.Integer,
    'cart_items': fields.List(fields.Nested(cart_item_fields)),
}


# Resource for Cart


class CartApi(Resource):
    @marshal_with(cart_fields)
    @auth_required("token")
    @roles_required('Customer')
    def get(self):
        cart = Cart.query.filter_by(user_id=current_user.id).first()
        return cart, 200
    











# ORDER API
    

order_fields = {
    'id': fields.Integer,
    'user_id': fields.Integer,
    'date': fields.DateTime(dt_format='iso8601'),
    'order_items': fields.List(fields.Nested({
        'id': fields.Integer,
        'product_id': fields.Integer,
        'name': fields.String,
        'price': fields.Float,
        'quantity': fields.Integer,
    })),
}



# Resource for Order


class OrderApi(Resource):
    @marshal_with(order_fields)
    @auth_required("token")
    @roles_required('Customer')
    def get(self):
        orders = Order.query.filter_by(user_id=current_user.id).all()
        return orders, 200


    @auth_required("token")
    @roles_required('Customer')
    def post(self):
        cart = Cart.query.filter_by(user_id=current_user.id).first()
        cart_items = cart.cart_items

        if not cart_items:
            return {"message": "Cart is empty"}, 400

        order = Order(user_id=current_user.id)
        db.session.add(order)
        for cart_item in cart_items:
            product = Product.query.get(cart_item.product_id)
            if product.quantity < cart_item.quantity:
                return {"message": "Product quantity not available"}, 400
            product.quantity = product.quantity - cart_item.quantity
            product.sold_quantity = product.sold_quantity + cart_item.quantity
            order_item = OrderItem(order_id=order.id, product_id=cart_item.product_id, name=cart_item.name, quantity=cart_item.quantity, price=cart_item.price)
            db.session.add(order_item)
            db.session.delete(cart_item)
        
        db.session.commit()
        db.session.add(order)
        db.session.commit()

        return {"message": "Order Placed"}, 201
    


# Resource for Search
    

class SearchApi(Resource):
    @cache.memoize(timeout=30)
    def get(self, query):
        if not query:
            return {"message": "Query cannot be empty"}, 400
        try:
            # If query is an integer or float, search for product price <= query
            if query.isdigit():
                products = Product.query.options(joinedload(Product.category)).filter(Product.price <= float(query)).all()
            # If query is a date, search for product manufacture_date >= query
            elif query.count('-') == 2:
                products = Product.query.options(joinedload(Product.category)).filter(Product.manufacture_date >= query).all()
            # Otherwise, search for product name or category name containing query (case-insensitive)
            else:
                products = Product.query.options(joinedload(Product.category)).filter(
                    or_(
                        Product.name.ilike(f'%{query}%'),
                        Product.category.has(Category.name.ilike(f'%{query}%'))
                    )
                ).all()
                
            # filter products with category that is active (with null safety)
            products = [product for product in products if product.category and product.category.active]
            return marshal(products, product_fields), 200
        except Exception as e:
            return {"message": f"Search error: {str(e)}"}, 500





api.add_resource(UserApi, '/users')

api.add_resource(CategoryApi, '/category/<int:category_id>')
api.add_resource(CategoryListApi, '/categories')

api.add_resource(ProductApi, '/product/<int:product_id>')
api.add_resource(ProductListApi, '/products')

api.add_resource(CartApi, '/cart')
api.add_resource(AddCartItemApi, '/cart-item')
api.add_resource(CartItemApi, '/cart-item/<int:cart_item_id>')

api.add_resource(OrderApi, '/order')

api.add_resource(SearchApi, '/search/<string:query>')