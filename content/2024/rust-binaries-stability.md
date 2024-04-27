Title: Rust binaries stability
Slug: rust-binaries-stability
Date: 2024-04-27 22:21:27
Category: Blog
Tags: Linux, Rust, planet AST, planet MoT


Recently, I've been thinking about Rust stability. Most web search results are discussing stability of the language itself, especially in the context of taking old Rust code and compiling it with recent toolchain. This is obviously important, but not the kind of stability that I had in mind. What I wanted to know is: "can I take my old Rust executable and use it on recent Linux?"

When I publish this post, Rust toolchain is at version 1.77.2. Rust itself was created in 2006, made publicly available in 2010 and saw first stable release (1.0) in 2015. Obviously I am not interested in anything built before 2015 - you can't take bleeding-edge programming language and expect stability. Also, it's not like I would be using toolchain that old today.

Skimming through the documentation, it's easy to notice nightly APIs that you have to explicitly opt-in to use. While I heard some of them remain in unchanged form for years, it's clear to me that you can't expect stability when you use API marked as not stable.

The typical Rust program will compile to mostly statically linked binary, with GNU libc linked dynamically. This is not the full story, as you can use musl instead, which also supports static linking, and apparently it is possible to avoid any C library if you try really hard. I am not really interested in these cases, especially since they seem to target somewhat special needs, including embedded systems.

For a typical Rust binary, the long-term stability will depend on two components that are not part of Rust at all: kernel and glibc. Linux takes long-term stability very seriously and is well known for not breaking the user space, so it's not really a concern.

I don't know much about GNU libc, but I found [the article discussing techniques employed to ensure backwards compatibility](https://developers.redhat.com/blog/2019/08/01/how-the-gnu-c-library-handles-backward-compatibility). This gives me some confidence that they take long-term stability similarly to Linux. When I think about this, about the only case of glibc breaking backwards compatibility I heard of is [related to anti-cheat software used by games](https://github.com/ValveSoftware/Proton/issues/6051), and as far as I understand, this was dubious from the very beginning.

It all indicates that Rust executables should be pretty stable. But as a tester, I know experience beats the theory every time. And I already _have_ a modern Linux, so if only I could find some old Rust executables, I could see for myself if they still work or not.

This is easy enough to do with GitHub search. I searched for projects written in Rust that were created before 2018. There's nothing special about 2018 - it's just a label for "old". Then for every project it found I checked if that's an application (and not a library or documentation), if it does releases through GitHub, and what is the oldest release with binary files attached. I repeated that until I decided I have enough. I'm not trying to be thorough, I want to find an answer in less than an hour.

I don't have any reason to assume these applications are malicious, but since these are random executables from the Internet, I wanted to separate them from the rest of the system. Podman helped me with that. I have used `fedora:38` image, only because my host is Fedora 38, and I assumed this way I should minimize potential compatibility problems, if any.

I don't really know how to use these programs, and it was not my goal to learn. I just tried to run each executable with `--help` and `--version` flags, hoping they are recognized. I expected to see _something_ if program still works, and get obvious error message if it does not.

Out of 9 projects tested, 8 appear to still work. The oldest one was from September 2016. The table below shows detailed results. Name of the application is link to the specific version that I tested.

|                               Application                                             | Version  |    Date    |  Works  |
|---------------------------------------------------------------------------------------|----------|------------|:-------:|
| [ripgrep](https://github.com/BurntSushi/ripgrep/releases/tag/0.0.2)                   | 0.0.2    | 2016-09-06 | ✅ <span class="sr-only">Yes</span> |
| [watchexec](https://github.com/watchexec/watchexec/releases/tag/1.0.0)                | 1.0.0    | 2016-10-15 | ✅<span class="sr-only">Yes</span> |
| [rip](https://github.com/nivekuil/rip/releases/tag/0.8.3)                             | 0.8.3    | 2016-10-18 | ✅<span class="sr-only">Yes</span> |
| [just](https://github.com/casey/just/releases/tag/v0.2.23)                            | v0.2.23  | 2016-11-24 | ✅<span class="sr-only">Yes</span> |
| [wstunnel](https://github.com/erebe/wstunnel/releases/tag/1.0)                        | 1.0      | 2017-12-07 | ✅<span class="sr-only">Yes</span> |
| [Firecracker](https://github.com/firecracker-microvm/firecracker/releases/tag/v0.1.0) | v.0.1.0  | 2018-03-05 | ✅ / ❌<span class="sr-only">It's complicated</span> |
| [RustScan](https://github.com/RustScan/RustScan/releases/tag/1.0.1)                   | 1.0.1    | 2020-07-19 | ✅ / ❌<span class="sr-only">It's complicated</span> |
| [cicada](https://github.com/mitnk/cicada/releases/tag/v0.9.29)                        | v0.9.29  | 2022-02-24 | ✅<span class="sr-only">Yes</span> |
| [swc](https://github.com/swc-project/swc/releases/tag/v1.2.24)                        | v1.2.24  | 2020-09-08 | ❌<span class="sr-only">No</span> |
| [swc](https://github.com/swc-project/swc/releases/tag/v1.3.105)                       | v1.3.105 | 2024-01-21 | ✅<span class="sr-only">Yes</span> |

I count Firecracker and RustScan as working, but they deserve a bit of explanation. They both showed errors on Fedora, but appear to work on Debian. Errors were "failed to initialize syslog: InvalidFd" (Firecracker) and "./rustscan: cannot execute: required file not found" (RustScan). For me they sound like missing runtime dependencies, and I consider them fundamentally the same as forgetting to specify a mandatory positional argument. But they also show something I did not consider initially - that long term stability might depend on Linux distribution as well.

On the other hand, I count swc as the only one that is not working. That's because the oldest version, v1.2.24, crashed with a segmentation fault. That was also a case for three later versions I have tried. The first version that appears to work is v1.3.105, released earlier this year. I don't know what this application is doing, but it seems to be something unusual.

To sum up: if you search the web trying to learn if Rust executables are stable in the long term, then the answer seems to be "yes".
