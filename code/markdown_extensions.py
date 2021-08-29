import markdown as md
from markdown.preprocessors import Preprocessor
from markdown.inlinepatterns import InlineProcessor
from markdown.blockprocessors import BlockProcessor
from markdown.treeprocessors import Treeprocessor
from markdown.extensions import Extension
import re
import xml.etree.ElementTree as etree
from pybtex.database import parse_file

"""
    Inline Processor for side notes
"""


"""
    Head block
"""
class HeadBlockProc(BlockProcessor):
    """
        Header block Processor
        {+head:title:css}

    """
    tag_pattern = r'\s*\{\+head:(.+?):(.+?)\}'  # {+head:title:css}

    def test(self, parent, block):
        return re.match(self.tag_pattern, block)

    def run(self, parent, blocks):
        m = re.match(self.tag_pattern,blocks[0])
        blocks[0] = re.sub(self.tag_pattern, '', blocks[0])
        e_head = etree.SubElement(parent,'head')
        attrib_dict = {'http-equiv':'Content-Type','content':'text/html; charset=iso-8859-1'}
        e_meta = etree.SubElement(e_head,'meta', attrib=attrib_dict)
        e_title = etree.SubElement(e_head,'title')
        e_title.text = m.group(1)
        attrib_dict = {'rel':'StyleSheet','href':m.group(2),'type':'text/css','media':'screen'}
        e_link = etree.SubElement(e_head, 'link', attrib=attrib_dict)
        return True  # or could have had no return statement

class HeadExt(Extension):
    """
        HeadExt
        Handles request to include HTML with page title and css with the tag:
        {+head:title:css}
    """
    def extendMarkdown(self, md):
        md.parser.blockprocessors.register(HeadBlockProc(md.parser),'head_ext',175)

"""
    Title block
"""
class TitleBlockProc(BlockProcessor):
    """
        Header block Processor
        {+title:header}

    """
    tag_pattern = r'\s*\{\+title:(.+?):(.*?)\}'  # {+title:header:icon}

    def test(self, parent, block):
        return re.match(self.tag_pattern, block)

    def run(self, parent, blocks):
        m = re.match(self.tag_pattern,blocks[0])
        blocks[0] = re.sub(self.tag_pattern, '', blocks[0])
        e_div = etree.SubElement(parent, 'div',attrib={'id':'header'})
        # If given - add icon in the left upper corner
        if m.group(2):
            e_icon = etree.SubElement(e_div,'img', attrib={'id':"out", 'src':m.group(2), 'class':"fltlft"})
        e_title = etree.SubElement(e_div,'div', attrib={'class':'headertext'})
        e_title.text = m.group(1)
        return True  # or could have had no return statement

class TitleExt(Extension):
    """
        TitleExt
        Handles request to for title tag:
        {+title:header}
    """
    def extendMarkdown(self, md):
        md.parser.blockprocessors.register(TitleBlockProc(md.parser),'title_ext',175)

"""
    Side bar  block
"""

def add_icon(parent,img,link,alt=None,text=None,state='out'):
    e_link = etree.SubElement(parent,'a',attrib={'href':link})
    if alt is None:
        alt = 'icon'
    if state == 'on':
        att = {'id':'on','onmouseover':'id="on";','onmouseout':'id="on";', 'src':img, 'alt':alt}
    else:
        att = {'id':'out','onmouseover':'id="on";','onmouseout':'id="out";', 'src':img, 'alt':alt}
    e_img=etree.SubElement(e_link,'img',attrib=att)
    if text is not None:
        e_div = etree.SubElement(parent,'div',attrib={'class':'icontext'})
        e_div.text = text

class SidebarBlockProc(BlockProcessor):
    """
        Sidebar  Processor
    """
    tag_pattern = r'\s*\{\+sidebar:([0-9])\}'

    sidebar = [('icon_home.jpg','index.htm','The Lab'),
               ('icon_people.gif','people.htm','People'),
               ('icon_jncover.gif','publications.htm','Publications'),
               ('icon_brain.jpg','research.htm','Research'),
               ('icon_suitpy.png','tools.htm','Tools')]

    def test(self, parent, block):
        return re.match(self.tag_pattern, block)

    def run(self, parent, blocks):
        m = re.match(self.tag_pattern,blocks[0])
        blocks[0] = re.sub(self.tag_pattern, '', blocks[0])
        e_div = etree.SubElement(parent, 'div',attrib={'id':'sidebar'})
        e_table = etree.SubElement(e_div,'table')
        for i,icon in enumerate(self.sidebar):
            e_tr = etree.SubElement(e_table,'tr',attrib={'align':'center'})
            e_td = etree.SubElement(e_tr,'td',attrib={'class':'iconcell'})
            if i == int(m.group(1)):
                state = "on"
            else:
                state = "off"
            add_icon(e_td,img='Pics/'+ icon[0],link = icon[1], text = icon[2], state = state,alt = icon[2])
        return True  # or could have had no return statement

class SidebarExt(Extension):
    """
        TitleExt
        Handles request to for title tag:
        {+title:header}
    """
    def extendMarkdown(self, md):
        md.parser.blockprocessors.register(SidebarBlockProc(md.parser),'sidebar_ext',175)

"""
    Icon cell: Arbitrary placed Icon + icon text in parent
"""
class IconcellProc(BlockProcessor):
    """
        Iconcell  Processor
    """
    tag_pattern = r'\s*\{\+iconcell:\s*(?P<title>.*?):\s*(?P<image>.*?):\s*(?P<left>.*?):\s*(?P<top>.*?):\s*(?P<link>.*)}'

    def test(self, parent, block):
        return re.match(self.tag_pattern, block)

    def run(self, parent, blocks):
        m = re.match(self.tag_pattern,blocks[0])
        d = m.groupdict()
        blocks[0] = re.sub(self.tag_pattern, '', blocks[0])
        style_str = f"left:{d['left']}; top:{d['top']}"
        e_div = etree.SubElement(parent, 'div',attrib={'class':'iconcell','style':style_str})
        alt_str = re.sub(r'<br>',' ',d['title'])
        add_icon(e_div,d['image'],link = d['link'],text = d['title'],state='out',alt = alt_str)
        return True  # or could have had no return statement

class IconcellExt(Extension):
    """
        TitleExt
        Handles request to for title tag:
        {+title:header}
    """
    def extendMarkdown(self, md):
        md.parser.blockprocessors.register(IconcellProc(md.parser),'iconcell_ext',175)


"""
    Toolcell
"""
class ToolcellProc(BlockProcessor):
    """
        Iconcell with a description on the right side
    """
    tag_pattern = r'\s*\{\+toolcell:\s*(?P<title>.*?):\s*(?P<image>.*?):\s*(?P<description>.*?):\s*(?P<link>.*)}'

    def test(self, parent, block):
        return re.match(self.tag_pattern, block)

    def run(self, parent, blocks):
        m = re.match(self.tag_pattern,blocks[0])
        d = m.groupdict()
        blocks[0] = re.sub(self.tag_pattern, '', blocks[0])
        e_div = etree.SubElement(parent, 'div',attrib={'class':'ToolCell'})
        e_table = etree.SubElement(e_div,'table')
        e_tr = etree.SubElement(e_table,'tr')
        e_td = etree.SubElement(e_tr,'td',attrib={'class':'ToolIcon'})
        alt_str = re.sub(r'<br>',' ',d['title'])
        add_icon(e_td,d['image'],link = d['link'],text = d['title'],state='out',alt = alt_str)
        e_td = etree.SubElement(e_tr,'td',attrib={'class':'ToolText'})
        e_p = etree.SubElement(e_td,'p',attrib={'class':'icontext'})
        e_p.text = d['description']
        return True  # or could have had no return statement

class ToolcellExt(Extension):
    """
        Handles request to for title tag:
    """
    def extendMarkdown(self, md):
        md.parser.blockprocessors.register(ToolcellProc(md.parser),'toolcell_ext',175)
"""
    Person cell
"""
class PersoncellBlockProc(BlockProcessor):
    """
        Personcell  Processor
    """
    tag_pattern = r'\s*\{\+personcell:\s*(?P<first>.*?):\s*(?P<last>.*?):\s*(?P<title>.*?):\s*(?P<details>.*?):\s*(?P<image>.*?):\s*(?P<email>.*?):\s*(?P<link>.*)}'

    def test(self, parent, block):
        return re.match(self.tag_pattern, block)

    def run(self, parent, blocks):
        m = re.match(self.tag_pattern,blocks[0])
        d = m.groupdict()
        blocks[0] = re.sub(self.tag_pattern, '', blocks[0])
        e_div = etree.SubElement(parent, 'div',attrib={'class':'PersonCell'})
        e_table = etree.SubElement(e_div,'table')
        e_tr = etree.SubElement(e_table,'tr')
        e_td = etree.SubElement(e_tr,'td',attrib={'class':'PersonIcon'})
        text = d['first'] + '<br>' + d['last']
        if d['link']:
            pass
        add_icon(e_td,d['image'],link = d['link'],text = text,state='out',alt = d['first'])
        e_td = etree.SubElement(e_tr,'td',attrib={'class':'PersonText'})
        e_p = etree.SubElement(e_td,'p',attrib={'class':'icontext'})
        e_p.text = '<b>' + d['first'] + ' ' + d['last'] + '</b>'
        e_p.text = e_p.text + '<br>' + d['title']
        e_p.text = e_p.text + '<br>' + d['details']
        e_span = etree.SubElement(e_td,'span',attrib={'class':'emailtext'})
        e_span.text = d['email']
        return True  # or could have had no return statement

class PersoncellExt(Extension):
    """
        TitleExt
        Handles request to for title tag:
        {+title:header}
    """
    def extendMarkdown(self, md):
        md.parser.blockprocessors.register(PersoncellBlockProc(md.parser),'personcell_ext',175)

"""
    reference (in UL)
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


class ReferenceProcessor(BlockProcessor):
    tag_pattern = r'\s*\{\+ref:\s*(.*?):\s*(.*)\}'

    def __init__(self,parser):
        self.bib = parse_file('source/publications.bib')
        super().__init__(parser)

    def test(self, parent, block):
        return re.match(self.tag_pattern, block)

    def run(self, parent, blocks):
        m = re.match(self.tag_pattern,blocks[0])
        blocks[0] = re.sub(self.tag_pattern, '', blocks[0])
        e_li = etree.SubElement(parent, 'li',attrib={'class':'pubs'})
        ref_key = m.group(1)
        ref_link = m.group(2)
        bib_e = self.bib.entries[ref_key]
        authors = bib_e.persons['author']
        text = ''
        num_auth = len(authors)
        for i,a in enumerate(authors):
            text = text + strip_brackets(a.last_names[0]) + ', ' + get_initials(a.first_names[0])
            if (i<num_auth-1):
                text = text + ', '
            else:
                text = text + ' '
        text = text + '(' + bib_e.fields['year'] + '). '
        text = text + strip_brackets(bib_e.fields['title']) + '. '
        text = text + '<em>'+ strip_brackets(bib_e.fields['journal'])
        if 'volume' in bib_e.fields:
            text = text + ', ' + bib_e.fields['volume']
        if 'number' in bib_e.fields:
            text = text + '(' + bib_e.fields['number'] + ')'
        text = text + '</em>'
        if 'pages' in bib_e.fields:
            text = text + ', ' + strip_doublehyphen(bib_e.fields['pages'])
        text = text + '.'
        e_li.text = text
        e_a = etree.SubElement(e_li, 'a',attrib={'class':'darklink', 'href':ref_link})
        attr = {'src':'Pics/pdf.gif','alt':'pdf format','border':'0','width':'25','height':'12'}
        e_img = etree.SubElement(e_a, 'img',attrib=attr)
        return True  # or could have had no return statement

class ReferenceExt(Extension):
    """
        TitleExt
        Handles request to for title tag:
        {+title:header}
    """
    def extendMarkdown(self, md):
        ref_proc = ReferenceProcessor(md.parser)
        md.parser.blockprocessors.register(ref_proc,'ref_ext',175)

"""
    Finalize tree
"""
class MyTreeprocessor(Treeprocessor):
    def run(self, root):
        doc = etree.Element('html')
        elements = root.getchildren()
        for el in elements:
            doc.append(el)
            root.remove(el)
        root.append(doc)
        return None
        # No return statement is same as `return None`

class TreeExtension(Extension):
    def extendMarkdown(self, md):
        md.treeprocessors.register(MyTreeprocessor(md.parser), 'tree', 1)

