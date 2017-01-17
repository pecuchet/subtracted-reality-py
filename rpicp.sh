#!/bin/bash
# copy files to the raspberry pi
 
ip=$1

if [ $# -eq 0 ]; then
    ip=192.168.0.3
fi

rsync . "pi@${ip}:/home/pi/subtracted-reality" -alz --progress --delete --exclude-from=.gitignore
