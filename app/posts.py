from datetime import datetime

from flask import request

from app.utils import success, stripArgs

sql = None

# check select calls for error

def create_post():
    args = stripArgs('auth', 'songid', 'caption')
    if not args[0]:
        return args[1]
    auth = args[1]['auth']
    songid = args[1]['songid']
    caption = args[1]['caption']
    user = sql.select('accounts', f"auth = '{auth}'")['data'][0]['id']
    sendDict = {
        'userid': user,
        'dt': str(datetime.now()),
        'songid': songid,
        'caption': caption,
        'likes': 0
    }
    return sql.insert('posts', sendDict)

def get_posts():
    args = stripArgs('auth', 'limit')
    if not args[0]:
        return args[1]
    auth = args[1]['auth']
    limit = args[1]['limit']
    id = sql.select('accounts', f"auth = '{auth}'")['data'][0]['id']
    allPosts = []
    queryResult = sql.select('friends', f"userid = {id}")
    if queryResult['type'] == 'error':
        return queryResult
    for userid in queryResult['data']:
        sel = sql.select('posts', f"userid = {userid['following']}")
        if sel['type'] == 'error':
            return sel
        allPosts += sel['data']
    allPosts.sort(key = lambda x: x['dt'])
    allPosts = allPosts[-limit:]
    return success(allPosts)
