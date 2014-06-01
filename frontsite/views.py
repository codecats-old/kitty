# -*- coding: utf-8 -*-
import json
from django.contrib import auth
from django.db.models import Sum
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
    def find_data(self):
        return models.Category.objects.all().order_by('-id')
    def find_detail(self):
        result = None
        if self.kwargs.has_key('id'):
            result = models.Category.objects.get(pk=self.kwargs['id'])
        return result
    @method_decorator(login_required)
    def post(self, *args, **kwargs):
        form = CategoryForm(self.request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            if self.kwargs.has_key('id'):
                category.id = self.kwargs['id']
            category.save()
            return redirect(reverse('frontsite:category'))
        return render(self.request, 'frontsite/category.html', {
            'form' : form,
            'category': self.find_detail(),
            'categories': self.find_data()
        })
    def get(self, *args, **kwargs):
        category = None
        if self.kwargs.has_key('id'):
            category = models.Category.objects.get(pk=self.kwargs['id'])
            if self.kwargs.has_key('delete') and self.kwargs['delete'] == 'delete':
                category.delete()
                return redirect(reverse('frontsite:category'))
        return render(self.request, 'frontsite/category.html', {
            'form' : CategoryForm(instance=category),
            'category': self.find_detail(),
            'categories': self.find_data()
        })

class User(FormView):
    template_name = 'frontsite/user.html'
    @method_decorator(login_required)
    def post(self, request):
        return HttpResponse('[{"post":1}]', content_type='application/json')
    @method_decorator(login_required)
    def get(self, *args, **kwargs):
        user = auth.models.User.objects.get(pk=self.kwargs.get('id'))
        #print user.profile.id
        votes = None
        if hasattr(user, 'profile'):
            votes = models.VoteUserProfile.objects.filter(user_profile=user.profile.id)\
                .annotate(Sum('strength')).order_by('-date')

        return render(self.request, self.template_name, {
            'user': user,
            'votes': votes
        })
def get_all_users(request):
    return render(request, 'frontsite/all_users.html', {
        'users' : auth.models.User.objects.all().annotate(vote_strength=Sum('profile__votes__strength'))
    })
class Locale(View):
    def get(self, request, lang):
        if self.kwargs['lang'] != None:
            translation.activate(self.kwargs['lang'])
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
        if hasattr(self.request.user, 'profile') == False:
            self.request.user.profile = models.UserProfile()
            self.request.user.profile.save()
            self.request.user.save()
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
def vote(request, profile_id):
    profile = models.UserProfile.objects.get(pk=profile_id)
    if profile and hasattr(request.user, 'profile'):
        vote = models.VoteUserProfile.objects.filter(author__id=request.user.profile.id, user_profile__id=profile.id)
        if not vote:
            vote = models.VoteUserProfile()
            vote.author, vote.user_profile, vote.strength = (request.user.profile, profile, 1)
            vote.save()
    return redirect(reverse('frontsite:all_users'))