import os

class Config(object):

    DEBUG = False
    SECRET_KEY = os.urandom(30).encode('hex')
    TEMP_DIR = 'tmp'
    LIB_DIR = 'books'

    MONGOHOST = 'localhost'
    MONGOPORT = 27017
    MONGODB = 'Alexandria'

class Debug(Config):

    DEBUG=True
