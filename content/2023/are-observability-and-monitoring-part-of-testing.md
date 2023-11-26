Title: Are observability and monitoring part of testing?
Slug: are-observability-and-monitoring-part-of-testing
Date: 2023-11-26 13:40:52
Category: Blog
Tags: AST, planet AST, planet MoT, testing

The Association for Software Testing is crowd-sourcing a book, [_Navigating the World as a Context-Driven Tester_](https://associationforsoftwaretesting.org/navigating-the-world-as-a-context-driven-tester-book/). The book is edited by [Lee Hawkins](https://therockertester.wordpress.com/), who posts questions on [Twitter](https://twitter.com/AST_News), [LinkedIn](https://www.linkedin.com/company/association-for-software-testing/), [Mastodon](https://sw-development-is.social/web/@AST), [Slack](https://associationforsoftwaretesting.org/2016/11/13/ast-members-slack/), and [the AST mailing list](http://eepurl.com/tCFsn). You don't have to be a member to give your answer to the most recent prompt, "Are observability and monitoring part of testing?". Mine is below.

-----------------

Most commonly these terms are used in context of operations, and activities related to them are responsibility of operators (system administrators, DevOps, site reliability engineers etc.), not testers.

That's because most commonly a team that develops a software - and that's where testers usually are - is different than a team that deploys software and makes sure it's up and running. And there are some good reasons for that.

For one, technical skills required to do these things well are quite distinct.

Two, there's a difference in work scope. Development team is mainly concerned about the software they develop and it assumes that certain dependencies are met (computing resources, database, message queue etc.). Operations team main job is to ensure these dependencies are indeed available, and usually it works on many projects at the same time.

Historically, these teams were often inside _different companies_. As users became always online and software vendors moved to software as a service model, this is less relevant today. However, it's worth pointing out that there are still security, legal and technical reasons for software vendor to leave operations to software users.

But the mere observation that most people working in software do not consider observability and monitoring to be a part of testing is not particularly interesting. I think much more intriguing question is: _could_ they be part of testing? Would it be _worth it_ for them to be a part of testing?

My firm belief is that core of "testing" is gathering of information and learning something about reality. As far as I understand it, observability is _precisely_ that. The main difference is that "testing" happens mostly before a release, and usually in somewhat contrived environment, while observability happens after software has been deployed and refers mostly to actual production environment, with all its complexity and quirks. Testing is also more directed and intentional, while observability system may gather all information available, just in case it turns out relevant later.

But I don't think it's controversial to say that information how software is actually used, what parts are most visited, for how long, when, on what environments and by how many users is _invaluable_ to a development team. For testers, it can be extremely useful, helping to design better tests and guiding focus towards "hot" areas where potential bugs would be more visible. It can also be used to design testing environments that better model actual production environments.

The point of monitoring is alerting a team about critical errors and recovering from them as soon as possible. _Some_ of these problems might be relevant and useful for a software development team - either because they were caused by their software, or because software could be improved to react better to similar errors in the future.

If we agree that observability and monitoring _can_ be useful for testers, the last question remains: what would it take to involve testers in these activities?

I can't answer that question from my own experience, but I do have some intuitions.

First and most important, there must exist a communication channel between operations and development team. Development team should be notified about **all** problems and they should be able to at least passively participate in post-mortem sessions. They should have an ability to influence metrics that are being gathered by observability system, and they should actively change their own software to expose particularly interesting and useful metrics.

Second, there needs to be a will to participate among testers themselves. Unfortunately, there are far too many testers that are happy to just continue things the way they have always been. Testers might also be overworked and overextended, and not very happy to take one more responsibility.

The same applies to operators, who likewise are not dying to have one more thing to do. And in case of operators, there's one more thing I have not discussed so far - _how exactly_ would working closely with development team benefit _them_?

Finally, the success might hang on buy-in from organization leaders. They need to understand the benefits of this cross-team collaboration and _actively make space for it_. It's not enough to set a goal without providing all the resources necessary to fulfill it.
