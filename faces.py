import logging
import click_log
import yaml

from PIL import Image, ExifTags

logger = logging.getLogger(__name__)
click_log.basic_config(logger)

try:
    import face_recognition
except ImportError:
    faces = None


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