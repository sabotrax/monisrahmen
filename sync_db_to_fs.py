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
from tinydb import TinyDB, Query

DEBUG = config('DEBUG', default=False, cast=bool)

db = TinyDB(config('PROJECT_PATH') + '/user_data/db.json')

removal_pending = []
# iterate over db
for picture in db:
    if DEBUG:
        print(picture)

    # is the file matching the entry existing?
    picture_path = config('PROJECT_PATH') + '/pictures'
    filePath = os.path.join(picture_path, picture["filename"])
    if not os.path.isfile(filePath):
        # if not, mark it for removal
        if DEBUG:
            print("file missing: ", picture["filename"])
        removal_pending.append(picture.doc_id)

# remove dangling db entries
if removal_pending:
    if DEBUG:
        print("removal pending")
        print(removal_pending)
    db.remove(doc_ids=removal_pending)
