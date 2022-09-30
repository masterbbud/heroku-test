from datetime import datetime

from flask import request

from app.accounts import auth_token_used

from utils import success, stripArgs

sql = None

def create_post():
    args = stripArgs('auth', 'songid', 'caption')
    if not args[0]:
        return args[1]
    auth = args[1]['auth']
    songid = args[1]['songid']
    caption = args[1]['caption']
    user = sql.select('accounts', f"auth = '{auth}'")[0]['id']
    sendDict = {
        'userid': user,
        'dt': str(datetime.now()),
        'songid': songid,
        'caption': caption,
        'likes': 0
    }
    return sql.insert('posts', sendDict)

def get_posts():
    args = stripArgs('auth')
    if not args[0]:
        return args[1]
    auth = args[1]['auth']
    id = sql.select('accounts', f"auth = '{auth}'")[0]['id']
    allPosts = []
    queryResult = sql.select('friends', f"userid = {id}")
    if queryResult['type'] == 'error':
        return queryResult
    for userid in queryResult:
        sel = sql.select('posts', f"userid = {userid['following']}")
        if sel['type'] == 'error':
            return sel
        allPosts += sel['data']
    allPosts.sort(key = lambda x: x['dt'])
    return success(allPosts)
