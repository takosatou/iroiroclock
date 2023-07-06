#!/usr/bin/bash

cd /home/pi/src/iroiroclock
/usr/bin/nohup /usr/bin/python3 iroiroclock.py >/dev/null 2>&1 &

