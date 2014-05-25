# -*- coding: utf-8 -*-
from django.contrib import auth
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import View, FormView
from frontsite.decorators import anonymous_required
from frontsite.forms import UserForm, LoginForm


class Index(View):
    template_name = 'frontsite/index.html'
    def get(self, request):
        print '>>>',request.user.is_authenticated()
        if request.user.is_authenticated() is False:
            return redirect(reverse('frontsite:login'))
        return render(request, self.template_name)

class Logout(View):
    template_name = 'frontsite/logout.html'
    def get(self, request):
        logout(request)
        return redirect(reverse('frontsite:index'))

class Login(FormView):
    model = User
    template_name = 'frontsite/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('frontsite:index')
    @method_decorator(anonymous_required)
    def form_valid(self, form):
        auth.login(self.request, form.user)
        return super(Login, self).form_valid(form)
    @method_decorator(anonymous_required)
    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data(form=self.form_class()))

class Registration(FormView):
    model = User
    template_name = 'frontsite/registration.html'
    form_class = UserForm
    success_url = reverse_lazy('frontsite:index')
    @method_decorator(anonymous_required)
    def form_valid(self, form):
        form.save()
        return super(Registration, self).form_valid(form)
    @method_decorator(anonymous_required)
    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data(form=self.form_class()))
