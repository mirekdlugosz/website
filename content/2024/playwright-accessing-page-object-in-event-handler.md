Title: Playwright - accessing <code>page</code> object in event handler
Slug: playwright-accessing-page-object-in-event-handler
Date: 2024-01-03 18:37:03
Category: Blog
Tags: planet AST, planet MoT, planet Python, Python, testing, tutorial

Playwright [exposes a number of browser events](https://playwright.dev/python/docs/api/class-page#events) and provides a mechanism to respond to them. Since many of these events signal errors and problems, most of the time you want to log them, halt program execution, or ignore and move on. Logging is also shown in [Playwright documentation about network](https://playwright.dev/python/docs/network#network-events), which I will use as a base for examples in this article.

## Problem statement

Documentation shows event handlers created with `lambda` expressions, but `lambda` poses significant problems once you leave the territory of toy examples:

- they should fit in single line of code
- you can't share them across modules
- you can't unit test them in isolation

Usually you want to define event handlers as normal functions. But when you attempt that, you might run into another problem - Playwright invokes event handler with some event-related data, that data does not contain any reference back to `page` object, and `page` object might contain some important contextual information.

In other words, we would like to do something similar to code below. Note that this example does not work - if you run it, you will get `NameError: name 'page' is not defined`. 

```python
from playwright.sync_api import sync_playwright
from playwright.sync_api import Playwright


def request_handler(request):
    print(f"{page.url} issued request: {request.method} {request.url}")


def response_handler(response):
    print(f"{page.url} received response: {response.status} {response.url}")


def run_test(playwright: Playwright):
    browser = playwright.chromium.launch()
    page = browser.new_page()
    page.goto("https://mirekdlugosz.com")

    page.on("request", request_handler)
    page.on("response", response_handler)

    page.goto("https://httpbin.org/status/404")

    browser.close()


with sync_playwright() as playwright:
    run_test(playwright)
```

I can think of three ways of solving that: by defining a function inside a function, with `functools.partial`and with a factory function. Let's take a look at all of them.

## Defining a function inside a function

Most Python users are so used to defining functions at the top level of module or inside a class (we call these "methods") that they might consider function definitions to be somewhat special. In fact, some other programming languages do encumber where functions can be defined. But in Python you can define them anywhere, including inside other functions.

```python
from playwright.sync_api import sync_playwright
from playwright.sync_api import Playwright


def run_test(playwright: Playwright):
    def request_handler(request):
        print(f"{page.url} issued request: {request.method} {request.url}")


    def response_handler(response):
        print(f"{page.url} received response: {response.status} {response.url}")


    browser = playwright.chromium.launch()
    page = browser.new_page()
    page.goto("https://mirekdlugosz.com")

    page.on("request", request_handler)
    page.on("response", response_handler)

    page.goto("https://httpbin.org/status/404")

    browser.close()


with sync_playwright() as playwright:
    run_test(playwright)
```

This works because [function body is not evaluated until function is called](https://docs.python.org/3/reference/compound_stmts.html#function-definitions) and [functions have access to names defined in their encompassing scope](https://peps.python.org/pep-0227/). So Python will look up `page` only when event handler is invoked by Playwright; since it's not defined in function itself, Python will look for it in the function where event handler was defined (and then next function, if there is one, then module and eventually builtins).

I think this solution solves the most important part of the problem - it allows to write event handlers that span multiple lines. Technically it is also possible to share these handlers across modules, but you won't see that often. They can't be unit tested in isolation, as they depend on their parent function.

## `functools.partial`

[`functools.partial` documentation](https://docs.python.org/3/library/functools.html#functools.partial) may be confusing, as prose sounds exactly like a description of standard function, code equivalent assumes pretty good understanding of Python internals, and provided example seems completely unnecessary.

I think about `partial` this way: it creates a function that has some of the arguments already filled in.

To be fair, `partial` is rarely _needed_. It allows to write shorter code, as you don't have to repeat the same arguments over and over again. It may also allow you to provide saner library API - you can define single generic and flexible function with a lot of arguments, and few helper functions intended for external use, each with a small number of arguments.

But it's invaluable when you have to provide your own function, but you don't have control over arguments it will receive. Which is _exactly_ the problem we are facing.

```python
from functools import partial

from playwright.sync_api import sync_playwright
from playwright.sync_api import Playwright


def request_handler(request, page=None):
    print(f"{page.url} issued request: {request.method} {request.url}")


def response_handler(response, page=None):
    print(f"{page.url} received response: {response.status} {response.url}")


def run_test(playwright: Playwright):
    browser = playwright.chromium.launch()
    page = browser.new_page()
    page.goto("https://mirekdlugosz.com")

    local_request_handler = partial(request_handler, page=page)
    local_response_handler = partial(response_handler, page=page)

    page.on("request", local_request_handler)
    page.on("response", local_response_handler)

    page.goto("https://httpbin.org/status/404")

    browser.close()


with sync_playwright() as playwright:
    run_test(playwright)
```

Notice that our function takes the same arguments as Playwright event handler, and then some. When it's time to assign event handlers, we use `partial` to create a new function, one that only needs argument that we will receive from Playwright - the other one is already filled in. But when function is executed, it will receive both arguments.

## Factory function

Functions in Python may not only define other functions in their bodies, but also return functions. They are called "higher-order functions" and aren't used often, with one notable exception of [decorators](https://realpython.com/primer-on-python-decorators/).

```python
from playwright.sync_api import sync_playwright
from playwright.sync_api import Playwright


def request_handler_factory(page):
    def inner(request):
        print(f"{page.url} issued request: {request.method} {request.url}")
    return inner


def response_handler_factory(page):
    def inner(response):
        print(f"{page.url} received response: {response.status} {response.url}")
    return inner


def run_test(playwright: Playwright):
    browser = playwright.chromium.launch()
    page = browser.new_page()
    page.goto("https://mirekdlugosz.com")

    page.on("request", request_handler_factory(page))
    page.on("response", response_handler_factory(page))

    page.goto("https://httpbin.org/status/404")

    browser.close()


with sync_playwright() as playwright:
    run_test(playwright)
```

The key here is that inner function has access to all of enclosing scope, including values passed as arguments to outer function. This allows us to pass specific values that are only available in the place where outer function is called.

## Summary

The first solution is a little different than other two, because it does not solve all of the problems set forth. On the other hand, I think it's the easiest to understand - even beginner Python programmers should intuitively grasp what is happening and why. 

In my experience higher-order functions takes some getting used to, while `partial` is not well-known and may be confusing at first. But they do solve our problem completely.
