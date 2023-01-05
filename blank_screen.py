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
from time import sleep, time

DEBUG = config('DEBUG', default=False, cast=bool)

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


def is_monitoring():
    monitor = False

    try:
        from_hour, from_minute = config('START_MONITORING', default="").split(":")
        to_hour, to_minute = config('END_MONITORING', default="").split(":")
    except ValueError:
        return monitor

    try:
        from_hour = abs(int(from_hour))
        to_hour = abs(int(to_hour))
        from_minute = abs(int(from_minute))
        to_minute = abs(int(to_minute))
    except Exception as e:
        print(e)
        return monitor

    now = datetime.now()
    this_hour = now.hour
    this_minute = now.minute
    print(f'now: {this_hour}:{this_minute}')

    if from_hour == 24:
        from_hour = 0
    if (from_hour != to_hour) and to_minute == 0:
        to_minute = 60
    if from_hour <= to_hour:
        if from_hour < this_hour < to_hour:
            monitor = True
        elif from_hour == this_hour:
            if from_minute <= this_minute < to_minute:
                monitor = True
    else:
        if from_hour <= this_hour < 24 or 0 <= this_hour < to_hour:
            monitor = True
        elif from_hour == this_hour:
            if from_minute <= this_minute < to_minute:
                monitor = True

    return monitor


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
    while True:
        if motion_detect():
            if DEBUG:
                print("motion detected")
            active = time()
            if blanked:
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
        else:
            if DEBUG:
                print("not much")
            idle = time()
            if not blanked and (idle - active > config('DISPLAY_TIMEOUT', cast=int)):
                if DEBUG:
                    print("blank now")
                dim_display("off")
                subprocess.run(["/usr/bin/vcgencmd", "display_power",
                                "0", "2"])
                blanked = True
        sleep(1)
