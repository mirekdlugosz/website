Title: Practicing the Rule of Three: Polish SAF-T
Slug: practicing-the-rule-of-three-polish-saf-t
Date: 2018-02-26 19:16:46
Category: Blog
Tags: application, testing

Testerzy.pl, one of the biggest websites for testers in Poland, published [short article](http://testerzy.pl/wiesci-ze-swiata-testerow/krytyczna-funkcja-sprawozdawcza-jpk-niedotestowana) about problems with system behind [SAF-T](https://en.wikipedia.org/wiki/SAF-T). It's in Polish, but Google Translate does not-terrible job at translating it to English. The bottom line is: application does not allow to input numbers with more than two significant digits. Testerzy.pl claim that system was "not tested enough".

<!-- more -->

I was not involved in the project in question and I cannot comment whether it was tested enough or not (and it's not exactly clear to me what "tested enough" is supposed to mean, but I digress). However, I can think of some other reasons why software could be released with problem like that.

* Specification explicitly said that numeric values must be expressed in format with two significant digits. Maybe someone brought this to attention of specification-makers, maybe not.
* Development process made it very hard to fix bugs in specification, while requiring software to conform to said specification (even when it was buggy).
* Information about the issue never left testing team. Maybe their priorities at the time didn't justify spending time on reporting it. Maybe their process made each reported problem such a hassle, that testers equivocated. Maybe someone found it just before lunch break and then forgot.
* None of decision-makers looked into reported issue. It still lingered in NEW queue at the time of release.
* Issue was reported and then closed as too minor to be worth any further work.
* After investigation by development team, it turned out that fix would require refactoring of significant part of application. Someone decided that benefits of fix do not outweigh potential costs.
* Problem was fixed, but then it was re-introduced sometime before the release. That could happen while fixing another issue in related part of application, or maybe they didn't have proper version control system set up.
* Fix was deferred until future release.

I'm sure you can come up with more reasons if you think about it for more than 10 minutes.

This is somewhat interesting case that gives us opportunity to discuss and reflect on role of testers, relationships between specification, needs and values, factors impacting business decisions and host of other topics related to software development. I find it very unfortunate that one of the poster-children of testing in Poland decided to reduce all these topics to only one word, and out of all the words, they have chosen one that suggests that testers did not do their job properly.

**Takeaway**: testers are messengers. They can't take responsibility for decisions that were made by other people based on messages that they brought.
