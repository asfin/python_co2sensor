#!/usr/bin/env python3

import json
import datetime
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from time import sleep

def get_data():
    data_path = "/home/user/temp.log"
    # 30000 ~ 1 day of measurements
    raw = [json.loads(line) for line in open(data_path, "r").readlines()[-30000:]]

    from_ts = int((datetime.datetime.now() - datetime.timedelta(hours=4)).timestamp())
    #data = {i["time"]:{"co2": i["co2"], "temp": i["temp"]} for i in raw if i["time"] > from_ts}
    data = [i for i in raw if i["time"] > from_ts]
    return data

def update_data():
    global dates, co2, temp
    data = get_data()

    dates = [datetime.datetime.fromtimestamp(i["time"]) for i in data]
    co2   = [i["co2"]  for i in data]
    temp  = [i["temp"] for i in data]

update_data()

fig, ax1 = plt.subplots()
ax2 = ax1.twinx()


#ax1.plot_date(x=dates, y=co2, fmt='b-')
#ax2.plot_date(x=dates, y=temp, fmt='r-')

def animate(i):
    print(i)
    update_data()
    ax1.cla()
    ax2.cla()
    plt.title("Last updated: {0:s}".format(dates[-1].ctime()))
    ax1.set_ylim([370, 1100])
    ax2.set_ylim([0, 40])

    l1, = ax1.plot_date(x=dates, y=co2, fmt='b-', label="co2 ({0:d})".format(co2[-1]))
    l2, = ax2.plot_date(x=dates, y=temp, fmt='r-', label="temp ({0:4.1f})".format(temp[-1]))

    plt.legend([l1, l2], [l1.get_label(), l2.get_label()])

    fig.savefig("/var/www/localhost/co2.png")

ani = animation.FuncAnimation(fig, animate, interval=17000)

plt.show()
