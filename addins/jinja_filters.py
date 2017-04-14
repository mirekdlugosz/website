#!/usr/bin/env python
# -*- coding: utf-8 -*- #

import datetime

def dict_replace(text, replacements):
    for key, val in replacements.iteritems():
        text = text.replace(key, val)
    return text

def current_year(t):
    today = datetime.date.today()
    return today.strftime("%Y")
