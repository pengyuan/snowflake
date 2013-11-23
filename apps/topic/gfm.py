#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import misaka
from misaka import HtmlRenderer, SmartyPants
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_by_name
#Process github-flavored markdown


class HighlighterRenderer(HtmlRenderer, SmartyPants):
    def block_code(self, text, lang):
        s = ''
        if not lang:
            lang = 'text'
        try:
            lexer = get_lexer_by_name(lang, stripall=True)
        except:
            s += '<div class="highlight"><span class="err">Error: language "%s" is not supported</span></div>' % lang
            lexer = get_lexer_by_name('text', stripall=True)
        formatter = HtmlFormatter(noclasses = True)
        s += highlight(text, lexer, formatter)
        return s

    def table(self, header, body):
        return '<table class="table">\n'+header+'\n'+body+'\n</table>'

# And use the renderer
renderer = HighlighterRenderer(flags=misaka.HTML_ESCAPE | misaka.HTML_HARD_WRAP | misaka.HTML_SAFELINK)
md = misaka.Markdown(renderer,
    extensions=misaka.EXT_FENCED_CODE | misaka.EXT_NO_INTRA_EMPHASIS | misaka.EXT_TABLES | misaka.EXT_AUTOLINK | misaka.EXT_SPACE_HEADERS | misaka.EXT_STRIKETHROUGH | misaka.EXT_SUPERSCRIPT)

def gfm(text, extensions=None):
    return md.render(text)