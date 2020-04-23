import click
import click_log
import logging
import shutil
import face_recognition

from os import listdir
from os.path import isfile, join
from pathlib import Path

from picture import Picture

logger = logging.getLogger(__name__)
click_log.basic_config(logger)

# Check duplicates


@click.command()
@click_log.simple_verbosity_option(logger)
@click.option('-s', '--source-path', help='Directory containing pictures to process')
@click.option('-t', '--target-path', help='Directory to move pictures')
@click.option('-m', '--move', help='Move or copy pictures to the target path', is_flag=True, default=False)
@click.option('-f', '--face-recognition', 'enable_face_recognition', help='Try to identify faces', is_flag=True, default=False)
def process(source_path, target_path, move, enable_face_recognition):
    logger.info(f"Listing files in {source_path}")
    files = list_files(source_path)
    logger.info(f"{len(files)} pictures found")

    if enable_face_recognition is True:
        known_faces = load_known_faces()

    for file_name in files:
        picture = Picture(source_path, file_name)
        logger.debug(f"Processing file {picture}")
        #process_picture(picture, target_path, move)
        if enable_face_recognition is True:
            recognize_faces(picture, known_faces)


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


def load_known_faces():
    logger.info("Loading known faces")

    faces = {
        "Guillaume": "./comparison_images/guillaume.png"
    }

    known_encodings = {}
    for name, image in faces.items():
        logger.info(f"Processing picture of {name}")
        known_image = face_recognition.load_image_file(image)
        encodings = face_recognition.face_encodings(known_image)

        if len(encodings) > 0:
            known_encodings.update({name: encodings[0]})
        else:
            logger.warning(f"No face found in {image}")
    logger.info("Known faces loaded")
    return known_encodings


def recognize_faces(pic, known_face_encodings):
    logger.info(f"Processing picture {pic.file_name}")
    let_try = True

    unknown_image = face_recognition.load_image_file(pic.full_path)
    unknown_encodings = face_recognition.face_encodings(unknown_image)
    if len(unknown_encodings) > 0:
        unknown_encoding = unknown_encodings[0]
    else:
        let_try = False
        logger.warning(f"No face found")

    if let_try is True:
        logger.info("Comparing face with known ones")
        results = face_recognition.compare_faces(list(known_face_encodings.values()), unknown_encoding)
        for idx, val in enumerate(results):
            if bool(val) is True:
                logger.info(f"{list(known_face_encodings.keys())[idx]} has been found in this picture")
    logger.info("Completed")


if __name__ == '__main__':
    process()
