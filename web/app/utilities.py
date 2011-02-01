from django.core.files.storage import default_storage

import os

def save(file, directory, filename=""):

    if filename != "":
        location = directory+filename
    else:
        location = directory+file.name

    return default_storage.save(location,file)
