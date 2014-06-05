from django.template import Library

register = Library()

@register.filter(name = 'commatodot')
def commatodot(value, arg):
    return str(value).replace(",", '.')

@register.filter_function
def order_by(queryset, args):
    args = [x.strip() for x in args.split(',')]
    return queryset.order_by(*args)

