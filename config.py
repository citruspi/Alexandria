class Config(object):

    DEBUG = False
    SECRET_KEY = 'CHANGEME'
    TEMP_DIR = 'tmp'
    LIB_DIR = 'books'

    MONGO = {
        'HOST' : 'localhost',
        'PORT' : 27017,
        'DATABASE' : 'Alexandria'
    }

class Debug(Config):

    DEBUG=True
