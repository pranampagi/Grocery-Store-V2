import os


class Config(object):
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
    SECRET_KEY = "6b2141f0c04cd59b92749b1f052a7a53df796735e9c123cd20e5aeb3abaf2fba04a5b556f2b640d12f819c42f8070298b46d49151562a4d9f2f7540fa9b85879"
    SECURITY_PASSWORD_SALT = "90383042910f10ba5bb80711049ac2e19eff7e8ca89219961f1363d499357235"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authentication-Token"
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_HOST = "localhost"
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 0
    # Celery configuration (must be in Flask config so conf.update preserves them)
    CELERY_BROKER_URL = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/2"


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///database.db")
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-me-in-production")
    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT", "change-me-in-production")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authentication-Token"
    # Cache — use Redis if REDIS_URL is set, else simple in-memory cache
    CACHE_TYPE = os.environ.get("CACHE_TYPE", "SimpleCache")
    CACHE_REDIS_URL = os.environ.get("REDIS_URL", None)
    # Celery — use Redis if REDIS_URL is set
    CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", os.environ.get("REDIS_URL", "redis://localhost:6379/1"))
    CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", os.environ.get("REDIS_URL", "redis://localhost:6379/2"))