# Example blog: This is the title
<section markdown="1">
Brain, Data, and Science is a blog by the diedrichsen lab on brain science, data science, and science in general. Instead of using wordpress or other platforms, we decided that we wanted full control over the formating to play creatively with a new way of communicating science. Inspired by Edward Tufte's work, we set up a automatic content delivery platform compiles blogs written in markdown language into a web-blog that looks aethetically pleasing and had all the functionality that we wanted.
</section>

<section markdown="1">
## Getting started
To contribute blogs or responses to Brain, Data, and Science, fork the repository. Each blog has it's own folder.
</section>

<section markdown="1">
## Fundamentals
### Headers and sections
Enclose sections that belong together into `;section;;//section;` tabs.

{{New thoughts}} can be highlighted in the begginning of the abstract to highlight them.

### Side notes
Side note are a specific feature of the Brain, Data, and Science blog and directly taken from the Tufte's work. They enable authors to provide supplementary information in the text without having the reader going to a different part of the paper.
When you have a simple comment, you can include it directly in the text {+side:s1:this is a sidenote}. You can also make general comments as margin notes that are unnumbered {+margin:m1:This is a margin note.}

### References
References can be cited as cite notes. To make the formating automatic, you want to provide a `reference.bib` file in bibtex formation.
References can then be cited using the tag from the bib-file, and are formated as sidenote {+ref: Yokoi2019}. When the same reference occurs the second time what happens then {+ref: Yokoi2019}?

### Formulas
Math type setting is achieved over MathJax. Math can be either included over inline math, using the dollar sign $a \ne 0$ or round paratheses as delimiter, such as: \\(ax^2 + bx + c = 0\\). Display equations are delimited by double dollar signs and separated from the main text using an empty line.

$$
x = {-b \pm \sqrt{b^2-4ac} \over 2a}.
$$

This ensures that the equations are rendered correctly in the html, but also in your markdown while writing.

### Code
Code come in code blocks or inline code. Inline code can be simply set using `\`Single quotes\``. Blocked code is

```
    os.chdir(f"{sourceDir}/{dirname}")
    with open("info.yaml", "r", encoding="utf-8") as info_file:
        info = yaml.load(info_file,Loader=yaml.FullLoader)
```

should be enclosed in triple <code>```</code>.

### Links
This is a [link](http://diedrichsenlab.org)

I get 10 times more traffic from [Google] [1] than from
[Yahoo] [2] or [MSN] [3].

[1]: http://google.com/        "Google"
[2]: http://search.yahoo.com/  "Yahoo Search"
[3]: http://search.msn.com/    "MSN Search"

### Images
Images are included
![Figure 1](/path/to/img.jpg)
</section>

<section markdown="1">
## Acknowledgements
The basic formating is based from Tufte-LaTeX and and the GitHub project tufte-css. The blog is based on Markdown....Indepe
</section>