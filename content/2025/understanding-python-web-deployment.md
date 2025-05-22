Title: Understanding Python web deployment
Slug: understanding-python-web-deployment
Date: 2025-05-22 18:48:09
Category: Blog
Tags: Linux, Python, planet AST, planet MoT, planet Python


Trying to deploy server-side Python web application may be overwhelming. Many tutorials will gladly tell you how to run it inside gunicorn, and how to put nginx in front of it, but they usually skim over details on **why** all this is needed. Why do you need both nginx and gunicorn? Why gunicorn and not Waitress or daphne? What is WhiteNoise and do you still need nginx if you have it? What even _is_ WSGI?

In this article I will share my mental model of distinct pieces and how they fit together. If I badly missed a mark somewhere, please [reach out and tell me how wrong I am]({filename}/pages/contact.md).

This is one of those topics that really benefits when you go through it in non-linear fashion. If you are here to learn, you might want to skim over headings and read sections in different order, or re-read selected sections out of order after reading the whole thing.

## The main model

Let's start with a high-level model of handling HTTP request.

{% figure
    {attach}understanding-python-web-deployment/main-model.png |
    alt_text=Overview of HTTP request/response cycle main model. There are three stages. The first stage is called Accepting, the second stage is called Translate and the third stage is called Process.
%}

That model follows the basic HTTP request/response cycle. Server passively waits for connections, which are initiated by clients. Client composes and sends a request. Server generates a response and sends it back, at which point connection is closed. If client decides it needs anything more, it sends new HTTP request.

The real world is complicated by HTTP/2, websockets and probably other things. HTTP/2 allows server to group multiple responses when addressing a single request. Websockets only start with HTTP request/response before switching to a completely different protocol. Some of these complexities will become relevant later.

## Accepting HTTP request

HTTP may seem simple. Client prepares a text message defining a request and sends it to a server. Server prepares a text message constituting a response and sends it back. This works well for text-based content, such as HTML, XML and JSON.

But there is so much more than that. The current iteration of HTTP standard has a separate document on caching alone, which is about 30 pages long. There are three different compression algorithms, each described in detail in separate documentation. There's an optional section about partial access to large resources. Then that whole thing may be wrapped in encrypted frames. HTTPS also involves special procedure for the initial handshake and a fair deal of cryptography. And on top of all that, you need to decide what to do with clients that do not conform to the specification.

Then, it's somewhat rare for a single physical machine to serve single domain (website). On one hand, one machine may serve multiple domains and there must be something that can decide how exactly a specific request directed at one of managed domains should be handled. On the other hand, modern web-based applications are usually distributed across multiple physical machines and there must be something that can choose a specific machine to handle particular incoming request. These days decision is often made based on the request content, analysis of recent traffic and knowledge of internal service infrastructure.

Unfortunately, the world out there is a dangerous place. Some invalid requests are actually malicious. What if client sends hundreds of thousands of requests? What if client opens a connection and never sends any data? What if client sends less data it claims it will? These sorts of questions do not come naturally from reading the specification alone, and answers have been hard won over the years.

As you can imagine, there's a lot of complexity, depth and lessons learned in last 30 years of HTTP usage. Most application developers don't want to deal with any of that - they would rather focus on simple request/response cycle and only dive deep into other areas as they are relevant to problems they face. They would happily outsource everything else to some other software.

That other software is usually called HTTP server, load balancer or router. Some popular programs in that problem space are [nginx](https://nginx.org/), [traefik](https://doc.traefik.io/traefik/) and [Kubernetes ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/).

It's worth noting that many web app hosting platforms that focus on ease of use have their own setup and do not give any choice in that matter. Part of value proposition of Heroku or Fly.io is that the first stage is taken care of by dedicated professionals, and you can jump straight into step two or even three.

## Translating between HTTP and programming language

Thanks to HTTP server, you have a sequence of bytes that constitute a valid HTTP request directed at your application. Your job is to produce a sequence of bytes that will constitute a valid HTTP response.

You _can_ write application that works on these primitives. [Python's built-in HTTP server](https://github.com/python/cpython/blob/main/Lib/http/server.py) is basically that. But for most application developers, this is too low level - they don't want to work with sequences of bytes, they want native objects and a library of helpers that make it easy to parse a request and construct a response. Reading and setting a cookie should take one line of code each.

Translating between a sequences of bytes and _some_ kind of internal programming language objects (and back from objects to sequence of bytes when processing a response) is the main goal of the second step in the main model. The name and specifics of the approach varies by a programming language. Usually that component is called "application server", "middleware" or "translation framework".

"Middleware" is overloaded term. The concept is also used in traefik, an HTTP server (step number 1), and Django, a Python web application development framework (step number 3). The world is a tangled web and depending on where you draw the lines and how much you are willing to squint, a lot of things are "in the middle" between some other things.

You can think of application server as a tool written in some programming language that helps developers working in that language to work with HTTP, by translating between byte sequences and programming language constructs. There are some exceptions, which I'll cover briefly near the end of article.

### Python - WSGI

In Python community, application servers usually are designed to run WSGI-compliant applications.

WSGI is an abstract specification, published as [PEP-333](https://peps.python.org/pep-0333/) and [PEP-3333](https://peps.python.org/pep-3333/). It's like a contract - for application server, it defines what it must provide to application, and what it should expect back. For application, it defines what it must provide back to application server, and what it should expect from it. The idea is that you should be able to run your application on any application server - and application server authors may write code once and support all applications. It's an example of adapter design pattern.

Popular application servers are [gunicorn](https://gunicorn.org/), [Waitress](https://docs.pylonsproject.org/projects/waitress/) and [bjoern](https://github.com/jonashaag/bjoern).

### Ruby - Rack

Rack is the main application server for Ruby web applications. These days it is both a concrete implementation of application server software, and _de facto_ specification of how Ruby applications should work with application servers. [unicorn](https://github.com/defunkt/unicorn) and [Puma](https://puma.io/) are independent projects capable of hosting "Rack applications".

### Java - Jakarta EE

Jakarta EE is a bit of overloaded term that may refer to either Jakarta EE software, or Jakarta EE specification. Jakarta EE software is concrete implementation of Jakarta EE specification. As far as I understand, the software was first and later the community formalized whatever it was doing into a specification.

So Jakarta EE software is a bit similar to Rack, as it's a specific software you can use which became a _de facto_ standard. Jakarta EE specification is a bit similar to WSGI, because it's just a document - the idea is that you should be able to use any application server with any application, as long as both are compliant with that document.

Most notable application servers are [Tomcat](https://tomcat.apache.org/) and [WildFly](https://www.wildfly.org/).

### Node.js - built-in

Node.js has HTTP server and helpers built in. That's because Node.js is built on top of a browser JavaScript engine, and JavaScript in a browser needs to deal with HTTP requests all the time. Node.js, as a _de facto_ JavaScript backend platform, already does the same thing as application server does for other languages.

### Rust - compiled-in

Rust does not provide HTTP helpers in standard library, and there is no generally accepted application server specification. Instead, there are multiple HTTP server libraries that solve many of the problems that your application is likely to deal with across the entire model. When you run application that uses one of these libraries, it binds to a socket and reads and writes byte sequences directly. At runtime, a single Rust application will effectively merge steps number 2 and 3 of the main model.

Popular libraries are [Actix Web](https://actix.rs/), [axum](https://github.com/tokio-rs/axum) and [Rocket](https://rocket.rs/).

## Adding value

At this point HTTP request is in the form suitable for a programming language. This is the step where majority of web application developers spend most of their time. Everything up to this point was a groundwork - things that had to be done, but it makes little difference how exactly they are done. Now we are getting close to the place that differentiates your application from all the other applications in the world.

In practice, many problems at this point are still shared and there is a room for outsourcing them. The objects and structures exposed to a programming language may still be relatively low level and a bit awkward to work with. Application likely needs to connect to one of popular database engines. A large part of application might be available to authenticated users, so there is a need for authentication framework. There are probably various levels of permissions and roles that users might have.

These problems are solved by frameworks or libraries. They differ mainly in how many of these problems they solve, and how opinionated they are in solutions they provide. Some popular frameworks are Django (Python), Flask (Python), FastAPI (Python), Quart (Python), Ruby on Rails (Ruby), Grape (Ruby), Spring (Java), Grails (Java), Apache Wicket (Java), Vaadin (Java), Apache Struts (Java), Meteor (JavaScript) or Next.js (JavaScript). In general, communities of most popular languages came up with at least one web application framework.

## Noteworthy exceptions and complications

### WSGI and ASGI

ASGI is another specification for Python. It serves the same role as WSGI.

Why two specifications? There are two main reasons. First, WSGI is written around HTTP request/response loop, and as such is unable to support newer protocols like websockets. Second, WSGI supports only synchronous functions, while asynchronous code is increasingly popular since it was introduced in Python 3.5. Some application developers concluded that performance gains they receive from asynchronous code is worth more for them than WSGI compatibility. ASGI was created in response to these needs.

From the main model perspective, WSGI and ASGI are functionally the same thing.

Practically speaking, gunicorn is go-to WSGI application server and uvicorn is go-to ASGI application server. Django is compatible with both WSGI and ASGI, while Flask users can easily move to Quart, developed by the same team. Some newer frameworks, like FastAPI, are exclusive to ASGI. There is also at least one application server capable of serving either WSGI or ASGI applications.

### WhiteNoise

[WhiteNoise](https://whitenoise.readthedocs.io) is a Python package for efficient static files serving. Static files are all files not generated dynamically by a Python program, such as stylesheets, frontend scripts, images and fonts.

It can act as a generic WSGI application wrapping around a target WSGI application. You can think of it as being somewhere between step number 2 and 3 of the main model. However, it also provides facilities to easily integrate with Django, and in such scenario it belongs firmly to step number 3.

The common knowledge of Python community is that static files should not be served by Python application, but instead should be handled by an HTTP server at the earlier stage of request/response cycle. WhiteNoise rejects that notion. It promises a high performance of serving static files while making sure they are correctly cached by CDN, proxies and client. It takes over one of responsibilities of an HTTP server.

Given all the things that HTTP server does, personally I would not be bold enough to skip it and open WhiteNoise-enabled application server directly to the world. But it might be worth considering in some special cases, like inside a container image or for internal company service.

### Phusion Passenger

[Phusion Passenger](https://www.phusionpassenger.com/) is application server notable for two main things. First, it's an example of application server written in different language that target application - Phusion Passenger is written in C++ and initially hosted only applications written in Ruby. Second, it's an example of application server compatible with multiple programming languages - newer versions can also host Python applications (compatible with WSGI) and Node.js applications.

### Granian

[Granian](https://github.com/emmett-framework/granian) is application server written in Rust, capable of hosting both WSGI and ASGI Python applications. It's notable because it's an example of application server written in different language than target application, but also because it's application server supporting both Python specifications.

### Spring Boot

Spring Boot supports multiple deployment models. It can be built into a package compatible with the Jakarta EE specification, intended to run on application server. But there is also an option to build it into standalone HTTP server application that directly responds to incoming HTTP requests. That option is similar to how HTTP servers are built in Rust.
