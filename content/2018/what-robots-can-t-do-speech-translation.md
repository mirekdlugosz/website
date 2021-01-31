Title: What robots can't do: speech translation
Slug: what-robots-can-t-do-speech-translation
Date: 2018-02-02 22:42:57
Category: Blog
Tags: testing

In the middle of Polish international relations crisis, we can see why robots won't take our jobs anytime soon.

<!-- more -->

A week ago, lower house of Polish parliament passed the bill that penalizes claims that Polish People or the Polish state is (in part) responsible for Holocaust and other crimes committed by Third Reich on territory of Poland. That happened at very apt time, merely a day before International Holocaust Remembrance Day. It was met with very strong reaction from Israel and other countries, including USA. Now we have the worst international relations crisis since December 2017.

To calm the situation down, Polish prime minister Mateusz Morawiecki issued [a statement](https://www.youtube.com/watch?v=R9bS9z5OiWY) yesterday. In the speech, he said "Obozy w których wymordowano miliony Żydów nie były polskie", but English subtitles displayed at the same time read "Camps where millions of Jews were murdered were Polish". That is, subtitles omitted "not" between "were" and "Polish" and as a result read exactly the opposite of what prime minister said. Prime minister office [said on Twitter](https://twitter.com/PremierRP/status/959193834860220419) that translation was done automatically by YouTube. The video was then taken down.

Politics aside, let's take a closer look at this automated translation system.

I imagine that there are really two independent systems - speech recognition (responsible for translating audio into text) and natural language translator (translates text from one human language to another).

Both of them use machine learning algorithms, which basically means that they are told whether their output is right or not and use that information as input for future operations. The idea is that computer program "learns" where it makes mistakes and changes itself to not make these mistakes again. For machine learning to work, there needs to be some way of telling whether output was correct or not.

Speech recognition success might be measured by the number of words it caught (did not miss), by the number of words it translated correctly ("two" vs "too", "here" vs "hear" etc.) or by types of noises it can handle without effect on results. Natural language translator performance might be measured against the number of words it translated correctly, correct order of words in sentence, correct usage of grammar features of target language (e.g. inflection) or by idiomaticity of produced text. It goes without saying that there might be other performance metrics as well.

It's important to note that creators of machine learning algorithms don't expect them to be 100% correct. Their expectations vary depending on task at hand and fall anywhere between 99,99% and being correct more often than not. Only few would complain if their system features overall success rate of 90%-95%.

If we try to apply some of our performance metrics to YouTube automated translation machine, we will see that speech recognition system has success rate of 87.5% (missed only one out of eight words), but natural language translator has success rate of whopping 100% (it translated everything correctly). Taken as one, these systems has success rate of 93.75%. Assuming that missing "not" is the only mistake in entire translation of prime minister statement (I can't know), then speech recognition success rate goes up all the way to 99.8%!

Seen from quantitative metrics point of view, YouTube automated translation system is rather good. Some may claim that it's on its way to automate job of human translators. 

Except that no human translator would ever make such mistake.

**Takeaway**: Robots will take over jobs in near future - these where quality doesn't matter or is measured by quantitative metrics.

As a bonus point, let's apply Jerry Weinbergs Rule Of Three to this situation. For those unaware, Rule Of Three says that if you can’t think of three possible explanations of why something happened, you haven’t thought enough.

1. It was indeed problem with automated translation system.
2. Speech recognition system caught all words, but natural language translator knew that "death camps" are usually "Polish", so it corrected this mistake.
3. Malicious agent in prime minister office manually prepared incorrect subtitles.
4. Malicious agent on YouTube side changed subtitles to be incorrect.
5. This never happened. [Initial screenshot](https://twitter.com/BlazejPapiernik/status/959185720173834242) was faked. Not entirely sure why prime minister office would play along and why Google representative would apologize.
