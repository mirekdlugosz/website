Title: Testing a new feature - should you start with automation or by inspecting it yourself?
Slug: testing-a-new-feature-should-you-start-with-automation-or-by-inspecting-it-yourself
Date: 2025-02-11 19:56:12
Category: Blog
Tags: planet AST, planet MoT, testing

A fellow engineer submitted a question to internal mailing list. The gist is: a new feature is supposed to be released in a few months and there is no automation coverage for it. What should a person with a Quality Software Engineer title do? Should they test the feature "manually" and contribute automation later, risking it happens after a release? Or should they start writing automation right away, potentially postponing finding and reporting important issues?

My answer is below.

There are no simple recommendations and go-to answers that are going to be usually correct. It all depends.

First and foremost, what is the state of the feature in general? Are we still at the ideation phase, is any code already developed, does developer consider it done, did anyone else test it already?

Second, where does that feature fit in entire product? Is this completely new thing, or extension to something that product already does? Is this on the critical path of product usage? Did any customers ask for that, or did we internally decide it's a good idea? Is it going to be marked as tech preview in release notes or not?

Third, what is the social context of your team? Are you the only Software Quality Engineer, or is there a larger team? What is the workload for you and others? Who develops unit tests? And are there unit tests for this feature?

Fourth, how does that feature fit your automation suite? Can you easily extend existing framework to account for the new thing, or do you need to create completely new capabilities first? How much time do you think it's going to take?

As a tester, your main job is to provide accurate information to the team. Ideally, you would do that sooner rather than later. You should be able to identify risks and start the conversation on what the team is going to do with them. If you can, propose solutions and advocate for them. If you can and have time for that, implement solutions yourself.

Personally, I always start with understanding of the feature. What is the goal? How is it achieved? What workflow do we envision? Where are "hot" points where workflow can fail (i.e. due to unmet dependency)? Depending on the size of the feature, I would spend at least few hours ensuring that my understanding is correct and verifying my assumptions. More often than not, I will encounter questions that I can't find answers for, and if I am (un)lucky - that nobody thought about before. I will try to do that without looking at the implementation, to not guide my thinking and to avoid biases.

Then - or while doing above - I will create a list of test ideas. I will keep it very lightweight, maybe a sentence for each idea. Usually it's a mix of things I want to verify and things I want to find answers for.

At this point I will start thinking about the most effective ways of performing these tests and finding answers. Sometimes I will use tools to help me; sometimes these are going to be tools I create myself. At this point I don’t think about maintainability, performance, error handling etc. - it’s too early for that. Sometimes I will look into unit tests (if there are any) and see if the answer is already there. It may happen that I find unit test for a thing close enough to one I was interested in. In such case I will leverage it. That means modifying the test or creating new one based on one that I found. I might try to submit a PR with this new or modified test, so it becomes a part of unit test suite, but usually it's not my first priority.

As I go through my list, usually I encounter things that are interesting, puzzling or noteworthy for other reasons. Often they trigger new test ideas that I did not think about earlier. I will perform them right away or add to the list, to check later.

When I decide I have seen enough, it's time to think what tests seem important enough to include in future regression runs. It's the act of balancing sometimes conflicting constraints - what value does the test bring in the great scheme of things? How costly it is to develop? How fast can it run? Where is the right place to run it? Usually only a fraction of test ideas are going to make it into regression suite.

Finally, obviously, I need to implement these regression tests. I will start with most important first and look for ways that other people could help with that.

So, to answer your question: neither of the two. Look for things that matter. Identify real problems and focus on letting others know about them quickly. Use tools to aid you, but remember that tool is only here to support you. Don't repeat the work that developers have already done. See if you can leverage the work of other team members.
