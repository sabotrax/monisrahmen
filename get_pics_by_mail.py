#!/usr/bin/env python3

import base64
import config
import email
import imaplib
import os

mail = imaplib.IMAP4_SSL(config.email_host, 993)
mail.login(config.email_user, config.email_pass)

mail.select('Inbox')
type, data = mail.search(None, 'ALL')
print("FETCH: ", type)
mail_ids = data[0]
#print(mail_ids)
id_list = mail_ids.split()
id_list.reverse()
#print(id_list)

#exit()

i = 0
#for num in data[0].split():
for num in id_list:
    typ, data = mail.fetch(num, '(RFC822)' )
    raw_email = data[0][1] # converts byte literal to string removing b''
    raw_email_string = raw_email.decode('utf-8')
    email_message = email.message_from_string(raw_email_string)

    # downloading attachments
    for part in email_message.walk():
        # this part comes from the snipped I don't understand yet...
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        fileName = part.get_filename()
        if bool(fileName):
            filePath = os.path.join(config.picture_path, fileName)
            if not os.path.isfile(filePath):
                fp = open(filePath, 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()
                subject = str(email_message).split("Subject: ", 1)[1].split("\nTo:", 1)[0]
                #print('Downloaded "{file}" from email titled "{subject}" with UID {uid}.'.format(file=fileName, subject=subject, uid=latest_email_uid.decode('utf-8')))
                #print('Downloaded "{file}" from email titled "{subject}".'.format(file=fileName, subject=subject))
    if i == 3:
        break
    else:
        i += 1
