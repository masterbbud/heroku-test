from bs4 import BeautifulSoup
import json
import requests

from flask import request

from app.utils import stripArgs, error, success

services = ['spotify', 'itunes', 'youtube', 'tidal', 'amazonMusic', 'soundcloud', 'youtubeMusic']

serviceToId = {service: f'ServiceButton {service} itemLinkButton {service}ItemLinkButton' for service in services}

sql = None

def add_song_request():
    args = stripArgs('url')
    if not args[0]:
        return args[1]
    url = args[1]['url']

    resultDict = getSongData(url)
    if not resultDict:
        return error('Songwhip query failed')

    songid = int(resultDict['id'])
    if not songExists(songid):
        title = resultDict['name']
        artist = resultDict['artists'][0]['name']
        links, img = getLinksAndImage(resultDict['url'])

        if not links or not img:
            return error('Songwhip scraping failed')

        res = createSong(songid, title, artist, img, links)
        if res['type'] == 'error':
            return res

    return success(str(songid))

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
    return sql.insert('songs', sendDict)

def songExists(id):
    res = sql.select('songs', f"id={id}")
    return True if res['type'] != 'error' and res['data'] else False

def getSong(id):
    res = sql.select('songs', f"id={id}")
    if res['type'] == 'success':
        if res['data']:
            return res['data'][0]
    return None
