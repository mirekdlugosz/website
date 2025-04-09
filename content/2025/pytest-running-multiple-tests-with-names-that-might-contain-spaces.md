Title: pytest: running multiple tests with names that might contain spaces
Slug: pytest-running-multiple-tests-with-names-that-might-contain-spaces
Date: 2025-04-09 20:28:38
Category: Blog
Tags: Linux, planet AST, planet MoT, planet Python, testing, tutorial

You most certainly know that you can run a single test in entire suite by passing the full path:

```bash
PRODUCT_ENV='stage' pytest -v --critical tests/test_mod.py::test_func[x1]
```

This gets old when you want to run around 3 or more tests. In that case, you might end up putting paths into a file and passing this file content as command arguments. You probably know that, too:

```bash
PRODUCT_ENV='stage' pytest -v --critical $(< /tmp/ci-failures.txt)
```

However, this will fail if your test has space in the name (probably as pytest parameter value). Shell still performs command arguments splitting on space.

To avoid this problem, use `cat` and `xargs`:

```bash
cat /tmp/ci-failures.txt |PRODUCT_ENV='stage' xargs -n 200 -d '\n' pytest -v --critical
```

I always thought that xargs runs the command for each line from stdin, so I would avoid it when command takes a long time to start. But turns out, xargs is a little more sophisticated - it can group input lines into subclasses and run a command once for each subclass.

`-n 200` tells xargs to use no more than 200 items in subclass, effectively forcing it to run pytest command once. `-d '\n'` tells it to only delimit arguments on newline, removing any special meaning from space.

`PRODUCT_ENV` and any other environment variables must be set after the pipe character, or exported beforehand, because each part of shell pipeline is run in a separate subshell.

After writing this article, I learned that since pytest 8.2 (released in April 2024), you can achieve the same by asking pytest to parse a file for you:

```bash
PRODUCT_ENV='stage' pytest -v --critical @/tmp/ci-failures.txt
```

However, everything written above still stands for scenarios where any other shell command is used in place of `pytest`.
