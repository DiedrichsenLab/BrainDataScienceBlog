# Example blog: This is the title
<section markdown="1">
{{Brain, Data, and Science}} is a blog by the Diedrichsenlab on brain science, data science, and science in general. Instead of using wordpress or other platforms, we decided that we wanted full control over the formatting to play creatively with form and content. Inspired by Edward Tufte's work, we build this Python code that compiles blogs written in markdown into a web-blog that looks aesthetically pleasing and has the functionality that we wanted.
</section>


<section markdown="1">

## Getting started
To contribute blogs to *Brain, Data, and Science*, fork or clone [the repository](https://github.com/DiedrichsenLab/BrainDataScienceBlog). Each blog has an own folder.

## Headers and sections
Headers are coded using the standard markdown notions


# Level 1
## Level 2
### Level 3

Enclose sections that belong together into `&lt;/section&gt; &lt;/section&gt;` tabs.

{{New thoughts}} can be highlighted in the beginning of a paragraph by enclosing them into `{{...}}`.

### Side notes
Side note are a characteristic feature of Tufte's work. They enable authors to provide supplementary information in the text without having the reader go to a different part of the paper.
When you have a simple comment, you can include it directly in the text{+side:this is a sidenote}. You can also make general comments as margin notes that are unnumbered {+margin:This is a margin note.}. When the viewport gets smaller (i.e. when viewing the page on a mobile device, side and margin notes disappear and are only shown when the user toggles them.)

### References
To include automatic reference formating, include a  `reference.bib` file in the enclosing folder.
References then can then be cited using the tag from the bib-file by using a `[+citet: Yokoi2019]` or `[+citep: Berlot2018]` tag. The `citet` citations are replaced with [+citet: Yokoi2019],  the `citep` citations are replaced with [+citep: Berlot2018]. The citations are then added to a reference section in the end of the document.{+side:You can also add citations to a side note [+citep: Berlot2018], so that the reference does not disrupt the flow of reading, but at the same time the information is right there.}

### Formulas
Math type setting is achieved over MathJax. Math can be either included over inline math, using the dollar sign `$a \ne 0$` with is set as $a \ne 0$. You can also use round paratheses as delimiter, such as: `\\(ax^2 + bx + c = 0\\)` which is set as \\(ax^2 + bx + c = 0\\) . Display equations are delimited by double dollar signs and separated from the main text using an empty line.

```
$$
x = {-b \pm \sqrt{b^2-4ac} \over 2a}.
$$
```

$$
x = {-b \pm \sqrt{b^2-4ac} \over 2a}.
$$

This ensures that the equations are rendered correctly in the html, but also in your markdown while writing.

### Code
Code comes in code blocks or inline code. Inline code can be simply set using single quotes <code>\`code\`</code>. Blocks of code should be enclosed in triple <code>```</code>

```
    os.chdir(f"{sourceDir}/{dirname}")
    with open("info.yaml", "r", encoding="utf-8") as info_file:
        info = yaml.load(info_file,Loader=yaml.FullLoader)
```

### Links
Links to external documents can be included as is standard in markdown with `[link](http://diedrichsenlab.org)` syntax which is being set as [link](http://diedrichsenlab.org).

### Images
Figures are included by inserting a paragraph starting with a Figure tag.

```
![Figure 1](/path/to/img.jpg)**Figure 1.** Some caption for figure 1.
```

The tag provides the file name of the figure to be included - the rest of the paragraph spells out the caption. So the above statement would be set to

![Figure 1](icon.png)**Figure 1.** Some caption for figure 1.

</section>

<section markdown="1">

## Acknowledgements
The basic formating is based from Tufte-LaTeX and and the GitHub project [tufte-css](https://edwardtufte.github.io/tufte-css/) by David Liepman. The code for the blog uses the [Python-Markdown library](https://python-markdown.github.io/)
</section>