from django import template


register = template.Library()


@register.filter('startswith')
def startswith(str, start):
    if str.startswith(start):
        return True
    return False
