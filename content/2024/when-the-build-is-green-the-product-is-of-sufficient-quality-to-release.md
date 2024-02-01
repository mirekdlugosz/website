Title: When the build is green, the product is of sufficient quality to release
Slug: when-the-build-is-green-the-product-is-of-sufficient-quality-to-release
Date: 2024-01-25 23:08:31
Category: Blog
Tags: AST, planet AST, planet MoT, testing

The Association for Software Testing is crowd-sourcing a book, [_Navigating the World as a Context-Driven Tester_](https://associationforsoftwaretesting.org/navigating-the-world-as-a-context-driven-tester-book/). The book is edited by [Lee Hawkins](https://therockertester.wordpress.com/), who posts questions on [Twitter](https://twitter.com/AST_News), [LinkedIn](https://www.linkedin.com/company/association-for-software-testing/), [Mastodon](https://sw-development-is.social/web/@AST), [Slack](https://associationforsoftwaretesting.org/2016/11/13/ast-members-slack/), and [the AST mailing list](http://eepurl.com/tCFsn). You don't have to be a member to give your answer to the most recent prompt, "When the build is green, the product is of sufficient quality to release". Mine is below.

-----------------

No, not really. At least not in any general sense. But you are free to choose to release based on single metric. If this is what you want, I would advise you to work on creating an environment that allows for this choice to succeed. I would also assume that you are aware of risks that this option entails, and you have considered other options as well.

If you want to release a software, you need a release strategy. You don't have to call it like that and you don't have to write it down, but it makes sense to spend few hours thinking about it. Here are some questions you should be able to answer:

* How many releases do you want to make? When you work under contract, there might be set number of releases that you will be able to make. Some specialized software is being used only once - think about space rocket controls, or software used during sports events like Olympics.
* How often do you want to release? Assuming there are going to be multiple releases, is there a specific frequency of releases that you want to maintain? Or are you going to release when you feel you are ready?
* Are you able to fix discovered problems after the release? Especially if you don't plan multiple releases, would you be able to release fixes for critical problems discovered afterwards?
* What are the risks of releasing software with unfixed problems? This greatly depends on the nature of these problems, but think also about your reputation and competition.
* What are the risks of holding a release to fix problems? This is mostly about all the things accompanying and related to release, e.g. marketing campaign that started well before the planned release date. Can you move things around? Can you afford to extend it?
* What does it take to actually make a release? All the technical aspects of getting the software to customers, including distribution logistics for physical copies, if there are any.
* What external factors might force you to make a release? These might be technical, like new version of operating system, or related to changed laws and regulations.
* How much in advance will you know about these external factors? Changes in laws are usually announced months or years in advance, but you might have only weeks to respond to changes in operating system.
* How does a release align with other things that company is doing? Your software is probably only a part of the company offering. Are you independent of other projects? Even when your software is the only thing that company provides, there are probably other branches in company that support it and they all have to work with common goal in mind.
* Who decides to make a release? Is that a development team, a product manager, a branch director, sales people? Software can't release itself, so who decides that this specific version is going to be made available to customers?

You can decide to empower the team to make release decisions whenever they see fit, disregarding most of outside factors and concerns. That's a perfectly valid choice!

The common risk of every single software release is that there might be important problems that you don't know about, and that you underestimated problems that you do know about - that they turn out to be more serious than you thought. By making a choice to release a new version based only on build results, you decide that these and some other risks are acceptable for you.

First set of risks revolves around quality of your automated checks suite that is run before the release. Common problems with such suites are lack of data variability and coverage gaps in areas that are hard to test, especially interactions with real external systems. If you don't maintain the discipline of only merging code that is covered by tests, you might also have insufficient coverage of newer features. Automated checks suite must also maintain a balance between thoroughness and execution time. It is common to keep separate pipelines for slow performance and security testing, and there's a risk of forgetting to run them before making a release.

If you make it easy to make a release, and you make a habit of frequent releases, there's a risk of losing vigilance. A Big Important Release acts as external pressure that keeps everyone cautious. When releases become a common thing, you might underestimate the importance of found issues, working under the assumption that you can always fix them later and make a new release. That assumption is true and valid for many software issues, but it will become a problem when it starts to be an excuse for sloppiness.

When release decision is made based on build results, releases are usually more frequent and smaller in scope (contain a limited number of changes). The argument goes, smaller releases are easier to test and inherently less risky, so it's better to release more frequently. On the other hand, smaller changes carry a risk of losing the forest for the trees. As your team is focused on small tasks, there might be nobody to consider the impact of these small changes on the product as a whole. Things that work well in isolation sometimes do not work well together.

Finally, there's a risk of that choice being wrong for your actual case. Many developers appreciate easy, small and frequent releases. But most of your customers just want to get the task done - they don't want to wait for update or be interrupted by it. They might have slow Internet connection or pay for downloaded data. They might be averse to change - people tend to be conservative and bear with arduous way of doing things, just because they have always done it like that.

If you want to release based on build results, you want to ensure that you have other ways to minimize these risks, and you have a safety net that minimizes the impact of them when they inevitably occur.

First, make it technically easy to release a new version of software. That usually means that release pipeline is fully automated. Whenever you decide to make a release, you should be able to just push a button and be confident that new version is available to customers.

Second, prepare a plan for when broken version is released, or release process itself fails. That might mean a simple way to yank and roll back a release, or empowering a team to quickly fix an issue and make another release. You might also schedule fire drills when you pretend that working release is broken, just to prepare for a real situation.

Third, if your delivery process allows it, consider rolling releases, blue/green deployments and post-release monitoring. The general idea is that you release new version to some small subset of your customers, and gradually make it available to others. That should be paired with monitoring, so if you notice that there are some problems with new version, you pause the release. This way most of customers never experience the broken behavior.

Finally, you need the ability to deliver new versions frequently. This is a given when you work on a software as a service, where you fully control who uses which version. But this dynamic changes as you move to software that is installed on customer devices, especially devices that are not always online.

To sum up, the quality of software, as signaled by build status, is only a small part of release equation. There's nothing wrong in deciding to focus on it, disregarding all the other factors. But you need to ensure that this is the right choice in your general business environment, and you should work on safety net that minimises the risk that this choice entails.
