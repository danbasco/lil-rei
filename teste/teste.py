import requests

link = "https://api.shinobu.host/api/v1/action/kiss"

payload = ""
headers = {}

response = requests.request("GET", link, headers=headers, data=payload)

print(response)