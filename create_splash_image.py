#!/usr/bin/env python3

import netifaces as ni
from PIL import Image, ImageDraw, ImageFont

try:
    ip_address = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']
    image_text = f'\\\\{ip_address}\\bilder'
except Exception as e:
    print(e)
    image_text = 'Kein Netzwerk!'

width = 600
height = 1024
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                          size=40)
img = Image.new('RGB', (width, height), color='black')
imgDraw = ImageDraw.Draw(img)
imgDraw.text((10, 10), image_text, font=font, fill=(119, 136, 153))
img2 = img.transpose(Image.Transpose.ROTATE_90)
img2.save('/home/schommer/monisrahmen/sitebin/splash.png')
