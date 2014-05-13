class Config(object):

    DEBUG = False
    SECRET_KEY = 'CHANGEME'
    TEMP_DIR = 'tmp'
    LIB_DIR = 'books'

    ALLOW_REGISTRATION = True

    MONGO = {
        'HOST' : 'localhost',
        'PORT' : 27017,
        'DATABASE' : 'Alexandria'
    }

class Debug(Config):

    DEBUG=True
