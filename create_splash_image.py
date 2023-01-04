#!/usr/bin/env python3

import netifaces as ni
import requests
import time
from decouple import config
from PIL import Image, ImageDraw, ImageFont

DEBUG = config('DEBUG', default=False, cast=bool)

image_text = f"E-Mail: {config('EMAIL_USER')}\n\n"

connected = False

for i in range(11):
    try:
        req = requests.get("https://google.com", timeout=5)
        connected = True
        break
    except (requests.ConnectionError, requests.Timeout):
        time.sleep(5)
        pass

if connected:
    ip_address = ni.ifaddresses(config('NETWORK_DEVICE'))[ni.AF_INET][0]['addr']
    # this path should match with the Samba configuration
    image_text += f'Freigabe: \\\\{ip_address}\\bilder'
else:
    image_text += config('NETWORK_ERROR')

# switched because of portrait mode
width = config('SCREEN_HEIGHT', cast=int)
height = config('SCREEN_WIDTH', cast=int)

font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                          size=config('FONT_SIZE', cast=int))
img = Image.new('RGB', (width, height), color='black')
imgDraw = ImageDraw.Draw(img)
imgDraw.text((10, 10), image_text, font=font, fill=(119, 136, 153))
img.save(config('PROJECT_PATH') + '/site_data/splash.png')
