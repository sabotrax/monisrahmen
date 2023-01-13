import hashlib
import os
from datetime import datetime
from decouple import config
from PIL import Image, UnidentifiedImageError
from tinydb import TinyDB, Query

DEBUG = config('DEBUG', default=False, cast=bool)

db = TinyDB(config('PROJECT_PATH') + '/user_data/db.json')


class DuplicateImageExeption(Exception):
    "Raised when an image is already existing"
    pass


# courtesy of ChatGPT
def count_files(directory):
    return len([f for f in os.listdir(directory) if not f.startswith('.')])


def get_hash(img_path):
    # This function will return the `md5` checksum for any input image.
    with open(img_path, "rb") as f:
        img_hash = hashlib.md5()
        while chunk := f.read(8192):
            img_hash.update(chunk)
    return img_hash.hexdigest()


# that's not a good function name
# but I like The Cure
def in_between_days(start, end):
    in_between = False

    try:
        from_hour, from_minute = start.split(":")
        to_hour, to_minute = end.split(":")
    except ValueError:
        return in_between

    try:
        from_hour = abs(int(from_hour))
        to_hour = abs(int(to_hour))
        from_minute = abs(int(from_minute))
        to_minute = abs(int(to_minute))
    except Exception as e:
        print(e)
        return in_between

    now = datetime.now()
    this_hour = now.hour
    this_minute = now.minute
    if DEBUG:
        print(f'now: {this_hour}:{this_minute}')

    if from_hour == 24:
        from_hour = 0
    if (from_hour != to_hour) and to_minute == 0:
        to_minute = 60
    if from_hour <= to_hour:
        if from_hour < this_hour < to_hour:
            in_between = True
        elif from_hour == this_hour:
            if from_minute <= this_minute < to_minute:
                in_between = True
    else:
        if from_hour <= this_hour < 24 or 0 <= this_hour < to_hour:
            in_between = True
        elif from_hour == this_hour:
            if from_minute <= this_minute < to_minute:
                in_between = True

    return in_between


def subtract_arrays(array1, array2):
    result = []
    for element in array1:
        if element not in array2:
            result.append(element)
    for element in array2:
        if element not in array1:
            result.append(element)
    return result


def validate_picture(filePath):
    hd = ""

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
            return hd
