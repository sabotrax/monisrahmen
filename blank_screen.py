#!/usr/bin/env python3

# this script should be run by your user's crontab
# see README.md

import atexit
import config
import RPi.GPIO as GPIO
import subprocess
from time import sleep, time

GPIO.setmode(GPIO.BCM)

# motion sensor
GPIO.setup(17, GPIO.IN)
GPIO.setup(27, GPIO.OUT)

# enable motion sensor
GPIO.output(27, GPIO.HIGH)

# display brightness pwm
GPIO.setup(18, GPIO.OUT)
dim = GPIO.PWM(18, 1000)


@atexit.register
def goodbye():
    GPIO.cleanup()
    subprocess.run(["/usr/bin/vcgencmd", "display_power",
                    "1", "2"])


def motion_detect():
    motion = GPIO.input(17)
    return motion


def dim_display(mode):
    if mode == "off":
        dim.start(0)
        for duty in range(0, 101, 1):
            dim.ChangeDutyCycle(duty)
            sleep(0.01)
        sleep(0.5)
    else:
        dim.start(100)
        for duty in range(100, -1, -1):
            dim.ChangeDutyCycle(duty)
            sleep(0.01)
        sleep(0.5)


if __name__ == "__main__":
    blanked = False
    active = idle = time()
    while True:
        if motion_detect():
            # print("motion detected")
            active = time()
            if blanked:
                subprocess.run(["/usr/bin/vcgencmd", "display_power",
                                "1", "2"])
                dim_display("on")
                blanked = False
        else:
            # print("not much")
            idle = time()
            if not blanked and (idle - active > config.display_timeout):
                # print("blank now")
                dim_display("off")
                subprocess.run(["/usr/bin/vcgencmd", "display_power",
                                "0", "2"])
                blanked = True
        sleep(1)
