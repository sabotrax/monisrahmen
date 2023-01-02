#!/bin/bash

# this script should be run by root's crontab
# see README.md

# change accordingly to your installation directory
cd /home/schommer/monisrahmen
# wait for network
#sleep 40
bin/python3 create_splash_image.py
/usr/bin/fbi -T 1 -a --noverbose site_data/splash.png &
sleep 20
sitebin/restart_fbi.sh
