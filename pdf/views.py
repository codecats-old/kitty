# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render
from easy_pdf.rendering import html_to_pdf
from easy_pdf.views import PDFTemplateView
from frontsite import models as frontsite_models


def generate(request):

    return HttpResponse(html_to_pdf('<h1>a</h1>'))


class HelloPDFView(PDFTemplateView):
    template_name = "rhymes.html"

    def get_context_data(self, **kwargs):
        kwargs['rhymes'] = [frontsite_models.Rhyme.objects.get(pk=kwargs['rhyme_id'])]
        return super(HelloPDFView, self).get_context_data(pagesize="A4", title="PDF", **kwargs)