import requests
url="https://valorant-api.com/v1/agents"
response = requests.get(url)
data = response.json()
for agent in data['data'][:3]:
    print(agent['displayName'])