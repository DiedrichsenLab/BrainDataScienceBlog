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

buildDir = '/Users/jdiedrichsen/Dropbox (Diedrichsenlab)/Sites/Diedrichsenlab/BrainDataScience'
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
        info['id']=dirname
    with open("text.md", "r", encoding="utf-8") as input_file:
        text = input_file.read()
        html = md.markdown(text,extensions=ext)
        with open(f"{buildDir}/{dirname}/index.htm", "w", encoding="utf-8", errors="xmlcharrefreplace") as output_file:
            output_file.write(html)
    return(info)


def make_index(blogs,name):
    tree = etree.ElementTree()
    Edoc = etree.Element('html')
    Ehead = etree.SubElement(Edoc,'head')
    t=etree.SubElement(Ehead,'title')
    t.text =  'Brain, Data, and Science'
    etree.SubElement(Ehead,'link',attrib={'rel':'stylesheet','href':'tufteSans.css'})
    etree.SubElement(Ehead,'link',attrib={'rel':'stylesheet','href':'toc.css'})
    etree.SubElement(Ehead,'meta',attrib={'name':'viewport','content':"width=device-width, initial-scale=1"})

    Ebody = etree.SubElement(Edoc,'body')
    Eh1 = etree.SubElement(Ebody,'h1')
    Eh1.text = 'Brain, Data, and Science'
    for i,blog in blogs.iterrows():
        Elink = etree.SubElement(Ebody,'a',attrib={'href':blog.id})
        Ediv = etree.SubElement(Elink,'div',attrib={'class':'tocContainer'})
        etree.SubElement(Ediv,'img',attrib={'class':'tocImage','src':f"{blog.id}/icon.png"})
        Etxt = etree.SubElement(Ediv,'div',attrib={'class':"tocText"})
        Etitle = etree.SubElement(Etxt,'p',attrib={'class':"tocTitle"})
        Etitle.text = blog.title
        Eauthors = etree.SubElement(Etxt,'p',attrib={'class':"tocAuthors"})
        Eauthors.text = ', '.join([str(elem) for elem in blog.authors])
        Edescrip = etree.SubElement(Etxt,'p',attrib={'class':"tocDescr"})
        Edescrip.text = blog.description
    tree._setroot(Edoc)
    tree.write(name)


def main():
    with open("list.yaml", "r", encoding="utf-8") as list_file:
        listing = yaml.load(list_file,Loader=yaml.FullLoader)
    info = []
    for blog in listing['blogs']:
        info.append(parse_blog(blog))
    allblogs = pd.DataFrame(info)
    make_index(allblogs,name=f"{buildDir}/index.htm")


if __name__ == "__main__":
    main()
