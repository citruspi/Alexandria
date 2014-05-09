from functools import wraps
from flask import session, redirect, url_for
from alexandria import mongo

def not_even_one(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if mongo.Books.find_one() is None:
            return redirect(url_for('upload'))
        return f(*args, **kwargs)
    return decorated_function

def authenticated(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):

        if not session.get('username'):

            return redirect(url_for('portal'))

        return f(*args, **kwargs)
    return decorated_function

def administrator(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        user = mongo.Users.find_one({'username': session.get('username')})

        if user['role'] != 0:

            return redirect(url_for('index'))

        return f(*args, **kwargs)
    return decorated_function
