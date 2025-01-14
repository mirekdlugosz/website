#!/usr/bin/env python3

import argparse
import logging
import math
from datetime import datetime
from pathlib import Path

import polars as pl
from markdown import Markdown
from pelican.settings import DEFAULT_CONFIG, get_settings_from_file
from pelican.plugins.readtime import strip_tags

pelicanconf = {
    **DEFAULT_CONFIG,
    **get_settings_from_file("pelicanconf.py"),
}

PELICAN_ROOT = Path(__file__).resolve().parent.parent.as_posix()


def pelican_content_path():
    content_path = pelicanconf.get("PATH")
    if not Path(content_path).is_absolute():
        content_path = Path(PELICAN_ROOT).joinpath(content_path).as_posix()
    return content_path


def extract_post_data(path):
    logging.debug(f"Processing {log_path}")
    md = Markdown(**pelicanconf.get("MARKDOWN", {}), extensions=["meta"])
    content = md.convert(path.read_text())
    text_content = strip_tags(content)

    title = " ".join(md.Meta.get("title", []))

    date = datetime.strptime(md.Meta.get("date")[0], "%Y-%m-%d %H:%M:%S")

    categories = [
        c.strip() for c in md.Meta.get("tags", ["UNCATEGORIZED"])[0].split(",")
    ]

    # this is copied from readtime plugin, but that implementation is
    # tightly coupled to internal Pelican objects
    avg_readtime = pelicanconf.get("READTIME_AVG_WPM", 230)
    words = len(text_content.split())
    reading_minutes = max(int(math.ceil(words / avg_readtime)), 1)

    rv = {
        "title": title,
        "date": date,
        "categories": categories,
        "content_length": len(text_content),
        "content_reading_time": reading_minutes,
    }
    return rv


def subset_stats(name, df: pl.DataFrame):
    posts, _ = df.shape
    total_chars = df.select(pl.sum("content_length")).item()
    average_chars = df.select(pl.mean("content_length")).item()
    average_reading_time = df.select(pl.mean("content_reading_time")).item()
    rv = {
        "Name": name,
        "Posts": posts,
        "Characters": total_chars,
        "Characters per post": average_chars,
        "Reading time per post": average_reading_time,
    }
    return rv


def get_reports_data(df: pl.DataFrame):
    categories_data = []
    years_data = []
    cats_column = pl.col("categories")
    years_column = pl.col("date")
    categories = (
        df.select(cats_column.flatten())
        .unique()
        .sort(cats_column.str.to_lowercase())
        .to_series()
        .to_list()
    )
    years = (
        df.select(years_column.dt.year())
        .unique()
        .sort(years_column)
        .to_series()
        .to_list()
    )

    for category in categories:
        category_df = df.filter(pl.col("categories").list.contains(category))
        categories_data.append(subset_stats(category, category_df))

    for year in years:
        year_df = df.filter(pl.col("date").dt.year() == year)
        years_data.append(subset_stats(str(year), year_df))

    years_data.append(subset_stats("Total", df))
    return [pl.DataFrame(data) for data in (categories_data, years_data)]


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        default=False,
        help="Print debugging messages",
    )
    parser.add_argument(
        "dir", nargs="?", default=pelican_content_path(), help="Directory to work on"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(level=log_level)
    logging.getLogger("MARKDOWN").setLevel(logging.CRITICAL)

    if not Path(args.dir).is_absolute():
        args.dir = Path(args.dir).resolve().as_posix()

    logging.debug(f"Working directory: {args.dir}")

    all_post_data = []

    for path in Path(args.dir).rglob("*.md"):
        log_path = path.relative_to(args.dir)
        if not path.is_file():
            logging.debug(f"Skipping non-file entry {log_path}")
            continue
        if path.match("pages/*.md"):
            logging.debug(f"Skipping page {log_path}")
            continue
        post_data = extract_post_data(path)
        all_post_data.append(post_data)

    df = pl.DataFrame(all_post_data)
    reports_data = get_reports_data(df)

    polars_config = {
        "float_precision": 2,
        "tbl_cell_numeric_alignment": "RIGHT",
        "tbl_hide_column_data_types": True,
        "tbl_hide_dataframe_shape": True,
        "tbl_rows": -1,
        "thousands_separator": " ",
    }
    with pl.Config(**polars_config):
        for report_data in reports_data:
            print(report_data)
