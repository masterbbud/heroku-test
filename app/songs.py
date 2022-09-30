from bs4 import BeautifulSoup
import json
import requests

from flask import request

services = ['spotify', 'itunes', 'youtube', 'tidal', 'amazonMusic', 'soundcloud', 'youtubeMusic']

serviceToId = {service: f'ServiceButton {service} itemLinkButton {service}ItemLinkButton' for service in services}

sql = None

def add_song_request():
    args = request.json
    url = args.get('url')
    if not url:
        return 'ERROR: Request needs url'
    return addSong(url)

def addSong(url):
    resultDict = getSongData(url)
    if not resultDict:
        return 'ERROR: Songwhip query failed'

    songid = int(resultDict['id'])
    if songExists(songid):
        return str(songid)

    title = resultDict['name']
    artist = resultDict['artists'][0]['name']
    links, img = getLinksAndImage(resultDict['url'])

    if not links or not img:
        return 'ERROR: Songwhip scraping failed'

    createSong(songid, title, artist, img, links)
    return str(songid)

def getSongData(url):
    res = requests.post('https://songwhip.com/', data=json.dumps({'url': url}))
    try:
        message = res.content.decode('utf-8')
    except Exception:
        return None
    resultDict = json.loads(message)
    return resultDict

def getLinksAndImage(url):
    try:
        songwhipPage = requests.get(url).content
    except Exception:
        return None, None

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

def createSong(songid, title, artist, img, links):
    sendDict = {
        'id': songid,
        'title': title,
        'artist': artist,
        'image': img
    }
    for i in services:
        if i in links:
            sendDict.update({i: links[i]})
    sql.insert('songs', sendDict)

def songExists(id):
    return True if sql.select('songs', f"id={id}") else False

def getSong(id):
    res = sql.select('songs', f"id={id}")
    if res:
        return res[0]
    return None