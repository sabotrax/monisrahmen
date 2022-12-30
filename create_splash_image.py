#!/usr/bin/env python3

import config
import netifaces as ni
from PIL import Image, ImageDraw, ImageFont

try:
    ip_address = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']
    # this path should match with the Samba configuration
    image_text = f'\\\\{ip_address}\\bilder'
except Exception as e:
    print(e)
    image_text = config.network_error

# switched because of portrait mode
width = config.screen_height
height = config.screen_width

font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                          size=config.font_size)
img = Image.new('RGB', (width, height), color='black')
imgDraw = ImageDraw.Draw(img)
imgDraw.text((10, 10), image_text, font=font, fill=(119, 136, 153))
img.save(config.project_path + '/sitebin/splash.png')
