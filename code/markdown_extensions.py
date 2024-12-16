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
import yaml
from build import copy_resource

# Global list of references
_references = []

_sourceDir = os.path.dirname(os.path.dirname(__file__))

with open(os.path.join(_sourceDir,'assets','stats_counter.html')) as f:
    _statstag = f.read()

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
        {+side:text}
    """
    def __init__(self,pattern,md):
        self.num_sidenote = 0
        super().__init__(pattern,md)

    def handleMatch(self, m, data):
        self.num_sidenote = self.num_sidenote+1
        Eside = etree.Element('span')
        id = f"sn{self.num_sidenote}"
        etree.SubElement(Eside,'label',attrib={'for':id,'class':'margin-toggle sidenote-number'})
        etree.SubElement(Eside,'input',attrib={'type':'checkbox','id':id,'class':'margin-toggle'})
        Espan = etree.SubElement(Eside,'span',attrib={'class':'sidenote'})
        Espan.text = m.group(1)
        return Eside, m.start(0), m.end(0)

class SidenoteExtension(Extension):
    def extendMarkdown(self, md):
        SIDE_PATTERN = r'\{\+side:(.+?)\}'
        md.inlinePatterns.register(SidenoteInlineProcessor(SIDE_PATTERN, md), 'sidenote', 174)

"""
    Inline Processor for Margin notes
"""
class MarginInlineProcessor(InlineProcessor):
    """
        Margin note Processor
        {+margin:text}
    """
    def __init__(self,pattern,md):
        self.num_margnote = 0
        super().__init__(pattern,md)

    def handleMatch(self, m, data):
        Eside = etree.Element('span')
        self.num_margnote = self.num_margnote+1
        id = f"mn{self.num_margnote}"
        El = etree.SubElement(Eside,'label',attrib={'for':id,'class':'margin-toggle'})
        El.text = self.md.htmlStash.store("&#8853;")
        etree.SubElement(Eside,'input',attrib={'type':'checkbox','id':id,'class':'margin-toggle'})
        Espan = etree.SubElement(Eside,'span',attrib={'class':'marginnote'})
        Espan.text = m.group(1)
        return Eside, m.start(0), m.end(0)

class MarginnoteExtension(Extension):
    def extendMarkdown(self, md):
        MARG_PATTERN = r'\{\+margin:(.+?)\}'
        md.inlinePatterns.register(MarginInlineProcessor(MARG_PATTERN, md), 'marginnote', 175)

"""
    New throught Processor for smallCAPS
"""
class CapsInlineProcessor(InlineProcessor):
    """
        Caps Processor
        {{Caps}}
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
        {+citep:bibid} -> (Jones et al., 2012)
        {+citet:bibid} -> Jones et al. (2012)
    """

    def __init__(self,pattern,md):
        self.bib = parse_file('references.bib')
        super().__init__(pattern,md)

    def handleMatch(self, m, data):
        mode = m.group(1)
        ref_key = m.group(2)
        # For multiple references, split the key
        ref_keys = ref_key.split(';')
        if mode== 'p':
            text = '('
        else:
            text = ''
        for i,ref_key in enumerate(ref_keys):
            if ref_key not in _references:
                _references.append(ref_key)
            bib_e = self.bib.entries[ref_key]
            authors = bib_e.persons['author']
            num_auth = len(authors)
            # assemble citation string
            if i > 0:
                text = text + '; '
            if (num_auth == 1 ):
                text = text + strip_brackets(authors[0].last_names[0])
            elif (num_auth == 2):
                text = text + strip_brackets(authors[0].last_names[0]) + ' & ' + strip_brackets(authors[1].last_names[0])
            else:
                text = text + strip_brackets(authors[0].last_names[0]) + ' et al.'
            if mode == 't':
                text = text + ' (' + bib_e.fields['year'] + ')'
            elif mode == 'p':
                text = text + ', ' + bib_e.fields['year']
            else:
                raise(NameError('can only understand +citep and +citet'))
        if mode== 'p':
            text = text + ')'


        # text = text + strip_brackets(bib_e.fields['title']) + '. '
        # text = text + '<em>'+ strip_brackets(bib_e.fields['journal'])
        # text = text + '</em>'
        # text = text + '.'

        Eref = etree.Element('span')
        Eref.text = text
        # etree.SubElement(Eside,'label',attrib={'for':ref_key,'class':'margin-toggle sidenote-number'})
        # etree.SubElement(Eside,'input',attrib={'type':'checkbox','id':ref_key,'class':'margin-toggle'})
        # Espan = etree.SubElement(Eside,'span',attrib={'class':'sidenote'})
        return Eref, m.start(0), m.end(0)

class ReferenceExtension(Extension):
    def extendMarkdown(self, md):
        REF_PATTERN = r'\[\+cite(.):\s*(.+?)\]'
        md.inlinePatterns.register(ReferenceProcessor(REF_PATTERN, md), 'ref', 175)

    def reset(self):
        global _references
        _references = []



"""
    Block Processor for Figure
"""
class FigureProcessor(BlockProcessor):
    RE_FENCE_START = r'!\[(.+?)\]\((.+?)\)'
    def __init__(self,md):
        self.md = md
        super().__init__(md.parser)

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
                Ep = etree.SubElement(parent, 'figure')
                El = etree.SubElement(Ep,'label',attrib={'for':filename,'class':'margin-toggle'})
                El.text = self.md.htmlStash.store("&#8853;")

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
                El = etree.SubElement(Efig,'label',attrib={'for':filename,'class':'margin-toggle'})
                El.text = self.md.htmlStash.store("&#8853;")
                etree.SubElement(Efig,'input',attrib={'type':'checkbox','id':filename,'class':'margin-toggle'})
                Ecap = etree.SubElement(Efig,'span',attrib={'class':'marginnote'})
                Ecap.text = caption
            Eimg = etree.SubElement(Efig,'img',attrib={'src':filename,'alt':m.group(1)})

        blocks.pop(0)
        return True

class FigureExtension(Extension):
    def extendMarkdown(self, md):
        MATH_PATTERN = r'\$(.*?)\$'
        md.parser.blockprocessors.register(FigureProcessor(md), 'fig', 175)

"""
    Finalize tree
"""
class MyTreeprocessor(Treeprocessor):

    def add_references(self,Eart):
        self.bib = parse_file('references.bib')
        Esec = etree.SubElement(Eart,'section')
        Eh2 = etree.SubElement(Esec,'h2')
        Eh2.text='References'
        for r in _references:
            bib_e = self.bib.entries[r]
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
            if 'journal' in bib_e.fields:
                text = text + '<em>'+ strip_brackets(bib_e.fields['journal']) + '</em>.'

            Ep = etree.SubElement(Esec,'p',attrib={'class':'hangingindent'})
            Ep.text =  self.md.htmlStash.store(text)


    def run(self, root):
        with open("info.yaml", "r", encoding="utf-8") as info_file:
            info = yaml.load(info_file,Loader=yaml.FullLoader)

        # Make HMTL Header
        Edoc = etree.Element('html')
        Ehead = etree.SubElement(Edoc,'head')
        Ecss1 = etree.SubElement(Ehead,'link',attrib={'rel':'stylesheet','href':'../tufteSans.css'})
        Ecss2 = etree.SubElement(Ehead,'link',attrib={'rel':'stylesheet','href':'../latex.css'})
        Emeta = etree.SubElement(Ehead,'meta',attrib={'name':'viewport','content':"width=device-width, initial-scale=1",'charset':'utf-8'})

        EMathHJax1 = etree.SubElement(Ehead,'script',
            attrib={'src':"../mathjax-config.js"})
        EMathHJax2 = etree.SubElement(Ehead,'script',
            attrib={'src':"https://polyfill.io/v3/polyfill.min.js?features=es6"})
        EMathHJax1 = etree.SubElement(Ehead,'script',
            attrib={'type':"text/javascript",'id':"MathJax-script",'src':"https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"})
        Ebody = etree.SubElement(Edoc,'body')
        Eart = etree.SubElement(Ebody,'article')

        # Add Navigation line
        Enav = etree.SubElement(Eart,'div',attrib={'class':'navline'})
        # Ea1 = etree.SubElement(Enav,'a',attrib={'href':'../../index.htm'})
        # Ea1.text = 'Diedrichsenlab'
        # Et1 = etree.SubElement(Enav,'span')
        # Et1.text = ' > '
        Ea2 = etree.SubElement(Enav,'a',attrib={'href':'../index.htm'})
        Ea2.text = 'Brain, Data, and Science'
        Et2 = etree.SubElement(Enav,'span')
        Et2.text = f" > {info['shorttitle']}"

        # Copy over the whole blog
        elements = list(root)
        for el in elements:
            Eart.append(el)
            root.remove(el)

        # Add reference section
        if len(_references)>0:
            self.add_references(Eart)

        # Make the footer
        if 'tweet' in info.keys():
            Ef = etree.SubElement(Eart,'div',attrib={'class':'footer'})
            html = f"<h3>Comments, discussions, and feedback:</h3> {info['tweet']}"
            Ef.text = self.md.htmlStash.store(html)

        # Add another navigation line
        Eart.append(Enav)

        # Add statscounter code in the end
        Estats = etree.SubElement(Ebody,'div')
        Estats.text =  self.md.htmlStash.store(_statstag)
        # Add

        root.append(Edoc)
        return None
        # No return statement is same as `return None`

class TreeExtension(Extension):
    def extendMarkdown(self, md):
        dict = self.getConfigInfo()
        md.treeprocessors.register(MyTreeprocessor(md), 'tree', 1)

