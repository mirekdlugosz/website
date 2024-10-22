Title: "Software Testing Strategies" by Heusser and Larsen - review
Slug: software-testing-strategies-by-heusser-and-larsen-review
Date: 2024-10-22 19:54:29
Category: Blog
Tags: planet AST, planet MoT, testing


This is the review of a book "Software Testing Strategies. A testing guide for the 2020s" by Matthew Heusser and Michael Larsen. The book was published in December 2023 by Packt. You can buy the ebook or printed copy directly from the publisher, at Amazon and perhaps a number of other places.

I admit I was a bit on the fence since I first heard about the book. The title sounds very promising and I know authors were involved in [AST](https://associationforsoftwaretesting.org/) and context-driven testing. But the price seems a bit high in this part of the world. Eventually I took the plunge and bought a copy in March. I finished reading after 5 or 6 weeks. I wrote this review in April.

## Things that I liked

The book is full of stories, examples and experience reports. You can easily tell that authors have actual experience with things that they talk about. This is a welcome change from a number of books and blog posts that are superficial and read as if authors had only theoretical knowledge of a thing they cover, if any. Overall, that makes for an easier reading and adds credibility. I especially appreciate that authors did not shy away from talking about their mistakes, blunders and errors. Too many experience reports are vanity in disguise.

Case studies in chapter 12 are wonderful. Testing community needs so much more of these. I dream that one day we might have a testing-focused [case library](https://commoncog.com/how-note-taking-can-help-you-become-an-expert/). I hope to write about this more in the future, and I would be more than happy to join a group that is working towards that goal. But until these dreams and hopes come true, chapter 12 is one of the closest things available to international audience.

There were things I have learned. Pairwise testing sounds like something I should have known, but somehow I missed it so far. Model-driven testing is something I encountered recently, but it was called by a different name. It also has a surprising connection to high-volume automation I have implemented in one of the projects.

I found it thought-provoking to introduce two new schools when discussing the schools of testing in chapter 15 - "The Agile school" and "The DevOps or CD school". The idea of testing schools themselves is a bit dated, caused a lot of controversy at the time and is now largely rejected by the community. So I'm not sure if it's a good thing to include it in the book, but I do appreciate the effort to modernize it.

I really enjoyed the description of testing work in the very first chapter. It did an excellent job at capturing the thrill of exploration and the joy of learning something new. Even though I am fortunate enough to enjoy these feelings most of the time at my daily job, I still found that part inspiring. It has this rare and precious effect that it makes you want to put the book down and go test something.

## Things I did not like

I don't think the title suits the content well. I have expected something similar to "Design Patterns" by the Gang of Four - a list of established and emerging strategies, each with a description, probably an example, and a summary that says when a strategy can be applied beneficially, and when it's better avoided. This book is not that.

The book is all over the place. It touches a huge number of topics, but dives deep into only a handful of them. Sometimes it's hard to understand why certain things were included and how they relate to everything else. This makes it challenging to decide which topics are worth studying more and which can be ignored for now.

It's unclear to me what level of experience is the reader assumed to have. For example, hexagonal architecture is introduced as early as chapter 3. But this is relatively advanced topic from software architecture area - something that most testers don't really encounter, and developers start to think about as they prepare to move to a senior role, or later. The way it's being described might make you think this is how most software looks like internally, which could not be further from truth.

The choice of software covered is baffling at times. Chapter 5 mentions couple of continuous integration systems. Somehow CircleCI and Travis CI were included, but GitHub Actions was not. The same chapter recommends Apache OpenOffice, which at this point of time is straight negligence. Apache OpenOffice is abandonware that barely manages to release a few bugfixes once a year or so. All the community has moved on to [LibreOffice](https://libreoffice.org), which sees 2 major releases every year and monthly bugfix releases. If you want to recommend free and open source office suite, LibreOffice is the only one in town.

There are occasional mistakes and typos in the text. Duplicated word in one place, sentence beginning by lowercase letter in another. These are mostly negligible. The one exception is in the chapter 13: "division by zero and interpreted code crashes tend to show up as 400 errors". I think this is a typo, but one that novices will not catch and instead learn the wrong thing. 400 errors are client-side errors; division by zero and crashes in interpreted code are most likely going to show up as 500 errors, server-side problems. I don't really blame the authors for this and other mistakes, but it's clear that the editor assigned by the publisher could do a better job. That's unfortunate.

## Conclusion

I want to like this book. I really do. But I am clearly not a target audience. So I'm thinking: to whom could I recommend it?

I think this might be a good book for someone early in their career, probably someone with 6 months up to a few years of experience. To readers with less experience I would recommend "Perfect Software" by Jerry Weinberg instead. More experienced folks might find "Lessons Learned in Software Testing" by Kaner, Bach and Pettichord to be more valuable. But there is a sweet spot between these two prominent works that this book seems to fill.

Perhaps this book can also help people who have been in testing for a very long time, settled a bit, feel they no longer keep up with the Joneses and want to change that. They won't learn ins and outs of everything in the current landscape of software development, but will get the useful overview. They will encounter all the most important ideas, and some buzzwords too.

That might be a bit of a stretch, but I guess this can also be an alright book for people who consider a career in IT, and are looking for single book that would give them the general overview of how the work looks like today. Ironically, these people might want to skip some of the parts that discuss testing in depth.
