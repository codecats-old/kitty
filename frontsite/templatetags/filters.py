from django import template
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.template import Library
import re

register = Library()

@register.filter(name='shorter')
def shorter(value):
    #return value
    short = value.split('<p>')
    # cut text height (rows)
    short = short[:5]
    short = '<p>'.join(short)
    short = short.split('</p>\n')
    #cut text width (cols)
    for i, value in enumerate(short):
        #be careful with too low limit (base64)
        short[i] = value[:1000000]
    short = '</p>\n'.join(short)

    return short

@register.filter(name='ngmodel')
def ng_model(value, prefix='fields.'):
    attrs = value.field.widget.attrs
    value.field.widget.attrs['ng-model'] = prefix + value.name
    return str(value)

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

class SetVarNode(template.Node):
    def __init__(self, new_val, var_name):
        self.new_val = new_val
        self.var_name = var_name
    def render(self, context):
        context[self.var_name] = self.new_val
        return ''

@register.tag
def setvar(parser,token):
    # This version uses a regular expression to parse tag contents.
    try:
        # Splitting by None == splitting by spaces.
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires arguments" % token.contents.split()[0]
    m = re.search(r'(.*?) as (\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError, "%r tag had invalid arguments" % tag_name
    new_val, var_name = m.groups()
    if not (new_val[0] == new_val[-1] and new_val[0] in ('"', "'")):
        raise template.TemplateSyntaxError, "%r tag's argument should be in quotes" % tag_name
    return SetVarNode(new_val[1:-1], var_name)