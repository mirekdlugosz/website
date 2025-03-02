Title: Customizing fonts’ look with OpenType features
Slug: customizing-fonts-look-with-opentype-features
Date: 2025-03-02 19:36:10
Category: Blog
Tags: Linux, Rust, planet AST, planet MoT, planet Python, projects, tutorial

Many programming fonts allow customization through OpenType features. For people who are picky about certain properties, like easily distinguishable `l` and `I` (lowercase L and uppercase i), a single toggle can make a difference between rejecting a font and starting to use it. Unfortunately, choosing the perfect font with the perfect setup is way harder than it should be. This post describes the tools that may help, including the one that I wrote recently.

Whenever I stumble upon a new font, I want to know:

* how does the font generally look?
* does the font allow customization of specific glyphs that bother me?
* when set up properly, how does the font fare against my current setup?

But first, how do you even learn about a new font? Two proven resources are [programmingfonts.org](https://www.programmingfonts.org/) and [codingfont.com](https://www.codingfont.com/). That topic is also frequently brought up on social media like Reddit in communities discussing editors, terminals and programming in general.

Let's say that [JetBrains Mono](https://www.jetbrains.com/lp/mono/) caught my attention. The demo page is nice enough, but does not give an option to type in custom text. I am not a fan of ligatures for code (the ones they say "reduces noise"), while I appreciate ligatures that "balance whitespace" - I wonder if I can disable one category? Also, I prefer slashed zero.

A few years ago, that would have been the end of it for me. The font looks nice, but there are some details I do not like. Today, I know that many of these details can often be customized through OpenType font features. But how can you learn what features the font supports, and what exactly do they change?

The best tools that I have found so far are web based: [Wakamai Fondue](https://wakamaifondue.com/) and [Bulletproof Font Tester](https://www.adamjagosz.com/bulletproof/). Other similar tools are [Axis-Praxis](https://www.axis-praxis.org/specimens/) and [FontDrop!](https://fontdrop.info/). All of them allow you to select a font file from local computer to explore its capabilities. Usually you want to select a file with "medium" or "regular" in name.

There are a few things that I like about Wakamai Fondue. It tries to display all characters affected by a given setting, so you can learn that in JetBrains Mono, "Character Variants 04" affects how letter "j" is displayed. You can toggle a setting on and off, making it easier to notice changes. It also gives you the internal name of OpenType font feature, so you know that slashed zero is accessed through a feature called `zero`. This becomes relevant later, when you try to apply settings on your machine.

There are also a few things that I like about Bulletproof Font Tester. It has a large collection of texts, including cases specifically designed to show each letter or common issues. It's easier to see how specific set of font features apply to the entire text. It remembers all the fonts you have selected during the session, making comparisons easier. It also provides interface to modify text layout properties, although I never use these.

The main thing I don't like is that there's no way to save your settings. It's not possible to pause your exploration and resume it another day. If you close a tab, you need to start from scratch. Comparing a new font to the one you are currently using involves setting it up in the tool - possibly multiple times. I have not found a good way to compare multiple fonts to each other. It's also not easy to compare effect of two different sets of features on a single font.

I decided to use recent Day of Learning at Red Hat to see if I can do anything about it. The result is called Font Feature Tester and you can [find it on GitHub](https://github.com/mirekdlugosz/font-feature-tester).

At the very core is a simple command line tool written in Rust that reads a font configuration file and generates an image of provided text set with that font.

There's also a Python script that automates the execution of the Rust tool across multiple configuration files and collects all the output images in a single directory. It's responsible for ensuring that images are consistent and use the same text, image size and colors.

Using web tools mentioned earlier, I can find a set of font features that look promising. Then I prepare a configuration file for each font I want to try - at the very least, that would be my current font and font I consider switching to. Then I run a Python script to generate images.

I can use a standard image viewer to see how the text looks. When I want to compare multiple fonts, I can open a few images at once and put them side by side.

{% figure
    {attach}customizing-fonts-look-with-opentype-features/font-feature-tester-example.png |
    display_caption |
    alt_text=Two images with sample text set in different fonts, displayed side by side |
    caption=Images generated by my tool. I would keep one as a reference, and cycle through images in the other
%}

That approach scales to any number of fonts and feature sets - you only need to add a new configuration file. Since all the data is written in files and somewhat automated, you can stop at any time and resume later.

One major gap is that you can't easily move your setup between all the tools. Once you find features you like, it's up to you to apply the same configuration in your terminal emulator, editor and desktop environment. At the end of the day, the ergonomics of my simple tool depend a lot on ergonomics of your desktop environment and image viewer.

## Vision for the future

Font Feature Tester is a barely minimal _viable_ product. It solves the very specific part of the larger problem, and manages to do that with support from other tools. The integration leaves a lot to desire. I can envision it growing into much more complete solution, so I thought it might be fun to finish this post by role playing a product manager. What is the end state of things? How can we get there?

I imagine the final version looking something like that:

{% figure
    {attach}customizing-fonts-look-with-opentype-features/font-feature-tester-ui.png |
    alt_text=Sketch of software window. There are tabs at the top. Main section displays a text set in specific font, using specific OpenType features. There's a section on the left with tools used to change font, OpenType features, colors etc.
%}

Each tab would display text set in specific font with specific font features enabled. It should be easy to move between tabs using keyboard shortcuts. There should be an option to disable a tab without closing it - so you can temporarily remove a specific setup from consideration, but you can also bring it back if you change your mind. Alternatively, there could be a history of closed tabs.

Options on the left side would allow to modify the current text setup. Obviously there needs to be a way to change font and font features, text properties and text content. One of the challenges is that some of these settings sometimes apply to all tabs, while other times should apply only to current tab. It's valid to want to increase font size for all tabs, but it's also valid to change font size for current tab only.

It's not clear to me how to handle a case where you want to compare images side by side. Some kind of split view is needed, possibly with tab locking.

The first step on the road towards that goal is introducing the graphical interface. For me, it makes sense to focus on single tab - just a view of image and options in the sidebar. Options can be added iteratively.

Some options may be improved over time. Font selection may start as a simple text field where the path to font is pasted. Later it may be changed to use file selection widget. Finally it can be integrated with something like fontconfig to also allow selecting fonts from these that are already installed. The same is true for OpenType font features - initially, it may be a text box, but later it should display a list of all font features available in the font, and provide a way to set a value for each feature. While most fonts support simple toggles, there are some fonts that support one of a few values for selected features. Interface should acknowledge that.

All the changes should be saved in configuration file, so program may be closed at any time. Ideally, current configuration file format would be reused, so the existing workflow could be supported while user interface is being developed.

Once the single font view is finished, it may be wrapped in a tabbed interface. At that point, the old Python tool-based workflow may be removed.

At one point, it would be great to ensure that the application works on Windows and macOS.

I don't know how far on that journey I will go, especially since creating desktop applications is not something I find particularly appealing. But if this is something you find interesting, feel free to [reach out to me]({filename}/pages/contact.md)!
