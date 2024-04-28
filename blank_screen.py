#!/usr/bin/env python3

# this script should be run by your user's crontab
# see README.md

import atexit
import RPi.GPIO as GPIO
import smtplib
import ssl
import subprocess
from datetime import datetime
from decouple import config
from email.message import EmailMessage
from helper import in_between_days
from time import sleep, time

DEBUG = config('DEBUG', default=False, cast=bool)
ms = config('MOTION_SENSOR')

GPIO.setmode(GPIO.BCM)

# Motion sensor
GPIO.setup(17, GPIO.IN)

if ms == "RCWL-0516":
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


def send_mail():
    msg = EmailMessage()
    msg.set_content("The body of the email is here")
    msg["Subject"] = "An Email Alert"
    msg["From"] = "from@example.com"
    msg["To"] = "to@example.com"

    context = ssl.create_default_context()

    with smtplib.SMTP("mail.example.com", port=587) as smtp:
        smtp.starttls(context=context)
        smtp.login("from@example.com", "secretpassword")
        smtp.send_message(msg)


if __name__ == "__main__":
    blanked = False
    active = idle = time()
    send_alert = False
    i = 0
    while True:
        if motion_detect():
            if DEBUG:
                print("motion detected")
            i = 0
            active = time()
            if blanked:
                # only unblank the display when not during off-hours
                if not in_between_days(config('START_DISPLAY_OFF'),
                                       config('END_DISPLAY_OFF')):
                    subprocess.run(["/usr/bin/vcgencmd", "display_power",
                                    "1", "2"])
                    dim_display("on")
                    blanked = False
                    #now = datetime.now()
                    #if not send_alert and (start_monitoring <= now <=
                                        #end_monitoring):
                        #print("send mail")
                        #send_mail()
                        #send_alert = True
                elif DEBUG:
                    print("off-hours")
        else:
            if DEBUG:
                if blanked:
                    print("blanked")
                else:
                    print(f"wait for it: {i}/{config('DISPLAY_TIMEOUT')}")
                    i += 1
            idle = time()
            if not blanked and (idle - active > config('DISPLAY_TIMEOUT',
                                                       cast=int)):
                if DEBUG:
                    print("blank now")
                dim_display("off")
                subprocess.run(["/usr/bin/vcgencmd", "display_power",
                                "0", "2"])
                blanked = True
        sleep(1)
