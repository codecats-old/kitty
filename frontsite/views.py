# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import render
from django.views.generic import View, FormView
from frontsite.forms import UserForm, LoginForm


class Index(View):
    template_name = 'frontsite/index.html'
    def get(self, request):
        return render(request, self.template_name)

class Login(FormView):
    model = User
    template_name = 'frontsite/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('frontsite:index')
    def form_valid(self, form):
        # form.authenticate()
        return super(Login, self).form_valid(form)

class Registration(FormView):
    model = User
    template_name = 'frontsite/registration.html'
    form_class = UserForm
    success_url = reverse_lazy('frontsite:index')
    def form_valid(self, form):
        form.save()
        return super(Registration, self).form_valid(form)

def login(request):
    pass