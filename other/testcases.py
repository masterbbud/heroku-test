import requests

# NOTES:
# Anything that includes personal data should be a POST call.
# Calling login or signup returns either:
#   If successful, the AUTH token for the specified account (either existing or new)
#   ERROR: SomeMessage if the creation/login failed


token = requests.post('https://masterbbud-python-test.herokuapp.com/login', json={'username': 'onemore', 'password': 'lucy'}).text

print(token)
response = requests.get('https://masterbbud-python-test.herokuapp.com/get-accounts')

print(response.text)

response = requests.post('https://masterbbud-python-test.herokuapp.com/account-data', json={'token': token})

print(response.text)

response = requests.post('https://masterbbud-python-test.herokuapp.com/add-song', json={'token': token})

print(response.text)

response = requests.post('https://masterbbud-python-test.herokuapp.com/create-post', json={'token': token})

print(response.text)

response = requests.post('https://masterbbud-python-test.herokuapp.com/add-song', json={'token': token})

print(response.text)
