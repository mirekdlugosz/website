import re

# this does the actual plugin registration, by putting `register` in namespace
from pelican.plugins.liquid_tags import register
from pelican.plugins.liquid_tags.mdx_liquid_tags import LiquidTags

THUMB_RE = re.compile(r'(?P<filepath>\S*)\s*(?P<display_caption>display_caption\s*)?\s*(?P<caption>.*)?', re.MULTILINE)


@LiquidTags.register('thumb')
def thumb(preprocessor, tag, markup):
    """
    Generates img tag for thumbnail wrapped in link to full-sized file

    Syntax is:
    {% thumb path_to_file [display_caption] [image description] %}
    """
    if not markup:
        raise ValueError("{% thumb %} requires filename")

    matches = THUMB_RE.match(markup)
    image_path = matches.group('filepath')
    display_caption = bool(matches.group('display_caption'))
    caption_text = matches.group('caption')

    if display_caption and not caption_text:
        raise ValueError(f"{{% thumb {image_path} %}}: display_caption without image description is invalid")

    image_stem, image_suffix = image_path.split('.')
    thumb_path = f"{image_stem}-min.{image_suffix}"

    alt_text = ""
    if caption_text:
        alt_text = f'" alt="{caption_text}'

    tag = f'<a href="{image_path}"><img src="{thumb_path}{alt_text}"></a>'

    if display_caption:
        tag = f'<figure>{tag}<figcaption>{caption_text}</figcaption></figure>'

    return tag
