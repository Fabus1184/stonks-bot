from matplotlib import markers
import requests
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker  
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
import time
import json
from discord_webhook import DiscordWebhook

(a,b) = (time.time()-604800, time.time())

url = "https://api.coingecko.com/api/v3/coins/ethereum/market_chart/range?vs_currency=eur&from=%s&to=%s" % (a,b)
response = requests.request("GET", url)

data = json.loads(response.text)

date = []
price = []
vol = []
cap = []

for x in data['prices']:
    price.append(x[1])
    date.append(x[0])

for x in data['total_volumes']:
    vol.append(x[1]/10**9)

# for x in data['market_caps']:
#     cap.append(x[1]/10**9)

date_raw = date
date = pd.to_datetime(date, unit='ms').to_numpy()

title = "ETH Stonks - " + time.strftime("%d.%m", time.localtime(a)) + " - " + time.strftime("%d.%m", time.localtime(b))

t = np.arange(0, len(date))
trend = np.poly1d(np.polyfit(t, price, 10))

trend = trend(t)

fig,ax = plt.subplots()
ax2=ax.twinx()
ax3=ax2.twinx()

stonks = (1-(trend[0]/trend[len(trend)-1])) * 100
stonks = np.around(stonks, 2)

if stonks > 0:
    stonks = "+" + str(stonks) + "%"
    color = "green"
else:
    stonks = str(stonks) + "%"
    color = "red"

n = 1
poi = np.array([])
poi = np.append(poi, np.sort((price))[0:n])
poi = np.append(poi, np.sort((price))[-n:])

poi = poi.tolist()
for place, item in enumerate(poi):
    poi[place] = price.index(item)


n = 3
derv = np.array([])
derv = np.append(derv, np.sort(np.diff(price))[0:n])
derv = np.append(derv, np.sort(np.diff(price))[-n:])

derv = derv.tolist()
for place, item in enumerate(derv):
    derv[place] = np.diff(price).tolist().index(item)



#---------------------------------------------------------------------------
ax3.plot(date, vol, color="tomato", linewidth=0.5, zorder=0, label="Volume" )
ax3.set_ylabel("", color="tomato",fontsize=14)
#---------------------------------------------------------------------------

ax2.plot(date, trend, color=color, linewidth=0.8, linestyle=":", label=stonks)
ax2.get_yaxis().set_visible(False)
#---------------------------------------------------------------------------

ax.plot(date, price, color="cornflowerblue", linewidth=0.7, label="Preis")
ax.set_ylabel("", color="cornflowerblue", fontsize=14)
ax.get_yaxis().set_major_formatter(mticker.FormatStrFormatter('%i €'))
ax.grid(b=True, which='both', linestyle="--", linewidth=0.3)


ax.plot(np.array(np.nan), np.array(np.nan), color="tomato", linewidth=0.5, zorder=0, label="Volume")
ax.plot(np.array(np.nan), np.array(np.nan), color=color, linewidth=0.8, linestyle=":", label=stonks)
ax.legend()

# for p in derv:
#     ax.plot(date[p], price[p], marker=".", color="gold")

for p in poi:
    ax.plot(date[p], price[p], color="darkorange", marker=".")
    ax.text(date[p], price[p], str(int(price[p]))+"€")

ax3.get_yaxis().set_major_formatter(mticker.FormatStrFormatter('%i Mrd. €'))
ax3.get_xaxis().set_major_formatter(mdates.DateFormatter('%A'))

#---------------------------------------------------------------------------

fig.autofmt_xdate()
plt.title(title)
plt.tight_layout()
plt.savefig("tmp.png", dpi=600)
plt.clf()

# ..........................................................................

url = "https://discord.com/api/webhooks/841014352899211304/tvk7zRL9n9r8HsPL8KvVoF5V7HZxVYa5PcZ-3l_1p6PioJ26d5pw3pvzyBAvdCvaDr5p"

webhook = DiscordWebhook(url=url)

with open("tmp.png", "rb") as f:
    webhook.add_file(file=f.read(), filename='tmp.png')

response = webhook.execute()