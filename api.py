from matplotlib import markers
import matplotlib
import requests
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker  
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
import time
import json
import discord

async def main(ctx, args):
    if not args:
        curr = "ethereum"
    else:
        curr = args[0]

    if len(args)>1:
        if str(args[1]).lower() in ("*","all"):
            (a,b) = (0, time.time())
        else:
            ss = int(args[1])
            (a,b) = (time.time()-(86400 * ss), time.time())
    else:
        (a,b) = (time.time()-(86400*7), time.time())


    url = "https://api.coingecko.com/api/v3/coins/%s/market_chart/range?vs_currency=eur&from=%s&to=%s" % (curr, a,b)
    response = requests.request("GET", url)
    response.raise_for_status()

    data = json.loads(response.text)

    date = []
    price = []
    vol = []
    cap = []

    #pot = 0

    for x in data['prices']:
        price.append(x[1])
        date.append(x[0])

    for x in data['total_volumes']:
        kek = x[1]

        # pot = np.floor(np.log10(kek))
        # kek = kek / 10**pot

        vol.append(kek)

    # for x in data['market_caps']:
    #     cap.append(x[1]/10**9)

    date_raw = date
    date = pd.to_datetime(date, unit='ms').to_numpy()

    title = curr.upper() + " Stonks - " + time.strftime("%d.%m", time.localtime(a)) + " - " + time.strftime("%d.%m", time.localtime(b))

    t = np.arange(0, len(date))
    trend = np.poly1d(np.polyfit(t, price, 10))

    trend = trend(t)

    fig,ax = plt.subplots()
    ax2=ax.twinx()
    ax3=ax2.twinx()

    stonks = (price[len(price)-1] / price[0] - 1) * 100

    stonks = np.around(stonks, 2)

    if stonks > 0:
        stonks = "+" + str(stonks) + "%"
        color = "green"
    else:
        stonks = str(stonks) + "%"
        color = "red"

    n = 1
    # poi = np.array([])
    # poi = np.append(poi, np.sort((price))[0:n])
    # poi = np.append(poi, np.sort((price))[-n:])

    # poi = poi.tolist()
    # for place, item in enumerate(poi):
    #     poi[place] = price.index(item)


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
    ax.get_yaxis().set_major_formatter(mticker.FormatStrFormatter("%.2f €"))
    ax.grid(b=True, which='both', linestyle="--", linewidth=0.3)


    ax.plot(np.array(np.nan), np.array(np.nan), color="tomato", linewidth=0.5, zorder=0, label="Volume")
    ax.plot(np.array(np.nan), np.array(np.nan), color=color, linewidth=0.8, linestyle=":", label=stonks)
    ax.legend(facecolor='white', framealpha=1)

    # for p in derv:
    #     ax.plot(date[p], price[p], marker=".", color="gold")

    # for p in poi:
    #     ax.plot(date[p], price[p], color="darkorange", marker=".")
    #     ax.text(date[p], price[p], str(np.around(price[p],2))+" €")

    #ax3.get_yaxis().set_major_formatter(mticker.FuncFormatter(lambda x, p: format(int(x), '.')))
    ax3.get_yaxis().set_major_formatter(mticker.FuncFormatter(lambda x, p : f"{int(x):,}".replace(",",".") + " €"))
    ax3.get_xaxis().set_major_formatter(mdates.DateFormatter('%d.%m.%y'))

    #---------------------------------------------------------------------------

    fig.autofmt_xdate()
    plt.title(title)
    plt.tight_layout()
    plt.savefig("tmp.png", dpi=600)
    plt.clf()

    # ..........................................................................

    
    await ctx.send("%s" % ctx.message.author.mention, file=discord.File("tmp.png"))

