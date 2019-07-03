Title: createPokémon.team retrospective
Slug: createpokemon-team-retrospective
Date: 2018-07-12 21:42:49
Category: Blog
Tags: development, practice

Last week I announced release of [createPokémon.team](https://createpokemon.team/). It took about three months of my free time, out of which one was "full-time". During that time, I had some ideas and observations that I wanted to share in this blog post. It crosses into rant territory at times.

<!-- more -->

## Three time's a charm

The version I have released is the third iteration of the basic idea for the tool. Each subsequent revision had more features and took more time to create. It also happened that each was rewritten from scratch, as they were all using different programming languages.

Overall, I am happy that I took this approach. It allowed me to have *something* early in the process - something that I could play with to see what is working, what might not be working and what might be missing. It allowed me to refine my ideas how this tool should look like and behave. And it solved my immediate problem, even if it could have solved it better.

I remember that long time ago, I read on some programmer blog that you need to create your project three times to get it right. I wouldn't hang on to number three too much, but I believe that gist of that advice is true - you are unlikely to get everything right on your first try, so it's better to create something quickly, learn from it, discover problems that lie ahead and prepare for them.

(The question what does it mean to "get it right" remains unanswered.)

## Perils of modern frontend development

I created my first website in early 2006. Back then it was very important for thought-leaders to teach newcomers about separation of concerns - that HTML is for basic structure, that CSS is for looks and JavaScript is for dynamic behavior, and that you should never mix them up. Simple website could consist of two or three files (depending on whether it was static or dynamic) and it could be created in dead simple editor like Windows Notepad. If you wanted to change something, you just changed file on disk and pressed Refresh in browser. When I started, it was relatively easy to grasp everything that is going on and how different pieces fit together.

That is no longer the case.

Today, you need to choose CSS pre-processor and language flavour that will be compiled to JavaScript. There are different package and module managers operating at different levels. There are CSS and JS minifiers. If you are serious about your website, you need to choose unit checking framework - and some of them have generic, pluggable architecture with different solutions for assertions, check running, result gathering and reporting. Everything is tied up by one of at least three different task runners. And these are only things that I cared to recognize - I'm sure that there are more tools in pipeline.

If that's too much for you, you can choose to use one of so-called "opinionated" frameworks that made most of decisions for you. One of them is Angular. Canonical way to get you started is running `ng new myproject` in command line. It creates 30 files and pulls in **1100** packages that take over **350 MB** of disk space combined. To see anything in your browser, you have to compile the project (!) and wait for about 10 seconds.

Compare that to AngularJS, where all you needed was additional library in HTML header and some simple controller in separate file.

Mental and computing resources required to start frontend development exploded in last couple of years. I feel bad for people starting today, as they will either feel overwhelmed and discouraged, or will learn to ignore fundamentals they build upon and just go with what everyone else seems to be doing - a very dangerous trait for developer.

## Angular

As mentioned above, AngularJS was easy to grasp at basic level. You would expect newer and improved version to be similar, right? You would be wrong.

Angular is all about enterprise-ready, platform-independent architecture. There are modules, components, directives, pipes and services - all having their own place in the grand scheme of things and all working with the rest in pre-specified ways. You can't just put together few methods from basic library and have *something* - you have to design it carefully first. Which is not necessarily wrong, but definitely overwhelming and time-consuming. It must have taken me few evenings of reading about Angular before I could write single useful line of code.

It took me some time to realize, that Angular has **constant complexity**. It's hard to create simple application in Angular, but creating complex system is not that much harder. This is curse for small projects and god-send for large ones. And I can't bring myself to *like* this approach - I much prefer Python, where simple things are simple and complex things are possible.

## Test-driven development

Angular is created with testability in mind. Its tooling tries very hard to make it easy for developer to write checks, even generating some basic ones by default. This was one of the reasons why I decided to stick with Angular, despite being repeatedly bitten by its complexity. One of the goals of my tool was to show that I am capable of creating automatic checks.

Test-driven development is very popular these days. The basic idea is that you write automatic checks first, and then develop program that would pass these checks. Much has been said about benefits of this approach and some people introduce the concept to beginner programmers.

I wanted to share some impressions about TDD, but I can't for very simple reason - it's nigh impossible to implement when you are not familiar with the language in which checks are written. TDD might work when you are able to sit and write a couple dozen of checks, but there is no way it is going to work if you constantly question whether basic language constructs actually do what you think they are doing. And since TypeScript was new for me (and JavaScript has some unpredictable behaviors here and there), that was exactly the case. I never wrote these automated checks.

## Builder and tester mindset

I self-identify as a tester. It is my job and my duty to seek better understanding of product, question what is obvious, provide valuable information, identify risks and areas of uncertainty and suggest improvements. For the tester, every bug discovered, every trail of a bug that might be hiding somewhere close, gives a feeling of excitement and engagement; the more complex the problem, the more intense the feeling.

When I was creating the tool, I had to constantly switch builder and tester hats. This showed me that things that I value as a builder are different from things that I value as a tester; my priorities and my emotional reactions are different as well.

As a builder, I care about clean, simple and maintainable code. I want to introduce changes that fit nicely into existing architecture and in a way that follows established conventions. I know which part of the code I am intimately familiar with and which are more vague. I know where I had to push myself to the limits and where it was easy for me to keep going.

As a builder, I was afraid and paralyzed by some of the bugs that I have discovered as a tester. I was reluctant to dig into more complex parts of the code. In my angst that I will discover something that will require me to tear down most of what I have build so far, I wished I **don't test anymore**.

Differences in mindset of tester and builder seem interesting and important. I feel they deserve further exploration. I will probably pick it up in future blog post.
