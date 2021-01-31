Title: Comments on ISTQB's "Vision on the Future of Software Testing"
Slug: comments-on-istqbs-vision-on-the-future-of-software-testing
Date: 2020-02-27 10:34:23
Category: Blog
Tags: testing

ISTQB's "Vision on the Future of Software Testing" made rounds on social media recently. I'm hopping on to this train with my own commentary.

<!-- more -->

The paper can be found on [ISTQB website](https://www.istqb.org/references/white-papers.html) ([direct link](https://www.istqb.org/documents/ISTQB_The_Vision_on_the_Future_of_Software_Testing_Final.pdf)). Feel free to read it first, and decide for yourself if my commentary has any merit. Or keep on reading, and see if ISTQB's paper is worth your time.

Below, I focus solely on content. ISTQB's paper has many editing mistakes, which I cover in [part 2]({filename}comments-on-istqbs-vision-on-the-future-of-software-testing-appendix.md).

## Introduction

First thing you might notice is that while document deals with the future, that future is never specified. The only reference to time frame is in following sentence: "The feedback we received [from surveyed Thought Leaders], while extremely interesting and practical was focused more on the near-term aspects of testing”. The way I read it, surveyed people gave opinion on near-term future, while writers wanted to focus on more distant future. On the side note, "near-term" is never defined either. We just don't know if ISTQB means months, years or decades, and that makes all the difference in interpretation and discussion with vision.

In introductory paragraphs, they say "We  surveyed a group of twenty Thought  Leaders in the IT testing discipline, such as Capers Jones, Bill Hefley, Robin Poston, Harry Sneed, to list a few." All names can be found on page 6. I fully understand it speaks much more about me than about ISTQB, and perhaps I am showing ignorance right now, but I have never heard about most of these people. List of surveyed "thought leaders" is missing many people who I would consider much more influential or relevant to topic at hand, starting with [Lisa Crispin](https://lisacrispin.com/) – who actually works in [company providing self-healing, AI-powered test automation tool](https://www.mabl.com/).

Customary for ISTQB, activities leading to formulation of vision is completely non-transparent. Who selected "thought leaders" and what was the key for selecting these specific people? Did they survey everyone they wanted, or did some people decline? When were interviews conducted, and how? What questions were asked, or what topics were covered during conversation? Did respondents answer independently? Could they revise their answers after reading answers from other people, or early version of report?

## Vision

If you haven't read original paper (and I can't blame you), here's the summary of vision. In future, there will be "testing technology solutions" which will somehow obtain all domain and expert knowledge that people have, and will use it to prepare testing plan that will answer "what?", "how?" and "why?". Before actually doing anything, these solutions will present that plan for acceptance by testing professional. At this stage, tester will be able to make changes to the plan. These changes, along with changes made in other solutions (existence of some global information exchange network for testing technology solutions is assumed), will serve as base for further learning and improvements of solutions. It's also stressed out that testing technology solutions will select quality attributes on their own, and will "teach" these attributes to human stakeholders.

Overall, that vision is something taken out of science-fiction movies from 1960s. Today, we are as close to fulfilling it as we were in 1960s.

### Conversing with computer

Vision calls for testers and testing experts to "join in dialog" with testing technology solutions. It's build on assumption that humans could have something resembling intelligent conversation with the machine.

I understand how for untrained eye it might look like we are close to creating systems capable of such feats. After all, we can already speak to machines. We can ask them to call hairdresser, and they can put scheduled visit in our calendars! But machines can't talk with receptionist on our behalf to book the visit, and they can't give opinion on which haircut would suit us best. And there is a world of difference in complexity of these tasks.

As a side note, presented vision is incoherent in that area. On one hand, testing technology solutions are supposed to learn from experts without people bending too much to machines, present information in clear, easy to understand way, and allow humans to introduce modifications and predict results of these modifications before committing to them. On the other hand, testing professionals are expected to greatly broaden their knowledge about these systems, mostly through time-consuming and costly formal education and certification schemes. I just can't see how we could have both of these at the same time.

### Global information exchange network

I love free software and open standards – I find idea of global network for information exchange between testing technology solutions very appealing. At the same time, it's painfully obvious for me that current machine learning revolution eludes established free software procedures.

Machine learning models need huge amounts of data, and that data is rarely shared in open way. Designers and maintainers of algorithms rarely give a second thought to their reproducibility - understood here as ability to bootstrap current revision of algorithm from first revision and initial set of data. Which is not surprising, given that these algorithms are closely guarded trade secrets, and re-building them from scratch is not something that anyone in company would ever need to do.

It's not clear why anybody would want to share data on this global network. After all, it only makes sense from business point of view to gain competitive edge by gathering data shared by others, but never revealing your own data. This is known as [free-rider problem](https://en.wikipedia.org/wiki/Free-rider_problem). The only realistic solution is strict policing, which requires for network to be neither global nor open.

Interestingly enough, there is ongoing discussion in open source/free software community on how you can prevent large actors from making huge profits while offloading all the costs to small group of creators. That problem is known as "open source sustainability" and the thing is, so far nobody really figured it out.

### Algorithm picking up its own performance metrics

According to ISTQB, testing technology solutions will be able to "learn the testing discipline" and "teach all stakeholders the quality attributes". In other words, future solutions will select their own tasks and performance metrics. I am speechless. Only someone who completely ignored everything that has been happening around artificial intelligence in last decade could say something like that.

End task is one of defining, if not the most important, property of machine learning algorithms. It says what algorithm is supposed to be doing. Maliciously defined task allows to lie and mislead, while maintaining facade of objectivity. Ill defined task results in algorithm inheriting and encoding negative phenomena, like racisms and other forms of discrimination. Undefined task makes it impossible to judge and check algorithm.

Performance metrics tell how well algorithm appears to be doing its job. They are one of primary defenses against overfitting – a situation where algorithm performs too well in laboratory, which most likely means it will perform poorly in real world setting.

Tasks and performance metrics are primary devices of controlling artificial intelligence. Giving them to machine means losing control over algorithms, and there is no way it could end up good. You might think *The Terminator*, but really look at [*Weapons of Math Destruction*](https://en.wikipedia.org/wiki/Weapons_of_Math_Destruction) for multiple examples of real, negative impact that machines have on us **right now**.

### Artificial intelligence ethics

As if somewhat aware of negative impact that artificial intelligence has on society, ISTQB decided to include statement about ethics. Unfortunately, they did so in completely unsatisfactory manner by hand-waving the whole issue:

> The ethical aspects of decision making by artificial intelligence (hopefully) will be resolved and this requires a level of  human intervention in the testing technology  solutions where ethical judgment is concerned.

Reflection on ethics is as old as humanity, and some of the greatest minds in history spent significant time trying to "solve" ethics (usually by trying to ground it in some unshakeable foundation, or derive it logically from first principles). And yet, we haven't progressed *that much* since Bible. Our tools, language and ways of thinking are much more sophisticated, but we aren't much closer to saying we are done than we were 2000 years ago. Ethics might as well be unsolvable, and expecting to have it solved in next couple of decades is not particularly reasonable.

### Explainable artificial intelligence

According to vision, machine itself will be able to explain various decisions it has taken. This is commendable goal. Many politicians, scientists and journalists expressed the need to go in that direction, and some very important work is being done to move us a little closer to fulfilling that goal.

But major problem is, biggest players on the market have very little incentive to prioritize explainability of their models. It's rather the opposite, they have reasons to ensure that nobody else understands inner workings of these models. After all, you can make some good money this way.

In fact, things are even worse than that. If reports from giants like Google and Facebook are to be trusted, these companies make it a point that their own employees working on these algorithms don't fully understand how their product will be used and who will it serve.

Fostering openness and transparency in such environment is not easy. Changes won't happen overnight and will require hard work and dedication of many actors, including governments. It seems community is just starting to realize we have a problem, time for solutions is yet to come.

## Preparation and Implementation

In section following the vision, ISTQB says that testers will have to gain "soft skills" such as decision-making, leadership, interpersonal communications, project management, and teamwork.

Formal education and certification schemes, including courses and certifications that do not exist yet, are presented as the best way of acquiring these skills. For a future where machines think and converse, you might consider these to be rather traditional, if not a little dated. Of course it's not very surprising in a paper coming from company whose main business **is** certification.

On a side note, one might wonder why ISTQB thinks testers don't have these skills already, or aren't actively working on acquiring them. "Quality coach" role is not exactly novel concept.

## Responsibilities of the Testing Professionals

Closing section, "Responsibilities of the Testing Professionals", is... surprisingly good! There isn't anything particularly silly, uninformed or controversial in these items.

I don't believe presented vision will be reality anytime soon. But in a world where it is realized, or will be realized soon, last section describes good and constructive attitude. In another time and place, I could support this part of paper.

## Summary

My biggest gripe with ISTQB paper is that it covers future that is never specified. That makes it hard to have any kind of discussion with their vision, as time frame governs argumentation that should be used.

For a short-term future (couple of years), paper is overly optimistic at best, helplessly incompetent at worst. While we can already see early attempts at systems similar to what they describe, there is enormous amount of work still required to fully realize such vision. I don't find it likely for this work to be completed in just couple of years, given that some actors are only starting to realize there is the problem, and others are actively pushing in other directions.

For a long-term future (couple of decades), vision is as good as any other going so far into the future. Some of predictions will never become reality, while other fields will advance beyond anything we could imagine today. What's not very clear is why ISTQB decided to write science-fiction story like that, and why they published it themselves instead of submitting to relevant magazine.

What's striking is complete misalignment of presented vision and everything that ISTQB created so far. It might even be argued that following current ISTQB teachings will actively hamper any efforts in realizing that vision. If there is one thing in the paper that should be taken seriously and worked upon right now, it's that certification industry must seriously review and update their education to face coming future. But that's lesson mainly for ISTQB, not so much for wider testing community.
