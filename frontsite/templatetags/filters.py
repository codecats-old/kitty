from django import template
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

@register.tag('++')
def increment_var(parser, token):

    parts = token.split_contents()
    if len(parts) < 2:
        raise template.TemplateSyntaxError("'increment' tag must be of the form:  {% increment <var_name> %}")
    return IncrementVarNode(parts[1])

class IncrementVarNode(template.Node):

    def __init__(self, var_name):
        self.var_name = var_name

    def render(self,context):
        try:
            value = context[self.var_name]
            context[self.var_name] = int(value) + 1
            return u""
        except:
            raise template.TemplateSyntaxError("The variable '%s' does not exist or not integer." % self.var_name)

@register.tag('set_int_var')
def set_var(parser, token):
    parts = token.split_contents()
    return SetVarNode(parts[1], parts[3])

class SetVarNode(template.Node):

    def __init__(self, new_val, var_name):
        self.new_val = new_val
        self.var_name = var_name

    def render(self, context):
        context[self.var_name] = int(self.new_val)
        return u''
