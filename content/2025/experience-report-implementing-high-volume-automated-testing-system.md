Title: Experience report: Implementing High Volume Automated Testing system
Slug: experience-report-implementing-high-volume-automated-testing-system
Date: 2025-08-06 18:23:20
Category: Blog
Tags: Python, case library, planet AST, planet MoT, planet Python, testing

I first heard about High Volume Automated Testing in 2017, and I've wanted to try it ever since. The opportunity came in 2022, when I was working on revamping a UI testing framework for software called Quipucords. This article focuses on the decision points I encountered, the alternatives I considered, and the choices I made. At the end, I share the lessons I learned from this experience.

Keep in mind that this is not intended to apply to all possible High Volume Automated Testing systems, nor is it meant to be an exhaustive list of such system design decisions. I can't talk about alternatives I didn't think of, I have not actually tried all the alternatives, and I was working in the context of the UI layer of a specific product.

I share [links to my implementation near the end of the article](#sample-implementation). Looking at the code might help to understand some of the more abstract parts for the article.

But before we begin, let's briefly talk about High Volume Automated Testing.

## What is High Volume Automated Testing

High Volume Automated Testing (HiVAT) takes the idea that automation changes the very concept of how tests can be created, run and evaluated, and extends it to its logical conclusion. When learning about test automation, people tend to think about programming a computer to do the same things that a human would do when interacting with a software, but faster and unaffected by boredom or fatigue. HiVAT is born from the question: why stop there? If you program a computer to interact with a software, you can program it to do things that would be too costly for a human to do, or which a human could never do.

I first heard about it in 2017, from the [article published by Cem Kaner in 2013](https://kaner.com/?p=278), but the idea is much older than that. Kaner gave a couple of talks on the topic in 2003 and 2004. He claims to have experienced systems like that first-hand in 1980s, and in various places he mentions prior work dating back to 1970s and even 1960s. However, the phrase "High Volume Automated Testing" and the acronym "HiVAT" are relatively obscure. They don't seem to be discussed in the community often, and I reckon most testers have never heard of them.

These days, the ideas behind HiVAT see mainstream recognition in property-based testing and fuzzing.

I highly recommend reading the [Kaner article](https://kaner.com/?p=278) for a better explanation and full background before moving on.

## Designing a HiVAT system

Kaner lists twelve techniques that he considers to be examples of HiVAT. So the very first decision to make is: do you want to implement one of already known techniques? If so, which one? If not, how is it different from established solutions?

I wanted a robot that is able to automatically and autonomously wander through the application web interface. It should click random links, fill the forms, edit and delete items where possible etc. The idea was that it should work without supervision for some time, say 15 to 30 minutes. During that time it would most likely cover all the same scenarios we explicitly covered in the standard test suite, but would do so in a random order, while canceling some operations, while repeating certain actions etc. If it encountered any problems, they would likely be caused by the specific data that was introduced or the order of actions that was taken. Ideally, it should just finish the session without any troubles.

This is one decision that I haven't considered too comprehensively. It was kind of obvious for me that in the context I was working in, this is how HiVAT would look like.

In Python-inspired pseudo-code, the entire system may be approximated as a relatively simple loop. That loop doubles as a map of the main decisions that we have to make.

```python
global browser_driver = create_browser_driver()

while should_still_run():
   methods = get_methods_available_at_this_place()
   chosen_method = random_choice(methods)
   method_arguments = get_arguments_required_for_method(chosen_method)
   try:
       chosen_method(method_arguments)
    except Exception:
       # could be a bug!
       handle_exception()
```

### What are the system stopping criteria?

An autonomous testing session can last a long time, but it can't run forever. So when should it stop? How can a system decide if it should keep going?

The obvious solution is to just let it run, basically outsourcing the decision outside of the system. It will stop when the process is killed. That can be done using `kill` command, by shutting down the machine, forcing a CI environment to stop execution etc. That approach has two fundamental problems: it's not particularly user-friendly and it might bring additional complexity if you need to clean up. Signal might be received in the middle of the loop, and you don't control when exactly it is sent.

Other approach is to let it run until the first exception, signaling a real issue. This builds on the assumption that issue might leave a system in erratic state that invalidates any later actions. The main drawback is that the faulty state might not apply to the entire system, and you lose the opportunity to observe how it operates for a longer period or under larger data volumes.
I imagine that for most systems, invalid data causes them to enter a partially broken but still functional state.

You can stop the execution after a number of loop iterations. The main problem is that actions are essentially random, and they exercise the system unevenly - a simple navigation between pages has different impact than creating a report that needs to be computed in background task. If you are unlucky, even a relatively large number of iterations might end up executing mostly vain actions.

You can stop the execution after a certain time. This has similar problem to counting loop iterations, but this time it's longer actions that take undue part of the assigned budget. It might happen that a long session did relatively few actions, because all of them happened to take a lot of time.

Finally, you can try to introduce some system-specific stopping criteria. One way would be keeping separate track of low-impact and high-impact actions, and stopping when both are exceeded. Another would be keeping track of the number of objects created.

I decided to go with loop iterations counter. That was very easy to implement and at this stage I intended to run the tool exclusively on a local machine. I assumed that after a few sessions I will be in a better position to decide if things should stay that way, or change. I wasn't too worried about placing uneven demands on the system during execution, as these should smooth out across many sessions.

### Which actions should be available to the system?

At every step, HiVAT should do "a random thing". But what does that mean? Are there any actions that should never be selected? How can a system know what actions are available?

In user interface, a single action may be broken down into multiple steps or interactions. Think about editing an existing object, like a user address. Usually user would have to click "Edit" button, which opens a form with address fields. After modifying the form user needs to click "Save" for data to be persisted in the system. Clicking "Cancel" discards changes.

There's no general consensus how that should be modeled by the test framework. Some people opt to provide methods for modifying a form, and a separate method for submitting changes. But that makes test code more verbose and ties tests to a specific implementation (what if form changes are saved automatically in the new version?). So other people think there should be a single method that both modifies a form and submits changes. But then the framework loses the ability to test a scenario where form is modified and user decides to cancel changes. This trade-off is explained in depth in ["Going Deeper into the Page Object Model" article by Blake Norrish](https://medium.com/@blakenorrish/going-deeper-into-the-page-object-model-4aee634d9c98). On a side note, highly recommended read.

The main problem is that the solution you might prefer from the point of view of a generic testing framework might not be the same solution that you would pick for autonomous software traversing program.

In my case, I decided to do both. Page objects provided separate methods for granular actions, like changing the form and clicking "Submit". At the same time, they also provided more abstract methods representing user intent, like "modify the address". Usually this more abstract method would just call a sequence of methods for more specific actions. While the traditional tests used abstract methods exclusively, the system I was developing was operating only on concrete methods.

The specifics of how the main loop may obtain available actions depend on the programming language and this is something that might be worth considering before writing a single line of code. You probably want a language with rich runtime introspection capabilities, so you can take a random object and just see what methods it has available. Dynamic dispatch seems to also be a must. Language that offers interpreted runtime with dynamic typing is going to have an edge over the language that requires compilation and static typing.

The problem was relatively easy to solve in Python with type hints, which was what I used. I'm not sure if I would be able to solve it in Rust, but that might say more about my Rust expertise than the language itself.

### How can a system call a method that requires arguments?

Conceptually, you can consider this an implementation detail of a previous section. Methods and functions usually require arguments. How can a system know what arguments are required? How can it differentiate valid values from invalid, and handle them appropriately?

Answer to the first question really depends on a programming language and features it offers. Similar to the previous section, languages with rich introspection capabilities will generally make it much easier than ones without. Here, however, a very strict typing will prove easier to use than a system with dynamic typing. If you need to pass "something" to a function for it to work, it helps to know the exact definition of "something". Practically speaking, you might need to create rich library of data transfer object classes that will model arguments taken by various methods across the system. It's even better if library can quickly generate DTOs filled with data. In case of Python, using type hints is almost required.

The second question refers not only to type validation, but also a business validation. If you have a method to delete a user, the argument of that method is not as much a string, but a string that represents the name of a user that exists in the system. Proper autonomous system needs a way of knowing if given input will pass system validation or not, and how to handle the second case.

For simplicity, I decided to stick to valid data. That changes a problem a little, as now my tool needs a way of obtaining such data, and possibly creating it on demand. Usually that can be done by manipulating the system database directly, or using APIs to manage the data. In my case it was not that much of a problem, as testing framework already had API tests and ability to obtain and create data. I only needed to wire these modules to the code I was writing.

One obvious alternative is for HiVAT to keep track of data it created (or deleted), and use that whenever existing data is needed to perform a step. That quickly gets complicated if your data has dependencies - testing software might want to perform a step that depends on specific data, but it would not be possible if it didn't happen to create that data first. This can be overcome with larger number of iterations in a single session.

This is one of the decision points that were mostly theoretical for me. I was extending an existing testing framework written in Python, and changing programming language was not up for debate. So I didn't need to weigh the options carefully as much as I had to figure out how to solve this specific problem in Python. As I mentioned, I decided to use type hints liberally and used introspection capabilities built into the language.

### How to handle actions history?

Should the history of actions be tracked? How? Where should it be stored? Should it be displayed? How should it look like, then? How can you make the history machine-readable, if that's desired?

This is one of the few decision points where you don't _really_ have to choose, but instead you can have your cake and eat it too. You can both save all the actions in more human-readable form in a log file and keep machine-readable format in memory during a session. You can serialize data from memory at the end of the session, or only if there was an issue during execution. Contrary to most of other decision points, there's no real reason why one choice here should prevent you from also doing another.

One of the most consequential choices is deciding where to store a list of actions. You can keep it in system memory, or you can persist it on a disk. The trade-offs are well known. If you decide to keep it in the memory, then you can lose everything if the entire system crashes. You also use the computer memory, making it unavailable to other processes, but that's probably negligible unless you run billions of actions. If you save to disk, you might need to think about ways of reading it back.

If you keep the data in system memory, you should probably model it as some kind of structured information. Depending on the programming language, you might also have an option to keep references to existing classes, instances or functions. This would make it much easier to use them if needed. You can always easily turn that into human-readable form. The alternative - keeping human-readable strings in memory - appears to be all downside and I struggle to take it seriously.

It's important to decide when the data is going to be displayed. I can think of four options: never, in real time (streaming, display action as soon as it is taken), at the end of the session and only in the case of failure. Displaying in real time and displaying in case of failure seem like main options to consider. The risk of displaying in case of failure is that a bug in HiVAT might prevent information from being displayed at all, which is especially problematic in case of critical failure of software under test. If you decide to display information in a streaming fashion, you might end up with a lot of information at the end of session where generally nothing noteworthy happened.

Finally, some actions might involve sensitive data, like private information or passwords. They probably should be protected, so they should be hidden or filtered out before being displayed. At the same time this is an information loss that would prevent fully reproducible session replays. If this is a concern, you should probably have different ways of storing and accessing human-readable and machine-readable data.

I decided to keep the history information in memory. Actions were modeled by a special class. A test runner would print action history only in the case of failure. When printed, actions were somewhere between human-readable and machine-readable. I did not go out of my way to make them easy for humans to read, but eventually I did not need to read them programmatically either.

Since there was no sensitive data that would require additional carefulness in handling, I did not implement any kind of filtering or hiding mechanism. However, this is something I did consider briefly.

### Should the system allow for a control of certain sequences?

The HiVAT system I envisioned relied heavily on randomness, but it's not hard to think about cases where it could be beneficial to limit it. Should every session be independent from all the previous ones and purely random? Or should there be a way to re-run the previous session? Should it be possible to constrain randomness of certain parts of the session? Which ones?

Some of these questions might make sense only in the context of an answer to a question posed in the previous section, and some of answers to these questions are self-evident from the answer given in the previous section. If you want the ability to replay the entire session, or any subset of it, then you need a way to store the history of all actions in machine-readable format on a persistent storage.

The ideal outcome is that if you have a session that finds an issue, you can re-run it on a brand new instance of software with empty database. That would be a significant step towards making all the issues reproducible.

And imagine you could have a system which takes a session that finds an issue and automatically reduces it to a minimal reproducible path. One session might last 15 minutes, but it doesn't mean that everything that happened during that time is equally important. Probably most of things could be safely skipped, as there is relatively short subpath that guarantees the occurrence of the issue.

These two scenarios were main things I was thinking about when making that decision. It's really a binary choice - should you design a system that allows to do these capabilities, or should you just give up on the entire thing? I haven't spent too much time considering randomness of specific choices, like always picking up the same item from the list. I feel if I went down this path, there would be a lot of decisions to be made around communicating to the system which parts should be more reproducible.

While I have not implemented a replay system, and didn't spend any time actually thinking how a critical path finder could be built, I decided that my system should be designed in a way that makes such changes in the future possible. In practice it meant identifying possible extension points and leaving around few hooks that might help later.

### How should unexpected errors be handled?

It's almost inevitable that system encounters an issue during a sufficiently long run, either due to a problem in a software under test, or due to a bug in the testing system itself. What should happen then?

This is something you might have covered when deciding about stopping criteria. One of the options back then was that the system should stop on the first error it can't handle.

But if you decided to stop based on a different condition, now is the time to revisit that choice. Should your system _also_ stop on an error? Or should it press forward, unreliability of later information be damned? Or should you design more elaborate error handling code?

First two choices were already discussed in an earlier section, so I'm going to focus only on the last one. Maybe your testing system can communicate with the software under test and revert it back to a known working state? Or maybe there are some actions that you know how to cancel or revert? Or maybe you can make decisions based on the nature of the issue and context of the action - e.g. transient network errors probably can be ignored or retried.

In my case, I decided to ignore some errors that I knew can be safely ignored, but make all the others fatal. That decision goes back to an earlier choice to only print actions history in case of error. If I decided to ignore errors and continue running, then I would have to find a way to still print history at the end of the run, or change that other decision and always print the entire history. But then it would make it harder to decide if any given session encountered issues or not.

## Sample implementation

The HiVAT system I implemented for Quipucords project is [available at GitHub](https://github.com/quipucords/camayoc/pull/369/commits/5a937bcc3f6449c4f05d0a47be591bb0d5ff0cae#diff-722cef0e3b0c3aaefa824850b47fa258106568ae03ccdd7987990c13d59ad02cR47). It's only 25 lines of code!

However, that brevity was possible thanks to a number of helpers and design decisions made along the way. The UI framework that made HiVAT possible is introduced in [Camayoc PR #365](https://github.com/quipucords/camayoc/pull/365).

## Lessons learned

The main lesson I learned was that my HiVAT was not a good fit for the project. In Quipucords, the most interesting part happens in the backend, when software interacts with the external world. Software that randomly walks the user interface and has limited ability to trigger interactions with the external world is not particularly helpful. I think this kind of tool would be much more applicable for more self-contained systems, like ecommerce, banking or social media.

Another important lesson is that some programming languages and design approaches can make non-deterministic testing much easier to implement. It definitely helps if you can make choices of technology and framework design while thinking about that particular use-case - it might be hard to bolt onto existing code.

The kind of HiVAT I created seems to be worth considering if your system meets two requirements:

1. It is stateful. This kind of testing requires application to live longer than a single request, ideally longer than any individual session. Most of backend code is like that. Frontend - standing alone - not necessarily. To give you an idea, this would not be a right approach to test a tool like grep, which needs to initialize every time it is started.

2. Most of the data comes from the user. There are hardly any pure systems like that - everything is interconnected. Online shops are pretty close (the inventory usually needs to be loaded from outside, but after initial setup, it's mostly user actions). Banks are also pretty close - obviously there are bank-to-bank transfers, and most banks don't allow to do _everything_ online, but a large part of everyday operations can be modeled this way. Things like Evernote, JIRA or Trello are largely user-generated, but they also offer various integrations with 3rd party services.

Of course if your system does not meet these two requirements, it might still be worth to consider some other kind of HiVAT.

*Thanks to [James Thomas](https://qahiccupps.blogspot.com/) for his feedback and review of an earlier draft of this blog post.*
