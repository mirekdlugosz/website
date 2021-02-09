Title: Improving Pelican website development loop
Slug: improving-pelican-website-development-loop
Date: 2021-02-09 11:38:27
Category: Blog
Tags: planet Python, Python, tutorial

I spend more time tinkering with my website than writing actual content. Here's how I streamlined feedback loop on my Pelican-based website.

<!-- more -->

Over the years, my main development flow looked something like that:

1. Change file
2. Possibly build static assets
3. Build site itself
4. Serve the site using some http server
5. Open the page in web browser, or refresh it if it's already opened
6. Check how the site looks, find possible problems, mistakes, typos etc.
7. Shut down http server
8. Go back to step 1

Since I started using it, Pelican itself included some convenience functions that removed few steps from my loop. Possibly the most significant was version 4.0.0, which included `--listen` flag. Along with `--autoreload`, it relieves me from having to manually build the site on source file change, starting http server and shutting it down.

Unfortunately, that does not apply to all the files I could be changing. I am using gulp to compile SCSS files into CSS, bundle styles/scripts into single file and minimize their size. While Pelican is able to pick up changes in theme files, it is not aware of theme source files and how to build them. So I still need to call `npx gulp` after each change when working on styling or scripts.

Another thing I missed a little is automatic refreshing of page in browser on website changes. Hugo and Vue.js development environments have that, and as far as I can tell, it completely solves the problem of browser using outdated, cached version of static resource. On Pelican, there were times when I had to manually navigate to stylesheet file and refresh it, since browser did not pick up changes I have made.

The other day, I learned that Pelican 4.1.0 introduced livereload server, which does exactly that. This is how default invoke task looks like:


```python
def livereload(c):
    from livereload import Server
    build(c)
    server = Server()
    # Watch the base settings file
    server.watch(CONFIG['settings_base'], lambda: build(c))
    # Watch content source files
    content_file_extensions = ['.md', '.rst']
    for extension in content_file_extensions:
        content_blob = '{0}/**/*{1}'.format(SETTINGS['PATH'], extension)
        server.watch(content_blob, lambda: build(c))
    # Watch the theme's templates and static assets
    theme_path = SETTINGS['THEME']
    server.watch('{}/templates/*.html'.format(theme_path), lambda: build(c))
    static_file_extensions = ['.css', '.js']
    for extension in static_file_extensions:
        static_file = '{0}/static/**/*{1}'.format(theme_path, extension)
        server.watch(static_file, lambda: build(c))
    # Serve output path on configured host and port
    server.serve(host=CONFIG['host'], port=CONFIG['port'], root=CONFIG['deploy_path'])
```

Apart from finding it little hard to read, I have certain reservations towards some of design choices. This version assumes Jinja files in theme are all in single directory, without any subdirectories - while I have some recurring sections extracted into partials. JS and CSS files are certainly most often changed, but sometimes I also work on images - and I would like Pelican to pick their changes, too. Finally, I don't like how watcher's callback function is specified four different times - if I wanted to change callback, I would have to do it multiple times.

After fixing these issues, I ended up with:


```python
def devserver(c):
    from livereload import Server

    server = Server()
    watched_globs = [
        CONFIG['settings_base'],
        f'{SETTINGS["PATH"]}/**/*.md',
        f'{SETTINGS["THEME"]}/templates/**/*',
        f'{SETTINGS["THEME"]}/static/**/*',
    ]
    for glob in watched_globs:
        server.watch(glob, lambda: html(c))
    html(c)
    server.serve(host=CONFIG['host'], port=CONFIG['port'], root=CONFIG['deploy_path'])
```

(Yes, I renamed `livereload` to `devserver` and `build` to `html`.)

Once I ran that task, I discovered it takes about 1 second for Pelican to rebuild site on any file change. That's a little too much for my taste - I found myself waiting for refresh to happen, wondering if it wouldn't be faster if I just hit refresh myself. I do want convenience, but not at the cost of that much speed.

Luckily, Pelican has built-in caching mechanism, and since version 4.5.0 allows to override specific settings from command line. I needed to change main building task slightly, and extracted watcher callback function for better readability:

```python
def html(c, extra_settings=None):
    cmd = '-s {settings_base}'
    if extra_settings:
        cmd = f'{cmd} -e {extra_settings}'
    pelican_run(cmd.format(**CONFIG))


def devserver(c):
    from livereload import Server

    def cached_html():
        html(c, extra_settings='CACHE_CONTENT=True LOAD_CONTENT_CACHE=True')

    server = Server()
    watched_globs = [
        CONFIG['settings_base'],
        f'{SETTINGS["PATH"]}/**/*.md',
        f'{SETTINGS["THEME"]}/templates/**/*',
        f'{SETTINGS["THEME"]}/static/**/*',
    ]
    for glob in watched_globs:
        server.watch(glob, cached_html)
    cached_html()
    server.serve(host=CONFIG['host'], port=CONFIG['port'], root=CONFIG['deploy_path'])
```

Now each file change results in full page rebuild after only 600 ms, which is reduction by around 40%. Same speedup ratio is maintained on another, more powerful machine, where caching brought rebuild time from 500 ms to 300 ms.

It saddens me a little that this is still few times slower than Hugo, which is capable of partial rebuilds in server mode. It seems that Pelican can do partial rebuilds, too, through `--write-selected` flag - however, it requires path to output file instead of source. Moreover, there doesn't seem to be an easy way for liveserver watcher to tell callback function which file exactly changed.

While working on this, I discovered that I already have gulp task for watching file changes and rebuilding static assets. It works in similar fashion, as foreground process that blocks terminal and finishes on `Ctrl + C`. I decided to let my main task invoke it in the background and redirect its output to main terminal window. As a result, messages from two servers are intertwined, but at least I can see what is happening.

```python
def devserver(c):
    from livereload import Server

    def cached_html():
        html(c, extra_settings='CACHE_CONTENT=True LOAD_CONTENT_CACHE=True')

    def start_npm_devserver():
        cmd = "npm run devserver".split()
        proc = subprocess.Popen(
            cmd,
            stdout=sys.stdout,
            stderr=subprocess.STDOUT,
            cwd=SETTINGS["THEME"],
        )
        return proc

    npm_devserver = start_npm_devserver()
    server = Server()
    watched_globs = [
        CONFIG['settings_base'],
        f'{SETTINGS["PATH"]}/**/*.md',
        f'{SETTINGS["THEME"]}/templates/**/*',
        f'{SETTINGS["THEME"]}/static/**/*',
    ]
    for glob in watched_globs:
        server.watch(glob, cached_html)
    cached_html()
    server.serve(host=CONFIG['host'], port=CONFIG['port'], root=CONFIG['deploy_path'])
    npm_devserver.terminate()
```

That version accomplishes everything that I wanted: changing any file results in automatic site rebuild, changing sources for static asset rebuilds them, and page in browser is refreshed automatically. My main loop now looks something like that:

1. Start development server (`inv devserver`)
2. Change file
3. Check how the site looks, find possible problems, mistakes, typos etc.
4. Go back to step 2
