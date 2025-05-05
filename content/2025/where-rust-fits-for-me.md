Title: Where Rust fits for me
Slug: where-rust-fits-for-me
Date: 2025-05-05 17:45:36
Category: Blog
Tags: Rust, planet AST, planet MoT, projects


I started eyeing Rust around mid-2023. My first program taught me it's not a language you can just learn on the job - you have to spend some time on fundamentals or you are going to have a really bad time. I did my part in early 2024 - I have read The Rust Book, went through [Rust By Practice](https://practice.course.rs/) and [rustlings](https://rustlings.cool/). Then I was looking for reasons to keep learning Rust, aside from the fun of it, potential job security and getting to understand programming at the deeper level.

Current Rust toolchain creates statically-linked binaries that can be run without any special runtime. That binary file is everything that you need to run a program on a specific CPU architecture and specific operating system. It's forward compatible and very likely to continue to just work in years to come. I explored that bit in [an article about binaries stability]({filename}/2024/rust-binaries-stability.md).

When you put things this way, Rust is almost the exact opposite of Python. Rust produces single binary, while Python programs tend to consist of multiple files. Rust does not need runtime environment, while Python not only needs Python binary, but also a virtual environment to store all the dependencies. And while Python as a language is stable and takes backwards compatibility seriously, the entire ecosystem is notorious to suffer from bit rot. You can't take a random Python program from 2018 and assume everything will just work after `pip install -r requirements.txt`. It might, but that's very hit and miss.

That makes Rust a very good choice for things that I expect to run in the future and I want them to just work then. Weeks or months might pass between invocations, but when the time comes, I want as little friction as possible. I want to run the thing, not to deal with uninstallable dependency. At the same time, the problem must be defined well enough that I can expect to want exact same solution in years to come.

That's why I have chosen Rust for my [ebook file renamer](https://github.com/mirekdlugosz/ebook-name-from-metadata) and [a tool to generate text from template file](https://github.com/mirekdlugosz/scrapbook/tree/main/gen-from-template-rs).

These days, when I encounter a task to automate and I think about best programming language to use, I tend to favor three choices.

**Shell**. It's really only good for setting up environment variables needed by other tools and occasional throwaway loop. I don't bother with Bourne Shell compatibility any more, unless I have a strong reason to. I draw the line at functions - if I need functions, I'll reach for something else.

**Python**. This is very much my default choice, as this is the language I am most comfortable in. However, backwards compatibility of ecosystem and bootstrapping the environment are major concerns. It's a natural choice if I can get away with just a standard library or I can be sure all the required packages are already there in the system, usually pulled in by some system-wide programs installed through standard operating system packages. It's also a good choice for one-off and _ad hoc_ programs that I don't expect to run in the future. Finally, it might be a good choice for programs that I work on regularly, like at least once a month - this way ecosystem problems don't pile up and can be dealt with one at a time.

**Rust**. Kind of fallback for cases that don't fit well in scenarios described above. Forward-compatible statically linked binary is a good choice for situations where I want a frictionless execution of a program in the future. It works best where problem is small enough to prepare a complete solution in couple of days.
