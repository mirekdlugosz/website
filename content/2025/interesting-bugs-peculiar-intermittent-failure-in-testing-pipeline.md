Title: Interesting bugs: peculiar intermittent failure in testing pipeline
Slug: interesting-bugs-peculiar-intermittent-failure-in-testing-pipeline
Date: 2025-03-26 19:22:30
Category: Blog
Tags: Linux, Python, case library, planet AST, planet MoT, planet Python, testing

Over the years I have encountered my share of memorable problems. They were remarkably complex, hard to debug, completely obvious in retrospect, or plain funny. This is the story of one of them.

At the beginning, there was a suite of automated tests that I was maintaining. One day one of them failed. Not a big deal, unfortunate reality is that some of them fail sometimes for various reasons. Usually they pass when run again and we can blame unreliable infrastructure, transient networking issue or misalignment of the stars. But few days later the same test failed again. And then again. It was clear that there's something going on and this particular test is intermittently failing. I had to figure out what is happening and how can I make the test provide the same result reliably.

(Note the choice of words here. My goal was not to make the test passing, or "green". There might as well have been a bug in the test itself, or in the product. At this point nobody knew. The main goal was understanding the issue and making sure test is reliably providing the same result - whether it is pass or fail.)

Before we move on, there's some relevant context that I need to share. That suite contained only UI tests. Running them all took about an hour. They were running against staging environment few times a day. The test that was failing was responsible for checking a chart which plots the data from last 30 days. There were other tests verifying other charts, sometimes using different time spans. The website used the same generic chart component in all cases. These other tests never failed.

On a high level, the failing test consisted of three main steps: request the data from last 30 days using the API, read the data from the graph on the website, and compare both. Test was considered failed if there was any difference between the data from these two sources. Python [deepdiff](https://github.com/seperman/deepdiff) package was used for comparison. To make it possible, data from API was locally transformed to mimic the structure returned by function responsible for reading the data from UI.

Testing infrastructure had few distinct pieces. There was a Jenkins server that triggered a test suite run at certain times of the day. Job executors were containers in a Kubernetes cluster. To facilitate UI testing, there was a Selenium Grid server with few workers hosted as virtual machines on OpenStack. Tests were running against staging environment of the product, which was also hosted on a Kubernetes cluster, but different than the one where job executors were. I believe all that was scattered across two data centers, with most of testing infrastructure being co-located, and product under test being elsewhere.

{% figure
    {attach}interesting-bugs-peculiar-intermittent-failure-in-testing-pipeline/infrastructure-diagram.png |
    caption=Not necessarily accurate illustration of infrastructure. |
    display_caption
%}

Now, let's get back to the story.

The very first thing I did was looking into test logs. Unfortunately, differences between objects as reported by deepdiff in this particular case are not easy to read (see below). The amount of data is overwhelming, and displaying everything in single line contributes to the challenge. The log made it clear that lists returned by API and read from UI are different, but it was not immediately obvious where exactly these differences are.

```output
>       assert not deepdiff.DeepDiff(expected_graph_data, actual_graph_data)
E       assert not {'values_changed': {"root[0]['Date']": {'new_value': '1970-01-01', 'old_value': '1970-01-02'}, "root[0]['Foo']": {'new_value': 46, 'old_value': 23}, "root[0]['Bar']": {'new_value': 60, 'old_value': 99}, "root[0]['Total']": {'new_value': 106, 'old_value': 122}, "root[1]['Date']": {'new_value': '1970-01-02', 'old_value': '1970-01-03'}, "root[1]['Foo']": {'new_value': 23, 'old_value': 26}, "root[1]['Bar']": {'new_value': 99, 'old_value': 92}, "root[1]['Total']": {'new_value': 122, 'old_value': 118}, "root[2]['Date']": {'new_value': '1970-01-03', 'old_value': '1970-01-04'}, "root[2]['Foo']": {'new_value': 26, 'old_value': 49}, "root[2]['Bar']": {'new_value': 92, 'old_value': 86}, "root[2]['Total']": {'new_value': 118, 'old_value': 135}, "root[3]['Date']": {'new_value': '1970-01-04', 'old_value': '1970-01-05'}, "root[3]['Foo']": {'new_value': 49, 'old_value': 68}, "root[3]['Bar']": {'new_value': 86, 'old_value': 60}, "root[3]['Total']": {'new_value': 135, 'old_value': 128}, "root[4]['Date']": {'new_value': '1970-01-05', 'old_value': '1970-01-06'}, "root[4]['Foo']": {'new_value': 68, 'old_value': 33}, "root[4]['Bar']": {'new_value': 60, 'old_value': 14}, "root[4]['Total']": {'new_value...ue': 25}, "root[24]['Bar']": {'new_value': 29, 'old_value': 78}, "root[24]['Total']": {'new_value': 106, 'old_value': 103}, "root[25]['Date']": {'new_value': '1970-01-26', 'old_value': '1970-01-27'}, "root[25]['Foo']": {'new_value': 25, 'old_value': 57}, "root[25]['Bar']": {'new_value': 78, 'old_value': 84}, "root[25]['Total']": {'new_value': 103, 'old_value': 141}, "root[26]['Date']": {'new_value': '1970-01-27', 'old_value': '1970-01-28'}, "root[26]['Foo']": {'new_value': 57, 'old_value': 48}, "root[26]['Bar']": {'new_value': 84, 'old_value': 18}, "root[26]['Total']": {'new_value': 141, 'old_value': 66}, "root[27]['Date']": {'new_value': '1970-01-28', 'old_value': '1970-01-29'}, "root[27]['Foo']": {'new_value': 48, 'old_value': 89}, "root[27]['Bar']": {'new_value': 18, 'old_value': 14}, "root[27]['Total']": {'new_value': 66, 'old_value': 103}, "root[28]['Date']": {'new_value': '1970-01-29', 'old_value': '1970-01-30'}, "root[28]['Foo']": {'new_value': 89, 'old_value': 61}, "root[28]['Bar']": {'new_value': 14, 'old_value': 66}, "root[28]['Total']": {'new_value': 103, 'old_value': 127}}, 'iterable_item_added': {'root[29]': {'Date': '1970-01-30', 'Foo': 61, 'Bar': 66, 'Total': 127}}}
```

Trying to understand this log felt daunting, so my next step was running the failing test locally, in isolation. Predictably, it passed. I didn't have the high hopes that I will be able to reproduce the problem right away, but that was a cheap thing to try, so I think it was worth giving a shot.

At this point I decided there is no way around it and I have to better understand how API and UI responses are different. I copied the log line into editor and inserted a new line character after each `},`. Few more changes later I had a form that was a little easier to decipher.

Deepdiff shows the differences between elements under the same index in lists. But focusing on elements with the same date value revealed that they are fundamentally the same. Values appearing under "old_value" in one list appears as "new_value" in the other list, just under different index. I have put colored overlay on the screenshot below to make it easier to see. You can think of these lists as mostly the same, but one is shifted when compared to other; or you can say that one list has extra element added at the end, while the other has extra element added at the very beginning. Specifically, API read data from January 2nd to February 1st, but UI displayed data from January 1st to January 31st. There's a large overlap, but deepdiff output obscured this key insight.

{% figure
    {attach}interesting-bugs-peculiar-intermittent-failure-in-testing-pipeline/more-readable-log.png |
    caption=Deepdiff output after editing. Color overlays shows that both lists have the same data, but in different places. |
    display_caption
%}

At this point I had an idea what is wrong, but I had no clue why, and why it would affect only this one single test. So in the next step I wanted to see if there are any patterns to the failure. I grabbed test results from last few weeks and put them in the spreadsheet. I added columns for basic things, like the result itself, how long did it take for test to finish, date and time when test was run. To make failing tests visually distinct, I added background color to highlight them. In separate column I tagged all rows where test was running for a first time in a given day. Then I added columns representing known issues that we encountered in previous few weeks, to see if all failures fall into one of them.

While there wasn't a clear and predictable pattern, I did notice a curious thing - **if** the test failed, it would fail in the first run of a given day. Subsequent runs of any day never failed. And the first run in a day always started shortly after midnight UTC.

{% figure
    {attach}interesting-bugs-peculiar-intermittent-failure-in-testing-pipeline/failures-spreadsheet.png |
    caption=Test results in a spreadsheet
%}

That allowed me to construct a working hypothesis: the issue is somehow related to time and there's only a short window when it may occur, maybe up to few hours. That window is located around midnight UTC. Such hypothesis explains why subsequent pipeline runs never failed, and why I was never successful at reproducing the issue locally - I am located east of UTC line and I would have to try running the test way outside of working hours. Of course I didn't know if I was up to something or I was just creating complex _ad hoc_ hypothesis that fits the data. But it directed my next step.

To corroborate the hypothesis I needed some new information, things I didn't have before. To gather it, I have added further logging in the test suite. First, I have used Selenium JavaScript execution capability to obtain the date and time as the browser "sees" it. Then I have done the same from Python, which both drives Selenium and requests data from API. The important part is that Python code is executed directly on test runner (container in Kubernetes) and JavaScript code is executed in the browser (Selenium Grid VM on OpenStack). 

```
diff --git package/tests/ui/test_failing.py package/tests/ui/test_failing.py
index 1234567..abcdef0 100644
--- package/tests/ui/test_failing.py
+++ package/tests/ui/test_failing.py
@@ -10,6 +10,13 @@ def test_failing_test(user_app, some_fixture):
     """
     view = navigate_to(user_app.some_app, "SomeViewName")
+    browser_time_string = view.browser.execute_script("return new Date().toTimeString()")
+    browser_utc_string = view.browser.execute_script("return new Date().toUTCString()")
+    view.logger.info(
+        "[JavaScript] Time right now: %s ; UTC time: %s",
+        browser_time_string,
+        browser_utc_string,
+    )
     expected_x_axis = get_xaxis_values()
     view.items.item_select(some_value)
     view.graph.wait_displayed()
diff --git package/utils/utils.py package/utils/utils.py
index 1234567..abcdef0 100644
--- package/utils/utils.py
+++ package/utils/utils.py
@@ -10,6 +10,14 @@ METRIC_MAP = {
 
 
 def _get_dates_range(some_param="Daily", date=None):
+    current_time = arrow.now()
+    log.info(
+        "[Python] Time right now: %s ; TZ name: %s ; TZ offset: %s ; UTC time: %s",
+        current_time,
+        current_time.strftime("%Z"),
+        current_time.strftime("%z"),
+        arrow.utcnow(),
+    )
     try:
         date = arrow.get(date)
     except TypeError:
```

With the above patch applied and deployed, all I needed to do was waiting for the next failure. I hoped that new logs would reveal some more information once it fails again.

That turned out to be true. JavaScript showed a date one day earlier than Python. In fact, the time in JavaScript was about 15 minutes earlier than in Python. So if test suite ran around midnight, and we got to offending test within 15 minutes of suite start, then Python would request data through API for some dates, but website in browser would think it is still the previous day, and request different set of dates. It means that the window where issue occurs is extremely small - just around 15 minutes each day.

```output
[JavaScript] Time right now: Thu Jan 01 1970 23:58:17 GMT+0000 (Coordinated Universal Time) ; UTC time: Thu, 01 Jan 1970 23:58:17GMT
[Python] Time right now: 1970-01-02T00:14:36.042473+00:00 ; TZ name: UTC ; TZ offset: +0000 ; UTC time: 1970-01-02T00:14:36.042473+00:00
```

This concludes the main part of the debugging story - at this point we knew what is wrong, we knew that failure is not caused by a bug in a test or a product, and it was clear that the solution is for all machines involved in testing to reconcile date and time. It also seemed like the JavaScript shows wrong date, which might mean that the issue is with Selenium Grid machines or OpenStack instance.

I connected to all Selenium Grid machines using SSH and checked their local time using `date` command. They were about 15 minutes behind their wall-clock time. I assumed the difference is caused by various OpenStack and underlying infrastructure maintenance work, so I just used `hwclock` to force OS clock to synchronize with hardware clock and moved on with my day.

Couple of days later I connected to these machines again and noticed that the local time is behind again, but only by about 15 seconds. It looked like the local clock is drifting by about 5 seconds a day. It might not sound like much, but it also meant that it's only a matter of time before original issue happens again. Clearly someone logging in to these machines every once in a while and resetting clock would not be a good long term solution - we needed something that can automatically keep time synchronized.

That something is called NTP and all the machines already had [chrony](https://chrony-project.org/) installed. However, it didn't seem to work correctly. While the commands succeeded and logs did not show any problems, the clock would just not change. After few frustrating hours I think I ruled out all possible causes at the operating system level and came to the conclusion that perhaps the NTP traffic to public servers is blocked by data center firewall. I reached out to OpenStack administrators for help and they told me that there is a blessed NTP server instance inside the data center that I should use. Once I configured chrony to use it as a source, everything finally worked.

This way browsers started to consistently report the same time as Python executors. That fixed the original issue and we did not observe any test failures caused by it again.

<!--
feedback questions:
- is this understandable? do you understand what the issue was and how it was solved?
- what feelings does it evoke? do you think "oh yeah, that's pretty cool thing, it would take me hours to do something like that" or "nah, this is obvious and mundane"?
-->
