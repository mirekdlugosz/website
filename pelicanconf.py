#!/usr/bin/env python

# {{{ imports
import sys
import os
import datetime
from pathlib import Path
sys.path.insert(0, os.path.dirname(__file__))
import addins.jinja_filters
from metadata import PROJECTS
# }}}
# {{{ main metadata
AUTHOR = 'Mirek Długosz'
SITENAME = 'Mirek Długosz personal website'
SITEURL = ''

PATH = 'content'
TIMEZONE = 'Europe/Warsaw'
LOCALE = 'C'
DEFAULT_LANG = 'en'
DEFAULT_DATE_FORMAT = '%d %B %Y'
# }}}
# {{{ feeds
FEED_DOMAIN = None
FEED_ATOM = None
FEED_RSS = None
FEED_ALL_ATOM = None
FEED_ALL_RSS = None
CATEGORY_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
TRANSLATION_FEED_ATOM = None
# }}}
# {{{ paths, URLs
AUTHOR_SAVE_AS = ''
ARTICLE_URL = "blog/{date:%Y}/{slug}/"
ARTICLE_SAVE_AS = f"{ARTICLE_URL}/index.html"
PAGE_URL = '{slug}.html'
PAGE_SAVE_AS = PAGE_URL
CATEGORY_URL = ''
CATEGORY_SAVE_AS = ''
TAG_URL = 'blog/tag/{slug}/'
TAG_SAVE_AS = f"{TAG_URL}index.html"
STATIC_URL = 'static/{path}'
STATIC_SAVE_AS = STATIC_URL

DIRECT_TEMPLATES = ['index', 'archives']
INDEX_SAVE_AS = 'blog/index.html'
ARCHIVES_URL = 'blog/archives.html'
ARCHIVES_SAVE_AS = ARCHIVES_URL

STATIC_PATHS = ['static',
                # directories that are not referenced in articles,
                # but should be placed somewhere in `static`
                '2015/bakeries-map']
EXTRA_PATH_METADATA = {}
static_path_root = Path(PATH) / 'static'
for static_file in static_path_root.glob('**/*'):
    if static_file.is_dir():
        continue
    target_path = static_file.relative_to(static_path_root).as_posix()
    static_file = static_file.relative_to(PATH).as_posix()
    EXTRA_PATH_METADATA[static_file] = {'save_as': target_path}
del static_path_root
# }}}
# {{{ pagination
INDEX_ARTICLES = 15
DEFAULT_PAGINATION = False
# DEFAULT_PAGINATION = 5
PAGINATION_PATTERNS = (
    (1, '{base_name}/', '{base_name}/index.html'),
    (2, '{base_name}/page/{number}/', '{base_name}/page/{number}/index.html'),
)
# }}}
# {{{ ignored files
READERS = {
    'htm': None,
    'html': None,
}

IGNORE_FILES = ['.#*',
                '*.Rmd',
                ]
# }}}
# {{{ theme and custom theme metadata
SHOW_ARTICLE_AUTHOR = False
USE_FOLDER_AS_CATEGORY = False

THEME = 'theme/'

PRELOAD_FONTS_NAMES = (
    "merriweather-v21-latin_latin-ext-regular",
)

CONTACT = (
    ('Email', 'mailto:mirek %at% mirekdlugosz.com', 'envelope fas'),
    ('Twitter', 'https://twitter.com/mirekdlugosz', 'twitter fab'),
    ('LinkedIn', 'https://www.linkedin.com/in/mirekdlugosz/en', 'linkedin-in fab'),
)

USE_OPEN_GRAPH = True
TWITTER_CARDS = True
TWITTER_USERNAME = "mirekdlugosz"

BUILD_DATE = datetime.date.today().year

JINJA_FILTERS = {
    'dict_replace': addins.jinja_filters.dict_replace,
}
# }}}
# {{{ plugins

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

SOCIAL_CARDS_TEMPLATE = './theme/src/img/social-card-template.png'
SOCIAL_CARDS_PATH = 'static/static/social-cards/'
SOCIAL_CARDS_FONT_FILENAME = 'DejaVuSans.ttf'
SOCIAL_CARDS_FONT_FILL = '#ffffff'
SOCIAL_CARDS_FONT_SIZE = 70
SOCIAL_CARDS_CANVAS_WIDTH = 1120
SOCIAL_CARDS_CANVAS_HEIGHT = 382
SOCIAL_CARDS_CANVAS_LEFT = 40
SOCIAL_CARDS_CANVAS_TOP = 248
SOCIAL_CARDS_LEADING = 15
SOCIAL_CARDS_CHARS_PER_LINE = 30
# }}}

# vim: fdm=marker
