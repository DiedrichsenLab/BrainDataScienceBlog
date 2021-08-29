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

buildDir = '/Users/jdiedrichsen/Dropbox (Diedrichsenlab)/Sites/Diedrichsenlab/BrainDataScience/'
sourceDir = '/Users/jdiedrichsen/Dropbox (Diedrichsenlab)/Sites/Brain_Data_Science_Blog'

def parse_blog(dirname):
    """
        Parsing
    """
    markdown_include = MarkdownInclude(configs={'base_path':'./source/', 'encoding': 'iso-8859-1'})
    head_ext = me.HeadExt()
    title_ext = me.TitleExt()
    sidebar_ext = me.SidebarExt()
    personcell_ext = me.PersoncellExt()
    tree_ext = me.TreeExtension()
    ref_ext = me.ReferenceExt()
    icon_ext = me.IconcellExt()
    toolcell_ext = me.ToolcellExt()

    print(f'parsing {dirname}')
    ext=['md_in_html',markdown_include,head_ext,title_ext,sidebar_ext,
    personcell_ext,tree_ext,ref_ext,icon_ext,toolcell_ext,'attr_list','footnotes']

    with open(f"{sourceDir}/{dirname}/info.yaml", "r", encoding="utf-8") as info_file:
        info = yaml.load(info_file,Loader=yaml.FullLoader)
    with open(f"{sourceDir}/{dirname}/text.md", "r", encoding="utf-8") as input_file:
        text = input_file.read()
        html = md.markdown(text,extensions=ext)
        with open(f"{buildDir}/{dirname}/index.htm", "w", encoding="utf-8", errors="xmlcharrefreplace") as output_file:
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
