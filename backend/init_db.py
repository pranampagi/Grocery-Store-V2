from app import app
from application.data import datastore
from application.models import db
from werkzeug.security import generate_password_hash
from application.models import Cart


with app.app_context():
    db.create_all()
    
    # Create the admin
    datastore.find_or_create_role(name='Admin', description='Administrator')
    datastore.find_or_create_role(name='Storemanager', description='Store Manager')
    datastore.find_or_create_role(name='Customer', description='Customer')
    db.session.commit()

    if not datastore.find_user(name='admin', username="admin", email="admin@email.com"):
        datastore.create_user(name='admin', username="admin", email="admin@email.com", password=generate_password_hash('uiop'), roles=['Admin'])

    if not datastore.find_user(name="storemanager", username="storemanager", email="storemanager@email.com"):
        datastore.create_user(name="storemanager", username="storemanager", email="storemanager@email.com", password=generate_password_hash('uiop'), roles=['Storemanager'])

    if not datastore.find_user(name="customer", username="customer", email="customer@email.com"):
        user = datastore.create_user(name="customer", username="customer", email="customer@email.com", password=generate_password_hash('uiop'), roles=['Customer'])
        db.session.commit()
        cart = Cart(user_id=user.id)
        db.session.add(cart)

    db.session.commit()