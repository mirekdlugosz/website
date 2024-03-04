Title: What's the best format for a test plan?
Slug: whats-the-best-format-for-a-test-plan
Date: 2024-03-04 10:15:57
Category: Blog
Tags: AST, planet AST, planet MoT, testing

The Association for Software Testing is crowd-sourcing a book, [_Navigating the World as a Context-Driven Tester_](https://associationforsoftwaretesting.org/navigating-the-world-as-a-context-driven-tester-book/). The book is edited by [Lee Hawkins](https://therockertester.wordpress.com/), who posts questions on [Twitter](https://twitter.com/AST_News), [LinkedIn](https://www.linkedin.com/company/association-for-software-testing/), [Mastodon](https://sw-development-is.social/web/@AST), [Slack](https://associationforsoftwaretesting.org/2016/11/13/ast-members-slack/), and [the AST mailing list](http://eepurl.com/tCFsn). You don't have to be a member to give your answer to the most recent prompt, "What's the best format for a test plan?". Mine is below.

-----------------

It should come as no surprise that there is no single "best" format.

Each document that we create should be _for someone_ and should respond to some real or perceived _need_. Otherwise, why bother writing it?

I imagine perspective on planning changes as you move up in corporate hierarchy. For directors and executives it's all about expected resource utilization and budgeting. I think they want to know how many people to hire, how many devices they need to buy, how much their cloud costs are going to go up; and what they can skip or cut out while still meeting the strategic objectives. I wouldn't know, I have never had this kind of job.

As an individual contributor, my perspective is different. When I am asked to create a test plan, my first thought is "who am I writing this for?" _I_ might not need it, and I _definitely_ don't need it in this very heavy form exemplified by templates floating around the web. Other testers in my team often don't need it either - they are just glad they didn't have to write it. Developers in my team don't care. Other testers in adjacent teams are usually busy with their own things. My manager might be happy to see it, and he might or might not forward it up the chain, but I never heard back from as close as skip-level manager.

Usually after test plan is written, there's a request for review and comments sent to a number of people. In the best case I will get few questions pointing out parts that could be clarified, or some suggestions for things that I have missed. I appreciate them. This helps me to be more thorough and allows others to better understand what is happening in other parts of the project.

However, I doubt if test plan is the most effective way of achieving these goals. While everything that test plans usually cover _is_ important, I feel whatever I put in document should be the conclusion of conversation, not the beginning of it.

Let's say I think we will need a team of three people to complete all testing activities in given time, while there's only me and one colleague. Putting that somewhere deep in test plan will not make a new person appear out from nowhere. In fact, I am much better off talking with my manager about this - because either we need to arrange for new person right now, or we need to highlight to other stakeholders that certain things are at risk because there are not enough people.

The same applies to any hardware and software that might be needed for testing. Most companies have processes for obtaining these, which I would have to follow independently of any test plan document. If I have any doubts on whether my request is going to be accepted, I'd better talk with my manager instead of hoping he will notice this crucial detail somewhere in a test plan that I send him.

This is also true for test ideas that I might put in test plan. I am happy to share them with developers - the best thing that can happen is that I bring their attention to a thing they have not thought about, and they will fix the bugs before any code is subjected to testing. But I haven't seen any evidence that a long, mostly irrelevant document is the best way to start that conversation.

In fact, I consider thinking about test ideas to be the most valuable part of test planning. Usually I would try to create a list of things I think would be worth testing, based on any resources I have available at the time. Often while writing things down I will realize I'm not exactly sure what is supposed to happen - which means that either I didn't fully understood what's going on, or I found a problem with specification. Sometimes I will also write down questions I will want to find answers for.

That list of test ideas is going to be my starting point for actual testing. However, not all test ideas need to be performed repeatedly, and not all of them are worth automating - which leaves open the question if they should be included in any kind of formal test plan.

And even if I did include the whole list in a test plan, considering it to be complete would be a grave mistake. I assume I will add more items later. Some ideas might come to me while doing other things, some might be prompted by conversations that are going to happen as project evolves, and some I will create in response to the actual behavior of developed software. When I test, there are always things that pique my interest, and more often than not they are worth following - no matter if they are included in test plan or not.

I think all the above points, and then some, are now widely understood in the industry. That's why test plans are not so ubiquitous as they once were. Personally, I can count on one hand the number of times I've been asked to create a test plan in a last few years. The software I work on is in continuous development and sees many relatively small releases. Large things, if they happen, take months to develop, not years. We practice backlog refinements, three amigos meetings and collectively write acceptance criteria, which often _are_ a lightweight form of test plan. Along with the other testers we are in the same team as developers, closely watch progress on new features and get a chance to interact with early versions of the software. I participate in code reviews and suggest improvements to unit tests, which allows me to share test ideas.

We get many of the same benefits that test plan could provide, but in less formal way and without spending much time writing it.
However, if I were asked to write a test plan, I would start by reading ["What Should A Test Plan Contain?" by Michael Bolton](https://developsense.com/blog/2008/12/what-should-test-plan-contain).
