#!/usr/bin/env python
# This file is only used if you use `inv publish` or
# explicitly specify it as your config file.

import os
import importlib
import sys
sys.path.append(os.curdir)

# * Python caches imports
# * within invoke, this is all single Python process
# * pelicanconf has been imported by socialcardsconf
# So if this is our first `inv publish` after `clean`, pelicanconf
# is cached version executed back when social cards were generated.
# Back then, `EXTRA_PATH_METADATA` could not include card images,
# because they were not generated yet. As a result, first `publish`
# after `clean` would put social card images in the wrong place.
# importlib.reload() fixes the problem and `publish` becomes
# idempotent again.
import pelicanconf
importlib.reload(pelicanconf)
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
