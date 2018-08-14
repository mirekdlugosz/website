#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

SITEURL = 'https://miroslaw-zalewski.eu'
RELATIVE_URLS = False

FEED_DOMAIN = SITEURL
FEED_ALL_ATOM = 'blog/feeds/atom.xml'
FEED_ALL_RSS = 'blog/feeds/rss.xml'
# CATEGORY_FEED_ATOM = 'blog/feeds/%s.atom.xml'
# CATEGORY_FEED_RSS = 'blog/feeds/%s.rss.xml'
TAG_FEED_ATOM = 'blog/feeds/%s.atom.xml'
TAG_FEED_RSS = 'blog/feeds/%s.rss.xml'
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
FEED_MAX_ITEMS = 25

DELETE_OUTPUT_DIRECTORY = True

# Following items are often useful when publishing

DISQUS_SITENAME = "miroslawzalewski"
# GOOGLE_ANALYTICS = ""
