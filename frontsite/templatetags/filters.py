from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.template import Library

register = Library()

@register.filter(name = 'commatodot')
def commatodot(value):
    return str(value).replace(",", '.')

@register.filter_function
def order_by(queryset, args):
    args = [x.strip() for x in args.split(',')]
    return queryset.order_by(*args)

@register.filter_function
def paginate(value, request):
    paginator = Paginator(value, 10)
    page = request.GET.get('page')
    try:
        value = paginator.page(page)
    except PageNotAnInteger:
        value = paginator.page(1)
    except EmptyPage:
        value = paginator.page(paginator.num_pages)
    return value