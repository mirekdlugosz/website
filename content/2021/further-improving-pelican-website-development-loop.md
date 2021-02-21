Title: Further improving Pelican website development loop
Slug: further-improving-pelican-website-development-loop
Date: 2021-02-21 13:27:15
Category: Blog
Tags: planet Python, Python

I continue experiments with improving Pelican-based website build time during local development. I managed to get some nice results.

<!-- more -->

In [previous article]({filename}improving-pelican-website-development-loop.md) I mentioned that site build time could be improved further with partial rebuilds, possibly by using `--write-selected` flag. For this to work, we would also need livereload package to pass changed file path to callback function.

I have tried running Pelican with that flag, but I have not noticed any impact on site build time. Searching the web lead me to [issue #2678 in main Pelican repo](https://github.com/getpelican/pelican/issues/2678) - as it turns out, `WRITE_SELECTED` setting got broken somewhere along the way and simply does not work as of Pelican 4.5.4.

After brief survey of Pelican source code, I identified function responsible for deciding whether content should be written or not: [`is_selected_for_writing`](https://github.com/getpelican/pelican/blob/2eb9c26cdb367033692cb75f3c8d9937cf7db94d/pelican/utils.py#L937). I modified it locally just enough to get it somewhat working, so I could decide how to move forward:

```diff
--- pelican/utils.py
+++ pelican/utils.py
@@ -942,9 +942,12 @@ def is_selected_for_writing(settings, path):
     any path is selected for writing.
     '''
     if settings['WRITE_SELECTED']:
-        return path in settings['WRITE_SELECTED']
+        for selected_path in settings['WRITE_SELECTED']:
+            if selected_path in path:
+                return True
+        return False
     else:
         return True
```

Unfortunately, `WRITE_SELECTED` did not live up to its promise. Full build of my website took 0.91 second. With `WRITE_SELECTED` set to two articles, that number was brought down to 0.85 second - a reduction by mere 6%.

These results, underwhelming as they were, do make sense when you consider where in the pipeline the filtering is applied. Before Pelican can decide if file should be written, it has already read all the content from disk, parsed it, filled in gaps in posts metadata from other sources and run a ton of signals - including all generator signals, which are commonly used by plugins modifying article contents.

But what if Pelican could skip content before reading it, instead of before writing it? Proof of concept turned out to be rather succinct:

```diff
--- pelican/readers.py
+++ pelican/readers.py
@@ -537,6 +537,8 @@ class Readers(FileStampDataCacher):
 
         path = os.path.abspath(os.path.join(base_path, path))
         source_path = posixize_path(os.path.relpath(path, base_path))
+        if 'READ_SELECTED' in self.settings and self.settings['READ_SELECTED'] not in source_path:
+            raise ValueError(f"Skipping {source_path}")
--- pelican/generators.py
+++ pelican/generators.py
@@ -808,13 +808,21 @@ class StaticGenerator(Generator):
                 if self._is_potential_source_path(f):
                     continue
 
-            static = self.readers.read_file(
-                base_path=self.path, path=f, content_class=Static,
-                fmt='static', context=self.context,
-                preread_signal=signals.static_generator_preread,
-                preread_sender=self,
-                context_signal=signals.static_generator_context,
-                context_sender=self)
+            try:
+                static = self.readers.read_file(
+                    base_path=self.path, path=f, content_class=Static,
+                    fmt='static', context=self.context,
+                    preread_signal=signals.static_generator_preread,
+                    preread_sender=self,
+                    context_signal=signals.static_generator_context,
+                    context_sender=self)
+            except Exception as e:
+                logger.error(
+                    'Could not process %s\n%s', f, e,
+                    exc_info=self.settings.get('DEBUG', False))
+                self._add_failed_source_path(f, static=True)
+                continue
+
```

Impact of this small patch was both surprising and impressive. My site built in mere 0.13 second. Compared to full build, that is reduction by 85%! Wow!

Unfortunately, that improvement has a cost. The consequence of limiting the amount of content that Pelican has to process is that all the skipped content is missing from created output files. If your theme puts links to discovered pages in top navigation bar, that bar might turn out empty. If your article links to another article, Pelican might complain that target article could not be found. Your archives pages might contain only this one article you have most recently modified.

I have [posted my proof of concept patch to Pelican community](https://github.com/getpelican/pelican/pull/2848) for further discussion, and was told that assortment of existing settings can be used to achieve similar results.

So far I have learned how to tell Pelican to read only subset of source files, and that doing so can significantly reduce site build time. But that brings me to the next problem - how can livereload callback function learn the path of changed source file?

It took me a moment to find out that livereload internals do know the path of file that changed. However, I could not find anything in package documentation about using this data.

After some more code reading, I learned that livereload Watcher class looks at callback function signature and may pass list of changed files as an argument, if callback does expect an argument. Otherwise, callback is invoked without any arguments. So that data is available to callback function, but function must declare that it will use it.

Later I discovered that even when function expects argument, it can still be invoked by Watcher without any - that happens when one of the watched files is removed. This means that callback function must take **optional** argument.

Now that we have all the building blocks, it's time to wire them up. The general idea is that callback function will obtain path of modified file and prepare three settings for next Pelican build: `ARTICLE_PATHS`, `PAGE_PATHS` and `STATIC_PATHS`. One of them will contain path to modified file, the other two will be empty.

This is how my current implementation looks like:

```python
@task
def get_path_settings(paths):
    """Helper for liveserver function. Groups modified file into PAGE, ARTICLE
    or STATIC path variables. Returns dict of all three, or empty dict.
    """
    PAGE_PATHS = []
    ARTICLE_PATHS = []
    STATIC_PATHS = []

    for filepath in paths:
        filepath = Path(filepath)

        if not filepath.is_relative_to(SETTINGS['PATH']):
            return {}

        filepath = filepath.relative_to(SETTINGS['PATH']).as_posix()
        if filepath.startswith(tuple(SETTINGS['STATIC_PATHS'])):
            STATIC_PATHS.append(filepath)
        elif filepath.startswith(tuple(SETTINGS['PAGE_PATHS'])):
            PAGE_PATHS.append(filepath)
        else:
            ARTICLE_PATHS.append(filepath)

    return {
        'PAGE_PATHS': PAGE_PATHS,
        'ARTICLE_PATHS': ARTICLE_PATHS,
        'STATIC_PATHS': STATIC_PATHS
    }


@task
def devserver(c, full_rebuild=False):
    from livereload import Server

    def cached_html(paths=None):
        extra_settings = 'CACHE_CONTENT=True LOAD_CONTENT_CACHE=True'

        if paths and not full_rebuild:
            paths_settings = get_path_settings(paths)
            for variable, changed in paths_settings.items():
                value_as_json = json.dumps(changed)
                extra_settings = f"{extra_settings} {variable}='{value_as_json}'"

        html(c, extra_settings=extra_settings)

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

One limitation of this approach is that when I modify file outside of main content directory (e.g. a theme template), it will trigger full rebuild. So far, I have not found a way to tell Pelican that it should build only content which is using specific template.

Since I have just started using this approach, possibly there are other limitations I am not yet aware of. As a precaution, I have also added `full_rebuild` argument to the task - it disables preparation of environment variables and just runs full build of the site. So if filtered build ever becomes problematic for my specific use-case, I can call `inv liveserver --full-rebuild` and continue working, just with a little slower builds.
