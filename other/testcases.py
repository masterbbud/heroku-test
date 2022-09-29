import requests

#response = requests.get('https://masterbbud-python-test.herokuapp.com/drop-songs')
#response = requests.get('https://masterbbud-python-test.herokuapp.com/add-song?name=lucyintheskywithdiamonds')
response = requests.get('https://masterbbud-python-test.herokuapp.com/add-song?name=lucy')
response = requests.get('https://masterbbud-python-test.herokuapp.com/get-songs')

print(response.text)