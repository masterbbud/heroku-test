import requests

# NOTES:
# Anything that includes personal data should be a POST call.
# Calling login or signup returns either:
#   If successful, the AUTH token for the specified account (either existing or new)
#   ERROR: SomeMessage if the creation/login failed


def run(query, json):
    # takes a query and runs it and returns data or None if error
    res = requests.post(f'https://masterbbud-python-test.herokuapp.com/{query}', json=json).json()
    print(res)
    if res['type'] == 'error':
        return None
    return res['data']

"""
print(requests.post('https://masterbbud-python-test.herokuapp.com/drop-table', json={'name': 'accounts'}).text)
print(requests.post('https://masterbbud-python-test.herokuapp.com/drop-table', json={'name': 'songs'}).text)
print(requests.post('https://masterbbud-python-test.herokuapp.com/drop-table', json={'name': 'posts'}).text)
print(requests.post('https://masterbbud-python-test.herokuapp.com/drop-table', json={'name': 'friends'}).text)

print(requests.post('https://masterbbud-python-test.herokuapp.com/create-table', json={'name': 'accounts'}).text)
print(requests.post('https://masterbbud-python-test.herokuapp.com/create-table', json={'name': 'songs'}).text)
print(requests.post('https://masterbbud-python-test.herokuapp.com/create-table', json={'name': 'posts'}).text)
print(requests.post('https://masterbbud-python-test.herokuapp.com/create-table', json={'name': 'friends'}).text)
"""

#run('create-table', {'name': 'blocked'})

run('get-table', {'name': 'accounts'})
run('get-table', {'name': 'songs'})
run('get-table', {'name': 'posts'})
run('get-table', {'name': 'friends'})
run('get-table', {'name': 'blocked'})

token = run('login', {'username': 'goodguy', 'password': 'lucy'})
run('get-posts', {'auth': token, 'limit': 10})
run('follow', {'auth': token, ' following': 1})
#songid = run('add-song', {'url': 'https://open.spotify.com/track/6V5iybikF6JLnCqxPpXZit?si=8d9658d2497544ac'})
#run('create-post', {'auth': token, 'songid': songid, 'caption': 'I HAVE COME TO EAT YOUR FAMILY.'})
run('get-posts', {'auth': token, 'limit': 10})
#token = run('login', {'username': 'onemore', 'password': 'lucy'})

#songid = run('add-song', {'url': 'https://open.spotify.com/track/6V5iybikF6JLnCqxPpXZit?si=8d9658d2497544ac'})

#run('create-post', {'auth': token, 'songid': songid, 'caption': 'I HAVE COME TO EAT YOUR FAMILY.'})
#run('get-posts', {'auth': token, 'limit': 2})
