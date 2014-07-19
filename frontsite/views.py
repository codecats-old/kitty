# -*- coding: utf-8 -*-
import json
from random import randint
from django.contrib import auth
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Sum, Count
from django.utils.translation import ugettext as _
from django.utils import translation
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.core import serializers
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponse, QueryDict
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import View, FormView
from frontsite.decorators import anonymous_required, login_required
from frontsite.forms import UserForm, LoginForm, CategoryForm, AvatarForm, RhymeForm, CommentForm
from frontsite import models
from frontsite import utils

def delete_comment(request, id):
    comment = models.Comment.objects.get(pk=id)
    rhyme = comment.rhyme
    comment.delete()
    return redirect(reverse('frontsite:rhyme_view', kwargs={'id':rhyme.id}))

def rhyme_view(request, id):
    def find_comments(rhyme):
        comments = models.Comment.objects.all().filter(rhyme=rhyme).order_by('-date')
        paginator = Paginator(comments, 10)
        page = request.GET.get('page')
        try:
            comments = paginator.page(page)
        except PageNotAnInteger:
            comments = paginator.page(1)
        except EmptyPage:
            comments = paginator.page(paginator.num_pages)
        return comments
    rhyme = models.Rhyme.objects.annotate(vote_strength=Sum('votes__strength')).get(pk=id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.rhyme = rhyme
            comment.author = request.user.profile
            comment.save()
            return redirect(reverse('frontsite:rhyme_view', kwargs={'id': id}))
    else:
        form = CommentForm()
    return render(request, 'frontsite/rhyme_view.html', {
        'rhyme': rhyme,
        'comments': find_comments(rhyme),
        'form': form
    })

class Rhyme(FormView):
    template_name = 'frontsite/rhyme.html'

    def find_data(self):
        rhymes = models.Rhyme.objects.all()\
            .annotate(vote_strength=Sum('votes__strength'))\
            .order_by('-created')
        paginator = Paginator(rhymes, 10)
        page = self.request.GET.get('page')
        try:
            rhymes = paginator.page(page)
        except PageNotAnInteger:
            rhymes = paginator.page(1)
        except EmptyPage:
            rhymes = paginator.page(paginator.num_pages)
        return rhymes

    @method_decorator(login_required)
    def post(self, *args, **kwargs):
        form = RhymeForm(self.request.POST)
        if form.is_valid():
            rhyme = form.save(commit=False)
            if self.kwargs.has_key('id'):
                rhyme.id = self.kwargs['id']
            rhyme.author = self.request.user.profile
            rhyme.save()
            rhyme.profiles.add(self.request.user.profile)
            return  redirect(reverse('frontsite:index'))
        if self.request.is_ajax():
            form = RhymeForm(self.request.body)
            print self.request.body
            print '--------------------------|||'
            print form.errors
            #print form
            #return HttpResponse(form)

        return render(self.request, self.template_name, {
            'form': form,
            'rhymes': self.find_data(),
            'rhymesAuthor': self.request.user.profile.created_rhymes,
            'rhymesStored': self.request.user.profile.stored_rhymes
        })

    def get(self, *args, **kwargs):
        rhyme, rhymesAuthor, rhymesStored = (None, None, None)
        if hasattr(self.request.user, 'profile'):
            rhymesAuthor, rhymesStored = (self.request.user.profile.created_rhymes, self.request.user.profile.stored_rhymes)
        if self.kwargs.has_key('id'):
            rhyme = models.Rhyme.objects.get(pk=self.kwargs['id'])
            if self.kwargs.has_key('delete') and self.kwargs['delete'] == 'delete':
                rhyme.delete()
                return redirect(reverse('frontsite:index'))

        rhymes = self.find_data()
        for rhymeitem in rhymes:
            setattr(rhymeitem, 'comments_count', len(rhymeitem.comments.all()))
        return render(self.request, self.template_name, {
            'form': RhymeForm(instance=rhyme),
            'rhymes': rhymes,
            'rhymesAuthor': rhymesAuthor,
            'rhymesStored': rhymesStored
        })

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

def avatar(request):
    if 'file' in request.FILES:
        avatar = models.Avatar()
        avatar.path = utils.handle_uploaded_file(request.FILES['file'], request.POST['user_id'])
        avatar.name = request.POST['user_id']
        if hasattr(request.user.profile, 'avatar'):
            request.user.profile.avatar.delete()
        avatar.profile = request.user.profile
        avatar.save()
    return redirect(reverse('frontsite:user', kwargs={'id': request.POST['user_id']}))

def show_avatar(request, path):
    response = HttpResponse(content_type = "application/octet-stream")
    with open(path, 'r') as f: response.content = f.read()
    return response

class User(View):
    template_name = 'frontsite/user.html'

    @method_decorator(login_required)
    def get(self, *args, **kwargs):
        user = auth.models.User.objects.get(pk=self.kwargs.get('id'))
        votes = None
        strength_sum = None
        if hasattr(user, 'profile'):
            votes = models.VoteUserProfile.objects.filter(user_profile=user.profile).order_by('-date')
        if votes:
            aggregate = votes.aggregate(Sum('strength'))
            if hasattr(aggregate, 'strength__sum'):
                strength_sum = aggregate['strength__sum']
        return render(self.request, self.template_name, {
            'user': user,
            'votes': votes,
            'votes_strength_count': strength_sum,
            'avatarForm': AvatarForm()
        })

def get_all_users(request):
    users = auth.models.User.objects.all().annotate(vote_strength=Sum('profile__votes__strength'))
    paginator = Paginator(users, 20)
    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request, 'frontsite/all_users.html', {
        'users' : users
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

def vote_rhyme(request, rhyme_id):
    vote = models.VoteRhyme.objects.filter(author__id=request.user.profile.id, rhyme__id=rhyme_id)
    if not vote:
        vote = models.VoteRhyme()
        vote.author, vote.rhyme, vote.strength = (request.user.profile, models.Rhyme.objects.get(pk=rhyme_id), 1)
        vote.save()
    if request.is_ajax():
        rhyme = models.Rhyme.objects.all().filter(pk=rhyme_id).annotate(vote_strength=Sum('votes__strength'))[0]
        print '>>>>>>>>>>>>>>>>>>>>>>>>'
        print rhyme.vote_strength
        return HttpResponse(json.dumps({'strength': rhyme.vote_strength}))
    return redirect(reverse('frontsite:index'))

def rhyme_store(request, id):
    rhyme = models.Rhyme.objects.get(pk=id)
    if not models.UserProfile.objects.filter(pk=request.user.profile.id, stored_rhymes__in=[rhyme.id]):
        request.user.profile.stored_rhymes.add(rhyme)
        request.user.profile.save()
    return redirect(reverse('frontsite:stored'))

def rhyme_unstore(request, id):
    rhyme = models.Rhyme.objects.get(pk=id)
    if models.UserProfile.objects.filter(pk=request.user.profile.id, stored_rhymes__in=[rhyme.id]):
        request.user.profile.stored_rhymes.remove(rhyme)
        request.user.profile.save()
    return redirect(reverse('frontsite:stored'))

def stored(request):
    return render(request, 'frontsite/stored.html')

def random(request):
    rhyme, last = (None, None)
    last = models.Rhyme.objects.all().order_by('-id')
    if last:
        while rhyme is None:
            try:
                rhyme = models.Rhyme.objects.get(pk=randint(1, last[0].id))
            except:
                pass
    return render(request, 'frontsite/random.html', {
        'rhyme': rhyme
    })

def most_popular(request):
    mostLiked = models.Rhyme.objects.all().annotate(vote_strength=Sum('votes__strength')).order_by('-vote_strength')[:5]
    mostSaved = models.Rhyme.objects.all().annotate(saved_count=Count('profiles')).order_by('-saved_count')[:6]
    """
    mostSaved = models.Rhyme.objects.raw('''
        SELECT tab.id, SUM("frontsite_voterhyme"."strength") AS "vote_strength"
        FROM(
            SELECT
            "frontsite_rhyme"."id", "frontsite_rhyme"."title", "frontsite_rhyme"."content",    "frontsite_rhyme"."created", "frontsite_rhyme"."author_id", "frontsite_rhyme"."category_id",

            COUNT("frontsite_rhyme_profiles"."userprofile_id") AS "saved_count"
            FROM "frontsite_rhyme"
            LEFT OUTER JOIN "frontsite_rhyme_profiles" ON ( "frontsite_rhyme"."id" = "frontsite_rhyme_profiles"."rhyme_id" )
            GROUP BY "frontsite_rhyme"."id", "frontsite_rhyme"."title", "frontsite_rhyme"."content", "frontsite_rhyme"."created", "frontsite_rhyme"."author_id", "frontsite_rhyme"."category_id"
            ORDER BY "saved_count"
            DESC LIMIT 6
        )tab
        LEFT OUTER JOIN "frontsite_voterhyme" ON ( tab."id" = "frontsite_voterhyme"."rhyme_id" )
        GROUP BY tab.id
    ''')
    """
    #or
    """
    mostSaved = models.Rhyme.objects.all().annotate(
        saved_count=Count('profiles', distinct=True),
        vote_strength=Sum('votes__strength', distinct=True)
    ).order_by('-saved_count')[:6]
    """
    for rhyme in mostSaved:
        for liked in mostLiked:
            if liked.id == rhyme.id:
                setattr(rhyme, 'vote_strength', liked.vote_strength)
    return render(request, 'frontsite/popular.html', {
        'mostLiked': mostLiked,
        'mostSaved': mostSaved
    })