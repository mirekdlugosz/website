Title: Registering for TestingCup
Slug: registering-for-testingcup
Date: 2018-02-20 22:50:51
Category: Blog
Tags: community, testing

Yesterday, I tried to register for TestingCup competition and conference. Number of issues I have encountered is well outside of my comfort zone.

<!-- more -->

A little bit of context. There are only 250 places for competition, offered in first-come first-served system during three rounds of registration - on 22nd January, yesterday and on 19th March. Yesterday's ticket were all reserved in mere 5 minutes. If you want to participate, you have to act really quick.

*Get tickets* button became active at 9.59. When I clicked it, I saw this screen:

[![Login screen]({attach}testingcup-registration/Screenshot_20180220_095516-min.png)](
{attach}testingcup-registration/Screenshot_20180220_095516.png)

Well, OK. I have no problem with creating account. But they could have said it earlier, so I would be already logged in when tickets became available.

Not the one to be held back, I proceeded to create new account. Since I was in hurry, I entered rather simple password, something like "testingiscool". Turned out, passwords have to contain uppercase letter and number:

[![Password constraints]({attach}testingcup-registration/Screenshot_20180219_100745-min.png)](
{attach}testingcup-registration/Screenshot_20180219_100745.png)

OK, fine. I decided to generate new random password using password manager. It was something like `0uPcYJ=bIELZDZe_NFSh`.

[![Password constraints]({attach}testingcup-registration/Screenshot_20180219_100819-min.png)](
{attach}testingcup-registration/Screenshot_20180219_100819.png)

Nope. Only now I know that some special characters are forbidden. I made a mental note to look up password policy later on and generated new password, this time without any special characters. Third time's a charm.

After finally creating account, I had to create new participant for myself. That makes sense, as one person can register entire team, but it makes me wonder if I could have done it earlier. Either way, I reserved ticket for both competition and conference.

The next step is paying for ticket. You would think that is the easiest part, right? After all, they want my money. Well, no. I couldn't find bank account number in *Dashboard* or on *Payment Summary* page. I looked at conference contact page and in *Rules and Regulations*. While this last document did state that I am required to transfer money to bank account specified by organizers, it didn't reveal the number itself.

After some frenzied clicking, I have figured out that in order to proceed, I am supposed to provide my personal details using form on *Billing Data* page. This unlocks *Download pro forma invoice* button on *Payment summary* screen. Clicking this button downloads PDF that - among other things - contains bank account number.

So, I opened *Billing Data* page and… I froze. I did notice lack of HTTPS back when I registered account, but only now, when I am no longer in hurry, I can fully comprehend that.

**The entire website, including all the forms, is served through unencrypted connection!**

[![Invoice data form page is not secured](
{attach}testingcup-registration/Screenshot_20180220_100852-min.png)](
{attach}testingcup-registration/Screenshot_20180220_100852.png)

Yes, you have read it right. Organizers of high-profile software testing conference did not deploy TLS on their website. They did it these days, when popular browsers scream "unsecure!" on unencrypted websites. These days, when all browsers support SNI and you aren't limited to one certificate per IP. These days, when certificates are given away for free by Let's Encrypt. These days, when transferring sensitive personal information through insecure channel is violation of [GDPR](https://www.eugdpr.org/) and puts you at risk of paying hefty fine.

Since I have already stopped for a moment to reflect upon lack of HTTPS, I decided to look around more carefully and investigate some of the things that I didn't want to spend time on before.

Password policy. I couldn't find anything about it. There are some constraints placed on passwords, but you won't know until you try to violate them. This is very common practice, but in this particular case - when people are racing against the clock to reserve one of available places - each incorrectly submitted form might make a difference between getting a ticket or not. I would highly appreciate knowing about these constraints beforehand.

Actually, I would highly appreciate if I knew in advance that I need to create account at all. Again, this is quite common practice and a lot of online shops do that, so I could have expected that. But a lot of online shops merge "create account" and "shipping details" forms into one, or just let you place an order without any account at all, and I could have expected that as well. This might have been clearer if account wouldn't be called "participant" - for me, I am not participant until I actually participate (or, at the very least, buy the ticket). My way of thinking made me disregard *Participant zone* button early on, but I really shouldn't.

Finding organizer's bank account number is hard, as you already know. I can see how putting it in PDF could have made sense, if only each participant would have individual bank account number. But they don't. Account number on invoice is just main account number of company behind the event - one that they use since at least 2012. I fail to see a reason why they decided to create this convoluted process instead of just putting account number someplace where it is easy to find, like on *Payment Summary* page. Or even in dashboard.

TestingCup is trying to reach international audience and, for the first time ever, their website is in English. This is generally a good thing. However, time of registration opening - arguably the most important information on entire website at the moment - is expressed without timezone. You have to guess that they mean local Poland's time.

First image below shows page that was displayed when I was reserving my ticket (actually, there were four boxes - I had to get back to this page to take screenshot and there weren't any tickets available anymore). Second image shows page that was displayed when I clicked *Options* button on dashboard. They are basically the same form, so why do they use two different interfaces?
<div markdown="1" class="row">
<div class="col-md-6">
[![New participant - four boxes one by one](
{attach}testingcup-registration/Screenshot_20180219_100420-min.png)](
{attach}testingcup-registration/Screenshot_20180219_100420.png)
</div>
<div class="col-md-6">
[![Change option - two boxes and selection list?](
{attach}testingcup-registration/Screenshot_20180219_101107-min.png)](
{attach}testingcup-registration/Screenshot_20180219_101107.png)
</div>
</div>

## Bugs found

* Lack of HTTPS
* Bank account number is hard to find
* Time expression does not include timezone
* Lack of clear information about entire registration process and which steps might be complete in advance to save time
* Two different user interfaces for fundamentally the same screen (add participant vs. change participation option)
* Password constraints are revealed only when password violates them

**Takeaway**: Spend some time thinking about your assumptions. Try to lift them during testing and see what happens. A lot of problems I have encountered were product of someone assuming that it's obvious that things should be done certain way and never challenging that assumption.
