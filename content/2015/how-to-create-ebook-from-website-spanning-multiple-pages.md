Title: How to create ebook from website spanning multiple pages
Slug: how-to-create-ebook-from-website-spanning-multiple-pages
Tags: tutorial, Linux
Category: Blog
Date: 2015-09-18 00:04:32

Every now and then I stumble upon book that disguises itself as website - it has table of contents and spans multiple interlinked pages, each dedicated to one coherent piece. Sometimes I like to take them offline, so I can read them on travel. Sometimes I like to take them off computer, because reading long passages of text on screen is not that convenient. Sometimes I would prefer to have them in ebook format, because that's what they really are. Here's how I do that.
<!-- more -->

**Disclaimer #1**: I am using Linux on my desktop, so instructions are for Linux computers. Both programs that I use, 
[httrack](https://www.httrack.com/) and [Calibre](http://calibre-ebook.com/), are cross-platform - you can run them on Windows and OS X too.

**Disclaimer #2**: The example that I use, one of [Karl Broman](http://kbroman.org/)’s tutorials, is released to public domain with source code publicly available. In this particular case you could save yourself a trouble by `git clone`-ing and `pandoc -t epub`-ing the entire thing. But usually you won't have that luxury.

**Disclaimer #3**: Most content that you find online is copyrighted, even if you can read it for free (as in *gratis*). Making offline copy probably falls under fair use. Sharing that copy with relatives or close friends probably does too, but is on slippery slope. Sharing that copy with anyone else is most likely illegal. Just don't do it, ok?

For the sake of this article, 
let's say that I want to make ebook out of Karl Broman's "[Organizing Data In Spreadsheets](http://kbroman.org/dataorg/)" tutorial.

## Download website

First I download it to my disk:

    :::text
    cd /tmp/
    httrack http://kbroman.org/dataorg/ -a -v -I0

`-v` is for verbose, so I know what is happening. 
`-I0` (this is capital i and zero) is for don't make `index.html` file and avoid confusion later on.
`-a` is for stay on the same address, i.e. download only files whose URL starts with address provided in command line. httrack is spider and it will happily follow any link that it finds, eventually downloading entire Internet. You have to limit the set of pages it should be interested in, and `-a` is the easiest way to do it. If the book you are interested in is not in one directory (or, more likely, in that directory there are also things you are not interested in and you can't simply delete them after download is completed), you will have to tweak [httrack filters](https://www.httrack.com/html/filters.html).

As a result, new directory with domain name (`kbroman.org`) will be created in working directory. Since I work in temporary location and all these files will be discarded anyway, I don't bother with `-N` option.

## Convert to ebook

Next, fire up Calibre.

Calibre is robust and highly customizable, so it provides one little, well-hidden checkbox that has power to suck out all joy of reading final ebook. I have to decide whether it should be selected or not right now, because after I import website into Calibre, it will be too late.

When this checkbox is selected, pages will be added in order of their appearane in first page of downloaded website. Calibre will then repeat that process for each linked page in search for missing content. If each chapter of your website is on exactly one web page, then you want to have checkbox selected.

When checkbox is unselected, wich is the default, Calibre will follow each link immediately and add pages in order it visits them. If first chapter of your book happens to contain link to last chapter, the last chapter will be immediately after first chapter in output ebook, which is not cool. But if each chapter page contains solely of links to pages that contain actual subchapters (like [SPSS online help](http://www-01.ibm.com/support/knowledgecenter/SSLVMB_23.0.0/statistics_mainhelp_ddita-gentopic1.dita)), then you totally want checkbox unselected.

OK, maybe that was convoluted. Let me get some visual aids here. Assume that this is the structure of links on website you have downloaded:

    :::text
    book
	├── A.html
	│   ├── C.html
	│   └── D.html
	├── B.html
	│   └── E.html
	└── C.html

If checkbox is selected, ebook content will be A.html, B.html, C.html, D.html and E.html. If checkbox is not selected, ebook content will be A.html, C.html, D.html, B.html and E.html.

To find this checkbox, go to `Preferences`, click `Plugins`, find `HTML to ZIP` (it's in `File type plugins` section) and click `Customize plugin`. We are talking about the one labeled `Add linked files in breadth first order`, which is the only one anyway.

![Checbox from hell]({attach}ebook-from-html-tutorial/checkbox-from-hell.png)

In my case (I want to turn Karl Broman's tutorial about data organization into ebook, remember?), I want this checkbox **selected**.

When I finally have this thing out of my way, I can add new book in HTML format. This can be done by selecting `Add books from a single directory` item under `Add books` menu; or by pressing `a` key when main window is focused. When file picker appear, navigate to directory where httrack downloaded website contet and select `index.html`.

![Calibre New Books menu]({attach}ebook-from-html-tutorial/add-page.png)

Eventually book will appear on list in the centre of window, presumably with correct metadata. I fix metadata if needed, make sure that book is selected and click "Convert books".

New window will appear. Target format can be selected in upper right corner. EPUB is default and is good enough for me, but select MOBI if you have Kindle.

Sometimes you might want to open `Structure Definition` section and remove ` or name()='h2'` part from XPath. This will stop Calibre from entering page break before every `h2` tag. This tag is used to denote subchapters, which are often very short (less than one page of book). The correct setting of that field really depends on structure of particular website you are trying to convert.

Then, in `Table of Contents`, you might want to select `Manually fine-tune the ToC after conversion is completed`. This step will have to be done after each converter run, but will allow to correct terribly messed up table of contents.

Clicking `OK` will produce website in ebook format.

## Tweak output file

Ebook created with default options is readable, but rather cumbersome to navigate. Each chapter starts with web page header and ends with web page footer. These things obviously make perfect sense on live website, but are cruft in ebook and will only annoy me as I skip them. I think it's best to remove them.

To do so, click `Convert books` button again and open `Search & Replace` section.

This section allows us to provide any number Search/Replacement pairs that will be processed while ebook is created. Search capabilities are virtually unlimited thanks to [regular expressions](http://www.regular-expressions.info/). After clicking wand icon, ebook source code will be displayed and we can see what exactly search expression will match.

Since I want to select elements in HTML structure and remove them, XPath would be much better. But Calibre supports only regexpes, so here goes.

* Start by pasting string that will unambiguously match beginning of unwanted HTML part. If you have used web browser's developers tool for that, make sure to double-check string in Calibre preview. This is required because httrack is not only website downloader, but also parser, and might slightly modify internal structure of web page in process. `<div class="x" id="y">` is the same as `<div id="y" class="x">` for parser, but not for regular expression.
* Then type `[\s\S]*?`, which basically means "any character any number of times". If you thought that "any character" is represented by dot, you should know that dot represents any character **except** the new line, and page structure we are interested in will almost certainly span multiple lines. `\s` is any white space character, `\S` is every character different from white space, so group `[\s\S]` will match any character including new line. Question mark means that capturing should not be greedy.
* Matching the end of unwanted string is the hardest part, because every closing tag in HTML looks exactly the same. The best method I have found so far is using positive lookahead to match, but not capture, HTML string that immediately follows unwanted part. When you find it, paste it and enclose in `(?=` and `)`.

In my example, header can be matched by this regexp:

    <div class="navbar">[\s\S]*?</div>\s*(?=<div class="container-narrow">)

And footer (including superfluous link to next section) by this one:

    <hr/>\s*<p>Next up[\s\S]*?</footer>

Replacement text is empty, because I want to remove these parts.

![Search and Replace section with expressions fille in]({attach}ebook-from-html-tutorial/search-and-replace.png)

I click `OK` to prepare book in ebook format. This time I obtain something that actually can be read in sequence without interruptions.

## Finishing touches

If you are still not happy about output file, play around with multitude of Calibre's options. 
Their enormous [user manual](http://manual.calibre-ebook.com/) might be helpful.
