#!/usr/bin/env python3

# import base64
import config
import email
import imaplib
import os
import re
from PIL import Image

imap = imaplib.IMAP4_SSL(config.email_host, config.email_port)
imap.login(config.email_user, config.email_pass)

imap.select('Inbox')
type, data = imap.search(None, 'ALL')
print("FETCH: ", type)
mail_ids = data[0]
id_list = mail_ids.split()
id_list.reverse()

i = 0
for num in id_list:
    if i == 3:
        break
    typ, data = imap.fetch(num, '(RFC822)')
    # converts byte literal to string removing b''
    raw_email = data[0][1]
    raw_email_string = raw_email.decode('utf-8')
    email_message = email.message_from_string(raw_email_string)
    x = re.search(r'Subject:\s([\w\s]+)\n', str(email_message), re.DOTALL)
    print(x)
    if not x or x.group(1).lower() != config.email_keyword:
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
                    print("image verified")
                    # rotate image because of the portrait orientation of the frame
                    # open twice because of verify()
                    img = Image.open(filePath)
                    img.load()
                    size = img.size
                    img_x, img_y = size[0], size[1]
                    print(f'size: {img_x}x{img_y}')
                    if img_y > img_x:
                        rotated_img = img.transpose(Image.ROTATE_270)
                        rotated_img.save(filePath)
                        print("rotated")
                    img.close()
                except Exception as e:
                    print(e)
                    os.remove(filePath)
    i += 1
    print("deleted email: ", num)
    #imap.store(num, "+FLAGS", "\\Deleted")

imap.expunge()
imap.close()
imap.logout()
