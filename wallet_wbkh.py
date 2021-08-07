import json
from discord_webhook import DiscordWebhook
import requests
import pickle
from coinbase.wallet.client import Client

TIM_API_SECRET = ""
TIM_API_KEY = ""

LAURUS_API_SECRET = ""
LAURUS_API_KEY = ""

TOM_API_SECRET = ""
TOM_API_KEY = ""

KNAAX_API_SECRET = ""
KNAAX_API_KEY = ""

def swap(string):
    assert string, str
    new = ""
    for k in string:
        if k not in (",","."):
            new += k
        else:
            if k == ",":
                new += "."
            else:
                new += ","
    return new



wallet = {}
wallet['Fabus'] = ""
wallet['Haegiz'] = ""
wallet['Leonard'] = ""

txt = ""
for w in wallet:
    url = "https://api.blockcypher.com/v1/eth/main/addrs/%s/balance" % wallet[w]
    data = requests.get(url)
    data.raise_for_status()
    data = json.loads(data.text)

    parra = data['balance']

    url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=eur"
    data = requests.get(url)
    data.raise_for_status()
    data = json.loads(data.text)

    price = data['ethereum']['eur']

    parra *= 10**-18*price
    txt += ("**%s**: %s€" % (w, swap(str('{:,.2f}'.format(parra))))) + "\n\n"

# COINBASE

client = Client(TIM_API_KEY, TIM_API_SECRET)
parra = float((client.get_account("ETH")["native_balance"]["amount"]))
txt += ("**%s**: %s€" % ("Tim", swap(str('{:,.2f}'.format(parra))))) + "\n\n"

client = Client(LAURUS_API_KEY, LAURUS_API_SECRET)
parra = float((client.get_account("ETH")["native_balance"]["amount"]))
txt += ("**%s**: %s€" % ("Laurus", swap(str('{:,.2f}'.format(parra))))) + "\n\n"

client = Client(TOM_API_KEY, TOM_API_SECRET)
parra = float((client.get_account("ETH")["native_balance"]["amount"]))
txt += ("**%s**: %s€" % ("Tom", swap(str('{:,.2f}'.format(parra))))) + "\n\n"

client = Client(KNAAX_API_KEY, KNAAX_API_SECRET)
parra = float((client.get_account("ETH")["native_balance"]["amount"]))
txt += ("**%s**: %s€" % ("Knaax", swap(str('{:,.2f}'.format(parra))))) + "\n\n"

# ----

url = webhook_url

webhook = DiscordWebhook(url=url, content=txt)

try:
    with open("last.wbhk","rb") as f:
        rm = pickle.load(f)
        webhook.delete(rm)
        f.close()
except:
    pass

response = webhook.execute()

with open("last.wbhk","wb") as f:
    pickle.dump(response, f)
    f.close()
