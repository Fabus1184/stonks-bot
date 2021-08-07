from discord_webhook import DiscordWebhook
import requests
import json

r = requests.get('https://cex.io/api/last_price/ETH/EUR')

data = {
"content":"**ETH-EUR:** %s€" % json.loads(r.text)['lprice'].replace(".",",")
}

url = 'wbkh'

result = requests.post(url, json=data)

result.raise_for_status()
