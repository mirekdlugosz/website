Title: Simple visual regression checking with Selenium and ImageMagick
Slug: simple-visual-regression-checking-with-selenium-and-imagemagick
Date: 2019-11-24 20:48:57
Category: Blog
Tags: automation, practice, Python, testing, tutorial

I wanted to ensure that recent change did not break backwards compatibility and I ended up with visual regression checking script built with freely available software.

<!-- more -->

Recently, I switched object ids used by [createpokemon.team](https://createpokemon.team/). One of the steps in entire process was creating backwards compatibility layer - these ids are exposed in URL and there might be bookmarks and links posted around which could suddenly stop loading some data. In my quest to gain confidence that this solution works, I created simple visual regression checking tool.

## Talk is cheap, show me the code!

[Completed solution is hosted at GitHub](https://github.com/mirekdlugosz/scrapbook/tree/master/create-pokemon-team-visual-diff). This post is intertwined with code samples, but they are not intended to fully work on their own.

## Testing goals and strategy

Overarching goal of this activity was rather vague "demonstrating that existing URLs continue to work".

There are two main sources of "existing URLs". One is version deployed to production. I can fill the form, copy part of URL and test new version against it. Since I know how backwards compatibility procedure works, I can come up with data that might be problematic, as well as reference data that should not be problematic.

Another source are real URLs that real users navigated to out in the wild. Thankfully, I added Google Analytics to website, and it does provide comprehensive list of all URLs - along with number of visits for each. With that data, I can prioritize checking Pokemon, moves and teams that are most popular.

"Continue to work" means two things: that form is populated with team data provided in URL, and that analysis outcome is unchanged.

Since these are questions about data, it's only natural to think about it in isolation of presentation. That reasoning would set us on path that includes gathering data from website – and since there is no machine-readable output available, that means scraping. But we can abuse the fact that there were no changes in UI and the same output will be presented in the same way. If there is no visible difference between old and new version, then data in both is sure to be the same. We don't need to know what the data actually is.

## Capturing screenshot with Selenium

In first iteration of my work, I focused on gathering screen snapshot automatically. To do that, I need to open web browser, navigate to required page, ensure that all client-side operations have completed, actually capture image of visible site content and save that on disk. This can be done in just couple lines of code:

```python
import random
from selenium import webdriver

teams = []  # loading URLs is skipped for brevity
team = random.choice(teams)

chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=chrome_options)
base_url = 'http://localhost:4200'
driver.get(f"{base_url}{team}")
time.sleep(5)
driver.save_screenshot('/tmp/selenium.png')
driver.quit()
```

After confirming that it indeed opens required page and saves screenshot, I added two command line flags:

```python
chrome_options.add_argument('--headless')
chrome_options.add_argument('--window-size=1920,2160')
```

This way browser opened by script is not visible on screen, so I can use computer without risk of interfering with automation. I increased window size vertically to gather entire page content on single run.

## Visual difference between two images

Thanks to [ImageMagick](https://imagemagick.org) library and set of tools, visual difference between two images can be produced with single command:

```sh
compare -compose src FIRST_FILE SECOND_FILE OUTPUT_FILE
```

I ran my script two times and saved page screenshots as two distinct files. After feeding them to above command, I obtained this (click to see full size):

{% figure
    {attach}simple-visual-regression-checking-with-selenium-and-imagemagick/sample-difference.png |
    caption=Sample visual difference between two teams |
    display_caption
%}

## Creating safe filenames

I want the ability to track image with differences to URL that triggered them, in case I need to analyse them in closer detail.

Using URL as image name seems natural. Unfortunately, full team definition can be quite lengthy (longest URL in my sample is 528 characters long), and ext4 file system limits file name length to 255 bytes (characters). This is often not enough.

To ensure uniqueness of file name while maintaining its limited length, I decided to use hash (checksum) of URL string as file name. To meet traceability requirement, I stored both hash and URL in separate file.

```python
import hashlib

def fs_sanitize(string):
    hash_ = hashlib.sha256(string.encode('utf-8'))
    return f"{hash_.hexdigest()}.png"

map_handle = open('map.txt', 'w')

team = random.choice(teams)
fs_friendly_url = fs_sanitize(team)
map_handle.write(f"{fs_friendly_url}\t{team}\n")

driver = webdriver.Chrome(options=chrome_options)
base_url = 'http://localhost:4200'
driver.get(f"{base_url}{team}")
time.sleep(5)

driver.save_screenshot(fs_friendly_url)

driver.quit()
map_handle.close()
```

## Optimizations

Google analytics stored some 400 000 unique URLs. This is way too much to check during a weekend project, not to mention that they can be downloaded only in batches of 5000. 

So first optimization is downloading only subset of them. I opted for 10&nbsp;000. Given that from 1600th item onwards, each URL was accessed less than 10 times, this is essentially exhaustive list of "popular" URLs and some random sample of less-popular URL.

But 10 000 is still too much. Assuming it would take only 3 seconds to process one team, it would still take good 8 hours to process all of them. I further reduced size of that list by drawing random sample from it.

```python
import random
teams_subset = random.sample(teams, 400)
```

Initially, I aimed for code simplicity. Since I needed two screenshots to compare, it was obvious that I should use loop.

Then I realized that I am basically doubling the execution time for no good reason. Instead, I should start two web drivers at once, ask each to open different page, wait a little and then obtain both screenshots, even if that means there will be some duplicated code.

```python
manager = {
    "actual": {
        "driver": None,
        "dir": pathlib.Path('actual_results/'),
        "base_url": 'http://localhost:4200'
    },
    "expected": {
        "driver": None,
        "dir": pathlib.Path('expected_results/'),
        "base_url": 'https://createpokemon.team'
    }
}

for run in manager:
    manager[run]["driver"] = webdriver.Chrome()

for team in random.sample(teams, 400):
    fs_friendly_url = fs_sanitize(team)

    for run in manager.values():
        base_url = run["base_url"]
        run["driver"].get(f"{base_url}{team}")
    time.sleep(5)
    for run in manager.values():
        screenshot_path = run["dir"].joinpath(fs_friendly_url)
        run["driver"].save_screenshot(screenshot_path.as_posix())

for run in manager.values():
    run["driver"].quit()
```

## Results analysis

I started with sorting all created images by size. This allowed me to quickly identify outliers:

```sh
$ ls -lahSr diff/
...
-rw-r--r-- 1 mdlugosz mdlugosz 5,6K Nov 24 14:43 67896595bd945c62fdb8c857afb6887baf50e1fb62904e9e7159fc034e7f0912.png
-rw-r--r-- 1 mdlugosz mdlugosz 5,6K Nov 24 14:36 0487b61857b7417920d0cb3a70641e74d563e417f0354c94a9f66b292a10686e.png
-rw-r--r-- 1 mdlugosz mdlugosz 5,7K Nov 24 14:43 869fce86191cf921fe253d1f1c792280b0c01d481a35b0da3d10ebe5b27824a6.png
-rw-r--r-- 1 mdlugosz mdlugosz 5,7K Nov 24 14:30 5e2a96809439a5bac1d235b16544c2385532d1a1ad379abb1586256540d75140.png
-rw-r--r-- 1 mdlugosz mdlugosz 5,9K Nov 24 15:14 9aa5ca526685da394c0cf401aa44596657298f19ee347b3f880c3f48e25b76a8.png
-rw-r--r-- 1 mdlugosz mdlugosz 6,2K Nov 24 14:01 7ce7e7f3d05560e26981e6b9c23773a0372f6cf6f1bc21c0ed6a0f8d4da61447.png
-rw-r--r-- 1 mdlugosz mdlugosz  20K Nov 24 13:52 862eceaaf4bcb06ffa0fdaf6b263999d1d5e2ec06b1f9d40533c311b9d89bef5.png
-rw-r--r-- 1 mdlugosz mdlugosz  27K Nov 24 14:51 0133026b0a0f64ca7cb00529d083ace2effd89fb4d1279283ca6e6d8087cc35e.png
drwxr-xr-x 2 mdlugosz mdlugosz  72K Nov 24 15:29 .
```

It turned out there are some cases where the same team does not produce identically-looking pages, but not for the reason I was interested in. Some Pokemon changed their displayed name slightly and sometimes new name takes different number of rows than old one. As a result, considerable part of page got moved vertically, causing a big diff.

Another problem is that during development, new version uses different domain than existing instance, and current URL is displayed near the bottom of page. This caused all pairs to report some differences. I skimmed over all images to confirm there are no unexpected changes, but I should strive for making images really identical. This would allow me to exclude all images with exact same size from analysis, making it trivial to identify cases that differed in significant way.

{% figure
    {attach}simple-visual-regression-checking-with-selenium-and-imagemagick/random-result.png |
    caption=Random 'nothing interesting to see here, move along' image |
    display_caption
%}

## Conclusion and ideas for further work

[Final version of code I have used is on GitHub](https://github.com/mirekdlugosz/scrapbook/tree/master/create-pokemon-team-visual-diff).

While this solution did get the work done, it is not perfect. There is number of things that could be done to improve performance and maintainability:

* Proper logging and exception handling should be added.
* Paths and parameters (like sample size) should be passed in as command line options, or loaded from environment.
* Screenshots of one team should be bit-by-bit identical to allow easier results analysis. This could be achieved by adjusting browser window size or by changing development version to produce exact same URL as production instance.
* Two webdriver instances are very far from fully utilizing available system resources. Main loop should be revamped to support larger number of concurrent web driver sessions. One way to achieve that is queueing mechanism, which would store list of URLs to process and assign them to web drivers that are free (web drivers would need to report they completed assigned work and can take up another task).
* Fixed wait times are widely considered a code smell in web automation. Of course webdriver should take screenshot as soon as page has fully loaded team data.
* Image diffs should be created in separate process. This would allow to fully utilize multiple CPUs on machine, but requires implementing another queueing mechanism (as well as efficient way to find pairs of images that were not yet processed).
