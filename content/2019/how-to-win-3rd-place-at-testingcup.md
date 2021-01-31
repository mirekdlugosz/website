Title: How to win 3rd place at TestingCup?
Slug: how-to-win-3rd-place-at-testingcup
Date: 2019-07-07 11:28:32
Tags: testing, tutorial

[TestingCup](http://testingcup.pl/) is annual testing competition in Poland and this year, I won 3rd place in individual category.

<!-- more -->

## Context: Competition rules

During TestingCup, we are given three hours to test application that we see for the first time and which is crafted specifically for competition. We earn points and the winner is the person who collected the most of them.

Points are earned in two ways: by reporting bugs and by creating testing process artifact. Number of points from bug report depends on severity - critical security issue and application crashes are worth the most, duplicates are worth the least (actually, they are worth negative points). It pays off to go really deep and find important problems, but it also pays off to maximize coverage and find many issues. Testing process artifact is single document that must comply with "widely-used standard", such as IEEE-829. It is graded against unknown checklist of elements it should contain - each checked box earns you some points. As far as I can tell, actual substance of document is of lesser importance.

Points are awarded by championships jury in non-transparent process. After the championships you are given your total number of points, but you don't know how much points you earned for each activity, what was final severity of your bug reports and which boxes on artifact checklist were checked. I guess you can ask over email? Jury decisions are final and there is no appeal process in place. Jury promises that each bug report goes through at least two jury members and they discuss until disagreements are resolved.

You can download application and accompanying documents, including list of known bugs and exemplary artifacts, from [MrBuggy website](http://www.mrbuggy.pl/).

## Prepare your machine

During the competition, you are expected to use your own machine. Organizers provide some minimal requirements it must meet (native Windows installation, particular .NET version or newer, RJ-45 connection, sometime others) and list of forbidden activities (mainly communicating with external parties and decompiling). Everything in-between is fair play. Which places preparation of machine among the most important things you can do to maximize your chances of winning.

Install every development tool and productivity software you know how to use, and also some that you only heard about. Last year, at one point I discovered that application stores data in SQLite database, but I didn't have tools to access it and poke around. This year, I installed git for Windows, Python, R with RStudio and tidyverse, Postman, LibreOffice suite, Greenshot, SQLiteBrowser, 7-zip and VS Code (including plugins for spell checking, linting and indentation). And probably some more. Even then, during competition there was a moment when I wished I had Jupyter Notebook installed.

Keep reference materials on your disk. When working on test process artifact, you might want to open ISTQB syllabus and ensure you haven't missed something obvious. Last year, I did not have any testing resources on my machine and I am sure my test report wasn't particularly good. This year, I had ISTQB syllabus, offline copies of [Michael Bolton](https://www.developsense.com/) and [James Bach](https://www.satisfice.com/) blogs and some other documents. Our task was to create test plan and I kept my cool just because I had access to article titled [*What Should A Test Plan Contain?*](https://www.developsense.com/blog/2008/12/what-should-test-plan-contain/).

This kind of feels like cheating, but you might prepare templates for critical test process artifacts. Championships rules do not forbid it. That was my idea for this year - I copied one of test reports from previous competitions and intended to use it as template. I did not, as this year we had to create test plan.

## Read instructions

I know this one is mentioned in virtually every "how to pass FooBar exam/certification" article, but I underestimated how important it really is.

This year we had the opportunity to evaluate our own reports and judge (anonymized) work of others after the competition. And clearly, some people did not read the instructions, or failed to understand them. I saw bug reports for things that were explicitly included in list of "known issues". I saw bug reports pointing out that features described in Change Request document are missing - you know, features that were requested by business, for which development has not yet started. I also saw test plan that was literally perfect, except for one small detail - it was completely off-topic, being based on delivered MrBuggy instead of Change Request document. I don't know how many points this person earned, because "document is on-topic" was not on the list of things we were supposed to check.

I don't want to bash these people or paint myself as superior. I want to stress out that you should read all of provided materials, especially instructions. And then you should read them again. And then you should read them from bottom to top, just to ensure you really understand what is expected from you, what will be held against you and what doesn't matter at all.

## Keep it simple

You know how articles [introducing various test process artifacts list all kinds of stuff as required](https://www.guru99.com/defect-management-process.html#2)? Following their advice is sure way to waste time and focus on least important tasks.

During competition, your bug reports must cover real problems and be understood by jury. There are no other requirements. Usually it's good idea to provide steps to reproduce, but sometimes there are so short that you may skip them. There are situations when it's required to point out what you expected to happen, but often this is obvious from context. You might describe testing environment in painstaking detail, but everyone has exactly the same, so why bother?

Same goes for the way you write your reports. Sure, you might show off your language proficiency, but is it worth it to spend 30 second looking for exact word that perfectly conveys what you mean? Someone else used simpler word and spend these 30 second thinking how to test specific requirement.

Simply put, don't waste time on information that is not required or necessary. Use simple words and simple grammar. Keep your sentences short and on point. Focus on discovering important problems fast and make sure they are communicated clearly.

## Track your time

It's pretty obvious, but important enough to state it explicitly. Keep track of time.

It's very easy to forget about passage of time when you face serious and interesting challenge, or when you are extremely focused on task at hand. Yet competition do not provide luxury of spending as much time as you want on everything that piqued your interest. You have to consciously control amount of time spent on each activity and feature. Concentrating for one hour on one thing only is not worth it.

This also means you have to be relentless in deciding it's time to move on. Sure, you might feel you are so close to revelation and be tempted to give it one more minute, but what you probably really feel is sunk cost fallacy. Leaving unfinished work is hard, but necessary. It might help to make a note so you can return to this problem later on.

## Abuse notes

This is another rather obvious, but nevertheless important point. You are working on the computer, which is able to store virtually unlimited amount of text. As part of conference pack you will be given pen and notebook. Make use of them.

This year, for the first time, HTTP API was supported way of interacting with MrBuggy. All calls required Authorization header, which had to include base64-encoded username and password. While organizers did provide simple tool to encode one string, re-typing usernames and copying them all the time would be huge waste of time. Instead, I kept encoded strings in VSCode. This way I could quickly select and copy them.

Last year, I added item to my notebook after covering each feature. This helped to direct further efforts into areas that were not yet tested, as well as provided overview for what I actually did. I also captured ideas that I would like to pursue further if time permits. This made it easier to leave some tasks unfinished when time for them was running out.

As you can see, notes don't have to be used in creative way to be useful. Just keep in mind they are an option and use them every time they can support your main activities.

## Don't bother with live results

Preliminary results are displayed live during the competition. You will do best if you ignore them completely.

Last year, my name was third on early results table (at least last time I saw it before competition ended). I felt pretty good about it and I thought I can actually get the trophy, so you can imagine my disappointment when final results were announced and I finished up seventh. This year, I fell out of top 10 around midway through the competition. Last time I saw my name, I had around 40 points. Near the end of competition, everyone had 50-70 points. That's pretty big gap and I was sure there is no way for me to close it, so I accepted I will finish on worse place than previous year. You can imagine my surprise when I was announced as winner of 3rd place.

Live results are misleading in part because they don't factor in test process artifact. It's worth 20 or so points, so it can impact your results quite a bit.

But what is much more important, live results are based entirely on self-assigned categories. If you decide your bug is critical security issue, your total points will increase by 10. Later jury might decide this bug should have much lower severity and your final points will go down considerably.

You can easily secure top spot in live results - just report all your bugs as most critical. Live results are as easy to game as they are meaningless.

## Practice at home?

I have not followed this one myself, so I can't say how important it actually is. Nevertheless, [MrBuggy website](http://mrbuggy.pl/) provides software used in previous editions of championships, along with list of known issues and example test process artifacts. You can download it, set timer for three hours and do dry-run of competition. Just write down all bug reports and document in some local file. Afterwards, compare list of bugs you found with list of all known bugs. Which did you fail to find? Why? What could you do differently to earn more points?

## Make it fun

Last, but not least, try to be positive towards entire championships and just have fun. 

Competition are not objective assessment of your skills, knowledge or worth as a tester. Neither are they very reliable measurement tool. As an example, the same person won first place in 2017, second place in 2018 and... fourteenth place this year. Shuffles like that are quite common and have many, many reasons.

Personally, I haven't prepared at all for my first championships in 2018. For 2019, I made a point to prepare my machine, but mostly relied on instinct and natural approach to problems during the competition. Winning a trophy is nice, but it was never the goal for me - I mostly wanted to know how well I naturally stand against the others. As it turns out, pretty well.

As a closing remark: if you had fun during competition, if you learned a single lesson, if you improved your craft in any way - you are the true winner. It doesn't matter if you were first or last in final standing.
