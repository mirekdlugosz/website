Title: Verify changes on your website before publishing them
Slug: verify-changes-on-your-website-before-publishing-them
Date: 2019-12-05 11:44:26
Category: Blog
Tags: Linux, tutorial, planet Python

Nice trick that lets you review changes done to website before publishing it. 

<!-- more --> 

I like static website generators. They are fast, secure, easy to tinker with and can be fully stored in version control system. 

One neat thing they allow is ability to see changes before publishing them. The idea is to get two versions of website – before change and after change – and compare them automatically. Then it's only matter of deciding if differences that you see are what you expected. 

```sh
cd ~/path/to/website
make clean && make publish  # build the website
rsync -av $HOSTING:domains/mirekdlugosz.com/public_html/ /tmp/live-website  # store live version in /tmp/
git diff --no-index /tmp/live-website/ ~/path/to/website/output/  # compare new and old
```

I usually run these commands when something in my build pipeline changes and I want to ensure it is backwards compatible. That's why I first copy existing website back to disk instead of rebuilding it – so I can be sure my reference version is bit-by-bit identical with live version.
