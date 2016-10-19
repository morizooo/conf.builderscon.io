import builderscon
import flasktools
import markdown
import markupsafe
import mdx_gfm
import model
import oauth
import oembed
import re

SESSION_SLIDE_EMBED_EXPIRES = 3600
SESSION_VIDEO_EMBED_EXPIRES = 3600

oembed_consumer = oembed.OEmbedConsumer()
oembed_endpoints = [
    [ 'https://www.youtube.com/oembed', [ 'https://*.youtube.com/*' ] ],
    [ 'http://www.slideshare.net/api/oembed/2', [ 'http://www.slideshare.net/*' ] ],
    [ 'http://speakerdeck.com/oembed.json', [ 'https://speakerdeck.com/*' ], ],
]
for ent in oembed_endpoints:
    e = oembed.OEmbedEndpoint(*ent)
    oembed_consumer.addEndpoint(e)

@builderscon.app.template_filter('video_embed')
def video_embed(url, **opt):
    key = "session.video.embed.html.%s" % url
    html = builderscon.cache.get(key)
    if html:
        return html

    o = flasktools.urlparse(url)
    if re.search(r'youtube\.com$', o.netloc, flags=re.UNICODE):
        if 'maxwidth' not in opt:
            opt['maxwidth'] = 600
        if 'maxheight' not in opt:
            opt['maxheight'] = 480
        res = oembed_consumer.embed(url, **opt)
        html = res['html']
        builderscon.cache.set(key, html, SESSION_VIDEO_EMBED_EXPIRES)
        return html
    html = '<a href="%s">%s</a>' % (url, url)
    builderscon.cache.set(key, html, SESSION_VIDEO_EMBED_EXPIRES)
    return html

@builderscon.app.template_filter('slide_embed')
def slide_embed(url):
    key = "session.slide.embed.html.%s" % url
    html = builderscon.cache.get(key)
    if html:
        return html

    o = flasktools.urlparse(url)
    if re.search(r'(slideshare\.net|speakerdeck\.com)$', o.netloc, flags=re.UNICODE):
        res = oembed_consumer.embed(url)
        html = res['html']
        builderscon.cache.set(key, html, SESSION_SLIDE_EMBED_EXPIRES)
        return html
    elif re.search(r'^docs\.google\.com$', o.netloc, flags=re.UNICODE):
        url = re.sub(r'/pub\?', '/embed?', url)
        o = flasktools.urlparse(url)
        q = flasktools.parse_qsl(o.query)
        q.append(('width', 400))
        html = '<iframe src="%s" frameborder="0" width="500" height="450"allowfullscreen="true" mozallowfullscreen="true" webkitallowfullscreen="true"></iframe>' % flasktools.urlunparse(o)
        html = res['html']
        builderscon.cache.set(key, html, SESSION_SLIDE_EMBED_EXPIRES)
        return html

    html = '<a href="%s">%s</a>' % (url, url)
    builderscon.cache.set(key, html, SESSION_SLIDE_EMBED_EXPIRES)
    return html

@builderscon.app.template_filter('dateobj')
def dateobj_filter(s, lang='en', timezone='UTC'): # note: this is probably going to be deprecated
    return model.ConferenceDate(s, lang=lang, timezone=timezone)

markdown_converter = markdown.Markdown(extensions=[mdx_gfm.GithubFlavoredMarkdownExtension()]).convert
@builderscon.app.template_filter('markdown')
def markdown_filter(s):
    return markdown_converter(s)

@builderscon.app.template_filter('audlevelname')
def audience_level_value_to_name(v):
    return v.title()

# Used in templates, when all you have is the user's input value
@builderscon.app.template_filter('langname')
def lang_value_to_name(v):
    for l in builderscon.LANGUAGES:
        if l.get('value') == v:
            return l.get('name')
    return ""

# Used in templates, when all you have is the user's input value
@builderscon.app.template_filter('permname')
def permission_value_to_name(v):
    return v.title()

@builderscon.app.template_filter('is_oauth_error')
def is_oauth_error(v):
    return type(v) is oauth.Error

@builderscon.app.template_filter('urlencode')
def urlencode_filter(s):
    if type(s) == 'Markup':
        s = s.unescape()
    s = s.encode('utf8')
    s = flasktools.quote_plus(s)
    return markupsafe.Markup(s)

