from flask import Blueprint

auth = Blueprint('auth',__name__)

@auth.route('/login')
def login():
    return "123"

@auth.route('/logout')
def logout():
    return "123"

@auth.route('/sign-up')
def signUp():
    return "123"