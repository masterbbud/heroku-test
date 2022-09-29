import requests

#response = requests.get('https://masterbbud-python-test.herokuapp.com/drop-songs')
#response = requests.get('https://masterbbud-python-test.herokuapp.com/add-song?name=lucyintheskywithdiamonds')
#response = requests.get('https://masterbbud-python-test.herokuapp.com/add-song?name=lucy')
#response = requests.get('https://masterbbud-python-test.herokuapp.com/get-songs')



response = requests.get('https://masterbbud-python-test.herokuapp.com/create-accounts')

print(response.text)
response = requests.get('https://masterbbud-python-test.herokuapp.com/sql-tables')

print(response.text)
response = requests.post('https://masterbbud-python-test.herokuapp.com/signup', json={'username': 'newuser', 'password': 'lucy'})

print(response.text)
response = requests.get('https://masterbbud-python-test.herokuapp.com/sql-tables')

print(response.text)
response = requests.get('https://masterbbud-python-test.herokuapp.com/get-accounts')

print(response.text)
response = requests.get('https://masterbbud-python-test.herokuapp.com/sql-tables')

print(response.text)

#response = requests.get('https://masterbbud-python-test.herokuapp.com/test-login')
#print(response.text)

quit()
response = requests.get('https://masterbbud-python-test.herokuapp.com/signup?username=sky&password=diamonds')
print(response.text)

response = requests.get('https://masterbbud-python-test.herokuapp.com/get-accounts')
print(response.text)