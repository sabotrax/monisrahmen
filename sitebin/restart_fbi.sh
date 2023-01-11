#!/bin/bash

# this script should be run by root's crontab
# see README.md

pkill -f /usr/bin/fbi
shopt -s globstar
# change accordingly to your installation directory
cd /home/schommer/monisrahmen/pictures
# remove trigger file
[ -e ../site_run/image_added ] && rm ../site_run/image_added
# add file types here
files=(**/*.gif **/*.jpg **/*.png)
#
# -t seconds - reload interval
# --blend milliseconds - blend time
/usr/bin/fbi -T 1 -a -t 120 -u --noverbose --blend 500 "${files[@]}"
