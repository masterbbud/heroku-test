from flask import request
from flask_bcrypt import Bcrypt

import secrets

sql = None

bcrypt = None # Bcrypt(app)

def login():
    """
    POST with a username and password, returns the AUTH key for that account or a warning based on the failure
        of the account lookup.
    """
    args = request.json
    username = args.get('username')
    if not username:
        return 'ERROR: Request needs username'
    password = args.get('password')
    if not password:
        return 'ERROR: Request needs password'

    acc = sql.select('accounts', f"username = '{username}'")
    if not acc:
        return 'ERROR: No Account'

    if bcrypt.check_password_hash(acc[0]['password'], password):
        return acc[0]['auth']
    else:
        return 'ERROR: Incorrect Password'

def signup():
    """
    POST with a username and password, creates an account if able and returns the AUTH key for that account or
        a warning based on the failure of the account lookup.
    """
    args = request.json
    username = args.get('username')
    if not username:
        return 'ERROR: Request needs username'
    password = args.get('password')
    if not password:
        return 'ERROR: Request needs password'

    acc = sql.select('accounts', f"username = '{username}'")
    if acc:
        return 'ERROR: Username already exists'

    pw = bcrypt.generate_password_hash(password).decode('utf-8')

    auth = get_auth_token()
    while auth_token_used(auth):
        auth = get_auth_token()
    
    sql.insert('accounts', {'username': username, 'password': pw, 'auth': auth})
    return auth

def follow_request():
    # needs auth instead of user
    args = request.json
    auth = args.get('auth')
    if not auth:
        return 'ERROR: Request needs auth'
    if not auth_token_used(auth):
        return 'ERROR: Invalid token'
    following = args.get('following')
    if not following:
        return 'ERROR: Request needs following'
    return follow(sql.select('accounts', f"auth = '{auth}'")[0]['id'], following)

def follow(user, following):
    acc = sql.select('friends', f"user = {user} and following = {following}")
    if acc:
        return 'ERROR: User already following'
    sql.insert('friends', {'user': user, 'following': following})
    return 'Followed successfully'

def account_data():
    args = request.json
    token = args.get('token')
    if not token:
        return 'ERROR: Request needs token'
    if not auth_token_used(token):
        return 'ERROR: Invalid token'
    else:
        return sql.select('accounts', f"auth = '{token}'")

def get_auth_token():
    return secrets.token_urlsafe(20)

def auth_token_used(token):
        return True if sql.select('accounts', f"auth = '{token}'") else False
