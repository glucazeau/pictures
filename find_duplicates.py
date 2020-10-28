import click
import click_log
import logging
import common
import os

from progress.bar import Bar

from picture import Picture, Duplicate

logger = logging.getLogger(__name__)
click_log.basic_config(logger)

pictures_sum = dict()


@click.command()
@click_log.simple_verbosity_option(logger)
@click.option("-c", "--path-to-clean", help="Directory containing files with potential duplicates to remove",
              required=True)
@click.option("-r", "--reference-path", help="Directory containing files to check duplicates against", required=False,
              default=None)
@click.option("-d", "--delete-duplicates/--do-not-delete-duplicates", help="If enabled, duplicates found will be deleted", required=False,
              default=False)
def process(path_to_clean, reference_path, delete_duplicates):
    files_to_clean = common.list_files(path_to_clean)
    nb_files_to_clean = len(files_to_clean)
    logger.info(f"{nb_files_to_clean} files to check for duplicates")
    if delete_duplicates is True:
        logger.info("/!\ Duplicates found will be deleted")

    if reference_path is not None:
        reference_files = common.list_files(reference_path)
    else:
        reference_files = []

    nb_reference_files = len(reference_files)
    logger.info(f"{nb_reference_files} reference files to compare")
    total_nb_files = nb_files_to_clean + nb_reference_files

    duplicates = {}
    p_reference_files = {}
    with Bar('Processing', max=total_nb_files) as bar:
        if reference_path is not None:
            for i in range(nb_reference_files):
                f = Picture(reference_files[i])
                p_reference_files[f.md5sum] = f
                bar.next()

        for i in range(nb_files_to_clean):
            p_file_to_clean = Picture(files_to_clean[i])
            is_duplicate(p_reference_files, duplicates, p_file_to_clean)
            bar.next()

    nb_duplicates = len(duplicates)
    if nb_duplicates == 0:
        logger.info("No duplicates found")
    elif nb_duplicates == 1:
        logger.info(f"One picture with duplicates found")
    else:
        logger.info(f"{nb_duplicates} pictures with duplicates found")

    if nb_duplicates > 0:
        with open('report.html', 'a') as the_file:
            the_file.write('''
                <html>
                    <head>
                    <style>
                    table, th, td {
                      border: 1px solid black;
                      border-collapse: collapse;
                    }
                    </style>
                    </head>
                    <body>
                        <table border="1"><tr><th>Original</th><th>Duplicates</th></tr>\n''')
            for d in duplicates.values():
                #logger.info(f"Original file: {d.original.full_path}")
                the_file.write('<tr>\n')
                the_file.write(
                    f'<!--Original--><td><img title="{d.original.full_path}" alt="{d.original.full_path}" src="file://{d.original.full_path}" width="25%" height="25%"></td>')
                the_file.write('\n<!--Duplicates--><td>')
                for v in d.duplicates:
                    #logger.info(f"  - {v.full_path}")
                    the_file.write(f'<img alt="{v.full_path}" src="file://{v.full_path}" width="25%" height="25%">\n')
                    if delete_duplicates is True:
                        logger.info(f"Deleting {v.full_path} (original: {d.original.full_path})")
                        os.remove(v.full_path)
            the_file.write('</td>\n</tr>\n')
            the_file.write('</table></body></html>')


def is_duplicate(p_reference_files, duplicates, file, delete=False):
    md5 = file.md5sum
    if md5 in p_reference_files.keys():
        # If another file was already a duplicate
        if md5 in duplicates.keys():
            duplicates[md5].add_duplicate(file)
        else:
            duplicates[md5] = Duplicate(p_reference_files[md5], file)
    else:
        p_reference_files[md5] = file


if __name__ == '__main__':
    process()
