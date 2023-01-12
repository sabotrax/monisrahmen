import hashlib
import os
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
