from flask import current_app as app, jsonify, request
from application.models import Product, Category, Cart, db
from .data import datastore
from werkzeug.security import generate_password_hash, check_password_hash
from flask_security import auth_required, roles_required, current_user, roles_accepted
from datetime import datetime
import json
# from application.tasks import create_product_csv
# from celery.result import AsyncResult
# from celery import shared_task
# import flask_excel as excel
# import time



@app.route('/admin')
@auth_required("token")
@roles_required('Admin')
def admin():
    return 'Admin'


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    confirm_password = data.get('confirm_password')
    if not name:
        return jsonify({"message": "name not provided"}), 400
    if not username:
        return jsonify({"message": "username not provided"}), 400
    if not email:
        return jsonify({"message": "email not provided"}), 400
    if not password:
        return jsonify({"message": "password not provided"}), 400
    if not confirm_password:
        return jsonify({"message": "confirm_password not provided"}), 400
    if password != confirm_password:
        return jsonify({"message": "password and confirm_password do not match"}), 400
    
    user = datastore.find_user(email=email)
    if user:
        return jsonify({"message": "User Already Exists"}), 400
    
    user = datastore.create_user(name=name, username=username, email=email, password=generate_password_hash(password), roles=['Customer'])
    db.session.commit()
    cart = Cart(user_id=user.id)
    db.session.add(cart)
    db.session.commit()

    return jsonify({"message": "User Created"}), 201



# Route for user login
@app.route('/user-login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    if not email:
        return jsonify({"message": "email not provided"}), 400
    if not password:
        return jsonify({"message": "password not provided"}), 400

    user = datastore.find_user(email=email)
    if not user:
        return jsonify({"message": "User Not Found"}), 404
    
    if not user.active:
        return jsonify({"message": "User not activated"}), 400

    if check_password_hash(user.password, password):
        db.session.commit()
        return jsonify({"token": user.get_auth_token(), "email": user.email, "role": user.roles[0].name}), 200
    else:
        return jsonify({"message": "Invalid Password"}), 400
    


@app.route('/manager-register', methods=['POST'])
def manager_register():
    data = request.get_json()
    name = data.get('name')
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    confirm_password = data.get('confirm_password')
    if not name:
        return jsonify({"message": "name not provided"}), 400
    if not username:
        return jsonify({"message": "username not provided"}), 400
    if not email:
        return jsonify({"message": "email not provided"}), 400
    if not password:
        return jsonify({"message": "password not provided"}), 400
    if not confirm_password:
        return jsonify({"message": "confirm_password not provided"}), 400
    if password != confirm_password:
        return jsonify({"message": "password and confirm_password do not match"}), 400
    
    user = datastore.find_user(email=email)
    if user:
        return jsonify({"message": "User Already Exists"}), 400
    
    user = datastore.create_user(name=name, username=username, email=email, password=generate_password_hash(password), roles=['Storemanager'], active=False)
    db.session.commit()

    return jsonify({"message": "User Created"}), 201



@app.route('/user-logout')
@auth_required("token")
@roles_accepted('Admin', 'Storemanager', 'Customer')
def logout():
    user = datastore.find_user(id=current_user.id)
    user.last_login_at = datetime.now()
    db.session.commit()
    return jsonify({"message": "User Logged Out"}), 200








#############################################################################################################################################

# ADMIN ROUTES

    

@app.route('/activate/storemanager/<int:id>', methods=['PUT'])
@auth_required("token")
@roles_required('Admin')
def activate_storemanager(id):
    user = datastore.find_user(id=id)
    if not user:
        return jsonify({"message": "User Not Found"}), 404
    user.active = True
    db.session.commit()
    return jsonify({"message": "User Activated"}), 200



@app.route('/activate/category/<int:id>', methods=['PUT'])
@auth_required("token")
@roles_required('Admin')
def activate_category(id):
    category = Category.query.filter_by(id=id).first()
    if not category:
        return jsonify({"message": "Category Not Found"}), 404
    category.active = True
    db.session.commit()
    return jsonify({"message": "Category Activated"}), 200



# @app.route('/delete/product/<int:id>', methods=['DELETE'])
# @auth_required("token")
# @roles_required('Admin')
# def delete_product(id):
#     product = Product.query.filter_by(id=id).first()
#     if not product:
#         return jsonify({"message": "Product Not Found"}), 404
#     if product.delete:
#         db.session.delete(product)
#         db.session.commit()
#         return jsonify({"message": "Product Deleted"}), 200
    
#     return jsonify({"message": "Product Not eligible for deletion"}), 400










#############################################################################################################################################


# OUT OF STOCK ROUTE



@app.route('/quantity', methods=['PUT'])
@auth_required("token")
@roles_accepted('Customer')
def update_quantity():
    data = request.get_json()
    for category in data:
        for item in data.get(category):
            product = Product.query.filter_by(id=item.get('product_id')).first()
            if not product:
                return jsonify({"message": "Product Not Found"}), 404

            if product.quantity < item.get('quantity'):
                print(product.quantity)
                item['quantity'] = product.quantity
            db.session.commit()
    return json.dumps(data, indent=4), 200, {'Content-Type': 'application/json'}
            



#############################################################################################################################################


# STORE MANAGER ROUTES


# @app.route('/download-csv')
# def download_csv():
#     try:
#         task = create_product_csv.delay()
#         return jsonify({"task_id": task.id}), 200
#     except:
#         return jsonify({"message": "Something went wrong"}), 400


# @app.route('/get-csv/<task_id>')
# def get_csv(task_id):
#     res = AsyncResult(task_id)
#     if res.ready():
#         filename = res.result
#         return send_file(filename, as_attachment=True)
#     else:
#         return jsonify({"message": "Task Pending"}), 400