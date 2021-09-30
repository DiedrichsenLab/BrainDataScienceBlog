import markdown as md
from markdown.preprocessors import Preprocessor
from markdown.inlinepatterns import InlineProcessor
from markdown.blockprocessors import BlockProcessor
from markdown.treeprocessors import Treeprocessor
from markdown.extensions import Extension
from markdown.util import AtomicString
import re
import xml.etree.ElementTree as etree
from pybtex.database import parse_file
import os
from build import copy_resource

"""
    Inline Processor for mathjax
"""

class MathInlineProcessor(InlineProcessor):
    def handleMatch(self, m, data):
        el = etree.Element('span')
        el.text = AtomicString('$' + m.group(1) + '$')
        return el, m.start(0), m.end(0)

class MathInlineExtension(Extension):
    def extendMarkdown(self, md):
        MATH_PATTERN = r'\$(.*?)\$'
        md.inlinePatterns.register(MathInlineProcessor(MATH_PATTERN, md), 'inMath', 175)

"""
    Block Processor for mathjax
"""

class MathBlockProcessor(BlockProcessor):
    RE_FENCE_START = r'\$\$'

    def test(self, parent, block):
        return re.match(self.RE_FENCE_START,block)

    def run(self,parent,blocks):
        blocks[0] = re.sub(self.RE_FENCE_START, '', blocks[0])
        e = etree.SubElement(parent, 'p')
        e.text = AtomicString('\n$$' + blocks[0] + '$$\n')
        blocks.pop(0)
        return True

class MathBlockExtension(Extension):
    def extendMarkdown(self, md):
        MATH_PATTERN = r'\$(.*?)\$'
        md.parser.blockprocessors.register(MathBlockProcessor(md.parser), 'math', 175)

"""
    Inline Processor for Sidenotes
"""
class SidenoteInlineProcessor(InlineProcessor):
    """
        Side note Processor
        {+side:id:text}
    """

    def handleMatch(self, m, data):
        Eside = etree.Element('span')
        id = m.group(1)
        etree.SubElement(Eside,'label',attrib={'for':id,'class':'margin-toggle sidenote-number'})
        etree.SubElement(Eside,'input',attrib={'type':'checkbox','id':id,'class':'margin-toggle'})
        Espan = etree.SubElement(Eside,'span',attrib={'class':'sidenote'})
        Espan.text = m.group(2)
        return Eside, m.start(0), m.end(0)

class SidenoteExtension(Extension):
    def extendMarkdown(self, md):
        SIDE_PATTERN = r'\{\+side:(.+?):(.+?)\}'
        md.inlinePatterns.register(SidenoteInlineProcessor(SIDE_PATTERN, md), 'sidenote', 174)

"""
    Inline Processor for Margin notes
"""
class MarginInlineProcessor(InlineProcessor):
    """
        Margin note Processor
        {+margin:id:text}
    """

    def handleMatch(self, m, data):
        Eside = etree.Element('span')
        id = m.group(1)
        etree.SubElement(Eside,'label',attrib={'for':id,'class':'margin-toggle'})
        etree.SubElement(Eside,'input',attrib={'type':'checkbox','id':id,'class':'margin-toggle'})
        Espan = etree.SubElement(Eside,'span',attrib={'class':'marginnote'})
        Espan.text = m.group(2)
        return Eside, m.start(0), m.end(0)

class MarginnoteExtension(Extension):
    def extendMarkdown(self, md):
        MARG_PATTERN = r'\{\+margin:(.+?):(.+?)\}'
        md.inlinePatterns.register(MarginInlineProcessor(MARG_PATTERN, md), 'marginnote', 175)

"""
    New throught Processor for smallCAPS
"""
class CapsInlineProcessor(InlineProcessor):
    """
        Caps Processor
        {+margin:id:text}
    """

    def handleMatch(self, m, data):
        Ecaps = etree.Element('span',attrib={'class':'newthought'})
        Ecaps.text = m.group(1)
        return Ecaps, m.start(0), m.end(0)

class CapsExtension(Extension):
    def extendMarkdown(self, md):
        CAPS_PATTERN = r'\{\{(.+?)\}\}'
        md.inlinePatterns.register(CapsInlineProcessor(CAPS_PATTERN, md), 'caps', 173)

"""
    Inline Processor for References
"""
def get_initials(names):
    name_list=re.findall(r'[^, .]+',names)
    text = ''
    for name in name_list:
        text = text+name[0]+'.'
    return text

def strip_brackets(string):
    match=re.search(r'[^{}]+',string)
    return match.group(0)

def strip_doublehyphen(string):
    new_str = re.sub(r'--',r'-',string)
    return new_str


class ReferenceProcessor(InlineProcessor):
    """
        Reference Processor
        {+ref:bibid}
    """

    def __init__(self,pattern,md):
        self.bib = parse_file('references.bib')
        super().__init__(pattern,md)

    def handleMatch(self, m, data):
        ref_key = m.group(1)
        bib_e = self.bib.entries[ref_key]
        authors = bib_e.persons['author']
        text = ''
        num_auth = len(authors)
        if (num_auth == 1 ):
            text = text + strip_brackets(authors[0].last_names[0])
        elif (num_auth == 2):
            text = text + strip_brackets(authors[0].last_names[0]) + ' & ' + strip_brackets(authors[1].last_names[0])
        else:
            text = text + strip_brackets(authors[0].last_names[0]) + ' et al.'
        text = text + ' (' + bib_e.fields['year'] + '). '
        text = text + strip_brackets(bib_e.fields['title']) + '. '
        text = text + '<em>'+ strip_brackets(bib_e.fields['journal'])
        text = text + '</em>'
        text = text + '.'

        Eside = etree.Element('span')
        etree.SubElement(Eside,'label',attrib={'for':ref_key,'class':'margin-toggle sidenote-number'})
        etree.SubElement(Eside,'input',attrib={'type':'checkbox','id':ref_key,'class':'margin-toggle'})
        Espan = etree.SubElement(Eside,'span',attrib={'class':'sidenote'})
        Espan.text = text
        return Eside, m.start(0), m.end(0)

class ReferenceExtension(Extension):
    def extendMarkdown(self, md):
        REF_PATTERN = r'\{\+ref:\s*(.+?)\}'
        md.inlinePatterns.register(ReferenceProcessor(REF_PATTERN, md), 'ref', 175)

"""
    Block Processor for Figure
"""
class FigureProcessor(BlockProcessor):
    RE_FENCE_START = r'!\[(.+?)\]\((.+?)\)'

    def test(self, parent, block):
        return re.match(self.RE_FENCE_START,block)

    def run(self,parent,blocks):
        m = re.match(self.RE_FENCE_START, blocks[0])
        # First copy the image file to the corresponding Build directory 
        filename = m.group(2)
        _,ext = os.path.splitext(filename)
        copy_resource(filename)
        
        # Get the caption
        caption = re.sub(self.RE_FENCE_START,'',blocks[0])

        if ext=='.htm' or ext=='.html':
            if len(caption)>0:
                Ep = etree.SubElement(parent, 'p')
                etree.SubElement(Ep,'label',attrib={'for':filename,'class':'margin-toggle'})
                etree.SubElement(Ep,'input',attrib={'type':'checkbox','id':filename,'class':'margin-toggle'})
                Ecap = etree.SubElement(Ep,'span',attrib={'class':'marginnote'})
                Ecap.text = caption
            # Doesn't seem to work on some files: TR=etree.parse(filename)
            # Overall it would be preferred solution (maybe try and then catch?)
            with open (filename, "r") as myfile:
                data=myfile.read()
                Efig = etree.SubElement(parent, 'div',
                    attrib={'class':'htmlfigsquare'})
                Efig.text = data
        else: # Static image 
            Efig = etree.SubElement(parent, 'figure')
            if len(caption)>0:
                etree.SubElement(Efig,'label',attrib={'for':filename,'class':'margin-toggle'})
                etree.SubElement(Efig,'input',attrib={'type':'checkbox','id':filename,'class':'margin-toggle'})
                Ecap = etree.SubElement(Efig,'span',attrib={'class':'marginnote'})
                Ecap.text = caption
            Eimg = etree.SubElement(Efig,'img',attrib={'src':filename,'alt':m.group(1)})
        
        blocks.pop(0)
        return True

class FigureExtension(Extension):
    def extendMarkdown(self, md):
        MATH_PATTERN = r'\$(.*?)\$'
        md.parser.blockprocessors.register(FigureProcessor(md.parser), 'fig', 175)

"""
    Finalize tree
"""
class MyTreeprocessor(Treeprocessor):
    def run(self, root):
        Edoc = etree.Element('html')
        Ehead = etree.SubElement(Edoc,'head')
        Ecss1 = etree.SubElement(Ehead,'link',attrib={'rel':'stylesheet','href':'../tufteSans.css'})
        Ecss2 = etree.SubElement(Ehead,'link',attrib={'rel':'stylesheet','href':'../latex.css'})
        Emeta = etree.SubElement(Ehead,'meta',attrib={'name':'viewport','content':"width=device-width, initial-scale=1"})

        EMathHJax1 = etree.SubElement(Ehead,'script',
            attrib={'src':"../mathjax-config.js"})
        EMathHJax2 = etree.SubElement(Ehead,'script',
            attrib={'src':"https://polyfill.io/v3/polyfill.min.js?features=es6"})
        EMathHJax1 = etree.SubElement(Ehead,'script',
            attrib={'type':"text/javascript",'id':"MathJax-script",'src':"https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"})
        Ebody = etree.SubElement(Edoc,'body')
        Eart = etree.SubElement(Ebody,'article')
        elements = list(root)
        for el in elements:
            Eart.append(el)
            root.remove(el)
        root.append(Edoc)
        return None
        # No return statement is same as `return None`

class TreeExtension(Extension):
    def extendMarkdown(self, md):
        dict = self.getConfigInfo()
        md.treeprocessors.register(MyTreeprocessor(md.parser), 'tree', 1)

