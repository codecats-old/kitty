# -*- coding: utf-8 -*-
import json
from django.contrib import auth
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
from frontsite.forms import UserForm, LoginForm
from frontsite.models import UserProfile


class Index(View):
    template_name = 'frontsite/index.html'
    @method_decorator(login_required)
    def get(self, request):
        if request.user.is_authenticated() is False:
            return redirect(reverse('frontsite:login'))
        return render(request, self.template_name)

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
            user_profile = UserProfile.objects.get(user_id=request.user.id)
        except:
            user_profile = None
        if request.is_ajax():
            json = serializers.serialize('json', [request.user, user_profile])
            return HttpResponse(json, content_type='application/json')

def token(request):
    return HttpResponse(request.COOKIES.get('csrftoken'))

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
