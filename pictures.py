import click
import click_log
import logging
import shutil

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
def process(source_path, target_path, move):
    logger.info(f"Listing files in {source_path}")
    files = list_files(source_path)
    logger.info(f"{len(files)} pictures found")
    for file_name in files:
        picture = Picture(source_path, file_name)
        logger.debug(f"Processing file {picture}")
        process_picture(picture, target_path, move)


def list_files(source_path):
    return [f for f in listdir(source_path) if isfile(join(source_path, f))]


def process_picture(picture, target_path, move=False):
    target_directory = f"{target_path}/{picture.year}/{picture.month}"
    Path(f"{target_directory}").mkdir(parents=True, exist_ok=True)
    if move:
        logger.info(f"Moving picture {picture.file_name} to {target_directory}")
        shutil.copyfile(picture.full_path, f"{target_directory}/{picture.file_name}")
    else:
        logger.info(f"Copying picture {picture.file_name} to {target_directory}")
        shutil.copyfile(picture.full_path, f"{target_directory}/{picture.file_name}")


if __name__ == '__main__':
    process()
