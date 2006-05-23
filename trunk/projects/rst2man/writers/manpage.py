# Author: 
# Contact: grubert@users.sf.net
# Copyright: 2003 - engelbert gruber - All Rights Reserved
# License: This module is put into the public domain.
#
# CVS: $Id: ManPageWriter.py 1720 2003-10-18 21:42:39Z grubert $

"""
Man page formatting for reStructuredText.

See http://www.tldp.org/HOWTO/Man-Page for a start.

Man pages have no subsection only parts.
Standard parts
  NAME ,
  SYNOPSIS ,
  DESCRIPTION ,
  OPTIONS ,
  FILES ,
  SEE ALSO ,
  BUGS ,
and
  AUTHOR .

"""

# NOTE: the macros only work when at line start, so try the rule
#       start new lines in visit_ functions.

DEBUG=1

__docformat__ = 'reStructuredText'

import sys
import os
import time
import re
from types import ListType
from sets import Set

import docutils
from docutils import nodes, utils, writers, languages


class Writer(writers.Writer):
    supported = ('ManPage')
    """Formats this writer supports."""
    output = None
    """Final translated form of `document`."""

    def __init__(self):
        writers.Writer.__init__(self)
        self.translator_class = Translator

    def translate(self):
        visitor = self.translator_class(self.document)
        self.document.walkabout(visitor)
        self.output = visitor.astext()

class Table:
    def __init__(self):
        self.content = 'toto'


class Translator(nodes.NodeVisitor):
    """"""
    words_and_spaces = re.compile(r'\S+| +|\n')
    document_start = """Man page generated from reStructeredText."""

    def __init__(self, document):
        nodes.NodeVisitor.__init__(self, document)
        self.settings = settings = document.settings
        lcode = settings.language_code
        self.language = languages.get_language(lcode)
        self.head = []
        self.body = []
        self.foot = []
        self.section_level = 0
        self.topic_class = ''
        self.colspecs = []
        self.compact_p = 1
        self.compact_simple = None
        self.in_docinfo = None
        #self.context = []
        self.context = Set()

## - - - -
## UTILS
## - - - -

    def comment_begin(self, text):
        """Return commented version of the passed text WITHOUT end of line/comment."""
        if debug:
            prefix = '\n.\\" '
            return prefix+prefix.join(text.split('\n'))
        else:
            return ''

    def comment(self, text, debug=DEBUG):
        """Return commented version of the passed text."""
        if debug:
            prefix = '\n.\\" '
            return prefix+prefix.join(text.split('\n'))+'\n'
        else:
            return ''

    def astext(self):
        """Return the final formatted document as a string."""
        return ''.join(self.head + self.body + self.foot)

## - - - - - - - - - - - - - - - - -
## TRYING TO IMPLEMENT THESE NODES
## - - - - - - - - - - - - - - - - -

    """ Typical table:
    .TS H
    | l |  l | .
    _
    Titre1 	 Titre2
    _
    aaa 	 111
    bbb 	 222
    _
    .TE

    will render like this:

    +--------+---------+
    |Titre1  |  Titre2 |
    +--------+---------+
    |aaa     |  111    |
    |bbb     |  222    |
    +--------+---------+

    """

    def visit_table(self, node):
        self.body.append(self.comment('visit_table'))
        self.active_table = Table()
        self.active_table.content = '\n.TS H'
        #self.body.append('\n.TS H')

    def depart_table(self, node):
        ##self.body.append('\n.TE ')
        self.active_table.content += '\n.TE '
        self.body.append(self.active_table.content)
        self.body.append(self.comment('depart_table'))

    def visit_tbody(self, node):
        self.body.append(self.comment('visit_tbody'))

    def depart_tbody(self, node):
        self.body.append(self.comment('depart_tbody'))

    def visit_tgroup(self, node):
        self.body.append(self.comment('visit_tgroup'))

    def depart_tgroup(self, node):
        self.body.append(self.comment('depart_tgroup'))

    def visit_thead(self, node):
        self.body.append(self.comment('visit_thead'))

    def depart_thead(self, node):
        self.body.append(self.comment('depart_thead'))

    def visit_row(self, node):
        self.body.append(self.comment('visit_row'))

    def depart_row(self, node):
        self.body.append(self.comment('depart_row'))

    def visit_entry(self, node):
        self.body.append(self.comment('visit_entry'))
        self.body.append('T{\n')

    def depart_entry(self, node):
        self.body.append('\nT}')
        self.body.append(self.comment('depart_entry'))

    def visit_definition(self, node):
        self.body.append(self.comment('visit_definition'))
        self.body.append('\\fB')

    def depart_definition(self, node):
        self.body.append(self.comment('depart_definition'))
        self.body.append('\\fR ')

    def visit_definition_list(self, node):
        self.body.append(self.comment('visit_definition_list'))

    def depart_definition_list(self, node):
        self.body.append(self.comment('depart_definition_list'))

    def visit_definition_list_item(self, node):
        self.body.append(self.comment('visit_definition_list_item'))

    def depart_definition_list_item(self, node):
        self.body.append(self.comment('depart_definition_list_item'))

## - - - - - - - - - -
## IMPLEMENTED NODES
## - - - - - - - - - -

    def visit_Text(self, node):
        data = node.astext()
        self.body.append(data.replace('-','\-'))
        #self.body.append(self.comment('visit_Text'))

    def depart_Text(self, node):
        pass

    def visit_title(self, node):
        self.body.append(self.comment('visit_title. Level: %s' % self.section_level))
        if self.section_level == 0:
            self.body.append('\n.TH ') # don't remove the space
            self.section_level += 1

    def depart_title(self, node):
        #self.section_level -= 1
        self.body.append('\n')
        self.body.append(self.comment('depart_title'))

    def visit_paragraph(self, node):
        self.body.append(self.comment('visit_paragraph'))
        # don't paragraph a paragraph that is in an option list item:
        if not 'option_list_item' in self.context:
            self.body.append('\n.PP\n')
        # don't paragraph just after a section:
        if not 'section' in self.context:
            self.body.append('\n.PP\n')

##         if len(self.context):
##             if not self.context[-1] == 'option_list_item':
##                 self.body.append('\n.PP\n')
##         else:
##             self.body.append('\n.PP\n')

    def depart_paragraph(self, node):
        self.body.append('\n')
        self.body.append(self.comment('depart_paragraph'))

    def visit_strong(self, node):
        self.body.append('\\fB')

    def depart_strong(self, node):
        self.body.append('\\fR')

    def visit_comment(self, node):
        self.body.append('\n.\\" ')

    def depart_comment(self, node):
        return

    def visit_literal_block(self, node):
        self.body.append('\n.nf\n')
        self.body.append(self.comment('visit_literal_block'))

    def depart_literal_block(self, node):
        self.body.append('\n.fi\n')
        self.body.append(self.comment('depart_literal_block'))

    def visit_option_list(self, node):
        self.body.append(self.comment('visit_option_list'))

    def depart_option_list(self, node):
        self.body.append(self.comment('depart_option_list'))

    def visit_option_list_item(self, node):
        self.body.append(self.comment('visit_option_list_item'))
        self.body.append('\n.TP 10\n')
        self.context.add('option_list_item')

    def depart_option_list_item(self, node):
        self.body.append(self.comment('depart_option_list_item'))
        self.context.discard('option_list_item')

    def visit_option_group(self, node):
        self.body.append(self.comment('visit_option_group'))

    def depart_option_group(self, node):
        self.body.append(self.comment('depart_option_group'))

    def visit_option(self, node):
        self.body.append(self.comment('visit_option'))

    def depart_option(self, node):
        self.body.append(self.comment('depart_option'))

    def visit_option_string(self, node):
        self.body.append(self.comment('visit_option_string'))
        self.body.append('\\fB')

    def depart_option_string(self, node):
        self.body.append('\\fR ')
        self.body.append(self.comment('depart_option_string'))

    def visit_option_argument(self, node):
        self.body.append(self.comment('visit_option_argument'))
        self.body.append('\\fI')

    def depart_option_argument(self, node):
        self.body.append('\\fR ')
        self.body.append(self.comment('depart_option_argument'))

## - - - - - - - - - - - -
## NOT IMPLEMENTED NODES
## - - - - - - - - - - - -

    def visit_title_reference(self, node):
        raise NotImplementedError, node.astext()
        self.body.append(self.starttag(node, 'cite', ''))

    def depart_title_reference(self, node):
        raise NotImplementedError, node.astext()
        self.body.append('[[/cite]]')

    def visit_address(self, node):
        raise NotImplementedError, node.astext()
        self.visit_docinfo_item(node, 'address', meta=None)

    def depart_address(self, node):
        self.depart_docinfo_item()

    def visit_admonition(self, node, name):
        raise NotImplementedError, node.astext()
        self.body.append(self.starttag(node, 'div', CLASS=name))
        self.body.append('[[p class="admonition-title"]]'
                         + self.language.labels[name] + '[[/p]]\n')

    def depart_admonition(self):
        raise NotImplementedError, node.astext()
        self.body.append('[[/div]]\n')

    def visit_attention(self, node):
        self.visit_admonition(node, 'attention')

    def depart_attention(self, node):
        self.depart_admonition()

    def visit_author(self, node):
        self.visit_docinfo_item(node, 'author')

    def depart_author(self, node):
        self.depart_docinfo_item()

    def visit_authors(self, node):
        pass

    def depart_authors(self, node):
        pass

    def visit_block_quote(self, node):
        self.body.append(self.comment('visit_block_quote'))

    def depart_block_quote(self, node):
        self.body.append(self.comment('depart_block_quote'))

    def check_simple_list(self, node):
        raise NotImplementedError, node.astext()
        """Check for a simple list that can be rendered compactly."""
        visitor = SimpleListChecker(self.document)
        try:
            node.walk(visitor)
        except nodes.NodeFound:
            return None
        else:
            return 1

    def visit_bullet_list(self, node):
        self.body.append(self.comment('depart_bullet_list'))

    def depart_bullet_list(self, node):
        self.body.append(self.comment('depart_bullet_list'))

    def visit_caption(self, node):
        raise NotImplementedError, node.astext()
        self.body.append(self.starttag(node, 'p', '', CLASS='caption'))

    def depart_caption(self, node):
        raise NotImplementedError, node.astext()
        self.body.append('[[/p]]\n')

    def visit_caution(self, node):
        self.visit_admonition(node, 'caution')

    def depart_caution(self, node):
        self.depart_admonition()

    def visit_citation(self, node):
        raise NotImplementedError, node.astext()
        self.body.append(self.starttag(node, 'table', CLASS='citation',
                                       frame="void", rules="none"))
        self.body.append('[[colgroup]][[col class="label" /]][[col /]][[/colgroup]]\n'
                         '[[col /]]\n'
                         '[[tbody valign="top"]]\n'
                         '[[tr]]')
        self.footnote_backrefs(node)

    def depart_citation(self, node):
        raise NotImplementedError, node.astext()
        self.body.append('[[/td]][[/tr]]\n'
                         '[[/tbody]]\n[[/table]]\n')

    def visit_citation_reference(self, node):
        raise NotImplementedError, node.astext()
        href = ''
        if node.has_key('refid'):
            href = '#' + node['refid']
        elif node.has_key('refname'):
            href = '#' + self.document.nameids[node['refname']]
        self.body.append(self.starttag(node, 'a', '[', href=href,
                                       CLASS='citation-reference'))

    def depart_citation_reference(self, node):
        raise NotImplementedError, node.astext()
        self.body.append('][[/a]]')

    def visit_classifier(self, node):
        raise NotImplementedError, node.astext()
        self.body.append(' [[span class="classifier-delimiter"]]:[[/span]] ')
        self.body.append(self.starttag(node, 'span', '', CLASS='classifier'))

    def depart_classifier(self, node):
        raise NotImplementedError, node.astext()
        self.body.append('[[/span]]')

    def visit_colspec(self, node):
        self.colspecs.append(node)

    def depart_colspec(self, node):
        pass

    def write_colspecs(self):
        raise NotImplementedError, node.astext()
        width = 0
        for node in self.colspecs:
            width += node['colwidth']
        for node in self.colspecs:
            colwidth = int(node['colwidth'] * 100.0 / width + 0.5)
            self.body.append(self.emptytag(node, 'col',
                                           width='%i%%' % colwidth))
        self.colspecs = []

##     def visit_comment(self, node,
##                       sub=re.compile('-(?=-)').sub):
##         raise NotImplementedError, node.astext()
##         """Escape double-dashes in comment text."""
##         self.body.append('[[!-- %s --]]\n' % sub('- ', node.astext()))
##         # Content already processed:
##         raise nodes.SkipNode
## 
    def visit_contact(self, node):
        self.visit_docinfo_item(node, 'contact')

    def depart_contact(self, node):
        self.depart_docinfo_item()

    def visit_copyright(self, node):
        self.visit_docinfo_item(node, 'copyright')

    def depart_copyright(self, node):
        self.depart_docinfo_item()

    def visit_danger(self, node):
        self.visit_admonition(node, 'danger')

    def depart_danger(self, node):
        self.depart_admonition()

    def visit_date(self, node):
        self.visit_docinfo_item(node, 'date')

    def depart_date(self, node):
        self.depart_docinfo_item()

    def visit_decoration(self, node):
        pass

    def depart_decoration(self, node):
        pass

    def visit_description(self, node):
        self.body.append('\n')

    def depart_description(self, node):
        pass

    def visit_docinfo(self, node):
        self.body.append(self.comment('visit_docinfo'))

    def depart_docinfo(self, node):
        self.body.append(self.comment('depart_docinfo'))

    def visit_docinfo_item(self, node, name):
        self.body.append(self.comment('%s: ' % self.language.labels[name]))
        if len(node):
            if isinstance(node[0], nodes.Element):
                node[0].set_class('first')
            if isinstance(node[0], nodes.Element):
                node[-1].set_class('last')

    def depart_docinfo_item(self):
        pass

    def visit_doctest_block(self, node):
        raise NotImplementedError, node.astext()
        self.body.append(self.starttag(node, 'pre', CLASS='doctest-block'))

    def depart_doctest_block(self, node):
        raise NotImplementedError, node.astext()
        self.body.append('\n[[/pre]]\n')

    def visit_document(self, node):
        self.body.append(self.comment(self.document_start))
        # BUG ad date and revision
        # BUG where do we get the name and the filemodification date.
        # self.body.append('.TH FOO 1 "%s" "Linux User Manuals"\n' % time.strftime("%B %Y"))

    def depart_document(self, node):
        self.body.append(self.comment('Generated by docutils ManPageWriter on %s.\n' 
                                    % (time.strftime('%Y-%m-%d %H:%M')) ) )

    def visit_emphasis(self, node):
        self.body.append('\n.I ')

    def depart_emphasis(self, node):
        self.body.append('\n')

    def visit_enumerated_list(self, node):
        self.body.append(self.comment('visit_enumerated_list'))

    def depart_enumerated_list(self, node):
        self.body.append(self.comment('depart_enumerated_list'))

    def visit_error(self, node):
        self.visit_admonition(node, 'error')

    def depart_error(self, node):
        self.depart_admonition()

    def visit_field(self, node):
        self.body.append(self.comment('visit_field'))

    def depart_field(self, node):
        self.body.append(self.comment('depart_field'))

    def visit_field_body(self, node):
        self.body.append(self.comment('visit_field_body'))
        if len(node):
            node[0].set_class('first')
            node[-1].set_class('last')

    def depart_field_body(self, node):
        self.body.append(self.comment('depart_field_body'))

    def visit_field_list(self, node):
        self.body.append(self.comment('visit_field_list'))

    def depart_field_list(self, node):
        self.body.append(self.comment('depart_field_list'))

    def visit_field_name(self, node):
        raise NotImplementedError, node.astext()
##         self.body.append(self.comment('visit_field_name'))
##         atts = {}
##         if self.in_docinfo:
##             atts['class'] = 'docinfo-name'
##         else:
##             atts['class'] = 'field-name'
##         if len(node.astext()) > 14:
##             atts['colspan'] = 2
##             self.context.append('[[/tr]]\n[[tr]][[td]]&nbsp;[[/td]]')
##         else:
##             self.context.append('')
##         self.body.append(self.comment('atts'))

    def depart_field_name(self, node):
        self.body.append(self.comment('depart_field_name'))

    def visit_figure(self, node):
        raise NotImplementedError, node.astext()
##         self.body.append(self.starttag(node, 'div', CLASS='figure'))

    def depart_figure(self, node):
        raise NotImplementedError, node.astext()
##         self.body.append('[[/div]]\n')

    def visit_footer(self, node):
        raise NotImplementedError, node.astext()
        #self.context.append(len(self.body))

    def depart_footer(self, node):
        raise NotImplementedError, node.astext()
##         start = self.context.pop()
##         footer = (['[[hr class="footer"/]]\n',
##                    self.starttag(node, 'div', CLASS='footer')]
##                   + self.body[start:] + ['[[/div]]\n'])
##         self.body_suffix[:0] = footer
##         del self.body[start:]

    def visit_footnote(self, node):
        raise NotImplementedError, node.astext()
##         self.body.append(self.starttag(node, 'table', CLASS='footnote',
##                                        frame="void", rules="none"))
##         self.body.append('[[colgroup]][[col class="label" /]][[col /]][[/colgroup]]\n'
##                          '[[tbody valign="top"]]\n'
##                          '[[tr]]')
##         self.footnote_backrefs(node)

    def footnote_backrefs(self, node):
        raise NotImplementedError, node.astext()
##         if self.settings.footnote_backlinks and node.hasattr('backrefs'):
##             backrefs = node['backrefs']
##             if len(backrefs) == 1:
##                 self.context.append('')
##                 self.context.append('[[a class="fn-backref" href="#%s" '
##                                     'name="%s"]]' % (backrefs[0], node['id']))
##             else:
##                 i = 1
##                 backlinks = []
##                 for backref in backrefs:
##                     backlinks.append('[[a class="fn-backref" href="#%s"]]%s[[/a]]'
##                                      % (backref, i))
##                     i += 1
##                 self.context.append('[[em]](%s)[[/em]] ' % ', '.join(backlinks))
##                 self.context.append('[[a name="%s"]]' % node['id'])
##         else:
##             self.context.append('')
##             self.context.append('[[a name="%s"]]' % node['id'])

    def depart_footnote(self, node):
        raise NotImplementedError, node.astext()
##         self.body.append('[[/td]][[/tr]]\n'
##                          '[[/tbody]]\n[[/table]]\n')

    def visit_footnote_reference(self, node):
        raise NotImplementedError, node.astext()
##         href = ''
##         if node.has_key('refid'):
##             href = '#' + node['refid']
##         elif node.has_key('refname'):
##             href = '#' + self.document.nameids[node['refname']]
##         format = self.settings.footnote_references
##         if format == 'brackets':
##             suffix = '['
##             self.context.append(']')
##         elif format == 'superscript':
##             suffix = '[[sup]]'
##             self.context.append('[[/sup]]')
##         else:                           # shouldn't happen
##             suffix = '???'
##             self.content.append('???')
##         self.body.append(self.starttag(node, 'a', suffix, href=href,
##                                        CLASS='footnote-reference'))

    def depart_footnote_reference(self, node):
        raise NotImplementedError, node.astext()
##         self.body.append(self.context.pop() + '[[/a]]')

    def visit_generated(self, node):
        pass

    def depart_generated(self, node):
        pass

    def visit_header(self, node):
        raise NotImplementedError, node.astext()
        #self.context.add(len(self.body))

    def depart_header(self, node):
        raise NotImplementedError, node.astext()
##         start = self.context.pop()
##         self.body_prefix.append(self.starttag(node, 'div', CLASS='header'))
##         self.body_prefix.extend(self.body[start:])
##         self.body_prefix.append('[[hr /]]\n[[/div]]\n')
##         del self.body[start:]

    def visit_hint(self, node):
        self.visit_admonition(node, 'hint')

    def depart_hint(self, node):
        self.depart_admonition()

    def visit_image(self, node):
        raise NotImplementedError, node.astext()
##         atts = node.attributes.copy()
##         atts['src'] = atts['uri']
##         del atts['uri']
##         if not atts.has_key('alt'):
##             atts['alt'] = atts['src']
##         if isinstance(node.parent, nodes.TextElement):
##             self.context.append('')
##         else:
##             self.body.append('[[p]]')
##             self.context.append('[[/p]]\n')
##         self.body.append(self.emptytag(node, 'img', '', **atts))

    def depart_image(self, node):
        raise NotImplementedError, node.astext()
##         self.body.append(self.context.pop())

    def visit_important(self, node):
        self.visit_admonition(node, 'important')

    def depart_important(self, node):
        self.depart_admonition()

    def visit_label(self, node):
        raise NotImplementedError, node.astext()
##         self.body.append(self.starttag(node, 'td', '%s[' % self.context.pop(),
##                                        CLASS='label'))

    def depart_label(self, node):
        raise NotImplementedError, node.astext()
##         self.body.append('][[/a]][[/td]][[td]]%s' % self.context.pop())

    def visit_legend(self, node):
        raise NotImplementedError, node.astext()
##         self.body.append(self.starttag(node, 'div', CLASS='legend'))

    def depart_legend(self, node):
        raise NotImplementedError, node.astext()
##         self.body.append('[[/div]]\n')

    def visit_line_block(self, node):
        raise NotImplementedError, node.astext()
##         self.body.append(self.starttag(node, 'pre', CLASS='line-block'))

    def depart_line_block(self, node):
        raise NotImplementedError, node.astext()
##         self.body.append('\n[[/pre]]\n')

    def visit_list_item(self, node):
        self.body.append(self.comment('visit_list_item'))

    def depart_list_item(self, node):
        self.body.append(self.comment('depart_list_item'))

    def visit_literal(self, node):
        self.body.append(self.comment('visit_literal'))

    def depart_literal(self, node):
        self.body.append(self.comment('depart_literal'))

    def visit_meta(self, node):
        raise NotImplementedError, node.astext()
##         self.head.append(self.emptytag(node, 'meta', **node.attributes))

    def depart_meta(self, node):
        pass

    def visit_note(self, node):
        self.visit_admonition(node, 'note')

    def depart_note(self, node):
        self.depart_admonition()

    def visit_organization(self, node):
        raise NotImplementedError, node.astext()
        self.visit_docinfo_item(node, 'organization')

    def depart_organization(self, node):
        raise NotImplementedError, node.astext()
        self.depart_docinfo_item()

    def visit_problematic(self, node):
        raise NotImplementedError, node.astext()
        if node.hasattr('refid'):
            self.body.append('[[a href="#%s" name="%s"]]' % (node['refid'],
                                                           node['id']))
            self.context.append('[[/a]]')
        else:
            self.context.append('')
        self.body.append(self.starttag(node, 'span', '', CLASS='problematic'))

    def depart_problematic(self, node):
        raise NotImplementedError, node.astext()
        self.body.append('[[/span]]')
        self.body.append(self.context.pop())

    def visit_raw(self, node):
        raise NotImplementedError, node.astext()
        if node.get('format') == 'html':
            self.body.append(node.astext())
        # Keep non-HTML raw text out of output:
        raise nodes.SkipNode

    def visit_reference(self, node):
        """E.g. email address."""
        pass

    def depart_reference(self, node):
        pass

    def visit_revision(self, node):
        self.visit_docinfo_item(node, 'revision')

    def depart_revision(self, node):
        self.depart_docinfo_item()

    def visit_section(self, node):
        self.body.append(self.comment('visit_section'))
        self.body.append('\n.SH ')
        # BUG first section = title should say NAME for whatis database.
        self.section_level += 1
        self.context.add('section')

    def depart_section(self, node):
        self.section_level -= 1
        self.body.append('\n')
        self.body.append(self.comment('depart_section'))
        self.context.discard('section')

    def visit_status(self, node):
        raise NotImplementedError, node.astext()
        self.visit_docinfo_item(node, 'status', meta=None)

    def depart_status(self, node):
        self.depart_docinfo_item()

    def visit_substitution_definition(self, node):
        """Internal only."""
        raise nodes.SkipNode

    def visit_substitution_reference(self, node):
        self.unimplemented_visit(node)

    def visit_subtitle(self, node):
        #raise NotImplementedError, node.astext()
        self.body.append(self.starttag(node, 'h2', '', CLASS='subtitle'))

    def depart_subtitle(self, node):
        raise NotImplementedError, node.astext()
        self.body.append('[[/h2]]\n')

    def visit_system_message(self, node):
        pass
##         #raise NotImplementedError, node.astext()
##         if node['level'] < self.document.reporter['writer'].report_level:
##             # Level is too low to display:
##             raise nodes.SkipNode
##         self.body.append(self.starttag(node, 'div', CLASS='system-message'))
##         self.body.append('[[p class="system-message-title"]]')
##         attr = {}
##         backref_text = ''
##         if node.hasattr('id'):
##             attr['name'] = node['id']
##         if node.hasattr('backrefs'):
##             backrefs = node['backrefs']
##             if len(backrefs) == 1:
##                 backref_text = ('; [[em]][[a href="#%s"]]backlink[[/a]][[/em]]'
##                                 % backrefs[0])
##             else:
##                 i = 1
##                 backlinks = []
##                 for backref in backrefs:
##                     backlinks.append('[[a href="#%s"]]%s[[/a]]' % (backref, i))
##                     i += 1
##                 backref_text = ('; [[em]]backlinks: %s[[/em]]'
##                                 % ', '.join(backlinks))
##         if node.hasattr('line'):
##             line = ', line %s' % node['line']
##         else:
##             line = ''
##         if attr:
##             a_start = self.starttag({}, 'a', '', **attr)
##             a_end = '[[/a]]'
##         else:
##             a_start = a_end = ''
##         self.body.append('System Message: %s%s/%s%s ([[tt]]%s[[/tt]]%s)%s[[/p]]\n'
##                          % (a_start, node['type'], node['level'], a_end,
##                             node['source'], line, backref_text))

    def depart_system_message(self, node):
        pass
        #self.body.append('[[/div]]\n')

    def visit_target(self, node):
        self.body.append(self.comment('visit_target'))

    def depart_target(self, node):
        self.body.append(self.comment('depart_target'))

    def visit_term(self, node):
        self.body.append(self.comment('visit_term'))

    def depart_term(self, node):
        self.body.append(self.comment('depart_term'))

    def visit_tip(self, node):
        self.visit_admonition(node, 'tip')

    def depart_tip(self, node):
        self.depart_admonition()

    def visit_topic(self, node):
        self.body.append(self.comment('topic: '+node.astext()))
        raise nodes.SkipNode
        ##self.topic_class = node.get('class')

    def depart_topic(self, node):
        ##self.topic_class = ''
        pass

    def visit_transition(self, node):
        raise NotImplementedError, node.astext()
        self.body.append(self.emptytag(node, 'hr'))

    def depart_transition(self, node):
        pass

    def visit_version(self, node):
        raise NotImplementedError, node.astext()
        self.visit_docinfo_item(node, 'version', meta=None)

    def depart_version(self, node):
        self.depart_docinfo_item()

    def visit_warning(self, node):
        self.visit_admonition(node, 'warning')

    def depart_warning(self, node):
        self.depart_admonition()

    def unimplemented_visit(self, node):
        raise NotImplementedError('visiting unimplemented node type: %s'
                                  % node.__class__.__name__)


class SimpleListChecker(nodes.GenericNodeVisitor):

    """
    Raise `nodes.SkipNode` if non-simple list item is encountered.

    Here "simple" means a list item containing nothing other than a single
    paragraph, a simple list, or a paragraph followed by a simple list.
    """

    def default_visit(self, node):
        raise nodes.NodeFound

    def visit_bullet_list(self, node):
        pass

    def visit_enumerated_list(self, node):
        pass

    def visit_list_item(self, node):
        children = []
        for child in node.get_children():
            if not isinstance(child, nodes.Invisible):
                children.append(child)
        if (children and isinstance(children[0], nodes.paragraph)
            and (isinstance(children[-1], nodes.bullet_list)
                 or isinstance(children[-1], nodes.enumerated_list))):
            children.pop()
        if len(children) <= 1:
            return
        else:
            raise nodes.NodeFound

    def invisible_visit(self, node):
        """Invisible nodes should be ignored."""
        pass

    visit_comment = invisible_visit
    visit_substitution_definition = invisible_visit
    visit_target = invisible_visit
    visit_pending = invisible_visit

# vim: set et ts=4 ai :
