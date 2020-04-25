import click
import click_log
import logging
import shutil
import face_recognition
import yaml

from os import listdir
from os.path import isfile, join
from pathlib import Path
from PIL import Image, ExifTags

from picture import Picture

logger = logging.getLogger(__name__)
click_log.basic_config(logger)

# Check duplicates


@click.command()
@click_log.simple_verbosity_option(logger)
@click.option('-s', '--source-path', help='Directory containing pictures to process', required=True)
@click.option('-t', '--target-path', help='Directory to move pictures', required=False)
@click.option('-m', '--move', help='Move or copy pictures to the target path', is_flag=True, default=False)
@click.option('-f', '--face-recognition', 'enable_face_recognition', help='Try to identify faces', is_flag=True, default=False)
@click.option('-c', '--comparison-images-directory', help='Set of people pictures to compare to', default="./comparison_images")
def process(source_path, target_path, move, enable_face_recognition, comparison_images_directory):
    files = list_files(source_path)
    logger.info(f"{len(files)} pictures found")

    if enable_face_recognition is True:
        known_faces = load_known_faces(comparison_images_directory)

    count = 1
    for file_name in files:
        picture = Picture(source_path, file_name)
        logger.info(f"{count}/{len(files)} - {picture.file_name}")
        #process_picture(picture, target_path, move)
        if enable_face_recognition is True:
            recognize_faces(picture, known_faces)
        count += 1


def list_files(source_path):
    return [f for f in listdir(source_path) if isfile(join(source_path, f))]


def process_picture(pic, target_path, move=False):
    target_directory = f"{target_path}/{pic.year}/{pic.month}"
    Path(f"{target_directory}").mkdir(parents=True, exist_ok=True)
    if move:
        logger.info(f"Moving picture {pic.file_name} to {target_directory}")
        shutil.move(pic.full_path, f"{target_directory}/{pic.file_name}")
    else:
        logger.info(f"Copying picture {pic.file_name} to {target_directory}")
        shutil.copyfile(pic.full_path, f"{target_directory}/{pic.file_name}")


def load_known_faces(comparison_images_directory):
    with open(f"{comparison_images_directory}/reference.yaml") as file:
        people_list = yaml.load(file, Loader=yaml.FullLoader)

    logger.info(f"Loading known faces of {len(people_list['people'])} people")
    known_encodings = {}
    for entry in people_list["people"]:
        name = entry['name']
        name_encodings = []
        for picture in entry['pictures']:
            logger.debug(f"Processing picture of {name}")
            picture_path = f"{comparison_images_directory}/{picture}"

            encoding = encode_face(picture_path)
            if encoding is not None:
                name_encodings.append(encoding)
        known_encodings.update({name: name_encodings})

    logger.info("Known faces loaded")
    return known_encodings


def encode_face(picture_path):
    rotate_picture(picture_path)
    known_image = face_recognition.load_image_file(picture_path)
    encodings = face_recognition.face_encodings(known_image)

    if len(encodings) > 0:
        return encodings[0]
    else:
        logger.debug(f"No face found in {picture_path}")
        return None


def recognize_faces(pic, known_face_encodings):
    let_try = True

    unknown_encoding = encode_face(pic.full_path)
    if unknown_encoding is None:
        let_try = False

    if let_try is True:
        logger.debug("Comparing face with known ones")

        for name, pictures in known_face_encodings.items():
            logger.debug(f"Looking for {name}")
            results = face_recognition.compare_faces(pictures, unknown_encoding)
            if True in results:
                logger.info(f"  -> found {name}")
    logger.debug("Completed")


def rotate_picture(picture_path):
    logger.debug(f"Rotating picture {picture_path} if needed")
    try:
        image = Image.open(picture_path)

        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break

        exif = dict(image._getexif().items())

        if exif[orientation] == 3:
            image = image.rotate(180, expand=True)
        elif exif[orientation] == 6:
            image = image.rotate(270, expand=True)
        elif exif[orientation] == 8:
            image = image.rotate(90, expand=True)

        image.save(picture_path)
        image.close()
    except (AttributeError, KeyError, IndexError):
        # cases: image don't have getexif
        logger.debug("No EXIF found")
        pass


if __name__ == '__main__':
    process()
