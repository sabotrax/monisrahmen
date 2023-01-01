#!/usr/bin/env python3

import config
import email
import hashlib
import imaplib
import os
import random
import re
import string
from email.header import decode_header
from PIL import Image
from time import time
from tinydb import TinyDB, Query

db = TinyDB(config.project_path + '/user_data/db.json')

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


i = 0
for num in id_list:
    if i >= 10:
        break
    typ, data = imap.fetch(num, '(RFC822)')

    msg = email.message_from_bytes(data[0][1])
    # decode the email subject
    email_subject, encoding = decode_header(msg["Subject"])[0]
    if isinstance(email_subject, bytes):
        # if it's a bytes, decode to str
        email_subject = email_subject.decode(encoding)
    print("Subject:", email_subject)
    # check the email subject for the keyword
    if not re.search(rf'{config.email_keyword}', email_subject, re.IGNORECASE):
        print("skip!")
        i += 1
        continue

    # decode email sender
    email_sender, encoding = decode_header(msg.get("From"))[0]
    if isinstance(email_sender, bytes):
        email_sender = email_sender.decode(encoding)
    print("From:", email_sender)

    # converts byte literal to string removing b''
    raw_email = data[0][1]
    raw_email_string = raw_email.decode('utf-8')
    email_message = email.message_from_string(raw_email_string)

    # download attachments
    for part in email_message.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        fileName = part.get_filename()
        if bool(fileName):
            # create image checksum
            raw = part.get_payload(decode=True)
            hashed_raw = hashlib.sha1()
            hashed_raw.update(raw)
            hd = hashed_raw.hexdigest()
            print("digest: ", hd)

            # look up checksum
            picture = Query()
            duplicate = db.search(picture.checksum == hd)
            # skip duplicates
            if duplicate:
                print("duplicate -> skip!")
                i += 1
                continue
            else:
                print("unique copy")

            # create unique file name
            letters = string.ascii_lowercase
            rnd_str = ''.join(random.choice(letters) for i in range(7))
            fileName = f'{rnd_str}-{fileName}'
            print("new file name: ", fileName)
            # skip if the file exists
            # if not os.path.isfile(filePath):

            filePath = os.path.join(config.picture_path, fileName)
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

                # write properties to db
                db.insert({'filename': fileName, 'sender': email_sender,
                           'date': int(time()), 'checksum': hd})

            except Exception as e:
                print(e)
                os.remove(filePath)
                i += 1
                continue

    i += 1
    if config.delete_email:
        print("deleted email: ", num)
        imap.store(num, "+FLAGS", "\\Deleted")

imap.expunge()
imap.close()
imap.logout()
