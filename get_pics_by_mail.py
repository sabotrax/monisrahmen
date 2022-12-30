#!/usr/bin/env python3

# import base64
import config
import email
import imaplib
import os
import random
import re
import string
from datetime import datetime
from PIL import Image

imap = imaplib.IMAP4_SSL(config.email_host, config.email_port)
imap.login(config.email_user, config.email_pass)

imap.select(config.email_inbox)
type, data = imap.search(None, 'ALL')
print("FETCH: ", type)
mail_ids = data[0]
id_list = mail_ids.split()
id_list.reverse()


# rotate image
# currently unused
def process_image(filePath):
    # rotate image because of the
    # portrait orientation of the frame
    # open twice because of verify()
    img = Image.open(filePath)
    img.load()
    size = img.size
    img_x, img_y = size[0], size[1]
    print(f'size: {img_x}x{img_y}')
    rotated_img = img.transpose(Image.Transpose.ROTATE_90)
    rotated_img.save(filePath)
    img.close()
    print("image rotated")


# create a useful file name
# currently unused
def create_filename(email_message):
    match = re.search(r'From:\s.*<(\S+@\S+)>\n', str(email_message))
    print(match)
    if match:
        filename = re.sub(r'[^\w]', '_', match.group(1))
        now = datetime.now()
        filename += now.strftime("-%Y%m%d-%H%M-")
        letters = string.ascii_lowercase
        rnd_str = ''.join(random.choice(letters) for i in range(5))
        filename += rnd_str
        return filename


i = 0
for num in id_list:
    if i >= 3:
        break
    typ, data = imap.fetch(num, '(RFC822)')
    # converts byte literal to string removing b''
    raw_email = data[0][1]
    raw_email_string = raw_email.decode('utf-8')
    email_message = email.message_from_string(raw_email_string)
    # check the email subject for the keyword
    match = re.search(r'Subject:\s([\w\s]+)\n', str(email_message), re.DOTALL)
    print(match)
    if not match or match.group(1).lower() != config.email_keyword:
        print("skip!")
        i += 1
        continue
    # download attachments
    for part in email_message.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        fileName = part.get_filename()
        if bool(fileName):
            filePath = os.path.join(config.picture_path, fileName)
            # skip if the file exists
            if not os.path.isfile(filePath):
                fp = open(filePath, 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()
                print("attachment: ", filePath)
                try:
                    # verify image
                    img = Image.open(filePath)
                    img.verify()
                    img.close()
                    print("image verified")
                except Exception as e:
                    print(e)
                    os.remove(filePath)
                    i += 1
                    continue

                #process_image(filePath)
    i += 1
    print("deleted email: ", num)
    #imap.store(num, "+FLAGS", "\\Deleted")

imap.expunge()
imap.close()
imap.logout()
