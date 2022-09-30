from datetime import datetime

from flask import request

from app.accounts import auth_token_used

sql = None

def create_post_request():
    args = request.json
    auth = args.get('auth')
    if not auth:
        return 'ERROR: Request needs auth'
    if not auth_token_used(auth):
        return 'ERROR: Invalid token'
    songid = args.get('songid')
    if not songid:
        return 'ERROR: Request needs songid'
    caption = args.get('caption')
    if not caption:
        return 'ERROR: Request needs caption'
    user = sql.select('accounts', f"auth = '{auth}'")[0]['id']
    createPost(user, songid, caption)

def createPost(user, songid, caption):
    sendDict = {
        'userid': user,
        'dt': str(datetime.now()),
        'songid': songid,
        'caption': caption,
        'likes': 0
    }
    sql.insert('posts', sendDict)
    return 'Created Post'

def get_posts_request():
    args = request.json
    auth = args.get('auth')
    if not auth:
        return 'ERROR: Request needs auth'
    if not auth_token_used(auth):
        return 'ERROR: Invalid token'
    return getPosts(sql.select('accounts', f"auth = '{auth}'")[0]['id'])

def getPosts(id):
    allPosts = []
    queryResult = sql.select('friends', f"user = {id}")
    if isinstance(queryResult, str):
        return queryResult
    for userid in queryResult:
        sel = sql.select('posts', f"userid = {userid['following']}")
        if isinstance(sel, str):
            return sel
        allPosts += sel
    allPosts.sort(key = lambda x: x.dt)
    return allPosts

def getFollowing(id):
    result = sql.read(f'SELECT * FROM friends WHERE user = {id}')
    return [i[2] for i in result]

