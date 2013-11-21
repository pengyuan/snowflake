import hashlib
import markdown as markdown_lib
import re

def gfm(text):
    """Processes Markdown according to GitHub Flavored Markdown spec."""
    extractions = {}

    def extract_pre_block(matchobj):
        match = matchobj.group(0)
        hashed_match = hashlib.md5(match.encode('utf-8')).hexdigest()
        extractions[hashed_match] = match
        result = "{gfm-extraction-%s}" % hashed_match
        return result

    def escape_underscore(matchobj):
        match = matchobj.group(0)

        if match.count('_') > 1:
            return re.sub('_', '\_', match)
        else:
            return match

    def newlines_to_brs(matchobj):
        match = matchobj.group(0)
        if re.search("\n{2}", match):
            return match
        else:
            match = match.strip()
            return match + "  \n"

    def insert_pre_block(matchobj):
        string = "\n\n" + extractions[matchobj.group(1)]
        return string
    
    # Configuration for urlize() function
    LEADING_PUNCTUATION  = ['(', '<', '&lt;']
    TRAILING_PUNCTUATION = ['.', ',', ')', '>', '\n', '&gt;']
     
    word_split_re = re.compile(r'(\s+)')
    punctuation_re = re.compile('^(?P<lead>(?:%s)*)(?P<middle>.*?)(?P<trail>(?:%s)*)$' % \
        ('|'.join([re.escape(x) for x in LEADING_PUNCTUATION]),
        '|'.join([re.escape(x) for x in TRAILING_PUNCTUATION])))
    simple_email_re = re.compile(r'^\S+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9._-]+$')

    def autolink(text, trim_url_limit=None, nofollow=False):
        """
        Converts any URLs in text into clickable links. Works on http://, https:// and
        www. links. Links can have trailing punctuation (periods, commas, close-parens)
        and leading punctuation (opening parens) and it'll still do the right thing.
     
        If trim_url_limit is not None, the URLs in link text will be limited to
        trim_url_limit characters.
     
        If nofollow is True, the URLs in link text will get a rel="nofollow" attribute.
        """
        trim_url = lambda x, limit=trim_url_limit: limit is not None and (x[:limit] + (len(x) >=limit and '...' or ''))  or x
        words = word_split_re.split(text)
        nofollow_attr = nofollow and ' rel="nofollow"' or ''
        for i, word in enumerate(words):
            match = punctuation_re.match(word)
            if match:
                lead, middle, trail = match.groups()
                #Let guys without 'http://' go
                if middle.startswith('http://') or middle.startswith('https://'):
                    middle = '<a href="%s"%s target="_blank">%s</a>' % (middle, nofollow_attr, trim_url(middle))
                if '@' in middle and not middle.startswith('www.') and not ':' in middle \
                    and simple_email_re.match(middle):
                    middle = '<a href="mailto:%s">%s</a>' % (middle, middle)
                if lead + middle + trail != word:
                    words[i] = lead + middle + trail
        return ''.join(words)
    
    
    text = re.sub("<pre>.*?<\/pre>", extract_pre_block, text, flags=re.S)
    #text = re.sub("(^(?! {4}|\t)\w+_\w+_\w[\w_]*)", escape_underscore, text)
    
    text = re.sub("\{gfm-extraction-([0-9a-f]{32})\}", insert_pre_block, text)
    text = autolink(text)
    text = re.sub("^[\w\<][^\n]*\n+", newlines_to_brs, text, flags=re.M)
#     str = str.replace(/\n/g,"<br />");  // ** GFM **
#                     str = str.replace(/^([ \t]*)/g, "<p>");
#                     str += "</p>"

    return text

def markdown(text):
    """Processes GFM then converts it to HTML."""
    text = gfm(text)
    text = markdown_lib.markdown(text)
    return text
