import bleach

from django import template

from markdown import Extension, markdown as markdown_fn
from markdown.inlinepatterns import (
    AUTOLINK_RE,
    AUTOMAIL_RE,
    AutolinkPattern,
    AutomailPattern,
    LINK_RE,
    LinkPattern,
    REFERENCE_RE,
    ReferencePattern,
    SHORT_REF_RE,
)

register = template.Library()


@register.filter(name="markdown")
def markdown(value):
    return markdown_fn(value, extensions=[NewTabExtension(), "markdown.extensions.attr_list"])


@register.filter("limit_markdown")
def limit_markdown(data):
    comment = bleach.clean(data, tags=["b", "i", "em", "a", "strong"], strip=True)
    return comment


class NewTabExtensionMixin(object):
    def handleMatch(self, m):
        el = super(NewTabExtensionMixin, self).handleMatch(m)
        if el is not None:
            el.set("target", "_blank")
        return el


class NewTabExtensionLinkPattern(NewTabExtensionMixin, LinkPattern):
    pass


class NewTabExtensionReferencePattern(NewTabExtensionMixin, ReferencePattern):
    pass


class NewTabExtensionAutolinkPattern(NewTabExtensionMixin, AutolinkPattern):
    pass


class NewTabExtensionAutomailPattern(NewTabExtensionMixin, AutomailPattern):
    pass


class NewTabExtension(Extension):

    """Modifies HTML output to open links in a new tab."""

    def extendMarkdown(self, md, *args):
        md.inlinePatterns["link"] = NewTabExtensionLinkPattern(LINK_RE, md)
        md.inlinePatterns["reference"] = NewTabExtensionReferencePattern(REFERENCE_RE, md)
        md.inlinePatterns["short_reference"] = NewTabExtensionReferencePattern(SHORT_REF_RE, md)
        md.inlinePatterns["autolink"] = NewTabExtensionAutolinkPattern(AUTOLINK_RE, md)
        md.inlinePatterns["automail"] = NewTabExtensionAutomailPattern(AUTOMAIL_RE, md)
