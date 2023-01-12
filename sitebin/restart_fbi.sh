#!/bin/bash

# change according to your installation directory
PROJECT_PATH=/home/schommer/monisrahmen
source ${PROJECT_PATH}/.env

pkill -f /usr/bin/fbi
shopt -s globstar

# remove trigger file
[ -e ${PROJECT_PATH}/site_run/image_added ] && rm ${PROJECT_PATH}/site_run/image_added

cd ${PROJECT_PATH}/pictures
# add file types here
files=(**/*.gif **/*.jpg **/*.png)

/usr/bin/fbi -T 1 -a -t $RELOAD_IMAGE -u --noverbose --blend $BLEND_IMAGE "${files[@]}"
