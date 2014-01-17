#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from misaka import HtmlRenderer, SmartyPants
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_by_name
import datetime
import misaka
from math import log
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

epoch = datetime.datetime(1970, 1, 1)
def epoch_seconds(date):
    """Returns the number of seconds from the epoch to date."""
    td = date - epoch
    return td.days * 86400 + td.seconds + (float(td.microseconds) / 1000000)

def hot_function(reply):
    s = reply.num_replies + reply.num_views/100
    order = log(max(abs(s), 1), 10)
    sign = 1 if s > 0 else -1 if s < 0 else 0
    seconds = epoch_seconds(reply.created_on) - 1134028003
    return round(order + sign * seconds / 45000, 7)