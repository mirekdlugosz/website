My personal website, hosted at [mirekdlugosz.com](https://mirekdlugosz.com). Built with [Pelican](https://getpelican.com) (Python 3).

Theme is [pelican-bootstrap3](https://github.com/getpelican/pelican-themes/tree/master/pelican-bootstrap3) customized beyond recognition. In fact, there's no CSS framework at all.

You need Node, npm and Python 3. Building website from new clone would be something like that:

```
python3 -m venv websitevenv
. ./websitevenv/bin/activate
pip install -U pip wheel
pip install -r requirements.txt
(cd theme/ && npm install)
invoke publish
```

See `invoke --list` for all the tasks.
