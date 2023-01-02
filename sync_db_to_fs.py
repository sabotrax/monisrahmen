#!/usr/bin/env python3

# synchonize database to filesystem

# if a picture has been deleted from the folder,
# its entry is still in the database.
# you could not re-add the picture
# as it would be identified as a duplicate.
# this script removes the dangling db entries

# this script should be run by your user's crontab
# see README.md

import config
import os
from tinydb import TinyDB, Query

db = TinyDB(config.project_path + '/user_data/db.json')

removal_pending = []
# iterate over db
for picture in db:
    # print(picture)

    # is the file matching the entry existing?
    filePath = os.path.join(config.picture_path, picture["filename"])
    if not os.path.isfile(filePath):
        # if not, mark it for removal
        # print("file missing: ", picture["filename"])
        removal_pending.append(picture.doc_id)

# remove dangling db entries
if removal_pending:
    # print(removal_pending)
    db.remove(doc_ids=removal_pending)
