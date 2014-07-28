# -*- coding: utf-8 -*-
from functools import wraps
import json
from django.http import HttpResponse
from django.shortcuts import render
from easy_pdf.rendering import html_to_pdf
from easy_pdf.views import PDFTemplateView
from os import path
#from frontsite import models as frontsite_models
import frontsite
from kitty.settings import BASE_DIR, SITE_ROOT


def generate(request):

    return HttpResponse(html_to_pdf('<h1>a</h1>'))


class ExporterPDFView(PDFTemplateView):
    template_name = "rhymes.html"

    def add_static_dir(func):
        @wraps(func)
        def wrapper(inst, *args, **kwargs):
            kwargs['STATIC_DIR'] = path.join(BASE_DIR, 'pdf', 'static', 'pdf')
            return func(inst, *args, **kwargs)
        return wrapper

    @add_static_dir
    def get_context_data(self, *args, **kwargs):
        if kwargs.has_key('rhyme_id'):
            kwargs['rhymes'] = [frontsite.models.Rhyme.objects.get(pk=kwargs['rhyme_id'])]
        elif kwargs.has_key('context'):
            if kwargs['context'] == 'all':
                kwargs['rhymes'] = frontsite.models.Rhyme.objects.all()
            elif kwargs['context'] == 'favorite':
                kwargs['rhymes'] = self.request.user.profile.stored_rhymes.all()
            else:
                ids = json.loads(kwargs['context'])
                kwargs['rhymes'] = frontsite.models.Rhyme.objects.all().filter(id__in=ids)
                print kwargs['rhymes']
        return super(ExporterPDFView, self).get_context_data(pagesize="A4", title="PDF", **kwargs)