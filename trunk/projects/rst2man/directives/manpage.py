# Author: Olivier Laurent
# Contact: olilau.p@gmail.com
# Revision: $Revision: $
# Date: $Date: $
# Copyright: This module has been placed in the public domain.

# Reference: http://www.linuxinfor.com/english/man7/man.html
# Example:
# .TH azureus "1"     "October 2004" "azureus 2.1.0.4" "User Commands"
#     title   section date           source             manual


"""
Directives for manpages.
"""

__docformat__ = 'reStructuredText'

from docutils import nodes, languages
from docutils.transforms import parts
from docutils.parsers.rst import directives


class ManPageTitle:
    def __init__(self, title, section='', date='', source='', manual=''):
        self.title = title
        self.section = section
        self.date = date
        self.source = source
        self.manual = manual

    def get_param_dict(self):
        return dict(title='''"%s"''' % self.title,
                    section='''"%s"''' % self.section,
                    date='''"%s"''' % self.date,
                    source='''"%s"''' % self.source,
                    manual='''"%s"''' % self.manual
                   )

    def render(self):
        return self.__str__()

    def __str__(self):
        dico = self.get_param_dict()
        return '%(title)s %(section)s %(date)s %(source)s %(manual)s' % dico


def manpage(name, arguments, options, content, lineno,
            content_offset, block_text, state, state_machine):
    """Man Page."""
    document = state_machine.document
    title_text = ManPageTitle(options.get('title', ''), # default to filename ?
                              options.get('section', '1'),
                              options.get('date', ''),
                              options.get('source', ''),
                              options.get('manual', '')
                             ).render()
    textnodes, messages = state.inline_text(title_text, lineno)
    titles = [nodes.Text(title_text, *textnodes)]
    text = '\n'.join(content)
    node_class = nodes.title
    node = node_class(text, *(titles + messages))
    return [node]

manpage.arguments = (0, 1, 1)
manpage.options = {
                    'title': directives.unchanged,
                    'section': directives.positive_int,
                    'date': directives.unchanged,
                    'source': directives.unchanged,
                    'manual': directives.unchanged
                  }
manpage.content = False

