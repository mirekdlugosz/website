Title: Automatic offline Twitter card images (og:image) generator for static sites
Slug: automatic-offline-twitter-card-images-og-image-generator-for-static-sites
Date: 2021-03-13 12:54:35
Category: Blog
Tags: planet Python, projects, Python
og_image_text: Automatic offline\nTwitter card images generator\nfor static sites

I felt a sudden desire to have visually appealing images in social media posts with links to my website, and after reviewing existing solutions, I ended up creating my own. In this post, I skim over solutions I have found and point out what mine does different.

<!-- more -->

You know how sometimes when you share a link on social media, it is displayed with big, eye-catching image? Something that may look a little like this:

{% figure
    {attach}pelican-social-cards-announcement/sample-card-with-image.png
%}

## A quick overview of existing solutions

Possibly the most common way of generating these images is creating them manually. If you are adept in tools like Adobe Photoshop, you can obtain great results in no time. If you aren't, there are websites that can help - [banners.beyondco.de](https://banners.beyondco.de/), [kapwing.com](https://www.kapwing.com/explore/og-image-template) and [motif.imgix.com](https://motif.imgix.com) are some that I have found.

There are two main problems with manual approach. First, it requires a lot of time to generate images for all of the content on your website. Second, it requires you to be extra careful if you want to maintain visual consistency of all the images.

Image-generating API services were created almost as if in a response to these limitations. They require you to register an account, but later you can just send carefully-crafted API request and they will send you generated image back in response. This allows for unattended generation of large number of images. Two popular websites providing services like that are [cloudinary.com](https://cloudinary.com/) and [og-image.vercel.app](https://og-image.vercel.app/).

My main problem with these services is somewhat philosophical. I don't fancy the idea of having my website build / deployment process dependent on some third-party, online API. For me, one of the benefits of static site generators is that they can be used in air-gapped environment. This is important component of ensuring that website is fully reproducible.

Possibly coming from similar position, some members of JavaScript community found another approach. They use their existing infrastructure to generate simple pages that look exactly how card image should look like. Then they open this page in browser automation tool, like Selenium, grab the snapshot of visible area and save it as an image. That solution was described by [Leigh Halliday](https://www.leighhalliday.com/serverless-og-image) and [Florian Kapfenberger](https://phiilu.com/generate-open-graph-images-for-your-static-next-js-site).

I can see the benefits of this approach, as CSS is great for reproducibly creating complex visual layouts, browser has all the text layout options you may ever need, and if you are creating the static site, chances are that you are already familiar with HTML and CSS.

But I can't shake off the feeling that this is completely overengineered. I shouldn't **need** a browser to create image. Then, performance of this approach is not great - on my machine, opening up page in Selenium and saving screenshot on disk takes well over a second. Surely there must be a faster way of doing that.

## Enter pelican-social-cards

I don't think my requirements are *that* special. I want a tool that could create social media images in fully automated fashion, that can run unattended (after initial configuration), that works locally (offline) and that is not terribly slow. But, apparently, nobody created something that would check all these boxes.

So I wrote it myself. Let me introduce [pelican-social-cards](https://github.com/mirekdlugosz/pelican-social-cards), a new plugin for [Pelican](https://blog.getpelican.com/).

Initial configuration is rather straightforward - all you really have to do is specifying template image through `SOCIAL_CARDS_TEMPLATE` variable. You probably also want to include `social-cards` directory in your `STATIC_PATHS` variable, and adjust one of many configuration settings. Plugin comes with [extensive documentation](https://github.com/mirekdlugosz/pelican-social-cards/blob/main/README.md) that describes all supported options.

It creates images that look something like this:

{% figure
    {attach}pelican-social-cards-announcement/sample-image.png
%}

If you like what you see, head on to [PyPI](https://pypi.org/project/pelican-social-cards/) and grab your copy while it's hot!

## Moving forward

One obvious drawback of my solution is tight coupling to Pelican. It will not work with any other site generator, which seriously limits its applicability. Extracting image generating code from Pelican binding code should be relatively straightforward, so hopefully this plugin may still be useful for others. [I am open to discussion]({filename}/pages/contact.md) about creating some shared library and set of plugins for popular static site generators, if there are people out there willing to work on that.

At the same time, I feel that using Python for image-generating tool will ultimately limit the audience and number of contexts in which it will be used. Ideally, such tool could be distributed as statically-linked binary, so anyone could just drop it on their computer and use it directly. Plugins should be simple wrappers around this binary, which should enable creation of plugin for any static site generator out there. I think there is real opportunity for someone who is looking for ideas for side project in Go, Rust, or maybe C++.
