import click
import click_log
import logging
import common

from picture import Picture

logger = logging.getLogger(__name__)
click_log.basic_config(logger)

pictures_sum = {}


@click.command()
@click_log.simple_verbosity_option(logger)
@click.option("-s", "--source-path", help="Directory containing pictures to process", required=True)
def process(source_path):
    files = common.list_files(source_path)
    logger.info(f"{len(files)} pictures found")

    duplicates = 0
    count = 1
    for file in files:
        picture = Picture(file)
        logger.info(f"{count}/{len(files)} - {picture.file_name}")
        duplicates += process_picture(picture)
        count += 1
    logger.info(f"{duplicates} duplicates found")


def process_picture(pic):
    if pic.md5sum in pictures_sum.keys():
        logger.info(f"{pic.full_path} is a duplicate of {pictures_sum[pic.md5sum]}")
        pictures_sum[pic.md5sum].append(pic.full_path)
        return 1
    else:
        pictures_sum[pic.md5sum] = [pic.full_path]
        return 0


if __name__ == '__main__':
    process()
