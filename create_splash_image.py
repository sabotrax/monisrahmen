#!/usr/bin/env python3

import config
import netifaces as ni
from PIL import Image, ImageDraw, ImageFont

try:
    ip_address = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
    # this path should match with the Samba configuration
    image_text = f'\\\\{ip_address}\\bilder'
except Exception as e:
    print(e)
    image_text = config.network_error

# switched because of the screen rotation
width = config.screen_height
height = config.screen_width

font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                          size=config.font_size)
img = Image.new('RGB', (width, height), color='black')
imgDraw = ImageDraw.Draw(img)
imgDraw.text((10, 10), image_text, font=font, fill=(119, 136, 153))
img_rotated = img.transpose(Image.Transpose.ROTATE_90)
img_rotated.save(config.project_path + '/sitebin/splash.png')
