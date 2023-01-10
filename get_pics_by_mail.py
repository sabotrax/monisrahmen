#!/usr/bin/env python3

import email
import imaplib
import os
import random
import re
import string
from decouple import config
from email.header import decode_header
from helper import get_hash
from PIL import Image
from time import time
from tinydb import TinyDB, Query

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


class DuplicateImageExeption(Exception):
    "Raised when an image is already existing"
    pass


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
                # verify image
                img = Image.open(filePath)
                img.verify()
                img.close()
                if DEBUG:
                    print("image verified")

                # create image checksum
                hd = get_hash(filePath)
                if DEBUG:
                    print("hexdigest: ", hd)

                # look up checksum
                picture = Query()
                duplicate = db.search(picture.checksum == hd)
                # skip duplicates
                if duplicate:
                    if DEBUG:
                        print("duplicate -> skip!")
                    raise DuplicateImageExeption
                else:
                    if DEBUG:
                        print("unique copy -> kept")

                # write image properties to db
                db.insert({'filename': fileName, 'sender': email_sender,
                           'date': int(time()), 'checksum': hd})

            except Exception as e:
                if DEBUG:
                    print(e)
                os.remove(filePath)
                continue

    if config('DELETE_EMAIL', default=False, cast=bool):
        if DEBUG:
            print("deleted email: ", id)
        imap.store(id, "+FLAGS", "\\Deleted")

imap.expunge()
imap.close()
imap.logout()
