import requests

# NOTES:
# Anything that includes personal data should be a POST call.
# Calling login or signup returns either:
#   If successful, the AUTH token for the specified account (either existing or new)
#   ERROR: SomeMessage if the creation/login failed

print(requests.post('https://masterbbud-python-test.herokuapp.com/create-table', json={'name': 'posts'}).text)
print(requests.post('https://masterbbud-python-test.herokuapp.com/create-table', json={'name': 'friends'}).text)

print(requests.post('https://masterbbud-python-test.herokuapp.com/get-table', json={'name': 'posts'}).text)
print(requests.post('https://masterbbud-python-test.herokuapp.com/get-table', json={'name': 'friends'}).text)

token = requests.post('https://masterbbud-python-test.herokuapp.com/login', json={'username': 'onemore', 'password': 'lucy'}).text

print(token)
response = requests.get('https://masterbbud-python-test.herokuapp.com/get-accounts')

print(response.text)

response = requests.post('https://masterbbud-python-test.herokuapp.com/account-data', json={'token': token})

print(response.text)

song = requests.post('https://masterbbud-python-test.herokuapp.com/add-song', json={'url': 'https://open.spotify.com/track/6V5iybikF6JLnCqxPpXZit?si=8d9658d2497544ac'}).text
print(song)

response = requests.post('https://masterbbud-python-test.herokuapp.com/create-post', json={'auth': token, 'songid': song, 'caption': 'This is a post.'})

print(response.text)

response = requests.post('https://masterbbud-python-test.herokuapp.com/follow', json={'auth': token, 'following': 2})

print(response.text)

response = requests.post('https://masterbbud-python-test.herokuapp.com/get-posts', json={'auth': token})

print(response.text)

