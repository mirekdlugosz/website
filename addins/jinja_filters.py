#!/usr/bin/env python
# -*- coding: utf-8 -*- #


def dict_replace(text, replacements):
    for key, val in replacements.items():
        text = text.replace(key, val)
    return text
