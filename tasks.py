import json
import logging
import os
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

from invoke import task
from invoke.tasks import call
from invoke.main import program
from pelican import main as pelican_main
from pelican.server import ComplexHTTPRequestHandler, RootedHTTPServer
from pelican.settings import DEFAULT_CONFIG, get_settings_from_file
from PIL import Image

SETTINGS_FILE_BASE = 'pelicanconf.py'
SETTINGS = {}
SETTINGS.update(DEFAULT_CONFIG)
LOCAL_SETTINGS = get_settings_from_file(SETTINGS_FILE_BASE)
SETTINGS.update(LOCAL_SETTINGS)


def env_var(name):
    return bool(os.environ.get(name, False))


CONFIG = {
    'settings_base': SETTINGS_FILE_BASE,
    'settings_publish': 'publishconf.py',
    'debug': env_var('DEBUG'),
    # Output path. Can be absolute or relative to tasks.py. Default: 'output'
    'deploy_path': SETTINGS['OUTPUT_PATH'],
    # Remote server configuration
    'domain': 'mirekdlugosz.com',
    'ssh_user': 'minio',
    'ssh_host': 'mydevil',
    'ssh_port': '22',
    'ssh_path': '/home/{ssh_user}/domains/{domain}/public_html/',
    # Host and port for `serve`
    'host': 'localhost',
    'port': 8000,
}

CONFIG['ssh_path'] = CONFIG['ssh_path'].format(**CONFIG)


@task
def clean(c, path=CONFIG['deploy_path']):
    """Remove generated files"""
    dir_path = Path(path)
    if dir_path.is_dir():
        shutil.rmtree(dir_path)


@task
def thumbnails(c, clean=False):
    """Generate image thumbnails"""
    cmd = [
        'python3',
        './scripts/generate-thumbnails.py',
        '--ignore', '/social-thumbs/'
    ]
    if clean:
        cmd.append('--rm')
    if CONFIG['debug']:
        cmd.append('--debug')
    c.run(' '.join(cmd))


@task
def clean_thumbnails(c):
    """Remove generated thumbnails"""
    thumbnails(c, clean=True)


@task
def webp(c, directory=""):
    """Generate webp version of images in output directory"""
    def is_image(path):
        suffix = Path(path).suffix.strip('.')
        return suffix in ('jpg', 'jpeg', 'png')

    logger = logging.getLogger('webp')
    log_level = logging.DEBUG if CONFIG['debug'] else logging.INFO
    logger.setLevel(log_level)

    if not directory:
        directory = CONFIG['deploy_path']

    print(f"Generating webp of image files inside '{directory}'")
    input_dir = Path(directory)

    for filepath in input_dir.glob('**/*'):
        if not is_image(filepath):
            continue
        output_path = f"{filepath.as_posix()}.webp"
        logger.debug(f"Writing {output_path}...")
        try:
            with Image.open(filepath) as im:
                im.save(output_path)
            logger.debug("   Done")
        except OSError:
            logger.error(
                f"Failed to process {filepath.as_posix()}", exc_info=True
            )


@task
def theme(c):
    """Generate static theme files"""
    with c.cd('theme/'):
        c.run('npx gulp')


@task(pre=[clean, thumbnails])
def html(c, extra_settings=None):
    """Build local version of site"""
    cmd = '-s {settings_base}'
    if CONFIG['debug']:
        cmd = f'{cmd} -D'
    if extra_settings:
        cmd = f'{cmd} -e {extra_settings}'
    pelican_run(cmd.format(**CONFIG))


@task
def serve(c):
    """Serve existing build at http://$HOST:$PORT/ (default is localhost:8000)"""

    class AddressReuseTCPServer(RootedHTTPServer):
        allow_reuse_address = True

    server = AddressReuseTCPServer(
        CONFIG['deploy_path'],
        (CONFIG['host'], CONFIG['port']),
        ComplexHTTPRequestHandler)

    sys.stderr.write('Serving at {host}:{port} ...\n'.format(**CONFIG))
    server.serve_forever()


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


@task(pre=[clean, thumbnails], post=[call(clean, path=SETTINGS["CACHE_PATH"])])
def devserver(c, full_rebuild=False):
    """Automatically rebuild site and reload browser tab upon file modification"""
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


@task(pre=[clean, thumbnails, theme])
def publish(c):
    """Build production version of site"""
    cmd = '-s {settings_publish}'
    if CONFIG['debug']:
        cmd = f'{cmd} -D'
    pelican_run(cmd.format(**CONFIG))


@task(pre=[publish, webp])
def rsync_upload(c):
    """Publish to production via rsync"""
    rsync_cmd = [
        'rsync',
        '-e "ssh -p {ssh_port}"',
        '-P',
        '-rvzc',
        '--delete',
        '--cvs-exclude',
        "--exclude='.*.swp'",
        '{} {ssh_user}@{ssh_host}:{ssh_path}',
    ]
    if env_var('DRY_RUN'):
        rsync_cmd.append('--dry-run')
    c.run(' '.join(rsync_cmd).format(
        CONFIG['deploy_path'].rstrip('/') + '/', **CONFIG
    ))
    purge_remote_cache_cmd = ' '.join([
        'ssh',
        '-p {ssh_port}',
        '{ssh_host}',
        "'devil www options {domain} cache purge'",
    ])
    if not env_var('DRY_RUN'):
        c.run(purge_remote_cache_cmd.format(**CONFIG))


def pelican_run(cmd):
    cmd += ' ' + program.core.remainder  # allows to pass-through args to pelican
    pelican_main(shlex.split(cmd))
