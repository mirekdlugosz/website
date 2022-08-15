Title: The problems with test levels
Slug: the-problems-with-test-levels
Date: 2022-08-15 12:18:00
Category: Blog
Tags: planet AST, planet MoT, planet Python, testing

## Test levels in common knowledge

A test pyramid usually distinguishes three levels: unit tests, integration tests and end to end tests; the last level is sometimes called "UI tests" instead.
The main idea is that as you move down the pyramid, tests tend to run faster and be more stable, but at the expense of being isolated.
Only tests on higher levels are able to detect problems in how building blocks work together.

ISTQB syllabus presents similar idea.
They distinguish four test levels: component, integration, system and acceptance.
These test levels drive a lot of thought around testing - each level has its own distinct definition and properties, guides responsibility assignment within a team, is aligned with specific test techniques and may be mapped to phase in software development lifecycle.
That's a lot of work!

Both of these categorizations share the idea that higher level encompasses level below it, and builds upon it.
There's also certain synergy effect at play here - tests at higher level cover something more than all the tests at the levels below.
That's why teams with "100% unit tests coverage" still get bug reports from actual customers.
As far as I can tell, these two properties - hierarchy and synergy - are shared by all test levels categorizations.

## The problems

I have some problems with this common understanding.
In my experience, while test levels look easy and simple, it's unclear how to apply them in practice.
If you give the same set of tests to two testers, they are likely to group them to test levels in very different ways.
Inconsistencies like that begs the question: are test levels actually useful categorization tool?

I know, because I have faced these issues when we tried to standardize test metadata in [Red Hat Satellite](https://www.redhat.com/en/technologies/management/satellite).

One of the things provided by Satellite is host management.
You can create, start, stop, restart or destroy the host.
If you have tests exercising these capabilities, you could file them under component level, because host management is one of components of Satellite system.

Satellite also provides content management.
You can synchronize packages from Red Hat CDN to your Satellite server and tell your hosts to use that exclusively.
This gives you ability to specify what content is available, e.g. you can offer specific version of PostgreSQL until all the apps are tested against newer version.
This also allows for faster updates, because all the data is already in your data center and you can use fast local connection to fetch it.
Tests exercising various content management features can be filed under component level, because content management is one of components of Satellite system.

You can set up host to consume content from specific content view.
Your test might create a host, create a content view, attach host to content view and verify that some packages are or are not available to this host.
You could file such test under integration level, because you integrate two distinct components.

But you could also file that test under system level, because serving specific filtered view of all available content to specific hosts based on various criteria is one of primary use cases of Satellite, and possibly the main reason people are willing to pay money for it.

For the sake of argument, let's assume that test above is integration level test, and system level is reserved for tests that exercise some larger, end to end flows.
Something like: create a host, create a content view, sync content to host, install a specific package update that requires restart and wait for a host to be back online.

Satellite may be set up to periodically send data about hosts to cloud.redhat.com.
When you test this feature, you might consider Satellite as a whole to be one component and cloud.redhat.com to be another component.
This leads to conclusion that such test should be filed under integration level.

While this conclusion is *logical* (it follows directly from premises), it doesn't *feel* right.
If test levels form a kind of hierarchy, then why test that exercises the system as a whole is on integration level?

You can try to eliminate the problem by lifting this test to system level.
But there still are two visibly distinct tests filed under single label - some system level tests exercise Satellite as a whole, and some system level tests exercise integration between Satellite and some external system.

Either way, your levels become internally inconsistent.

Let's leave integration and system level for now.
How about acceptance level?

Satellite is a product that is developed and sold to anyone who wants to buy it.
There is no "acceptance" phase in Satellite lifecycle.
Each potential customer would run their own acceptance testing, and while the team obviously appreciated the feedback from these sessions, it was rarely considered to be a "release blocker".

Given these circumstances, we decided to create a simple heuristic - if the test covers issue reported by customer, then this test should be on acceptance level.

Soon we realized that a large number of customer issues are caused by specific data they have used, or specific environment in which the product operates.
Our heuristic elevated tests from component or integration level way up to acceptance level.

This shows the biggest problem with acceptance level - it belongs to completely different categorization scheme.
Acceptance level is not defined by **what** is being tested, but by **who** performs the testing.

Perhaps there was a time when that distinction had only theoretical meaning.
As a software vendor, you built units, integrated them, verified that system as a whole performs as expected and sent that to customer, who would verify that it fits the purpose.
Acceptance level tests were truly something greater than system level tests.

But we don't live in such world anymore.
These days, most software is in perpetual development.
There's no separate "acceptance" phase, because what is subject to acceptance testing of one customer, is actual production version of another customer.
If product is changed based on acceptance testing results, all customers receive that change.

Perhaps placing acceptance testing at the level above system testing was always something that only made sense in very specific context - when developing business software tailored to specific customer that does not subscribe to "all companies are software companies" world view.

While I do not have this kind of experience, I have heard about military contractor that had to submit each function for independent verification by US Army staff, because army needed to be _really_ sure there's nothing dicey going on in the system.
I find it believable.
I can think of bunch of reasons why a customer would want to run acceptance tests on units smaller than the whole system.
One of them would be a really high stake - when a bug in a system could mean a difference between being alive and dead.
Another would be when system is expected to last decades and it's really important for a customer to obtain certain knowledge and prepare for future maintenance.
Military, government (especially intelligence), medicine and automotive all sound like a places where customer might want to verify parts of the system.

Finally, what about unit (component) level?
Are _they_ simple?

Most of testers learn to understand unit tests as a thing that is a developer problem - they are created, maintained and run by developers.
Of course you might question this understanding in the world of shifting left, DevTestOps and "quality is everyone's responsibility" mantra, but let's ignore that discussion for now.
If unit tests are developers problem, we should see what developers think about them.

Apparently, they [discuss at length what unit even *is*](https://dev.to/tyrrrz/unit-testing-is-overrated-150e).
There's also an anecdote floating around of a [person that covered 24 different definitions of unit test in the first morning of their training course](https://martinfowler.com/bliki/UnitTest.html).

## Could we do better?

I think it's clear that there are problems with common understanding of test levels.
But the question remains: are these problems with that specific implementation of the idea, or is the idea of tests levels itself completely busted?
Could there be another way of defining test levels?
Would it be free of problems discussed above?

My thinking about test levels is guided by two principles.
First, levels are hierarchical - higher level should built upon things from the level below.
Obviously, the higher level should be, in some way, more than simple sum of these things below.
Second, it should be relatively obvious to which level a given test belongs.
"Relatively", because borderline cases are always going to exist in one form or another, and we are humans, so we are going to see things a little different sometimes.
But these should be exceptions, not the norm.

**Function level**.
For large majority of us, function is the smallest building block of our programs.
That's why the lowest level is named after it.
On the function level, your tests focus on individual functions in isolation.
Most of the time, you would try various inputs and verify outputs or side-effects.
Of course it helps when your functions are pure and idempotent.
This is the level mainly targeted by techniques like fuzzing and property-based testing.

**Class level**.
The name comes from object-oriented paradigm, where we tend to group functions that work together into classes.
The main goal of tests at this level is to verify integration between functions.
These functions may, but don't have to, be grouped in the single class.
Since classes group behavior and state, the setup code is much more common on this level - you will find yourself ensuring that class is in specific state before you can test what you actually care about.
Test cleanup code will also appear more often than on function level, for the same reason.
Property-based testing is harder to apply at this level.

**Package level**.
This name is inspired by Python naming convention, where package is a collection of modules (i.e. functions and classes) that work together to achieve single goal.
This is also what package level tests are all about - they test interactions between classes, and between classes and functions.
These are the tests that pose the first challenge for common understanding of test levels.
Some people might consider them integration tests (because there are few classes working together, and you want to test how well they integrate with each other), while others would consider them unit tests (because package is designed to solve the single "unit" of domain problem).
For me, package is something that is coherent enough to have somewhat clear boundary with the rest of the system, but not abstract enough to be considered for extraction from the system into 3rd-party library.
This level might be easier to understand in relation to the next level.

**Service level**.
The name comes from microservice architecture.
We can discuss at length whether microservices are right for you, and if they are anything more than a buzzword, but that is a discussion for another time.
What's important is that your project consists of multiple packages (unless you are in the business of creating libraries).
Some of these packages, or some sets of packages, have very clearly defined responsibility within the system, and boundaries that set them apart from the rest of the system.
At least theoretically, these packages *could* be extracted into separate library (or separate API service) that your project would pull in as a dependency.
Service level tests focus at these special packages, or collections of packages.

Service level is where things start to become really interesting.
All levels below are focused on code organization.
At service level, you have to face the question of why are you developing the software at all.
Service level is primarily driven by business needs, and relationship between them and specific system components.
Some services encapsulate "business logic" - external constraints that system has to adhere to.
Other services exist only to support these core services or to enable integration with other systems.
Some services are relatively abstract and are likely to be implemented by some open source library (think about database access service or user authentication service).

Service level is also where testers traditionally got involved, because some services exist only to facilitate interaction of the system with outside world.
Think about generating HTML, sending e-mails, REST API endpoints, desktop UIs etc.


**System level**.
For large number of intents and purposes, system is a synonym of "software".
These days, where everything is interconnected and integrated, sometimes it might be hard to clearly define "system" boundaries.
I would use a handful of heuristics: your customers buy a copy of a system, or license to use a system, or create an account within a system.
System is what users interact with.
System has a name, and this name is known to customers.
System is subject to your company marketing and sales efforts.
Most of the things we know and use everyday are systems: Spotify, Netflix, Microsoft Windows, Microsoft Word, ...

A lot of systems truly *are* a collection of services (subsystems).
Most of discussions around software architecture focus on how to arrange services in a way that responsibilities and boundaries are clear.
For many architects, the end goal is to design a system in a way that makes it possible to swap one service implementation for another without impacting the whole thing.

While this separation is important from development perspective, it's also crucial that it is **not** visible by a customer.
If user *feels*, or worse - *knows* that she moves from one subsystem to another, more often than not it means that UX attention is required.

System level tests focus on exercising integration between subsystems and exercising system as a whole.
Often they will interact with a system through the interface that is known to users - desktop UI, web page or public API.
For that reason, system level tests tend to be relatively slow and brittle.
To offset that, usually you will focus only on happy paths and most important end-to-end journeys.

**Offering level**.
Many companies are built around single product and never reach this level.
But when a company is big enough and offers multiple products, usually it is important that these products work well together.

Today, one of the best examples is Amazon and AWS.
AWS provides access to many services, including EC2 virtual machines, S3 storage and RDS managed databases.
Most of these services are maintained by dedicated teams, and customers may decide to pay for one and not another.
But customers might also decide to embrace AWS completely.
When they do, it's *really* important that setting up EC2 machine to store data on S3 is easy, ideally easier than any other cloud storage.
Amazon understands that and offers products that group and connect existing services into ready to use solutions for common business problems.

Testing on this level poses unique technical and organizational challenges.
Company engineering structure tends to be organized around specific products.
Each product will be built by different team using different technology stack and tools, and might have different goal and target audience.
To effectively test at this level, you need people working across organization and you need to fill the gaps that nobody feels responsible for.
Often you need endorsement from the very top of company leadership, because most of the teams already have more work than they can handle - and if they are to help with offering testing, that must be done at expense of something else.

## But this proposal is bad

I am not claiming that above proposal is perfect.
In fact, I can find few problems with it myself, which I discuss briefly below.
But I think it is step in right direction and provides good foundation that you can adjust to your specific situation.

If we follow the pattern that higher level is a collection of elements at the level below, we might notice that function is not the smallest unit - most functions are executing multiple system calls, and some system calls might encapsulate multiple processor instructions.
I've decided to skip these levels, because I don't have any experience working with systems so low in the stack.
But I imagine people working on programming languages, compilers and processors might have a case for level(s) below function level.

You might find "class level" to have a misleading name if you work in the language that does not have classes.
In functional languages, like Lisp or Haskell, it might be more fitting to use "higher-order functions level".
I don't think the label is the most important part here - the point is, tests at that level verify integration between functions.

Python naming conventions differentiate between modules and packages.
Without going into much detail, module is approximated by single file, and package is approximated by single directory.
In Python, package is a collection of modules.
Java also differentiates between modules and packages, but the relationship is inverted - package is a collection of classes and functions, and module is a collection of related packages.
Depending on your goals and language, it might make sense to maintain both "module level" and "package level".

Unless you are working on microservices, you might prefer to call "service level" a "subsystem level".
My answer is the same as to "class level" in purely functional languages - it doesn't matter that much *how* you call it, as long as you are being consistent.
Feel free to use a name that better suits your team and your technology stack naming conventions.
The point of service / subsystem level is that these tests cover part of the system that has clearly defined responsibility.

Users these days expect integrations between various services that they use.
Take Notion as an example - it can integrate with applications such as Trello, Google Drive, Slack, Jira and GitHub.
These integrations need to be tested, but it's unclear to which level these tests belong.
They aren't system level tests, because they cover system as a whole and something else.
They aren't offering level tests either, because Trello, Slack and GitHub are not part of your company offer.
I think that sometimes there might be a need for new level, which we might call "3rd party integrations level".
I would place it between system level and offering level, or between service level and system level.

## Why bother discussing test levels, anyway?

You tell me!

This article focuses more on "what" of test levels than on "why", but that's a fair question.
To wrap the topic, let's quickly go over some of the reasons why you might want to categorize tests by their levels.

Perhaps you want to track trends over time.
Is most of your test development time spent at function level or service level?
Can you correlate that with specific problems reported by customers?
Does it look like gaps in coverage are emerging from the data?

Perhaps you want to gate your tests on results of tests at the level below.
So first you run function level tests, and once they all pass, you run class level, and once they all pass, you run package level...
You get the idea.

Perhaps you have different targets for each level.
Tests on lower levels tend to run faster, while tests on higher levels tend to be more brittle.
So maybe you are OK with system level tests completing in 2 hours, but for function level tests, finishing in 15 minutes is unacceptable.
And maybe you target 100% pass rate at the function level, but you understand it's unreasonable to expect more than 95% pass rate at the system level.

Perhaps you need a tool to guide your thinking on where testing efforts should concentrate.
As a rule of thumb, you want to test things on the lowest level possible.
As you move up in test levels hierarchy, you want to focus on things that are specific and unique to this level.
It's also generally fine to assume that building blocks on each level are working as advertised, since they were thoroughly tested on the level below.

Whatever you do with test levels, I think it makes sense to use a classification that can be applied unanimously by all team members.
Hopefully the one proposed above will give you some ideas on how to construct such classification.
