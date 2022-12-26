#!/bin/bash

# this script should be run by root's crontab
# see README.md

pkill -f /usr/bin/fbi
shopt -s globstar
# change this path according to your installation
cd /home/schommer/monisrahmen/pictures
files=(**/*.jpg **/*.png)
#
# -t seconds - load interval
# --blend milliseconds - blend time
/usr/bin/fbi -T 1 -m 1024x600 -a -t 30 -u --noverbose --blend 500 "${files[@]}"
