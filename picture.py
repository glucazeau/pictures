import hashlib
import exifread
import os
from datetime import datetime

EXIF_DATE_TAG_NAME = "EXIF DateTimeOriginal"


class Duplicate(object):
    def __init__(self, original, duplicate):
        self.original = original
        self.duplicates = [duplicate]

    def add_duplicate(self, duplicate):
        self.duplicates.append(duplicate)


class Picture(object):
    def __init__(self, full_path):
        self.file_name = os.path.basename(full_path)
        self.full_path = full_path
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

                split_char = "_"

                if self.file_name.startswith("IMG_"):
                    file_name_without_extension = file_name_without_extension.replace("IMG_", "")

                if self.file_name.startswith("IMG-"):
                    file_name_without_extension = file_name_without_extension.replace("IMG-", "")
                    split_char = "-"

                parts = file_name_without_extension.split(split_char)
                self.date_taken = parts[0]
                try:
                    parsed_date = datetime.strptime(str(self.date_taken), "%Y%m%d")
                    self.year = parsed_date.year
                    self.month = parsed_date.month
                except ValueError as e:
                    pass

    def __str__(self):
        return f"{self.file_name} - {self.year}/{self.month} - {self.md5sum}"

    def __eq__(self, obj):
        return isinstance(obj, Picture) and obj.md5sum == self.md5sum
