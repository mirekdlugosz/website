#!/usr/bin/env python
import markdown
from typogrify.filters import typogrify


def dict_replace(text, replacements):
    for key, val in replacements.items():
        text = text.replace(key, val)
    return text


def from_markdown(text):
    markdown_extensions = ["smarty", "sane_lists"]
    converted = markdown.markdown(
        text, extensions=markdown_extensions, output_format="html5",
    )
    return typogrify(converted)
