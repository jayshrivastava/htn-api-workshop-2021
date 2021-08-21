import requests

response = requests.post('https://htn-api.jayantsh.repl.co/')
print(response.json())

response = requests.post('https://htn-api.jayantsh.repl.co/0')
print(response.json())