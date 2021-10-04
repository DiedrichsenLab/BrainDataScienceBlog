# from bs4 import beatifulsoup
import markdown as md
import markdown_extensions as me
from markdown_include.include import MarkdownInclude
import xml.etree.ElementTree as etree
import re
import sys
import yaml
import os
import pandas as pd
import shutil

buildDir = '/Users/jdiedrichsen/Dropbox (Diedrichsenlab)/Sites/Diedrichsenlab/BrainDataScience'
sourceDir = '/Users/jdiedrichsen/Dropbox (Diedrichsenlab)/Sites/BrainDataScienceBlog'

def copy_resource(filename):
    """
        Copies resource file from current directory to the corresponding
        location in the build directory.
    """
    currdir = os. getcwd()
    folder = os.path.basename(currdir)
    target = os.path.join(buildDir,folder,filename)
    shutil.copy2(filename,target)

def parse_blog(dirname):
    """
        Parsing
    """
    markdown_include = MarkdownInclude(configs={'base_path':'./source/', 'encoding': 'iso-8859-1'})
    tree_ext = me.TreeExtension()
    side_ext = me.SidenoteExtension()
    margin_ext = me.MarginnoteExtension()
    ref_ext = me.ReferenceExtension()
    math_ext = me.MathInlineExtension()
    math_bext = me.MathBlockExtension()
    fig_ext = me.FigureExtension()

    print(f'parsing {dirname}')
    ext=['md_in_html',markdown_include,tree_ext,side_ext,margin_ext,ref_ext,
         math_ext,math_bext,fig_ext]

    os.chdir(f"{sourceDir}/{dirname}")
    copy_resource("icon.png")
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

    # Add Navigation line
    Enav = etree.SubElement(Ebody,'div',attrib={'class':'navline'})
    # Ea1 = etree.SubElement(Enav,'a',attrib={'href':'../index.htm'})
    # Ea1.text = 'Diedrichsenlab'
    # Et1 = etree.SubElement(Enav,'span')
    Enav.text = 'Brain, Data, and Science'


    Eh1 = etree.SubElement(Ebody,'h1')
    Eh1.text = 'Brain, Data, and Science'
    for i,blog in blogs.iterrows():
        Elink = etree.SubElement(Ebody,'a',attrib={'href':blog.id + '/index.htm'})
        Ediv = etree.SubElement(Elink,'div',attrib={'class':'tocContainer'})
        etree.SubElement(Ediv,'img',attrib={'class':'tocImage','src':f"{blog.id}/icon.png"})
        Etxt = etree.SubElement(Ediv,'div',attrib={'class':"tocText"})
        Etitle = etree.SubElement(Etxt,'p',attrib={'class':"tocTitle"})
        Etitle.text = blog.title
        Eauthors = etree.SubElement(Etxt,'p',attrib={'class':"tocAuthors"})
        Eauthors.text = ', '.join([str(elem) for elem in blog.authors])
        Edescrip = etree.SubElement(Etxt,'p',attrib={'class':"tocDescr"})
        Edescrip.text = blog.description
        Edescrip = etree.SubElement(Etxt,'p',attrib={'class':"tocDate"})
        Edescrip.text = f"First published: {blog['released']}"
    Ebody.append(Enav)
    tree._setroot(Edoc)
    tree.write(name)


def main():
    """ Build all blogs"""
    with open("list.yaml", "r", encoding="utf-8") as list_file:
        listing = yaml.load(list_file,Loader=yaml.FullLoader)
        info = []
        for blog in listing['blogs']:
            info.append(parse_blog(blog))
        allblogs = pd.DataFrame(info)
        make_index(allblogs,name=f"{buildDir}/index.htm")

if __name__ == "__main__":
    main()