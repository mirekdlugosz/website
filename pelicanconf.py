#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

import sys
import os
import datetime
sys.path.insert(0, os.path.dirname(__file__))
import addins.jinja_filters
from metadata import PROJECTS

AUTHOR = 'Mirek Długosz'
SITENAME = 'Mirek Długosz personal website'
SITEURL = ''

PATH = 'content'
TIMEZONE = 'Europe/Warsaw'
LOCALE = 'C'
DEFAULT_LANG = 'en'
DEFAULT_DATE_FORMAT = '%d %B %Y'
BUILD_DATE = datetime.date.today().year

STATIC_PATHS = ['root', 'certificates', 
                # directories that are not referenced in articles,
                # but should be placed somewhere in `static`
                '2015/bakeries-map']

USE_FOLDER_AS_CATEGORY = False

FEED_DOMAIN = None
FEED_ATOM = None
FEED_RSS = None
FEED_ALL_ATOM = None
FEED_ALL_RSS = None
CATEGORY_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
TRANSLATION_FEED_ATOM = None

AUTHOR_SAVE_AS = ''
AUTHORS_SAVE_AS = ''
ARTICLE_URL = "blog/{date:%Y}/{slug}/"
ARTICLE_SAVE_AS = ARTICLE_URL + '/index.html'
PAGE_URL = '{slug}.html'
PAGE_SAVE_AS = PAGE_URL
CATEGORY_URL = ''
CATEGORY_SAVE_AS = ''
CATEGORIES_URL = ''
CATEGORIES_SAVE_AS = ''
TAG_URL = 'blog/tag/{slug}/'
TAG_SAVE_AS = TAG_URL + 'index.html'
TAGS_URL = ''
TAGS_SAVE_AS = ''
ARCHIVES_URL = 'blog/archives.html'
ARCHIVES_SAVE_AS = ARCHIVES_URL
STATIC_URL = 'static/{path}'
STATIC_SAVE_AS = STATIC_URL
INDEX_SAVE_AS = 'blog/index.html'

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

READERS = {
    'htm': None,
    'html': None,
}

IGNORE_FILES = ['.#*',
                '*.Rmd',
                ]

EXTRA_PATH_METADATA = {
    'root/.htaccess': {'save_as': '.htaccess'},
}

SHOW_ARTICLE_AUTHOR = False

CONTACT = (
    ('Email', 'mailto:mirek %at% mirekdlugosz.com', 'envelope fas'),
    ('Twitter', 'https://twitter.com/mirekdlugosz', 'twitter fab'),
    ('LinkedIn', 'https://www.linkedin.com/in/mirekdlugosz/en', 'linkedin-in fab'),
)

INDEX_ARTICLES = 15
DEFAULT_PAGINATION = False
# DEFAULT_PAGINATION = 5
PAGINATION_PATTERNS = (
    (1, '{base_name}/', '{base_name}/index.html'),
    (2, '{base_name}/page/{number}/', '{base_name}/page/{number}/index.html'),
)

THEME = 'theme/'

PLUGIN_PATHS = ['../pelican-plugins', 'plugins']
PLUGINS = [
    'thumb_tag',
    'neighbors',
    'rename_to_slug',
    'summary',
    'readtime',
]
SUMMARY_END_MARKER = '<!-- more -->'

MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.codehilite': {'css_class': 'highlight', 'linenums': False},
        'markdown.extensions.extra': {},
        'markdown.extensions.fenced_code': {},
        'markdown.extensions.meta': {},
        'markdown.extensions.toc': {'anchorlink': True},
    },
    'output_format': 'html',
}

TYPOGRIFY = True

USE_OPEN_GRAPH = True

JINJA_FILTERS = {
    'dict_replace': addins.jinja_filters.dict_replace,
}
