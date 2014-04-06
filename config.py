import os

class Config(object):

    DEBUG = False

class Debug(Config):

    DEBUG=True
    SECRET_KEY = os.urandom(30).encode('hex')
    TEMP_DIR = 'tmp'
    LIB_DIR = 'books'
