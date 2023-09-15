import requests

url = "https://api.iocparser.com"

payload = {}
headers= {}

response = requests.request("GET", url, headers=headers, data = payload)
print(response.text.encode('utf8'))