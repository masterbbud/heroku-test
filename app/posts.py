from datetime import datetime

from flask import request

sql = None

def create_post_request():
    args = request.json
    auth = args.get('auth')
    if not auth:
        return 'ERROR: Request needs auth'
    songid = args.get('songid')
    if not songid:
        return 'ERROR: Request needs songid'
    caption = args.get('caption')
    if not caption:
        return 'ERROR: Request needs caption'
    user = sql.select('accounts', f"auth = '{auth}'")['id']
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

def get_posts_request():
    args = request.json
    auth = args.get('auth')
    if not auth:
        return 'ERROR: Request needs auth'
    getPosts(sql.select('accounts', f"auth = '{auth}'")['id'])

def getPosts(id):
    allPosts = []
    for userid in sql.select('friends', f"user = {id}"):
        allPosts += sql.select('posts', f"userid = {userid['following']}")
    allPosts.sort(key = lambda x: x.dt)
    return allPosts

def getFollowing(id):
    result = sql.read(f'SELECT * FROM friends WHERE user = {id}')
    return [i[2] for i in result]

