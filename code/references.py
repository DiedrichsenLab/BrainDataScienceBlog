# from bs4 import beatifulsoup
import markdown as md
import markdown_extensions as me
from markdown_include.include import MarkdownInclude
from bs4 import BeautifulSoup
from markdown_include.include import MarkdownInclude
import xml.etree.ElementTree as etree
import re


def parse_file(filename):
    """
        Parsing
    """
    markdown_include = MarkdownInclude(configs={'base_path':'./source/', 'encoding': 'iso-8859-1'})
    head_ext = me.HeadExt()
    title_ext = me.TitleExt()
    sidebar_ext = me.SidebarExt()
    personcell_ext = me.PersoncellExt()
    tree_ext = me.TreeExtension()

    ext=['md_in_html',markdown_include,head_ext,title_ext,sidebar_ext,personcell_ext,tree_ext,'attr_list','footnotes']

    with open(f"source/{filename}.md", "r", encoding="utf-8") as input_file:
        text = input_file.read()
        html = md.markdown(text,extensions=ext)
        with open(f"build/{filename}.htm", "w", encoding="utf-8", errors="xmlcharrefreplace") as output_file:
            output_file.write(html)

def read_html(filename):
    with open(f"build/{filename}.html", "r", encoding="utf-8") as input_file:
        text = input_file.read()
        soup = BeautifulSoup(text, 'html.parser')
        return soup

if __name__ == "__main__":
    parse_file('publications')
    # s = read_html('index')
    pass
