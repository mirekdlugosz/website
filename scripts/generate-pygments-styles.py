#!/usr/bin/env python3

import argparse
from tempfile import mkdtemp
from pathlib import Path
from pygments.formatters import HtmlFormatter
from pygments.styles import get_all_styles


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", action="store", default="",
                        help="Path to directory where files should be written")
    parser.add_argument("-p", "--prefix", action="store", default=".highlight pre",
                        help="Prefix to use before styled classes")
    return parser.parse_args()


def main():
    args = parse_args()
    if not args.directory:
        args.directory = mkdtemp()

    output_dir = Path(args.directory)

    if not output_dir.is_dir():
        print("Specified path doesn't seem to be a directory, exiting")
        raise SystemExit()

    for style_name in get_all_styles():
        output_path = output_dir.joinpath(f"{style_name.replace('-', '')}.scss")
        print(f"Writing {output_path}...", end=" ")
        content = HtmlFormatter(style=style_name).get_style_defs(args.prefix)
        with open(output_path, 'w') as fh:
            fh.write(content)
        print("Done")


if __name__ == "__main__":
    main()
