import requests

response = requests.get('https://masterbbud-python-test.herokuapp.com/sql-test')
print(response.text)

response = requests.get('https://masterbbud-python-test.herokuapp.com/add-song?name=testsong')