import os
base_dir = os.path.dirname(__file__)

class Config(object):
    DEBUG = False
    TESTING = False

    ES_USER = "elastic"
    ES_PWD = "gNKzZmmj*_K1*cM2-9nG"
    ES_SERVER = "https://localhost:9200"

    MONGO_SERVER = "localhost:27017"
    INDEX = "athlete"

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'jdlfjds7834kjfksdfhdsds'
    

class ProductionConfig(Config):
    ...

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True