"""
A tag to include the javascript for loginas. Either inline javascript
(default, simple deployment) or external (Content Security Policy aware, bit
harder deployment)
"""

from django import template

from loginas.settings import CSP_FRIENDLY

register = template.Library()


@register.inclusion_tag(filename="loginas/javascript.html")
def javascript():
    return {"csp_aware": CSP_FRIENDLY}
