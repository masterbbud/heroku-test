import requests

#response = requests.get('https://masterbbud-python-test.herokuapp.com/drop-songs')
#response = requests.get('https://masterbbud-python-test.herokuapp.com/add-song?name=lucyintheskywithdiamonds')
#response = requests.get('https://masterbbud-python-test.herokuapp.com/add-song?name=lucy')
#response = requests.get('https://masterbbud-python-test.herokuapp.com/get-songs')

response = requests.get('https://masterbbud-python-test.herokuapp.com/signup?username=sky&password=diamonds')
print(response.text)

response = requests.get('https://masterbbud-python-test.herokuapp.com/get-accounts')
print(response.text)