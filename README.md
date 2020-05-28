# How I build

```bash
$ nix-shell --pure --command "pdflatex AaronResume.tex"
$ sudo mv AaronResume.pdf /var/www/main/resume.pdf
```


# About

LaTeX resume template, perhaps, one day, an orgmode export option??

This is my resume. Feel free to use it as a template, 
just be careful not to accidentally leave my information in. 
You don't want to submit my resume for yourself. That would be awkward.

I'm using a constants.tex file alongside the 
main one to avoid putting my personal info online.  

Adapt the foo version of it so that you can do the same if you want.

```bash
$ cp fooconstants.tex constants.tex
$ vi constants.tex # insert your address, phone etc...
```

I presume if you're conscientious enough to figure out how to edit the latex, 
you'll be conscientious enough to only use your own info.

I hope as a template, this serves you well.

Cheers!
