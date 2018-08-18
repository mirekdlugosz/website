#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

import sys
import os
import datetime
sys.path.insert(0, os.path.dirname(__file__))
import addins.jinja_filters
from metadata import PROJECTS

AUTHOR = 'Mirosław Zalewski'
SITENAME = 'Mirosław Zalewski'
SITEURL = ''

PATH = 'content'
TIMEZONE = 'Europe/Warsaw'
LOCALE = 'C'
DEFAULT_LANG = u'en'
DEFAULT_DATE_FORMAT = '%d %B %Y'
BUILD_DATE = datetime.date.today().year

STATIC_PATHS = [str(_) for _ in range(2015, BUILD_DATE + 1)]
STATIC_PATHS.extend(['root', 'certificates'])

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
TAGS_URL = 'blog/tags.html'
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
DISPLAY_ARTICLE_INFO_ON_INDEX = True

CONTACT = (
    ('Email', 'mailto:mz %at% miroslaw-zalewski.eu', 'envelope far'),
    ('LinkedIn', 'https://www.linkedin.com/in/miroslawzalewski/en', 'linkedin-in fab'),
    ('Twitter', 'https://twitter.com/zalewskiEU', 'twitter fab'),
)

DEFAULT_PAGINATION = False
# DEFAULT_PAGINATION = 5
PAGINATION_PATTERNS = (
    (1, '{base_name}/', '{base_name}/index.html'),
    (2, '{base_name}/page/{number}/', '{base_name}/page/{number}/index.html'),
)

THEME = 'theme/'

PLUGIN_PATHS = ['../pelican-plugins']
PLUGINS = [
    'summary',
    'neighbors',
]
SUMMARY_END_MARKER = '<!-- more -->'

MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.codehilite': {'css_class': 'highlight', 'linenums': False},
        'markdown.extensions.extra': {},
        'markdown.extensions.meta': {},
        'markdown.extensions.toc': {'anchorlink': True},
    },
    'output_format': 'html5',
}

JINJA_FILTERS = {
    'dict_replace': addins.jinja_filters.dict_replace,
}
