import requests

response = requests.get('https://masterbbud-python-test.herokuapp.com/get-test')
print(response.json())