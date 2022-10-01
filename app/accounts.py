from flask import request
from flask_bcrypt import Bcrypt

import secrets

from app.utils import stripArgs, error, success, auth_token_used

sql = None

bcrypt = None # Bcrypt(app)

def login():
    """
    POST with a username and password, returns the AUTH key for that account or a warning based on the failure
        of the account lookup.
    """
    args = stripArgs('username', 'password')
    if not args[0]:
        return args[1]
    username = args[1]['username']
    password = args[1]['password']

    acc = sql.select('accounts', f"username = '{username}'")
    if acc['type'] == 'error':
        return acc
    if not acc['data']:
        return error('No account')

    if bcrypt.check_password_hash(acc['data'][0]['password'], password):
        return success(acc['data'][0]['auth'])
    else:
        return error('Incorrect password')

def signup():
    """
    POST with a username and password, creates an account if able and returns the AUTH key for that account or
        a warning based on the failure of the account lookup.
    """
    args = stripArgs('username', 'password')
    if not args[0]:
        return args[1]
    username = args[1]['username']
    password = args[1]['password']

    acc = sql.select('accounts', f"username = '{username}'")
    if acc['type'] == 'error':
        return acc
    if acc['data']:
        return error('Username already exists')

    pw = bcrypt.generate_password_hash(password).decode('utf-8')

    auth = get_auth_token()
    while auth_token_used(auth):
        auth = get_auth_token()
    
    res = sql.insert('accounts', {'username': username, 'password': pw, 'auth': auth})
    if res['type'] == 'error':
        return res
    return success(auth)

def follow_request():
    # needs auth instead of user
    args = stripArgs('auth', 'following')
    if not args[0]:
        return args[1]
    auth = args[1]['auth']
    following = args[1]['following']
    res = sql.select('accounts', f"auth = '{auth}'")
    if res['type'] == 'error':
        return res
    user = res['data'][0]['id']
    other = sql.select('accounts', f"id = {following}")
    if other['type'] == 'error':
        return other
    if not len(other['data']):
        return error('No account found to follow')
    block = sql.select('blocked', f"userid = {following} and blocked = {user}")
    if block['type'] == 'error':
        return block
    if len(block['data']):
        return error('Follow request was blocked')
    acc = sql.select('friends', f"userid = {user} and following = {following}")
    if acc['type'] == 'error':
        return acc
    if len(acc['data']):
        return error('User already following')
    res = sql.insert('friends', {'userid': user, 'following': following})
    if res['type'] == 'error':
        return res
    return success('Followed successfully')

def block_request():
    """
    Removes the blocking user from following the auth'd user, then
    adds their id to a 'blocked' table so they can't follow again
    """
    args = stripArgs('auth', 'blocking')
    if not args[0]:
        return args[1]
    auth = args[1]['auth']
    blocking = args[1]['blocking']
    res = sql.select('accounts', f"auth = '{auth}'")
    if res['type'] == 'error':
        return res
    user = res['data'][0]['id']
    other = sql.select('accounts', f"id = {blocking}")
    if other['type'] == 'error':
        return other
    if not len(other['data']):
        return error('No account found to block')
    already = sql.select('blocked', f"userid = {user} and blocked = {blocking}")
    if already['type'] == 'error':
        return already
    if len(already['data']):
        return error('User already blocked')
    acc = sql.select('friends', f"userid = {blocking} and following = {user}")
    if acc['type'] == 'error':
        return acc
    if len(acc['data']):
        delreq = sql.delete('friends', f"userid = {blocking} and following = {user}")
        if delreq['type'] == 'error':
            return delreq
    res = sql.insert('blocked', {'userid': user, 'blocked': blocking})
    if res['type'] == 'error':
        return res
    return success('Blocked successfully')

def account_data():
    args = stripArgs('auth')
    if not args[0]:
        return args[1]
    auth = args[1]['auth']
    return sql.select('accounts', f"auth = '{auth}'")

def get_auth_token():
    return secrets.token_urlsafe(20)
