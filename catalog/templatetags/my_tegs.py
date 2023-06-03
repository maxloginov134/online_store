from django import template

register = template.Library()


@register.filter()
def app_media(val):
    if val:
        return f'/media/images/{val}'

    return '/static/no_image.jpg'
