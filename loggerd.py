#!/usr/bin/env python3

import json
from time import sleep

from co2read import open_hid, close_hid, read_data

hid_fd = open_hid()
with open("/home/user/temp.log", "a") as log:
    while True:
        res = read_data(hid_fd)
        log.write(json.dumps(res, sort_keys=True)+"\n")
        log.flush()

close_hid(hid_fd)
