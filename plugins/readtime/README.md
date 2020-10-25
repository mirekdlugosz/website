# 'pelican-readtime' - A Read Time Plugin for Pelican Static Site Generator

Usage
-----

This plugin only uses standard modules(re, html, math, etc), so no extra module installation like BeautifuSoup. To use it, just install the plugin in virtual environment shared with pelican.

Then you can put the following code in whichever template you what, like *article.html*.

```html
    {% if article.readtime %}
    <div><b>Read in {{article.readtime.minutes}} min.</b></div>
    {% endif %}
```

Credits
-----

This is custom fork of `readtime` plugin created by [Michael Li](https://github.com/wayofnumbers), which itself is revised version of [jmaister's readtime plugin](https://github.com/jmaister/readtime).


Reference
-----
[1] Wikipedia - [Words per minute](https://en.wikipedia.org/wiki/Words_per_minute) <br>
[2] Medium - [Read Time](https://help.medium.com/hc/en-us/articles/214991667-Read-time) <br>
