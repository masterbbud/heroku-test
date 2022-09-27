import requests
import json

from sql import SQL

from bs4 import BeautifulSoup

from classes import User, Post

services = ['spotify', 'itunes', 'youtube', 'tidal', 'amazonMusic', 'soundcloud', 'youtubeMusic']

serviceToId = {}
for service in services:
    serviceToId[service] = f'ServiceButton {service} itemLinkButton {service}ItemLinkButton'

sql = SQL('test.sqlite')

def addSong(url):
    resultDict = getSongData(url)

    songid = int(resultDict['id'])
    if sql.songExists(songid):
        return sql.getSong(songid)

    title = resultDict['name']
    artist = resultDict['artists'][0]['name']
    links, img = getLinksAndImage(resultDict['url'])

    sql.addSong(songid, title, artist, img, links)

def getSongData(url):
    res = requests.post('https://songwhip.com/', data=json.dumps({'url': url}))
    try:
        message = res.content.decode('utf-8')
    except Exception:
        print('Failed to get data from server')
    resultDict = json.loads(message)
    return resultDict

def getLinksAndImage(url):
    try:
        songwhipPage = requests.get(url).content
    except Exception:
        print('Failed to get link data for the song')
        return {}

    soup = BeautifulSoup(songwhipPage, "html.parser")

    availableLinks = {}
    for service, id in serviceToId.items():
        obj = soup.find('a', attrs={'data-testid': id})
        if obj:
            link = obj.get('href')
            if link:
                availableLinks[service] = link

    imgsrc = ''
    img = soup.find('div', attrs={'data-testid': 'backgroundImage'})
    if img:
        img = img.findChild('img')
        if img:
            imgsrc = img.get('src')

    return availableLinks, imgsrc

def createUser(username, password):
    # Tries to create a user account. Returns True and the account if successful, returns False and the account if not
    if sql.userExists(username):
        return False, sql.getUser(username)
    sql.createUser(username, password, False)
    return True, sql.getUser(username)

def createPost(userid, songid, caption):
    sql.createPost(userid, songid, caption)

sql.initSongs()
sql.initUsers()
sql.initPosts()
sql.initFriends()

songs = [
    'https://open.spotify.com/track/2nfuaBc2X0uhVSr21HVpdC?si=85be007b69454998',
    'https://open.spotify.com/track/6AzPHXMvAtBmzISu4NhOIm?si=5cc28b75db694c92',
    'https://open.spotify.com/track/7kyiHjkFdmHcYcIJtFAdaF?si=b791af69c8a24d8f',
    'https://open.spotify.com/track/2nfuaBc2X0uhVSr21HVpdC?si=1b10f78f1f1d4166',
    'https://open.spotify.com/track/3gJ3yI4UgOg8lY8EUxrFvO?si=84f65c7957e34b48'
]

for song in songs:
    addSong(song)

for song in sql.read('SELECT * from songs'):
    print(song)

createUser('masterbbud', 'none')

for user in sql.read('SELECT * from users'):
    print(user)

#createPost(sql.read('SELECT * from users')[0][0], sql.read('SELECT * from songs')[0][0], 'Hello')

#for post in sql.read('SELECT * from posts'):
#    print(post)

currentUser = User.create(sql.read('SELECT * from users')[0])
currentUser.post(sql, sql.read('SELECT * from songs')[0][0], 'TestCaption')
currentUser.follow(sql, currentUser.id)
for i in currentUser.getPosts(sql):
    print(i.toString(sql))