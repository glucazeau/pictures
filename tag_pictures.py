import click
import click_log
import logging

import common
import faces

from picture import Picture

logger = logging.getLogger(__name__)
click_log.basic_config(logger)


@click.command()
@click_log.simple_verbosity_option(logger)
@click.option('-s', '--source-path', help='Directory containing pictures to process', required=True)
@click.option('-c', '--comparison-images-directory', help='Set of people pictures to compare to', required=False, default="./comparison_images")
def process(source_path, comparison_images_directory):
    files = common.list_files(source_path)
    logger.info(f"{len(files)} pictures found")

    known_faces = faces.load_known_faces(comparison_images_directory)

    count = 1
    for file_name in files:
        picture = Picture(source_path, file_name)
        logger.info(f"{count}/{len(files)} - {picture.file_name}")
        faces.recognize_faces(picture, known_faces)
        count += 1


if __name__ == '__main__':
    process()
