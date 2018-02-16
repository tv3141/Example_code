# -*- encoding: utf-8 -*-
"""
Given a file with URLs to files, one URL per line, download all files into the
given directory.
"""
import argparse
import logging
import os
import os.path
import requests
import sys
from functools import partial
from multiprocessing.pool import Pool


MIN_PYTHON = (3, 2)
if sys.version_info < MIN_PYTHON:
    sys.stderr.write("Python %s.%s or later is required\n" % MIN_PYTHON)
    sys.exit(1)


# Logger settings
LOG_LEVEL = logging.INFO
FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(stream=sys.stdout,
                    level=LOG_LEVEL,
                    format=FORMAT)
logger = logging.getLogger(__name__)


def parse_args(cli_args):
    """
    Provide basic user interface and parse command line arguments.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-n', dest='nprocs', type=int, default=1,
                        help='Number of parallel processes.')
    parser.add_argument('file_with_urls', help='File with URLs to files.')
    parser.add_argument('directory', help='Store downloaded files in this directory.')
    args = parser.parse_args(cli_args)
    return args


def download_url(directory, url):
    """
    Download the image at ``url`` into ``directory``.

    Common exceptions are caught and logged. Existing images are not overwritten.
    """
    file_path = os.path.join(directory, os.path.basename(url))
    if os.path.exists(file_path):
         logger.error('File exists: ' + file_path)
         return

    try:
        logger.info('Downloading ' + str(url))
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        logger.error(type(e).__name__ + ': ' + str(e))
    except requests.exceptions.Timeout as e:
        logger.error(type(e).__name__ + ': ' + str(e))
    except requests.exceptions.TooManyRedirects as e:
        logger.error(type(e).__name__ + ': ' + str(e))
    except requests.exceptions.SSLError as e:
        logger.error(type(e).__name__ + ': ' + str(e))
    except (requests.exceptions.URLRequired,
            requests.exceptions.MissingSchema,
            requests.exceptions.InvalidSchema,
            requests.exceptions.InvalidURL) as e:
        logger.error(type(e).__name__ + ': ' + str(e))

    try:
        with open(file_path, 'xb') as fileobject:
            fileobject.write(response.content)
    except FileExistsError as e:
        logger.error(type(e).__name__ + ': ' + str(e))


def download_urls(urls, directory, nprocs=1):
    """Download images using multiple processes."""
    download = partial(download_url, directory)
    with Pool(nprocs) as pool:
        pool.map(download, urls)


def get_urls(file_with_urls):
    """Read URLs line-by-line from text file."""
    with open(file_with_urls, 'r', newline=None) as fileobject:
        urls = [url.strip('\n') for url in fileobject.readlines()]
    return urls


def setup_download_dir(directory):
    """Make sure ``directory`` exists."""
    os.makedirs(directory, exist_ok=True)  # exist_ok was added in Python3.2


def main():
    args = parse_args(sys.argv[1:])
    setup_download_dir(args.directory)
    urls = get_urls(args.file_with_urls)
    download_urls(urls, args.directory, args.nprocs)


if __name__ == '__main__':
    main()
