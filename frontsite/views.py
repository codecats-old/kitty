# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import View

class IndexView(View):
    def get(self, request):
        return render(request, 'frontsite/index.html')

# def index(request):
#     return render(request, 'frontsite/index.html')

def registration(request):
    pass

def login(request):
    pass