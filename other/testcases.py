import requests

#response = requests.get('https://masterbbud-python-test.herokuapp.com/drop-songs')
#response = requests.get('https://masterbbud-python-test.herokuapp.com/add-song?name=lucyintheskywithdiamonds')
#response = requests.get('https://masterbbud-python-test.herokuapp.com/add-song?name=lucy')
#response = requests.get('https://masterbbud-python-test.herokuapp.com/get-songs')



response = requests.get('https://masterbbud-python-test.herokuapp.com/create-accounts')

print(response.text)
token = requests.post('https://masterbbud-python-test.herokuapp.com/signup', json={'username': 'betteruser', 'password': 'lucy'}).text

print(token)
response = requests.get('https://masterbbud-python-test.herokuapp.com/get-accounts')

print(response.text)

response = requests.post('https://masterbbud-python-test.herokuapp.com/get-account-data', json={'token': token})

print(response.text)
