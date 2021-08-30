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
        with open(f"{buildDir}/{dirname}.htm", "w", encoding="utf-8", errors="xmlcharrefreplace") as output_file:
            output_file.write(html)

def read_html(filename):
    with open(f"build/{filename}.html", "r", encoding="utf-8") as input_file:
        text = input_file.read()
        soup = BeautifulSoup(text, 'html.parser')
        return soup

def main():
    parse_blog("example_blog1")

if __name__ == "__main__":
    main()
