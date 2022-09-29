import requests

# NOTES:
# Anything that includes personal data should be a POST call.
# Calling login or signup returns either:
#   If successful, the AUTH token for the specified account (either existing or new)
#   ERROR: SomeMessage if the creation/login failed


response = requests.get('https://masterbbud-python-test.herokuapp.com/create-accounts')

print(response.text)
token = requests.post('https://masterbbud-python-test.herokuapp.com/login', json={'username': 'anotheruser', 'password': 'lucy'}).text

print(token)
response = requests.get('https://masterbbud-python-test.herokuapp.com/get-accounts')

print(response.text)

response = requests.post('https://masterbbud-python-test.herokuapp.com/account-data', json={'token': token})

print(response.text)
