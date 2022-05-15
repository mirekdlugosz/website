#!/usr/bin/env python3

import argparse
import logging
import math
from pathlib import Path

from PIL import Image
from pelican.settings import DEFAULT_CONFIG, get_settings_from_file

pelicanconf = {
    **DEFAULT_CONFIG,
    **get_settings_from_file('pelicanconf.py'),
}

PELICAN_ROOT = Path(__file__).resolve().parent.parent.as_posix()
THUMBNAIL_SUFFIX = pelicanconf.get('THUMBNAIL_SUFFIX', '-min')
THUMBNAIL_HEIGHT = pelicanconf.get('THUMBNAIL_HEIGHT', 150)
# dict of {path: (width, height)}
THUMBNAIL_SIZES = pelicanconf.get('THUMBNAIL_SIZES', {})


def pelican_content_path():
    content_path = pelicanconf.get('PATH')
    if not Path(content_path).is_absolute():
        content_path = Path(PELICAN_ROOT).joinpath(content_path).as_posix()
    return content_path


def is_image(path):
    suffix = Path(path).suffix.strip('.')
    return suffix in ('jpg', 'png')


def is_ignored(path, ignored_list):
    if not ignored_list:
        return False
    absolute_path = path.absolute().as_posix()
    for item in ignored_list:
        if item in absolute_path:
            return True
    return False


def is_thumbnail(path):
    return THUMBNAIL_SUFFIX in path.name


def thumbnail_path(path):
    thumbnail_name = f"{path.stem}{THUMBNAIL_SUFFIX}{path.suffix}"
    return path.with_name(thumbnail_name)


def get_thumbnail_dimensions(path, img):
    config_size = THUMBNAIL_SIZES.get(path.resolve().as_posix(), None)
    if config_size:
        logging.debug(f"Found {path} in THUMBNAIL_SIZES, setting size to {config_size}")
        return config_size

    current_width, current_height = img.size
    prop = THUMBNAIL_HEIGHT / current_height
    target_width = math.floor(current_width * prop)

    if prop > 1:
        logging.debug(f"Using source size for resizing in {path}")
        return current_width, current_height

    return target_width, THUMBNAIL_HEIGHT


def create_thumbnail(path):
    thumb_path = thumbnail_path(path)
    if thumb_path.exists() and not args.force:
        logging.debug(f"Refusing to overwrite existing {thumb_path}")
        return

    img = Image.open(path)
    width, height = get_thumbnail_dimensions(path, img)
    img = img.resize((width, height), Image.Resampling.LANCZOS)
    img.save(thumb_path)
    logging.info(f"Created {thumb_path}")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--force", action="store_true", default=False,
                        help="Generate thumbnail even if one already exists")
    parser.add_argument("-r", "--rm", action="store_true", default=False,
                        help="Only remove thumbnails")
    parser.add_argument("-i", "--ignore", action="append", dest="ignored",
                        help="Ignore files with paths containing argument")
    parser.add_argument("-d", "--debug", action="store_true", default=False,
                        help="Print debugging messages")
    parser.add_argument("dir", nargs="?", default=pelican_content_path(),
                        help="Directory to work on")
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(level=log_level)

    if not Path(args.dir).is_absolute():
        args.dir = Path(args.dir).resolve().as_posix()

    logging.debug(f"Working directory: {args.dir}")

    THUMBNAIL_SIZES = {
        Path(PELICAN_ROOT).joinpath(key).resolve().as_posix(): value
        for key, value in THUMBNAIL_SIZES.items()
    }

    for path in Path(args.dir).glob('**/*'):
        log_path = path.relative_to(args.dir)
        if not path.is_file():
            logging.debug(f"Skipping non-file entry {log_path}")
            continue
        if not is_image(path):
            logging.debug(f"Skipping non-image file {log_path}")
            continue
        if is_ignored(path, args.ignored):
            logging.debug(f"Skipping file in ignored path {log_path}")
            continue
        if is_thumbnail(path):
            if args.rm:
                logging.info(f"Removing thumbnail {log_path}")
                path.unlink()
            else:
                logging.debug(f"Skipping existing thumbnail {log_path}")
            continue

        if not args.rm:
            create_thumbnail(path)
