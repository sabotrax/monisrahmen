#!/usr/bin/env python3

# this script should be run by your user's crontab
# see README.md

import atexit
import config
import RPi.GPIO as GPIO
import subprocess
from time import sleep, time

GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.IN)
GPIO.setup(27, GPIO.OUT)

GPIO.output(27, GPIO.HIGH)


@atexit.register
def goodbye():
    GPIO.cleanup()
    subprocess.run(["/usr/bin/vcgencmd", "display_power",
                    "1", "2"])


def motion_detect():
    motion = GPIO.input(17)
    return motion


if __name__ == "__main__":
    blanked = False
    active = idle = time()
    while True:
        if motion_detect():
            #print("motion detected")
            active = time()
            if blanked:
                subprocess.run(["/usr/bin/vcgencmd", "display_power",
                                "1", "2"])
                blanked = False
        else:
            #print("not much")
            idle = time()
            if not blanked and (idle - active > config.display_timeout):
                #print("blank now")
                subprocess.run(["/usr/bin/vcgencmd", "display_power",
                                "0", "2"])
                blanked = True
        sleep(1)
