import os
import uuid

def generate_filename(filename):

    ext = filename.split(".")[-1]

    return str(uuid.uuid4()) + "." + ext


def ensure_folder(path):

    if not os.path.exists(path):

        os.makedirs(path)