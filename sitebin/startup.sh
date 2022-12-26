#!/bin/bash

# this script should be run by root's crontab
# see README.md

# change this path according to your installation
cd /home/schommer/monisrahmen
# wait for network
sleep 20
bin/python3 create_splash_image.py
/usr/bin/fbi -T 1 -a --noverbose sitebin/splash.png &
sleep 20
sitebin/restart_fbi.sh