Title: Announcing Kustosz
Slug: announcing-kustosz
Date: 2022-05-15 14:06:01
Category: Blog
Tags: planet Python, projects, Python

I'm happy to announce [Kustosz](https://www.kustosz.org/), a new [feed reader](https://en.wikipedia.org/wiki/News_aggregator) that aims to help you focus on worthwhile content.

<!-- more -->

These days, many open source RSS readers still try to fill the void left out by Google Reader - their main goal is to provide familiar visuals and user experience. Meanwhile, proprietary feed readers incorporate machine learning techniques to guide you through the vast ocean of content and try to "relieve" you from the burden of "reading everything".

I find both of these approaches problematic. Google Reader has been discontinued a decade ago. Everyone who wanted "a Google Reader alternative" has settled on something else or moved on a long time ago. There's no reason for a new project to try to solve this exact problem.

While it's tempting to save time and mental capacity by allowing computers to decide what content you should focus on, this is also a fast lane to [filter bubbles](https://en.wikipedia.org/wiki/Filter_bubble). Today, we are intimately familiar with psychological, social, and political problems created by employing this approach at scale. It's more important than ever to let people decide what they want to read.

That's why Kustosz comes from a different angle. Its goal is to make it easy and convenient to read content that **you** find worthwhile.

Kustosz provides easy to use, straightforward and distraction-less interface, where your content takes a central place. It works straight in your browser, so you don't have to install additional software on your computer. It fits your device, no matter if you use a phone, tablet, or desktop with an external monitor.

We are all busy, and sometimes we can't read the entire article in one go. That's why Kustosz tracks how much you have read and lets you pick up right where you left at any time, on any device.

To enable you to make the most use of Kustosz features, it automatically downloads full article content from the source website. It doesn't matter if the feed author publishes only article lead, you don't have to leave Kustosz unless you choose to.

Kustosz is not discouraged when the article you want to read is not in the site's RSS feed. You can add any web page manually.

While Kustosz doesn't make any decisions for you, it's here to automate menial tasks. It has a built-in duplicate detector that can automatically hide articles you have already seen. It provides a flexible and powerful filter system that you can use to automatically hide articles you are not interested in.

And the best part is, your data is yours. Kustosz is [open source](https://github.com/KustoszApp) and hosted on your server. This ensures that you are in control of Kustosz, its data and what it does.

From the technical point of view, Kustosz utilizes familiar modern client-server architecture. Frontend is [Vue.js (v3)](https://vuejs.org/) web application that relies heavily on features that became widely supported in recent years, like CSS grid or JavaScript Intersection Observer API.

Backend is [Django](https://www.djangoproject.com/) web application that serves REST-like API with help of [Django REST framework](https://www.django-rest-framework.org/). Most of the work is done in background tasks managed by [Celery](https://docs.celeryq.dev/). All the hard work of accessing and processing RSS / Atom feed files is done by the excellent [reader](https://github.com/lemon24/reader) library. I want to stress how immensely grateful I am to [Adrian](https://death.andgravity.com/) for creating and maintaining this exemplary piece of code.

I've been using Kustosz as my primary feed reader for about a month now, and I consider it pretty stable and fit for purpose. But it's software, so of course it has bugs - especially in contexts distinctly different from mine. If you encounter them, feel free to create an issue or submit PR at [GitHub](https://github.com/KustoszApp).

As is true for most of the software, I don't think Kustosz will ever be *truly* finished. Right now it's primarily concerned with text content available on public websites, but my big dream is to support various content sources - things like email newsletters and social media sites immediately spring to mind. On the other hand, I don't think I want to re-implement [RSS Bridge](https://github.com/RSS-Bridge/rss-bridge) just for a sake of it.

Another dream of mine is to provide an integrated notepad. Reading is great, but truly worthwhile articles are thought-provoking and invitation to the conversation. Active reading demands you write down what you understood. It would be great if you could do that from the convenience of a single application.

There's also a little more mundane work to do - things like user interface translation framework, WebSub protocol support, and improving documentation.

Nonetheless, if Kustosz sounds like a tool you could use, please head on to [Kustosz website](https://www.kustosz.org/) or [documentation page](https://docs.kustosz.org/en/stable/), where you will find system requirements and installation instructions. There's also a [container image](https://docs.kustosz.org/en/stable/installation.html#trying-it-out) you may use to quickly spin up an instance for testing.
