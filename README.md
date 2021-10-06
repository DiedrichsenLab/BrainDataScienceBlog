# BrainDataScienceBlog
This is a repository with the code and raw materials to build the [*Brain, Data, and Science*](http://diedrichsenlab.org/BrainDataScience) Blog. It is heavily build on the [Tufte.css](https://edwardtufte.github.io/tufte-css/) and the [markdown library](https://python-markdown.github.io/).

## Installation 

Fork or clone the [GitHub repository](https://github.com/DiedrichsenLab/BrainDataScienceBlog).

The repro required `python v >= 3.8`. You also need to have the following dependencies installed: 

```
pip install markdown
pip install xml
pip install yaml
pip install pandas
pip install shutil 
pip intall pybtex
```

## Building the webpage

A single Markdown file can be compiled to the target directory using: 

`python3 build.py`

## Writing a new blog

Each blog has its own directory in the repository. The directory name serves as the id for the blog. The code builds and includes all the blogs that are listed in `list.yaml`. 

All blogs must have the following files:

* `icon.png`: a square icon for the blog (ideally 150x150px)
* `info.yaml`: Basic information about the blog 
* `text.md`: Markdown file with text
* `references.bib`: Optional bibtex file with references - insert a blank file if you don't use citations. 

Blogs are written in plain markdown `.md` language. I like to use the free editor [Typora](https://typora.io/) which is a clean wysiwyg editor for markdown that also sets formulas correctly. Besides the standard markdown, we are using the following tags as markdown extensions:  

`<p>,<div>,<...>`: Any block-level html tag will be untouched and included as is. 

`{+side:text}`: Adds a numbered side note. 

`{+margin:text}`: Adds a margin note without a number. 

`{{text}}`: Formats text in Small Caps - you can highlight new thoughts at the beginning of a paragraph like this. 

 `[+citep:bibtex-id]` and `[+citet:bibtex-id]`: Citation to a reference in the `references.bib` file. 

`![alt title:filename] Caption`: Block-level tag (separate from rest by blank lines) that includes a Figure. 

For more information about formating options, see this [example blog](http://www.diedrichsenlab.org/BrainDataScience/example_blog/index.htm).

For problems, comments, or question, please use the [Issue channel on GitHub](https://github.com/DiedrichsenLab/BrainDataScienceBlog/issues). 

