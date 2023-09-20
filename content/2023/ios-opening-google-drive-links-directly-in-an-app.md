Title: iOS: Opening Google Drive links directly in an app
Slug: ios-opening-google-drive-links-directly-in-an-app
Date: 2023-09-20 23:48:24
Category: Blog
Tags: AST, planet AST, planet MoT, tutorial

In [AST](https://associationforsoftwaretesting.org/), we use Slack for internal communication and Google Drive for file sharing.
Since we are all volunteers, many people are active only in evenings.
And since there are many people in US, their evening might be well in the night for me.
So it happens that someone sends a link to Google Doc on Slack, I want to check it out, but I'm not in a mood to turn on my computer.

I use iPhone.
I have all Google apps installed and AST account logged in.
However, Slack can only open links in Safari or open Share Sheet, and Google apps did not register themselves in Share Sheet for whatever reason.
So there's no easy way to open a link directly in an app.

Luckily, there is a solution.

As [Apple StackExchange user points out, Google apps register secret protocols that can be used to open current page in a specific app](https://apple.stackexchange.com/a/227149).
I guess these are used by "Open this page in $APP" bars that appear on top of page in a browser? <!-- $ -->
Either way, if you have a link to Google doc, something like `https://docs.google.com/document/d/somerandomhashhere/edit`, you can prepend `Googledocs://` protocol and Safari will open Google Docs app automatically.
In other words, `https://docs.google.com/document/d/somerandomhashhere/edit` opens Safari, but `Googledocs://https://docs.google.com/document/d/somerandomhashhere/edit` opens the same document in Google Docs app.

Of course copying a link, opening Safari, typing secret protocol and pasting a link gets boring very fast.
This is where Apple Shortcuts come in.

If you didn't know, Shortcuts is built-in application that allows you to write scripts in something resembling [Scratch](https://scratch.mit.edu/).
Interface is rather clunky and debugging is a PITA, but Shortcuts has two things that make it stand out: it comes with built-in interfaces to most parts of the system, and it allows you to run custom programs on iOS device without thinking about Apple development ecosystem.

Here's a recipe for a shortcut I have created.
I won't explain precisely how to create a new one and where to click to modify it, as such instructions are at risk of getting outdated really quick.
See also a screenshot of how full shortcut looks on my phone, below.

1. Add "Receive input from" action. In first placeholder, I unchecked everything but "Safari web pages" and "URLs". In second placeholder, I checked "Show in Share Sheet". I also selected that if there's no input, it should "Get Clipboard".
2. Add "Get text from" action. I have "Shortcut Input" selected here. I'm actually not 100% sure if this action is even needed. Maybe it just passes data verbatim to the next step.
3. Add "Combine with" action. In first placeholder, I have "Text", which is a text from previous step. In second placeholder, I selected "Custom" and then typed "Googledocs://". I _feel_ I should be able to just concatenate two text streams, but I haven't found more straightforward way of doing this.
4. Add "Open URLs" action. As only placeholder I have selected "Combined Text", which is result of previous action.

{% figure
    {attach}ios-opening-google-drive-links-directly-in-an-app/shortcut-recipe.png |
    caption=Shortcut recipe for opening link directly in Google app
%}

When you click a name on top, you can change the shortcut name and icon.
There are no Google apps icons and only few predefined colors are available, but you can make up something that looks close enough to Google branding.

As far as I can tell, you can send Google Slides link to Google Docs app and it will still do the right thing.
So you probably don't need more than single generic "Open in Google app" shortcut.
But if it ever stops working like that, or you like selecting apps explicitly, you may duplicate your new shortcut and create new ones for Google Sheets, Google Slides and Google Drive (for links to directories).
For reference, here's a list of protocols that they use:

* `Googledocs://` - Google Docs (text documents)
* `Googlesheets://` - Google Sheets (spreadsheets)
* `Googleslides://` - Google Slides (presentations)
* `Googledrive://` - Google Drive (folders, directories)

Now whenever someone sends a link to Google drive on Slack, I can long-press it, select "Share..." and pick one of my shortcuts from near the bottom.
This automatically opens a document in specified Google app.
