#!/usr/bin/env python

# {{{ imports
import sys
from pathlib import Path
from ruamel.yaml import YAML
sys.path.insert(0, str(Path(__file__).parent))
import addins.jinja_filters
# }}}
# {{{ main metadata
AUTHOR = 'Mirek Długosz'
SITENAME = 'Mirek Długosz personal website'
SITEURL = ''

PATH = 'content'
TIMEZONE = 'Europe/Warsaw'
LOCALE = 'en_US.utf8'
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

DIRECT_TEMPLATES = ['index']
INDEX_SAVE_AS = 'blog/index.html'

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
    ('Email', 'mailto:mirek %at% mirekdlugosz.com', 'envelope'),
    ('Mastodon', 'https://fosstodon.org/@mirekdlugosz', 'mastodon'),
    ('LinkedIn', 'https://www.linkedin.com/in/mirekdlugosz/en', 'linkedin'),
)

USE_OPEN_GRAPH = True
TWITTER_CARDS = True
TWITTER_USERNAME = "mirekdlugosz"
MASTODON_HANDLES = [
    "https://fosstodon.org/@mirekdlugosz",
]
FEDIVERSE_CREATORS = [
    "@mirekdlugosz@fosstodon.org",
]

JINJA_FILTERS = {
    'dict_replace': addins.jinja_filters.dict_replace,
    'markdown': addins.jinja_filters.from_markdown,
}

PROJECTS = YAML(typ="safe").load(Path("projects.yaml"))
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

THUMBNAIL_SIZES = {
    'content/2021/pelican-social-cards-announcement/sample-card-with-image.png': (342, 300),
    'content/2024/30-days-of-ai-in-testing-experience-report/responses-plot.png': (800, 502),
    'content/2025/customizing-fonts-look-with-opentype-features/font-feature-tester-example.png': (783, 406),
    'content/2025/customizing-fonts-look-with-opentype-features/font-feature-tester-ui.png': (506, 391),
    'content/2025/interesting-bugs-peculiar-intermittent-failure-in-testing-pipeline/infrastructure-diagram.png': (500, 320),
    'content/2025/interesting-bugs-peculiar-intermittent-failure-in-testing-pipeline/more-readable-log.png': (500, 242),
    'content/2025/interesting-bugs-peculiar-intermittent-failure-in-testing-pipeline/failures-spreadsheet.png': (500, 305),
    'content/2025/understanding-python-web-deployment/main-model.png': (650, 232),
}

SOCIAL_CARDS_TEMPLATE = './theme/src/img/social-card-template.jpg'
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
SOCIAL_CARDS_FORMAT_EXTENSION = 'jpg'
# }}}

# vim: fdm=marker
