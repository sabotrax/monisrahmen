#!/bin/bash
pkill -f /usr/bin/fbi
shopt -s globstar
cd /home/schommer/monisrahmen/pictures
files=(**/*.jpg **/*.png)
/usr/bin/fbi -noverbose -T 1 -m 1024x600 -a -t 60 --blend 500 -u "${files[@]}"
