import click
import click_log
import logging

from os import listdir
from os.path import isfile, join

from picture import Picture

logger = logging.getLogger(__name__)
click_log.basic_config(logger)


@click.command()
@click_log.simple_verbosity_option(logger)
@click.option('-s', '--source-path', help='Directory containing pictures to process')
def process(source_path):
    logger.info(f"Listing files in {source_path}")
    files = list_files(source_path)
    logger.info(f"{len(files)} pictures found")
    pictures = []
    for file_name in files:
        picture = Picture(source_path, file_name)
        pictures.append(picture)
        logger.info(f"Processing file {picture}")


def list_files(source_path):
    return [f for f in listdir(source_path) if isfile(join(source_path, f))]


if __name__ == '__main__':
    process()
