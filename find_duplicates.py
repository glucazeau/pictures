import click
import click_log
import logging
import common

from progress.bar import Bar

from picture import Picture

logger = logging.getLogger(__name__)
click_log.basic_config(logger)

pictures_sum = dict()


@click.command()
@click_log.simple_verbosity_option(logger)
@click.option("-s", "--source-path", help="Directory containing pictures to process", required=True)
def process(source_path):
    files = common.list_files(source_path)
    nb_files = len(files)
    logger.info(f"{nb_files} pictures found")

    duplicates = {}
    with Bar('Processing', max=nb_files) as bar:
        for i in range(nb_files):
            picture = Picture(files[i])
            duplicates = process_picture(picture, duplicates)
            bar.next()
    nb_duplicates = len(duplicates)
    if nb_duplicates == 0:
        logger.info("No duplicates found")
    elif nb_duplicates == 1:
        logger.info(f"One picture with duplicates found")
    else:
        logger.info(f"{nb_duplicates} pictures with duplicates found")
    if nb_duplicates > 0:
        for md5sum, pictures in duplicates.items():
            logger.info(f"- {pictures}")


def process_picture(pic, duplicates):
    if pic.md5sum in pictures_sum.keys():
        duplicates[pic.md5sum] = pictures_sum[pic.md5sum]
        duplicates[pic.md5sum].append(pic.full_path)
    else:
        pictures_sum[pic.md5sum] = [pic.full_path]
    return duplicates


if __name__ == '__main__':
    process()
