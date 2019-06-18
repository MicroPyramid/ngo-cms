from django import template

register = template.Library()


@register.filter(name='imgname')
def imgname(value):
    x = value.split(' / ')
    print(x)
    return x[-1]


@register.filter(name='menu_count')
def menu_count(menus):
    men = 0
    for m in menus:
        if m.is_active:
            men = men + 1
    return men
