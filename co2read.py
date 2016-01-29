#!/usr/bin/env python3

import os
import fcntl
import time

key = bytes(8)
hidpath = "/dev/hidraw0"
HIDIOCSFEATURE_9 = 0xC0094806


def open_hid(path=hidpath, key=key):
    hid_fd = os.open(path, os.O_RDWR)
    fcntl.ioctl(hid_fd, HIDIOCSFEATURE_9, b"\x00" + key)
    return hid_fd


def close_hid(hid_fd):
    return os.close(hid_fd)


def decrypt_hid(data):
    cstate = [0x48,  0x74,  0x65,  0x6D,  0x70,  0x39,  0x39,  0x65]
    shuffle = [2, 4, 0, 7, 1, 6, 5, 3]
    
    phase1 = [0] * 8
    for i, o in enumerate(shuffle):
        phase1[o] = data[i]
    
    phase2 = [0] * 8
    for i in range(8):
        phase2[i] = phase1[i] ^ key[i]
    
    phase3 = [0] * 8
    for i in range(8):
        phase3[i] = ( (phase2[i] >> 3) | (phase2[ (i-1+8)%8 ] << 5) ) & 0xff
    
    ctmp = [0] * 8
    for i in range(8):
        ctmp[i] = ( (cstate[i] >> 4) | (cstate[i]<<4) ) & 0xff
    
    out = [0] * 8
    for i in range(8):
        out[i] = (0x100 + phase3[i] - ctmp[i]) & 0xff
    
    if out[4] != 13 or sum(out[:3])&0xFF != out[3]:
        return None
    return tuple(out[:3])


def parse_ans(ans):
    res = {
        "time": int(time.time())
    }
    for i in ans:
        k, v = i[0], i[1] << 8 | i[2]
        if k == 0x50:
            res["co2"] = v
        elif k == 0x42:
            res["temp"] = round(v/16.0-273.15, 2)
    return res


def read_data(hid_fd):
    maxtries = 20
    first_seen = None
    hist = []
    while maxtries:
        maxtries -= 1
        data = os.read(hid_fd, 8)
        ans = decrypt_hid(data)
        if ans is None:
            continue
        if first_seen == ans[0]:
            break
        if not first_seen:
            first_seen = ans[0]
        hist.append(ans)
    res = parse_ans(hist)
    return res


if __name__ == '__main__':
    hid_fd = open_hid(hidpath)
    data = read_data(hid_fd)
    print(data)
    close_hid(hid_fd)
