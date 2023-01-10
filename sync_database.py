#!/usr/bin/env python3

# synchonize database to filesystem

# if a picture has been deleted from the folder,
# its entry is still in the database.
# you could not re-add the picture
# as it would be identified as a duplicate.
# this script removes the dangling db entries

# this script should be run by your user's crontab
# see README.md

import os
from decouple import config
from helper import validate_picture, DuplicateImageExeption, subtract_arrays
from PIL import UnidentifiedImageError
from time import time
from tinydb import TinyDB

DEBUG = config('DEBUG', default=False, cast=bool)

db = TinyDB(config('PROJECT_PATH') + '/user_data/db.json')

# first part: sync db to fs
removal_pending = []
db_pictures = []
# iterate over db
for picture in db:
    # is the file matching the entry existing?
    picture_path = config('PROJECT_PATH') + '/pictures'
    filePath = os.path.join(picture_path, picture["filename"])
    if not os.path.isfile(filePath):
        # if not, mark it for removal
        if DEBUG:
            print("file missing: ", picture["filename"])
        removal_pending.append(picture.doc_id)
    else:
        # otherwise keep them for the second part
        db_pictures.append(picture["filename"])

# remove dangling db entries
if removal_pending:
    if DEBUG:
        print("removal pending")
        print(removal_pending)
    db.remove(doc_ids=removal_pending)

if DEBUG:
    print("part one done")

# second part: sync fs to db
if DEBUG:
    print("db count:", len(db_pictures))

# read directory
fs_files = []
picture_path = config('PROJECT_PATH') + '/pictures'
for entry in os.listdir(picture_path):
    if os.path.isfile(os.path.join(picture_path, entry)):
        fs_files.append(entry)
print("fs count:", len(fs_files))

# remove duplicates
fs_files = subtract_arrays(db_pictures, fs_files)
print("rest: ", len(fs_files))
now = int(time())
for fileName in fs_files:
    try:
        picture_path = config('PROJECT_PATH') + '/pictures'
        filePath = os.path.join(picture_path, fileName)
        # verify picture and check for duplicate
        hd = validate_picture(filePath)

        # write properties to db
        db.insert({'filename': fileName, 'sender': config('UNKNOWN_SENDER'),
                    'date': now, 'checksum': hd})
    except DuplicateImageExeption:
        if DEBUG:
            print("duplicate --> skip!")
        os.remove(filePath)
        pass
    except UnidentifiedImageError:
        if DEBUG:
            print("unkown file: ", fileName)
        pass

if DEBUG:
    print("part two done")
