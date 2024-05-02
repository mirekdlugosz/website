Title: Association for Software Testing Board of Directors report - April 2024
Slug: ast-bod-report-april-2024
Date: 2024-05-02 23:56:19
Category: Blog
Tags: AST, planet AST, planet MoT


In my [Association for Software Testing 2023 elections proceedings](https://associationforsoftwaretesting.org/about-the-ast-a-professional-body-for-testers/board-of-directors/election-proceedings/2023-election/2023-election-mirek-dlugosz/) I advocated for transparency. In the spirit of practising what I preach, this blog post summarizes my work for AST in April 2024.

* Found a way to send messages to [BlueSky](https://bsky.app/profile/ast-news.bsky.social) and [Mastodon](https://sw-development-is.social/web/@AST) from Zapier.
* Met with Chris and Gwen to discuss remaining items from Phone.com migration (see [January report]({filename}ast-bod-report-january-2024.md)). I hope to finally close that in May.
* Removed old, no longer used passwords from shared LastPass folders.

Integration of Zapier with BlueSky and Mastodon deserve a bit longer explanation.

There are two sources of our automatic messages - we periodically re-publish posts and videos from our archives, and we forward [blog posts from our members](https://associationforsoftwaretesting.org/about-the-ast-a-professional-body-for-testers/membership/blog-syndication/). For a longest time, we published that on [Facebook](https://www.facebook.com/profile.php?id=100064365177059), [LinkedIn](https://www.linkedin.com/company/association-for-software-testing/) and [Twitter](https://twitter.com/AST_News). Last year Twitter announced they will require paid subscription to access API, which in turn rendered most existing automations useless. We had to turn off ours.

BlueSky and Mastodon quickly rose to prominence as possible Twitter replacements, so we created new accounts there. However, Zapier did not support them natively. In fact, it still does not.

But after a bit of focused searching, I was able to learn that Zapier also supports arbitrary code execution jobs, at least as long as code is JavaScript or Python, and follows certain rules. What's more, I was able to find [scripts created](https://github.com/marisadotdev/ZapierLoomlyBluesky) by [other people](https://cromwell-intl.com/open-source/python-social-media-automation/python-program.html). After adjusting them a bit, they ran perfectly.

Integrating Zapier with BlueSky and Mastodon was one of the things I wanted to tackle since I joined a Board, and it makes me really happy that I was able to finally complete this.

If you are interested in becoming a better tester, advancing the practice of software testing or just want to support my work, consider [subscribing to AST newsletter](http://eepurl.com/tCFsn) and [becoming a member](https://associationforsoftwaretesting.org/about-the-ast-a-professional-body-for-testers/membership/become-a-member-of-the-the-association-for-software-testing/). If you have any questions, ideas or would like to work together, you can email me at `mirekdlugosz %at% associationforsoftwaretesting.org` or [get in touch through other channels]({filename}../pages/contact.md).
