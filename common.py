from os import listdir
from os.path import isfile, join


def list_files(source_path):
    files = [f for f in listdir(source_path) if isfile(join(source_path, f))]
    return files
