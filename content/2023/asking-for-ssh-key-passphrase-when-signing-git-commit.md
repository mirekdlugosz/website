Title: Asking for ssh key passphrase when signing git commit
Slug: asking-for-ssh-key-passphrase-when-signing-git-commit
Date: 2023-01-05 18:19:01
Category: Blog
Tags: Linux, planet MoT, planet Python, tutorial

git has an option to sign commits and tags.
This allows you to verify that change indeed comes from a person it claims to come from.
Since 2.34.0, ssh can be used to sign things.
Which is nice, because everyone already has ssh configured to authorize pushes, so you can re-use the same key for authenticity certification.

I started signing all my commits in November 2022, using [Danilo Bargen's blog post](https://blog.dbrgn.ch/2021/11/16/git-ssh-signatures/) as a guide.
Instead of hard-coding my public ssh key in config file, I told git to get it from `ssh-add -L`.

This setup works well overall, but has one problem - `git commit` will fail if I forget to load private key into ssh keyring first. It's easy enough to recover from this without losing commit message, but wouldn't it be nice if git asked for ssh key password automatically?

Turns out it's very simple to do!
First, create a helper script and save it somewhere.
Here's mine:

```bash
#!/usr/bin/env bash

SSH_KEY=$(ssh-add -L)
if [ "$?" -eq 0 ]; then
    echo "$SSH_KEY"
else
    ssh-add
    ssh-add -L
fi
```

Then, change `defaultKeyCommand` in global git config file to use a helper script:

```
[gpg "ssh"]
    defaultKeyCommand = /path/to/helper/script
```

Now `git commit` will ask for ssh key passphrase if no key has been loaded yet.
