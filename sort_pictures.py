import click
import click_log
import logging
import shutil

from pathlib import Path

import common

from picture import Picture

logger = logging.getLogger(__name__)
click_log.basic_config(logger)

# Check duplicates


@click.command()
@click_log.simple_verbosity_option(logger)
@click.option("-s", "--source-path', help='Directory containing pictures to process", required=True)
@click.option("-t", "--target-path', help='Directory to move pictures", required=False)
@click.option("-m", "--move', help='Move pictures to the target path instead of copying them)", is_flag=True, default=False)
def process(source_path, target_path, move):
    files = common.list_files(source_path)
    logger.info(f"{len(files)} pictures found")

    count = 1
    for file in files:
        picture = Picture(file)
        logger.info(f"{count}/{len(files)} - {picture.file_name}")
        process_picture(picture, target_path, move)
        count += 1


def process_picture(pic, target_path, move=False):
    target_directory = f"{target_path}/{pic.year}/{pic.month}"
    Path(f"{target_directory}").mkdir(parents=True, exist_ok=True)
    if move:
        logger.info(f"Moving picture {pic.file_name} to {target_directory}")
        shutil.move(pic.full_path, f"{target_directory}/{pic.file_name}")
    else:
        logger.info(f"Copying picture {pic.file_name} to {target_directory}")
        shutil.copyfile(pic.full_path, f"{target_directory}/{pic.file_name}")


if __name__ == '__main__':
    process()
