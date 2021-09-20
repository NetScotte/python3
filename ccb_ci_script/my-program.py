# -*- coding: utf-8 -*-
from sys import stdout
from time import sleep

pre = ''
while True:
    with open('shepherd_scripts.log', 'r') as f:
        r = f.read().replace(pre, '')
        print(r)
        stdout.flush()
        pre += r
    sleep(5)
    break
