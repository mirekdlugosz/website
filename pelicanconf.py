#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import addins.jinja_filters

AUTHOR = u'Miros\u0142aw Zalewski'
SITENAME = u'Miros\u0142aw Zalewski'
SITEURL = ''

PATH = 'content'
TIMEZONE = 'Europe/Warsaw'
LOCALE = 'C'
DEFAULT_LANG = u'en'
DEFAULT_DATE_FORMAT = '%d %B %Y'

STATIC_PATHS = ['2015', '2016', '2017', '2018', '2019',
                'main',
                'certificates']

FEED_DOMAIN = None
FEED_ATOM = None
FEED_RSS = None
FEED_ALL_ATOM = None
FEED_ALL_RSS = None
CATEGORY_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
TRANSLATION_FEED_ATOM = None

USE_FOLDER_AS_CATEGORY = False
DISPLAY_CATEGORIES_ON_MENU = False
DISPLAY_CATEGORIES_ON_SIDEBAR= False
# Eventually, we want to drop About Me page for main website (`/`)
# Reverse values of variables below then
DISPLAY_LINKS_ON_MENU = False 
DISPLAY_PAGES_ON_MENU = True

DISPLAY_TAGS_INLINE = True

SHOW_ARTICLE_AUTHOR = False
DISPLAY_ARTICLE_INFO_ON_INDEX = True

AUTHOR_SAVE_AS = ''
AUTHORS_SAVE_AS = ''
ARTICLE_URL = "blog/{date:%Y}/{slug}/"
ARTICLE_SAVE_AS = ARTICLE_URL + '/index.html'
PAGE_URL = 'blog/pages/{slug}.html'
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

LINKS = (
        ('My résumé', '/'),
        )

# Social widget
SOCIAL = (('Email', 'mailto:mz %at% miroslaw-zalewski.eu'),
          ('GitHub', 'https://github.com/mirzal/'),
          ('BitBucket', 'https://bitbucket.org/mirzal/'),
          ('StackExchange', 'http://stackexchange.com/users/4352116/miros%C5%82aw-zalewski?tab=accounts'),
          ('LinkedIn', 'http://www.linkedin.com/in/miroslawzalewski/en'),
          ('RSS feed', '/blog/feeds/rss.xml'),
#         ('', '#'),
          )
SOCIAL_MAIN = (#('Email', 'mailto:mz %at% miroslaw-zalewski.eu', 'envelope'),
               ('LinkedIn', 'http://www.linkedin.com/in/miroslawzalewski/en', 'linkedin'),
               ('Stack Exchange', 'http://stackexchange.com/users/4352116/miros%C5%82aw-zalewski?tab=accounts', 'stack-exchange'),
               ('GitHub', 'https://github.com/mirzal/', 'github'),
               ('BitBucket', 'https://bitbucket.org/mirzal/', 'bitbucket'),
               ('Twitter', 'https://twitter.com/zalewskiEU', 'twitter'),
               #('My blog', '/blog/', 'rss'),
               #('About me', '', 'user'),
        )

DEFAULT_PAGINATION = False
#DEFAULT_PAGINATION = 20
PAGINATION_PATTERNS = (
    (1, '{base_name}/', '{base_name}/index.html'),
    (2, '{base_name}/page/{number}/', '{base_name}/page/{number}/index.html'),
)

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

READERS = { 
        'htm': None,
        'html': None,
        }

IGNORE_FILES = ['.#*', 
        '*.Rmd',
        ]

THEME = 'theme/'
PYGMENTS_STYLE = 'solarizedlight'

PLUGIN_PATHS = ['/home/minio/sources/pelican-plugins']
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
        'current_year': addins.jinja_filters.current_year,
        }
