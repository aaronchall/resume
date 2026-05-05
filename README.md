# How to build

You need nix installed on your system. 
If you're using nix on Apple (darwin) you'll need to update the flake.nix.
After that:

For a reproducible build:

```bash
$ nix build
```

Or interactively for a tighter development loop:

```bash
$ nix develop
```
and then run:

```bash
$ python -m resume
```

# About

Python to LaTeX resume template.

This is my resume. Feel free to use it as a template, 
just be careful not to accidentally leave my information in. 
You don't want to submit my resume as yours. That would be awkward.

Cheers!
