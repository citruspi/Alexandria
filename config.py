import os

class Config(object):

    DEBUG = False
    SECRET_KEY = os.urandom(30).encode('hex')
    TEMP_DIR = 'tmp'
    LIB_DIR = 'books'

    MONGO = {
        'HOST' : 'localhost',
        'PORT' : 27017,
        'DATABASE' : 'Alexandria'
    }

class Debug(Config):

    DEBUG=True
