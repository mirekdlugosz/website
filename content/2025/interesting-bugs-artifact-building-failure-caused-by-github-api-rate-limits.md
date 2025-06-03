Title: Interesting bugs: Artifact building failure caused by GitHub API rate limits
Slug: interesting-bugs-artifact-building-failure-caused-by-github-api-rate-limits
Date: 2025-06-03 18:01:24
Category: Blog
Tags: Linux, case library, planet AST, planet MoT, planet Python, testing

This is a story of a memorable bug I encountered at work. As with every story of that kind, there are a few ways to look at it: it might save you some time if you encounter a similar issue; it surfaces the hidden work - work that is not visible when you only look at the output and artifacts; it demonstrates the benefits of broad knowledge. I'm sharing it as a contribution to testing [case library](https://commoncog.com/how-note-taking-can-help-you-become-an-expert/).

I was introducing a Jenkins pipeline to run for every pull request submitted to a project repository. One of the pipeline steps was to build a deployment artifact from the version of code with proposed changes. The artifact was a container image.

The application was following a standard architecture for web apps, with a separate backend and frontend communicating through an HTTP API. Each component had a separate repository hosted on GitHub and technically had an independent release policy that could result in version numbers that do not match. At the time, whole software was shipped as a single container image comprising both frontend and backend.

The container image was nominally a backend build artifact. One step in the container building procedure was to download the frontend files. The container build script recognized a special version "latest", which caused script to ask GitHub API for latest releases and extract version of the newest one.

Not long after the pipeline was introduced, the team noticed that jobs sometimes fail at the container building step. Logs indicated GitHub responded with [HTTP status 429 Too Many Requests](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429). This happens when GitHub thinks that the client is exceeding the API rate limits.

However, the team was small and at the most active days created no more than a few pull requests. Even at the very unlucky timing, the combined pipeline runs from all pull requests should create no more than a dozen or two API requests in an hour. GitHub claimed to allow up to 60 requests per hour and it seemed extremely unlikely that we would routinely exceed that.

It should be noted that nobody in the team reported any problems with building containers locally. Developers were doing that for months already, often multiple times a day.

No matter how unlikely it seemed that our pipeline generated more than 60 requests per hour, that's _some_ clue - and one that is cheap to verify. I created a spreadsheet with one column to store the date of pipeline run, and another column to indicate if an error occurred or not. Assuming that rate limiting is the root cause, we would expect failures when there are several runs in the same one-hour window. The earlier ones would succeed, and later ones would fail. Runs that are far removed in time from other runs should never fail. Of course, this pattern was not found in the data.

{% figure
    {attach}interesting-bugs-artifact-building-failure-caused-by-github-api-rate-limits/errors-tracking-spreadsheet.png |
    caption=Timestamps of pipeline runs and whether GitHub API responded with an error. Rows in green are consistent with the model of exceeding allotted API requests, rows in red are not consistent with the model. |
    display_caption
%}

The next step was to learn more about the GitHub API rate limits. When reading a documentation page on that topic, I learned there are multiple pools with different limits. 60 requests per hour is for unauthenticated users, grouped by IP address. Each authenticated user gets 5000 requests per hour.

At this point I need to share a bit of information about the wider infrastructure. This is subliminal context - something that you learn at some point when working in a company. It is not strictly related to your role and position, so it's not something that you would think about constantly; but it's a kind of background information you can draw from when thinking about issues that you face.

Jenkins controller was running inside a container deployed on OpenShift. Most of the work - including building deployment artifacts - was done on short-lived virtual machines provisioned on OpenStack. OpenShift and OpenStack operated from internal company network. The network was set up that outgoing connections to external world were allowed, but they all were routed through a limited number of proxy servers.

That allowed me to form a hypothesis - our pipeline is rate limited because from GitHub point of view, a sizable chunk of the company appears as a single IP address and is counted against a shared limit. It's unlikely for our Jenkins agents to generate over 60 requests during normal operation, but all the development teams sharing OpenStack resources? I can see _that_ happening.

This was not a research project, so I wasn't exactly interested in refuting or corroborating that hypothesis. It's enough that when stated like that, it provides clear steps towards solving the issue. If we authenticate our GitHub API requests, that should convince GitHub to count our requests against a different pool than the one shared with other OpenStack users. It will also increase our limit almost hundredfold, from 60 to 5000.

Requests may be authenticated by including a specific header with a token value. Token management, including ensuring they are not expired, is a separate topic I will not delve into here. In my case, the hardest part was working around the amount of layers that token value needs to be passed through. Jenkins created a virtual machine on OpenStack and provided GitHub API token value in environment variable. Pipeline at one point called `make build-container`, which is basically a shortcut for more extensive `podman build` command. `Containerfile` copied `Makefile` from backend project source directory to container build environment, and called `make fetch-ui` **there**. That in turn used `curl` to obtain data from the GitHub API. And this is where token needed to be used.

{% figure
    {attach}interesting-bugs-artifact-building-failure-caused-by-github-api-rate-limits/process-wrappers.png |
    caption=Illustration of number of wrappers around a command that actually connects with GitHub API servers. Some wrappers are skipped for brevity, like agent.jar executable. |
    display_caption
%}

Child processes in Linux by default inherit the environment from their parent, so the basic solution is to ensure a specific environment variable is set by Jenkins and all the layers below indeed recognize it. Two things complicate the picture here.

First, the container build environment drops most of the surrounding environment variables. This is in part to ensure consistent and reproducible build environment. Variables that you want to use when creating a container need to be explicitly opted in.

The second thing is worse. Environment variables present in the build stage end up embedded in the final container image. Setting an environment variable fundamentally shares a value with all the people who have access to the container image. When it comes to things like access tokens, this becomes an unacceptable security liability.

Luckily, the problem was identified in the last few years and the container build tools now support secret mounting. They are special files that are available to containers at the build stage, but are exempted from final container image. It means that at one point after creating a Jenkins agent virtual machine, but before issuing an API request, the environment variable content needs to be written to a file, and that file must be passed as a secret to container build environment.

The final touch was ensuring that everything still works when an environment variable with a GitHub token is not set. Developers never experienced the problem locally and they shouldn't be forced to maintain and set up a GitHub token in their own environment.

The final version of the solution I implemented at the time can be viewed in [GitHub PR](https://github.com/quipucords/quipucords/pull/2483).

After merging the PR, we no longer observed pipeline failures at the container image building step caused by GitHub API rate limits. It means that the proposed solution turned out to be correct.
