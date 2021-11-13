from django import template

register = template.Library()


@register.filter
def bootstrap_level_tag_map(value):
    bootstrap_level_tags = {
        'debug': 'dark',
        'info': 'info',
        'success': 'success',
        'warning': 'warning',
        'error': 'danger',
    }
    return bootstrap_level_tags[value]
