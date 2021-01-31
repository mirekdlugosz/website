Title: Popularity of Google Analytics among R and python bloggers
Slug: popularity-of-google-analytics-among-r-and-python-bloggers
Date: 2015-10-13 23:25:55
Category: Blog
Tags: Linux

One day I was wondering whether anyone actually reads that blog. A thought about setting up Google Analytics crossed my mind, but legitimate concerns about users privacy made me hesitant. Then I wanted to try out Piwik, but installation and configuration requires some effort and I wasn't sure if I want to make that investment. Eventually I figured out that I should probably do whatever other R and python bloggers are doing. But first I had to learn what it is.

<!-- more -->

I quickly started drawing out solution based on `httr` and `rvest`/`xml2`. In my data storage, I obviously needed columns for blog address, community name, Google Analytics usage and Piwik usage. Some blogs might be present in both 
[R-bloggers](http://www.r-bloggers.com/) and [Planet Python](http://planetpython.org/), so maybe use two columns for community instead of one. Then I made hypothesis that companies might care about usage metrics more than individuals - to test it I would need to keep information whether blog is run by company or not. But first I would have to figure it out. Blog name might be strong indicator of that, so storing it would be good idea…

Then I stopped for a moment. I actually don't need any of these things. I want to know how many people use Google Analytics and how many people use Piwik. Popularity of other tracking/analytical services would be good to have, but I don't really know what other options there are and I guess I don't care enough to research it. So let's focus on Google Analytics and Piwik now.

I was able to collect data using these shell commands:

	#!bash
    cd /tmp/
    mkdir R python
    wget 'http://www.r-bloggers.com/blogs-list/' -O r.html
    xmllint --html --xpath '//*[@id="linkcat-3"]/ul/li/a/@href' r.html 2>/dev/null |sed -e 's:\s*href="\([^"]*\)":\1\n:g' | uniq > r-list
    wget 'http://planetpython.org/' -O python.html
    xmllint --html --xpath '//*[@id="menu"]/ul/li[7]/ul/li/a/@href' python.html 2>/dev/null |sed -e 's:\s*href="\([^"]*\)":\1\n:g' | sort -u > python-list
	wget --tries=2 -T 5 -i r-list --directory-prefix=R/
	wget --tries=2 -T 5 -i python-list --directory-prefix=python/

Then I could get raw numbers using following commands:

	#!bash
	$ grep -l -i 'google-analytics\.com/' python/* |wc -l
	253
	$ grep -l -i 'google-analytics\.com/' R/* |wc -l
	191
	$ ls -1 python |wc -l
	531
	$ ls -1 R |wc -l
	547
	$ grep -l -i 'piwik\.js' python/* |wc -l
	12
	$ grep -l -i 'piwik\.js' R/* |wc -l
	6

Finally, I calculated percentages using your ordinary calculator. Granted, this is not reproducible, but I just can't use shell arithmetic syntax or `bc` without looking them up on the web. Anyway, Google Analytics is used by 35% of R bloggers and by 48% of python bloggers. I actually expected it to be more popular among R bloggers, because they usually focus on statistics and data analysis, what makes them more likely to care about their website usage statistics. Well, turns out it's not a case. Piwik usage is negligible.

Let's look up at time required by each step:

- Finding pages that list all blogs aggregated by R-bloggers and Planet Python: *5 minutes*
- Figuring out XPath expressions to extract links to aggregated blogs: *5 minutes*
- Evaluating viability of `xmlstarlet`, because `xmllint` output format is insane: *20 minutes*
- Learning how to make `xmllint` output usable, because I don't remember what was wrong with `xmlstarlet`: *10 minutes*
- Downloading all pages linked by R-bloggers: *90 minutes*
- Reading `wget` man page and figuring out how to not waste time waiting for nothing: *10 minutes*
- Downloading all pages linked by Planet Python: *15 minutes*
- Counting sites with Google Analytics and Piwik: *5 minutes*

Total: 2 hours and 40 minutes (160 minutes), but could be reduced to just over one hour by using correct `wget` flags from the start and by downloading all pages linked by both R-bloggers and Planet Python in parallel.

Had I gone with R, in the same time **maybe** I would have function for downloading website content in faulty network environment.

**Takeaway lesson**: Premature generalisation is root of quite some evil. Don't waste time writing programs that answer questions that maybe you might want to ask in the future.
