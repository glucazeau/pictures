import hashlib
import exifread
import os

from datetime import datetime

EXIF_DATE_TAG_NAME = "EXIF DateTimeOriginal"


class Picture(object):
    def __init__(self, directory, file_name):
        self.directory = directory
        self.file_name = file_name
        self.full_path = f"{self.directory}/{self.file_name}"
        self.date_taken = None
        self.year = None
        self.month = None

        self.__get_md5_sum__()
        self.__get_date_taken__()

    def __get_md5_sum__(self):
        hash_md5 = hashlib.md5()
        with open(self.full_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        self.md5sum = hash_md5.hexdigest()

    def __get_date_taken__(self):
        with open(self.full_path, 'rb') as fh:
            tags = exifread.process_file(fh, stop_tag=EXIF_DATE_TAG_NAME)
            if EXIF_DATE_TAG_NAME in tags:
                self.date_taken = tags["EXIF DateTimeOriginal"]
                parsed_date = datetime.strptime(str(self.date_taken), "%Y:%m:%d %H:%M:%S")
                self.year = parsed_date.year
                self.month = parsed_date.month
            else:
                # remove extension
                file_name_without_extension = os.path.splitext(self.file_name)[0]
                # try with dash
                split_with_dash = file_name_without_extension.split("-")
                if len(split_with_dash) > 1:
                    self.date_taken = split_with_dash[1]
                else:
                    split_with_underscore = file_name_without_extension.split("_")
                    self.date_taken = split_with_underscore[1]
                parsed_date = datetime.strptime(str(self.date_taken), "%Y%m%d")
                self.year = parsed_date.year
                self.month = parsed_date.month

    def __str__(self):
        return f"{self.file_name} - {self.year}/{self.month} - {self.md5sum}"

    def move(self):
        raise NotImplementedError
