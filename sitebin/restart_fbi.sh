#!/bin/bash

# this script should be run by root's crontab
# see README.md

pkill -f /usr/bin/fbi
shopt -s globstar
# change accordingly to your installation directory
cd /home/schommer/monisrahmen/pictures
# add filetypes here
files=(**/*.jpg **/*.png)
#
# -t seconds - reload interval
# --blend milliseconds - blend time
/usr/bin/fbi -T 1 -m 1024x600 -a -t 30 -u --noverbose --blend 500 "${files[@]}"
