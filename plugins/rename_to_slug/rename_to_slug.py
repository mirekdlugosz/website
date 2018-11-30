'''
rename_to_slug
===================================

This plugin ensures that local file name is the same as article slug
'''

import os
from pelican import signals


def rename_to_slug(generator, content):
    src = content.source_path
    _, ext = os.path.splitext(src)
    dest = os.path.join(os.path.dirname(src), content.slug + ext)
    if os.path.basename(src) != os.path.basename(dest):
        os.rename(src, dest)


def register():
    signals.article_generator_write_article.connect(rename_to_slug)
