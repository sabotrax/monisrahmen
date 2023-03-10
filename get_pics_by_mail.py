#!/usr/bin/env python3

import email
import imaplib
import os
import random
import re
import string
from decouple import config
from email.header import decode_header
from helper import validate_picture, DuplicateImageExeption
from pathlib import Path
from PIL import UnidentifiedImageError
from time import time
from tinydb import TinyDB

DEBUG = config('DEBUG', default=False, cast=bool)

db = TinyDB(config('PROJECT_PATH') + '/user_data/db.json')

imap = imaplib.IMAP4_SSL(config('EMAIL_HOST'), config('EMAIL_PORT',
                                                      default=993, cast=int))
imap.login(config('EMAIL_USER'), config('EMAIL_PASS'))

imap.select(config('EMAIL_INBOX'))
type, data = imap.search(None, 'ALL')
if DEBUG:
    print("FETCH: ", type)
mail_ids = data[0]
id_list = mail_ids.split()
id_list.reverse()
image_added = False

for i, id in enumerate(id_list):
    if DEBUG:
        print("counter: ", i)
    if i == config('FETCH_EMAIL', cast=int):
        if DEBUG:
            print("bye!")
        break

    typ, data = imap.fetch(id, '(RFC822)')
    msg = email.message_from_bytes(data[0][1])

    # decode the email subject
    email_subject, encoding = decode_header(msg["Subject"])[0]
    if isinstance(email_subject, bytes):
        # if it's a bytes, decode to str
        email_subject = email_subject.decode(encoding or 'utf8')
    if DEBUG:
        print("Subject:", email_subject)
    # check the email subject for the keyword
    email_keyword = config('EMAIL_KEYWORD')
    if not re.search(rf'{email_keyword}', email_subject, re.IGNORECASE):
        if DEBUG:
            print("skip!")
        continue

    # decode email sender
    email_sender, encoding = decode_header(msg.get("From"))[0]
    if isinstance(email_sender, bytes):
        email_sender = email_sender.decode(encoding)
    if DEBUG:
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
            raw = part.get_payload(decode=True)

            # create unique file name
            letters = string.ascii_lowercase
            rnd_str = ''.join(random.choice(letters) for i in range(7))
            fileName = f'{rnd_str}-{fileName}'
            if DEBUG:
                print("new file name: ", fileName)

            # save file (for now)
            picture_path = config('PROJECT_PATH') + '/pictures'
            filePath = os.path.join(picture_path, fileName)
            fp = open(filePath, 'wb')
            fp.write(part.get_payload(decode=True))
            fp.close()
            if DEBUG:
                print("attachment: ", filePath)

            try:
                # verify picture and check for duplicate
                hd = validate_picture(filePath)

                # write image properties to db
                db.insert({'filename': fileName, 'sender': email_sender,
                           'date': int(time()), 'checksum': hd})

                image_added = True

            except DuplicateImageExeption:
                if DEBUG:
                    print("duplicate --> skip!")
                os.remove(filePath)
                pass
            except UnidentifiedImageError:
                if DEBUG:
                    print("unkown file: ", fileName)
                os.remove(filePath)
                pass

    if config('DELETE_EMAIL', default=False, cast=bool):
        if DEBUG:
            print("deleted email: ", id)
        imap.store(id, "+FLAGS", "\\Deleted")

# trigger fbi restart
if image_added:
    Path(config('PROJECT_PATH') + '/site_run/image_added').touch(exist_ok=True)

imap.expunge()
imap.close()
imap.logout()
