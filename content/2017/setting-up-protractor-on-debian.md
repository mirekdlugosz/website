Title: Setting up Protractor on Debian GNU/Linux
Slug: setting-up-protractor-on-debian-gnu-linux
Date: 2017-04-18 12:45:12
Category: Blog
Tags: Linux, Protractor, tutorial

[Protractor](http://www.protractortest.org/) is test framework for web applications written on top of [Angular](https://angular.io/). Unfortunately, installing it on Debian is non-obvious, as it has not yet found its way into repository and existing documentation is catered to needs of Mac OS users. This guide will help you to get through this process without messing up your entire system.

<!-- more -->

## Install Node

Protractor runs on top of [Node](https://nodejs.org), which you must install before doing anything else:

    # apt-get install nodejs nodejs-legacy

Contrary to its name, `nodejs-legacy` is not legacy version of Node software, but compatibility layer that lets it use `node` binary name. Node in Debian is invoked using `nodejs` binary, because [another program in repository already provided `node` name](https://lists.debian.org/debian-devel-announce/2012/07/msg00002.html). 
Since entire Node ecosystem expects `node` to refer to Node binary, installing compatibility layer saves a lot of hassle; and since [that other program has been removed](https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=797929), there is no reason to not install it.

As a side note, Debian proper provides ancient Node version that you shouldn't bother with. Latest LTS version (as of time of this writing) can be found in [experimental](https://packages.debian.org/experimental/nodejs). Use [apt-pinning](http://jaqque.sbih.org/kplug/apt-pinning.html) to get it.

While we are at installing packages from repository, you might also consider installing `jq` and `default-jre`. `jq` is nice little shell utility to retrieve data from JSON files; we will use it in next step when downloading npm. `default-jre` pulls in `openjdk-8-jre` (Java 8), which is required to run Selenium standalone server. Protractor can connect to browsers directly, so running Selenium standalone is not mandatory, but it seems to be preferred by majority of community. You might as well pull it in now.

## Install and configure npm

Protractor can be installed using npm, default package manager for Node development environment. Upstream distributes npm with Node itself, but Debian decided to decouple these packages. The problem is, Debian's npm package fell out of grace many years ago and is so outdated, that it outright fails to install some packages. At time of this writing, it was even [considered for removal](https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=857986). Luckily, npm can be installed or updated separately from Node. By using npm. That leaves us in funny place, where we need npm, but we need npm to install npm.

This can be remedied by downloading npm manually and running this version to install npm.

	$ cd /tmp/
	$ wget 'https://registry.npmjs.org/npm/' -O registry.json
	$ wget "https://registry.npmjs.org/npm/-/npm-$(jq -r '."dist-tags".latest' registry.json).tgz"
	$ tar xf /tmp/npm-*.tgz

At this point we have npm ready to use in `/tmp/package/bin/npm-cli.js`, but before we actually run it, we should consider one quirk of this package manager. Namely, it installs everything in `node_modules` subdirectory of **current working directory**. This makes it easy to create semi-virtual environment with all packages needed for project you are working on, but it also makes it easy to install binaries in random places in directory tree, never to find them again.

npm also supports installation of global packages, but they are system-wide and go to `/usr/`.

To solve these issues, we will configure npm to treat global packages as available to current user only. We will need to repeat this setup for each user on the system, but it is small price to pay for centralized storage of node modules accessible from anywhere without messing up with file system permissions.

Start by creating `~/.npm-global` directory. Directory structure inside closely resembles `~/.local`, which would be more appropriate from XDG point, but I do enjoy ability to `rm -rf` one directory in order to nuke entire thing.

Then, add `~/.npm-global/bin/` directory to your `$PATH`. For current shell session, this can be done with command below. For persistent change, you should modify `~/.profile` or `~/.bashrc` file. Depending on your system setup, you might need to log out and log in back again to see changes in new terminal emulator windows.

    $ export PATH=~/.npm-global/bin:$PATH

Now you can set up npm to use new directory and install npm properly:

	$ ./package/bin/npm-cli.js config set prefix '~/.npm-global'
	$ ./package/bin/npm-cli.js install -g npm@latest

## Install Protractor

After all these changes, you can finally install Protractor

    $ npm install -g protractor

Protractor requires WebDriver browser drivers to be available. You can download and install them with command below; I have not yet found a way to use `chromiumdriver` package from Debian repository.

    $ webdriver-manager update

As noted before, majority of Protractor users seem to talk with browsers through Selenium standalone server. If you are among them, make sure to run `webdriver-manager start` before running `protractor`. If you prefer for Protractor to talk with browsers directly (works only for chromedriver and geckodriver, i.e. Chrome, Chromium and Firefox), make sure that your `protractor.conf.js` file contains following line:

    directConnect: true
