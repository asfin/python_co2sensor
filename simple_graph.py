#!/usr/bin/env python3

import json
from datetime import datetime
import matplotlib.pyplot as plt

data_path = "/home/user/temp.log"

data = [json.loads(line) for line in open(data_path, "r").readlines()]

dates = [datetime.fromtimestamp(i["time"]) for i in data]
co2   = [i["co2"]  for i in data]
temp  = [i["temp"] for i in data]

fig, ax1 = plt.subplots()
ax2 = ax1.twinx()

ax1.set_ylim([370, 1100])
ax2.set_ylim([0, 40])

ax1.plot_date(x=dates, y=co2, fmt='b-')
ax2.plot_date(x=dates, y=temp, fmt='r-')

plt.show()
