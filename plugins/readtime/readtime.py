import logging
import math

from pelican import signals, contents
from html.parser import HTMLParser

logger = logging.getLogger(__name__)


class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.fed = []

    # this method is called whenever a 'data' is encountered.
    def handle_data(self, d):
        self.fed.append(d)

    # join all content word into one long sentence for further processing
    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)   		# Feed the class with html content, get the fed list
    return s.get_data()


def calculate_readtime(content_object):
    if isinstance(content_object, contents.Static):
        return

    READTIME_AVG_WPM = content_object.settings.get('READTIME_AVG_WPM', 230)
    text = strip_tags(content_object.content)
    words = text.split()
    num_words = len(words)
    minutes = int(math.ceil(num_words / READTIME_AVG_WPM))

    # set minimum read time to 1 minute
    minutes = max(minutes, 1)

    logger.debug(f" {content_object.get_relative_source_path()} approximate read time: {minutes}")

    content_object.readtime = {
        "minutes": minutes,
    }


def register():
    signals.content_object_init.connect(calculate_readtime)
