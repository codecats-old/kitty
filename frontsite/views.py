# -*- coding: utf-8 -*-
import json
from django.contrib import auth
from django.utils.translation import ugettext as _
from django.utils import translation
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.core import serializers
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import View, FormView
from frontsite.decorators import anonymous_required, login_required
from frontsite.forms import UserForm, LoginForm, CategoryForm
from frontsite import models

class Index(View):
    template_name = 'frontsite/index.html'
    @method_decorator(login_required)
    def get(self, request):
        print '>>>>', _('klucz')
        return render(request, self.template_name)

class Category(FormView):
    def post(self, request):
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            return redirect(reverse('frontsite:category'))
        return render(request, 'frontsite/category.html', {
            'form' : form
        })
    def get(self, request):
        categories = models.Category.objects.all()
        return render(request, 'frontsite/category.html', {
            'form' : CategoryForm(),
            'categories': categories
        })

class User(View):
    @method_decorator(login_required)
    def delete(self, request):
        return HttpResponse('[{"delete":1}]', content_type='application/json')
    @method_decorator(login_required)
    def post(self, request):
        return HttpResponse('[{"post":1}]', content_type='application/json')
    @method_decorator(login_required)
    def put(self, request):
        return HttpResponse('[{"put":1}]', content_type='application/json')
    @method_decorator(login_required)
    def get(self, request):
        try:
            user_profile = models.UserProfile.objects.get(user_id=request.user.id)
        except:
            user_profile = None
        if request.is_ajax():
            json = serializers.serialize('json', [request.user, user_profile])
            return HttpResponse(json, content_type='application/json')
        else:
            pass

class Locale(View):
    def get(self, request, lang):
        if self.kwargs['lang'] != None:
            translation.activate(self.kwargs['lang'])
            print '>>LOCALE>>', _('klucz')
        return redirect(reverse('frontsite:index'))
def token(request):
    return HttpResponse(_('klucz') + request.COOKIES.get('csrftoken'))

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
    def form_valid(self, form):
        form.save()
        return super(Registration, self).form_valid(form)
    @method_decorator(anonymous_required)
    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data(form=self.form_class()))
