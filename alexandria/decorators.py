from functools import wraps
from flask import session, redirect, url_for, request, abort
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

        print request.method

        if request.method == 'GET':

            token = request.args.get('token')
            user =  mongo.Users.find_one({'tokens.token': token})

            if not (token and user):

                #abort(403)
                pass

        elif request.method == 'POST':

            token = request.form.get('token')
            user =  mongo.Users.find_one({'tokens.token': token})

            if not (token and user):

                #abort(403)
                pass

        else:

            #abort(405)
            pass

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
