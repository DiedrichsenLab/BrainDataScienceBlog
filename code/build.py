# from bs4 import beatifulsoup
import markdown as md
import markdown_extensions as me
from markdown_include.include import MarkdownInclude
from bs4 import BeautifulSoup
from markdown_include.include import MarkdownInclude
import xml.etree.ElementTree as etree
import re
import sys
import yaml
import os
import pandas as pd

buildDir = '/Users/jdiedrichsen/Dropbox (Diedrichsenlab)/Sites/Diedrichsenlab/BrainDataScience/'
sourceDir = '/Users/jdiedrichsen/Dropbox (Diedrichsenlab)/Sites/BrainDataScienceBlog'

def parse_blog(dirname):
    """
        Parsing
    """
    markdown_include = MarkdownInclude(configs={'base_path':'./source/', 'encoding': 'iso-8859-1'})
    tree_ext = me.TreeExtension()
    side_ext = me.SidenoteExtension()
    margin_ext = me.MarginnoteExtension()
    ref_ext = me.ReferenceExtension()

    print(f'parsing {dirname}')
    ext=['md_in_html',markdown_include,tree_ext,side_ext,margin_ext,ref_ext]

    os.chdir(f"{sourceDir}/{dirname}")
    with open("info.yaml", "r", encoding="utf-8") as info_file:
        info = yaml.load(info_file,Loader=yaml.FullLoader)
    with open("text.md", "r", encoding="utf-8") as input_file:
        text = input_file.read()
        html = md.markdown(text,extensions=ext)
        with open(f"{buildDir}/{dirname}/index.htm", "w", encoding="utf-8", errors="xmlcharrefreplace") as output_file:
            output_file.write(html)
    return(info)


def make_index(blogs,name):
    Edoc = etree.Element('html')
    Ehead = etree.SubElement(Edoc,'head')
    t=etree.SubElement(Ehead,'title')
    t.text =  'Brain, Data, and Science'
    etree.SubElement(Ehead,'link',attrib={'rel':'stylesheet','href':'tufteSans.css'})
    etree.SubElement(Ehead,'link',attrib={'rel':'stylesheet','href':'toc.css'})
    etree.SubElement(Ehead,'meta',attrib={'name':'viewport','content':"width=device-width, initial-scale=1"})

    Ebody = etree.SubElement(Edoc,'body')
    Eart = etree.SubElement(Ebody,'article')
    Eh1 = etree.SubElement(Eart,'h1')
    Eh1.text = 'Brain, Data, and Science'
    ESect = etree.SubElement(Eart,'section')
    for blog in blogs:
        Ediv = etree.SubElement(ESect,'div',attrib={'class':'tocContainer'})
      <div class="tocContainer">
        <a href="blog_example.htm">
          <img class="tocImage" src="assets/icon_suitpy.png">
        </a>
        <div class="tocText">
          <a href="blog_example.htm"><p class="tocTitle">Example Blog</p></a>
          <p class="tocAuthors">Jörn Diedrichsen</p>
          <p class="tocDescr">In this blog, I describe the philosophy and technology behind the Brain, Data, and Science blog and explain of how to contribute... </p>
        </div>
      </div>

def main():
    with open("list.yaml", "r", encoding="utf-8") as list_file:
        listing = yaml.load(list_file,Loader=yaml.FullLoader)
    info = []
    for blog in listing['blogs']:
        info.append(parse_blog(blog))
    allblogs = pd.DataFrame(info)
    make_index(allblogs,name="index.htm")


if __name__ == "__main__":
    main()
