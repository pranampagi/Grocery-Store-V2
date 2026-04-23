from flask_security import SQLAlchemyUserDatastore
from .models import db, User, Role
from flask_caching import Cache


datastore = SQLAlchemyUserDatastore(db, User, Role)

cache = Cache()