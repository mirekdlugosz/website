Title: Playing with Rust
Slug: playing-with-rust
Date: 2023-07-04 11:18:55
Category: Blog
Tags: Linux, planet AST, planet MoT, Rust


Recently I saw a post on LinkedIn with two samples of Python code, allegedly written by junior and senior programmers.
Both did the same thing - calculate a sum of numbers representing UTF-8 code points of characters in a string.
Setting aside that senior example was definitely not written by experienced Python programmer, I thought it's really contrived example, because how often do you need a sum of UTF-8 code points making up a string?
Later, I thought it _may_ be a part of problem that is more fun - given a number, is it a sum of numbers representing UTF-8 code points of characters in a valid English word?
I decided to use that as an opportunity to get some experience with Rust, a language I have never worked with.

Before we get to Rust, let's focus on a problem itself.
I have [already written about deciding whether string is a valid English word or not]({filename}../2016/how-to-use-r-to-recognize-if-given-string-is-a-word.md).
For the sake of this exercise, let's assume we can create a dictionary of all valid English words.
As long as we have it, we can solve our problem by answering a question: "is this number a sum of UTF-8 code points of characters of any word in a dictionary?".

This looks like a yes-no question, but there are three main cases to consider.
First, there might be no match - our number does not map to any word in a dictionary.
Second, there might be a single match.
Finally, there may be multiple matches.
For example, "lady", "rare", "five" and "nine" all have codepoints that sum to 426.

Trivia: there are almost 2000 sets of words with the same sum.
The pair of words that are still relatively common with the largest sum is "electrocardiographically" (ECG or EKG) and "electroencephalographies" (EEG), each summing up to 2544.

Then there's a question of user interface.
Should a dictionary be read from well-known place, or passed as input to the program?
Should program output boolean value (there is a word mapping to specified number / there isn't such word), or the word itself?
Should it stop at first match, or should it display all matching words?

Not willing to spend too much time on these questions, I decided that dictionary should be specified through mandatory command line argument, program should output all matching words and also signal search result through exit status (0 when words are found, 1 when there is no word mapping to specified number).
Optionally, user should be able to pass `-q` flag, which suppresses any output.
In this case, we are allowed to exit early on first match.

Now, let's move on to Rust.
The first thing I noticed is ease of setting up development environment - you just [download a single shell script and run it](https://rustup.rs/).
When it finishes, you will have compiler, standard library, package manager and code formatter available right at your fingertips.
If you decide to remove Rust from your system, just run a single command, or delete two directories.
Shell script is only responsible for detecting environment and downloading installer, so if you don't want to pipe random scripts to your shell, you can [manually download correct installer and verify cryptographic sum before executing it](https://rust-lang.github.io/rustup/installation/other.html).
Default installation also includes a tool to manage Rust versions, cross-compilation targets etc.
The only thing missing is LSP app for code editor, but it can be opted in with `-c rust-analyzer,rust-src`, or installed later.

Default package manager, `cargo`, is the main entry point for project management needs.
It can be used to create new project, setup build environment for downloaded project, or manage dependencies of project you are working on.
But it also wraps code formatter, linter, test runner and benchmarking tool.
This allows you to grab a random project and start hacking by using familiar commands.
I especially like `cargo run`, which builds the current project and runs it.
It's really good for basic "modify-build-run-verify" development loop.

During development, I have used "[The Rust Programming Language](https://doc.rust-lang.org/book/title-page.html)", also known as "Rust book".
It looks like pretty good introduction, covering all the fundamental ideas, but it's definitely meant as a tutorial that you follow from the beginning to the end.
Once I got hang of the very basics, I found myself jumping randomly between multiple chapters, looking for answers to specific questions I had.

I didn't like that book emphasizes quick and easy solutions, often without as much as a mention of other, usually better approaches.
One example is chapter about file reading, which only covers convenience function `fs::read_to_string`, but doesn't say anything about `io::BufReader`.

Another area where I found the book to be lacking is common conventions and idiomatic code.
Sometimes they are mentioned, but not always, and if you don't read cover-to-cover, you are sure to miss some.
Appendix grouping them all in one place, or maybe a reference to another book or resource, would be really helpful.
One of the questions that I had was: what should I do when my function could return different values, depending on arguments, while one value can be easily derived from another?
Should I put both on struct?
Should I return "stronger" and let caller transform it?
What if there are multiple callers with various needs?

Finally, I understand why the book focuses on standard library and doesn't cover crates (third-party packages).
But that makes some parts, like chapter about command line arguments, completely worthless.
In this case, you want to use [clap](https://docs.rs/clap/latest/clap/) almost every time.

All in all, my first contact with Rust was pretty enjoyable and I am looking forward to working with it more in the future.
My main concern at the moment is if I will find actual uses for it.

If you are interested in code I have written, you can [find it over at GitHub](https://github.com/mirekdlugosz/scrapbook/tree/main/ord_sum_to_word).
