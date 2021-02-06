#!/usr/bin/env python
# This file is only used if you use `inv publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

SITEURL = 'https://mirekdlugosz.com'
RELATIVE_URLS = False

FEED_DOMAIN = SITEURL
FEED_ALL_ATOM = 'blog/feeds/atom.xml'
FEED_ALL_RSS = 'blog/feeds/rss.xml'
# CATEGORY_FEED_ATOM = 'blog/feeds/{slug}.atom.xml'
# CATEGORY_FEED_RSS = 'blog/feeds/{slug}.rss.xml'
TAG_FEED_ATOM = 'blog/feeds/{slug}.atom.xml'
TAG_FEED_RSS = 'blog/feeds/{slug}.rss.xml'
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
FEED_MAX_ITEMS = 25

DELETE_OUTPUT_DIRECTORY = True

DISQUS_SITENAME = "miroslawzalewski"
GOOGLE_ANALYTICS = 'UA-2205779-7'
