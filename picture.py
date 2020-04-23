import hashlib
import exifread


class Picture(object):
    def __init__(self, directory, file_name):
        self.directory = directory
        self.file_name = file_name
        self.full_path = f"{self.directory}/{self.file_name}"

        hash_md5 = hashlib.md5()
        with open(self.full_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        self.md5sum = hash_md5.hexdigest()

        #with open(self.full_path, 'rb') as fh:
        #    tags = exifread.process_file(fh, stop_tag="EXIF DateTimeOriginal")
        #    self.date_taken = tags["EXIF DateTimeOriginal"]

    def __str__(self):
        return f"{self.file_name} - {self.md5sum}"

    def move(self):
        raise NotImplementedError
