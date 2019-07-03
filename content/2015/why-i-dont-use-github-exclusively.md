Title: Why I don't use GitHub exclusively and why you should consider it as well
Slug: why-i-dont-use-github-exclusively
Category: Blog
Date: 2015-09-06 19:26:47

Earlier this year, [bad PR stunt by SourceForge caused many users to reevaluate their relationship with website](http://arstechnica.com/information-technology/2015/05/sourceforge-grabs-gimp-for-windows-account-wraps-installer-in-bundle-pushing-adware/).
Recently, [Google turned Google Code to read-only mode](http://google-opensource.blogspot.com/2015/03/farewell-to-google-code.html),
with promise to pull the plug completely in foreseeable future. Source code hosting services landscape changed immensely, with GitHub being about the only major player left. There are reasons to not be happy with that situation. Hopefully, you will keep them in mind the next time you wonder where to host your new open source project.
<!-- more -->

## You don't own GitHub and GitHub doesn't owe you anything

GitHub is proprietary platform developed by GitHub Inc. and hosted on their servers. Apart from paid plans, which give you private repositories or enterprise-oriented features, they promise free source code hosting service and various development and project-management tools for people who release their work under one of open source licenses.

The problem is, GitHub Inc. is not obligated to provide you anything.

GitHub Inc. is business entity whose primary goal is earning money (it's, like, economics 101). Whatever their reasons to provide services free of charge to open source projects were, there is no guarantee that these reasons are valid in future. Once they are no longer valid, I assure you that free of charge tier will be dropped.

Maybe you find this scenario extremely unlikely, because you believe that providing free services for open source projects was crucial and instrumental in GitHub Inc. success and they have no inertia to maintain that position without free services. Fair point, especially since I have put my own beliefs into your mouth. Anyway, their lack of obligations doesn't have to exhibit in drastic changes. It might be something smaller, like limiting number of projects per user or 
[closing down projects they find inappropriate](http://www.theregister.co.uk/2013/12/19/feminist_software_foundation_c_plus_equality/).

Sure, that case was very controversial and your usual open source project is unlikely to find itself in the middle of such storm. But we are not interested in who was right or wrong there. What really matters is the power relationship. GitHub Inc. owns GitHub servers and has final word in deciding who stays and who leaves. They are both morally and legally entitled to manage their own space any way they see fit. You are guest there and if one day you find yourself *persona non grata*, all you will be able to do is finding new place to hang out.

## You are subject to vendor lock-in

OK, so you are not afraid of GitHub Inc. dropping free of charge plans or kicking you out of GitHub, because git is decentralized and you have entire repo with history on your computer and you only need a new place to host it, right? 

Well, git might be decentralized, but all other tools that you use to collaborate on software development probably aren't. And if any of these tools is provided by GitHub, you might find out the hard way you have effectively locked yourself in GitHub and you are unable to move to another vendor.

As of September 2015, free GitHub account includes source code hosting, issue tracker, wiki and static website hosting. We have already established that moving git repository to another hosting is easy due to decentralized nature of git. But what about the others?

Issue tracker is probably the most important one; it's also the hardest to move out of GitHub. The tricky part is not getting your data out (there are plenty of tools for that), but getting it into new system. First of all, your issue tracking software of choice must have some kind of importing tool. Then, that tool must be compatible with whatever format your exporting tool produced. By the way - that pool of exporting tools? Each one of them produces something slightly different.

Your main concern will be moving data out of GitHub into something else, but once you achieve that, you will notice that quality of migration is equally important. You should succeed in transferring all issues descriptions and comments. You will probably move basic metadata, such as dates and authors. But what about relationships between issues? On GitHub, you simply type `#NUMBER` and it becomes link to issue `NUMBER`. Will your new system work in the same fashion? If not, will you be able to extract relationships from raw GitHub data dump and present them in way suitable for importing tool?

Then, it would be nice to retain relationships between issues and commits. GitHub was nice enough to detect SHA-1 hashes and automatically link them to commits in repository. Your new system probably won't be aware of your new code hosting infrastructure. 

"Hey", you might say, "that should be easy enough to fix. Let me just figure out regex for SHA-1 hash." Okay, go ahead. But remember that your commit messages probably reference issues in the same manner. And you can't change commit message without changing commit hash. So let's just hope that your new issue tracking system will retain IDs of issues, or you won't be able to track down what kind of problem some particular commit was supposed to fix.

And then there are pull requests, which are simple commits in pure git world, so they literally can't even be moved out. Just forget about preserving relationships between issues, pull requests and pull request discussions.

Similar set of challenges awaits if you decide to migrate your project's wiki. Getting entire wiki out of GitHub is dead simple - you `git clone` it. But then you have to import it into your new system, which might not be as easy. First off, your target wiki system probably expects pages in different format than the one you have used on GitHub. And since every wiki development team thinks it's compulsory for them to use their own markup syntax, prepare for writing your own converter. Then, it would be nice to preserve history of pages, but your history is in git diffs and your wiki system probably expects it in structured database. Finally, if you have referred issues, commits or pull requests in your wiki, you already know the rest of the story.

The last service you might want to move out of GitHub is your website. Luckily, this one is free of obstacles. GitHub automatically processes everything you push into pages repository using [`jekyll`](http://jekyllrb.com/). All you have to do is `git clone` website repository and use `jekyll` yourself. Then you can publish HTML pages on your new hosting using FTP, SSH or whatever they provide.

So far I have talked about things that GitHub Inc. provides you explicitly. But there is one more thing that you gain from GitHub; a thing that you wish you could transfer, but you can't. This is project URL.

If your GitHub project ever received any press coverage, they probably included link to github.com domain. If you decided to move your git repository somewhere else, there is no way to automatically redirect all GitHub visitors there. The best thing you can do is set up new branch, `git rm` everything, push simple README with new URL and hope that people click it. You are better off if they published link to your GitHub website, because GitHub pages have [`jekyll-redirect-from`](https://github.com/jekyll/jekyll-redirect-from) plugin enabled, and it supports `redirect_to` metadata. But since you don't control where people writing about your project will direct their readers, you can't relay on that.

## GitHub web interface encourages sloppy git practices

So, I have you worried about vendor lock in a little bit, but that kid next door has written C compiler in Lisp by the time he was eight and you have to catch up quickly or the only job you will ever get will be at McDonald's. You know that life is too short to focus on anything else than achieving perfection in software development. While this is laudable goal, I have bad news for you - GitHub web interface will actively hinder your attempts to achieve it.

Let me tell you a little secret - you can't get git commit messages format wrong. There are, like, three rules to follow. First, the first line is for short summary; that line shouldn't be longer than 50 characters. Second, there is empty line after summary. Third, a longer description should have lines hard wrapped at about 70th column, but absolutely no longer than 80 characters. That 80 columns mark is common practice among software developers whose [roots can be traced back to times before 
computers](https://en.wikipedia.org/wiki/Punched_card#IBM_80-column_punched_card_formats_and_character_codes). Summary should not exceed 50 characters, because some common `git log` formats will include commit hash and/or graph in the same line, and we still want to fit entire thing in 80 columns.

Because 80 columns rule is so prevalent, virtually every programming editor makes it easy to follow it. There are column counters, rulers, visual cues, settings to hard wrap text before 80th column, you name it. If you use command line git interface, it will pick one of suitable editors automatically. You can't get git commit messages format wrong.

Now, GitHub web interface is not a programming editor ([yet](https://github.com/atom/atom)?). It will create commit messages that follow rule number two, but that's about it. GitHub could warn you if your summary is longer than 50 characters; it could include ruler in textarea for description; it could provide checkbox for "wrap my description at 70th column"; it could do multitude of other things. But it doesn't.

Some foremost git users, such as Linux and git itself, will not accept commits without some custom tags in messages (note: these are not to be confused with `git tag`). Their main purpose is indicating person responsible for writing a patch, reviewing it or testing software after it was applied, but can be used in any way a project sees fit. Some of these tags were deemed so important, that git reference implementation includes command line switches that create them automatically.

You have probably guessed by now that GitHub web interface does not provide any tools to aid you in working with tags.

And if you have a bit of déjà vu while reading this section, it's probably because I have reiterated [points brought out by by Linus Torvalds](https://github.com/torvalds/linux/pull/17), git creator himself.

## GitHub imposes particular workflow

Maybe you are not concerned about practices encouraged by GitHub web interface, because you don't believe in world outside of your shell and you are one of these people who actually learned how to use git command line tool. Then you are probably well aware that git supports many different workflows, but GitHub is focused on only one of them.

git is very robust tool. It supports both centralized and decentralized software development models. It supports bazaar-like workflows, where everyone is free to do as she pleases, workflows build around one integration manager and structured workflows with hierarchy of roles.
It supports feature branches and release branches. It supports pull requests, rebasing, cherry-picking and whatnot. git robustness is the reason it scales extremely well and is used by everyone from individual developers to huge projects like Linux and LibreOffice.

But GitHub Inc. blessed us with One True Way of Doing Things called "[GitHub Flow](https://guides.github.com/introduction/flow/index.html)". On GitHub, everything else is second-class citizen.

Don't get me wrong. It's not that I have something against GitHub Flow in particular (although [some other people do](https://julien.danjou.info/blog/2013/rant-about-github-pull-request-workflow-implementation)). It certainly works for some people and some projects. But there is a reason that so many software development models were invented - one size does not fit all. What works for some projects will not work for others. And this is kind of unfortunate when your preferred workflow is not GitHub Flow.

Sure, GitHub is just remote repository after all, so you can use any git workflow that you like. But it might mean that you have to take issue tracker, code review or discussions out of GitHub. And when you have to work around GitHub limitations to get your work done, why do you even bother using it in the first place?

## Monopolies are bad

This one will be quick. Monopolies are no good for you. They tend to provide lower quality services at higher prices. Monopolies are not even good for monopolists, because monopolists tend to allocate their resources inefficiently. There are no redeemable qualities in monopolies, period.

You have done your economics 101 homework and you see dangers of monopolies, but maybe GitHub Inc. is not monopolist and there is nothing to worry about? 
[According to Wikipedia](https://en.wikipedia.org/w/index.php?title=Comparison_of_source_code_hosting_facilities&oldid=677921579#Popularity),
as of August 2015, GitHub hosted over 10 million projects and over 26 million users. Next in line, SourceForge, had 3,5 million projects and 325 thousand users. BitBucket, closing the podium, had 2,5 million projects and barely 100 thousands users. And this is not adjusted to the fact that many users have accounts on all these sites. Some projects are hosted on multiple sites as well, but this is probably less frequent.

So, yeah, GitHub Inc. is pretty much monopolist.

## Better alternatives exist

First, a disclaimer: what constitute "better" alternative depends on your needs, preference and depth of wallet. One size does not fit all and there is no system superior to GitHub in every way imaginable. But there are systems that get some things better than GitHub.

If you want private remote, [BitBucket](https://bitbucket.org/) offers unlimited number of private repositories in their free of charge plan. Access may be granted to five users, or more if you are willing to pay.

By the way, BitBucket is provided by Atlassian, company responsible for one of the best issue tracking systems I have worked with - JIRA. They also develop git repository management platform for self hosting - Stash, continuous integration platform Bamboo, code review tool Crucible, communication tool HipChat, wiki called Confluence and desktop git client SourceTree. They can provide you with entire stack of nicely integrated software development tools hosted on your own servers, assuming that money is not an issue.

If you believe that open source projects should be hosted on open source platforms, you should be interested in [Gitorious](https://gitorious.org/). Unfortunately, Gitorious was acquired by GitLab B.V. in March 2015, and then shut down in June. GitLab B.V.'s own [GitLab](https://gitlab.com) is open source as well, but some features are only available in proprietary Enterprise Edition.

If you think that you shouldn't pass responsibility for your code hosting to anyone else, [git reference implementation may act as server](https://git-scm.com/book/it/v2/Git-on-the-Server-The-Protocols). You only need computer with SSH daemon running hooked up to fat enough pipe. There are also open source web interfaces for git repositories, issue tracking systems and wikis that you can host on your own server. The main challenge is in integrating them all together.

Finally there are specialized hosting providers that will gladly help you out if your project meets certain criteria. Among them is 
[alioth](http://alioth.debian.org/) (for Debian packages), 
[FreeDesktop](http://www.freedesktop.org/wiki/) (for Linux desktop tools), 
[KDE](https://projects.kde.org/) (for projects using KDE Frameworks) and
[Savannah](http://savannah.gnu.org/) (for GNU projects).

## Conclusions

Congratulations for reading so far! If you have made it here, you probably think that I think that GitHub is evil and we should actively fight against it's domination, or at least avoid it all costs. 

Well, not really.

GitHub Inc. and GitHub do some things right. First of all, it's highly available remote git repository with web interface. That is quite a big deal in itself.
Second, there is some anecdotal evidence that "network effect" of GitHub really exists and moving your project there will get you more contributions in form of reported issues, pull requests and whatnot. Historically, GitHub might have played substantial part in positioning git as *de facto* standard of source control software, so they deserve credit here. Finally, GitHub Flow is extensively documented, which makes it easy to get started;plus, it does work for some projects and some people.

These are all good reasons to use GitHub. But I don't think they are good reasons to use GitHub **exclusively**. Instead, create account on one of competing sites and 
[configure your local git repository to push into both sites at once](http://stackoverflow.com/questions/14290113/git-pushing-code-to-two-remotes).
That's what I have done.
