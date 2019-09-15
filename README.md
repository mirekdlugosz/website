My personal website, hosted at [mirekdlugosz.com](https://mirekdlugosz.com). Built with [Pelican](https://getpelican.com) (Python 3).

Theme is very highly customized [pelican-bootstrap3](https://github.com/getpelican/pelican-themes/tree/master/pelican-bootstrap3), now running [Bootstrap 4](https://getbootstrap.com/).

You need Node to build the theme (`npm install && npx gulp`). You need pelican, typogrify and Markdown the build the site (see `requirements.txt`). You also need [pelican-plugins](https://github.com/getpelican/pelican-plugins) in **parent** of this directory.

## Using Docker to build the site

First, build container image with all dependencies:

    docker build --network host -t pelican_website .

Now, run container to build the site itself. There are couple of ways to approach it:

1. Build website and copy artifacts back to host:

        docker run pelican_website publish
        docker cp $(docker ps -lq):/var/www/pelican/output ./output/
        docker rm $(docker ps -lq) # remove container

2. Use container to run multiple build commands:

        # start container
        docker run -dt -p 8000:8000 --entrypoint 'sh' pelican_website
        docker exec $(docker ps -lq) make html
        docker exec $(docker ps -lq) make serve
        # or connect for interactive session
        docker exec -ti $(docker ps -lq) sh
        # once you are done, remove the container
        docker stop $(docker ps -lq)
        docker rm $(docker ps -lq)

3. Run interactive session in container - container is removed automatically once session ends:

        docker run --rm -ti -p 8000:8000 --entrypoint /bin/sh pelican_website

You can share local `content` directory with container by appending following option to any `run` command above: `-v ./content/:/var/www/pelican/content/`. This way you won't have to rebuild container image every time you change site content. You still need to rebuild container if you change the theme.
