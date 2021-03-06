# -*- coding: utf-8 -*-
import json
from random import randint
from django.contrib import auth, messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Sum, Count, Q
from django.forms import model_to_dict
from django.utils.translation import ugettext as _
from django.utils import translation
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.core import serializers
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponse, QueryDict, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import View, FormView
from frontsite.decorators import anonymous_required, login_required
from frontsite.forms import UserForm, LoginForm, CategoryForm, AvatarForm, RhymeForm, CommentForm, UserUpdateForm
from frontsite import models
from frontsite import utils

def typehead_search(request, query):
    rhymes = models.Rhyme.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))\
                .annotate(vote_strength=Sum('votes__strength'))
    if request.user.is_authenticated() and not request.user.is_staff:
        rhymes = rhymes.filter(Q(public=True) | Q(author=request.user.profile))
    if not request.user.is_authenticated():
        rhymes = rhymes.filter(public=True)
    rhymes = rhymes.order_by('-created')[:10]
    return HttpResponse(json.dumps(
        [dict(model_to_dict(item).items() + {'vote_strength': item.vote_strength}.items())  for item in rhymes]
    ))

@login_required
def count_author_rhyme_votes(request):
    author = request.user.profile
    authors_rhymes = models.Rhyme.objects.all().filter(author=author)
    strength = authors_rhymes.aggregate(vote_strength=Sum('votes__strength'))
    rhymes = authors_rhymes.annotate(vote_strength=Sum('votes__strength'))\
                .filter(vote_strength__gt=0).order_by('-vote_strength')[:10]
    data = []
    for rhyme in rhymes:
        model_items = model_to_dict(rhyme).items()
        external_items = {
            'vote_strength': rhyme.vote_strength if rhyme.vote_strength is not None else 0
        }.items()
        data.append(dict(model_items + external_items))
    return HttpResponse(json.dumps({
        'success': True,
        'strength': strength['vote_strength'],
        'data': data
    }))

@login_required
def map_order(request):
    maps = json.loads(request.body)[u'map']
    stored = models.RhymeProfiles.objects.all().filter(owner=request.user.profile)
    for map in maps:
        print map
        for store in stored:
            if int(map[u'id']) == store.id:
                store.position_no = map[u'position']
                store.save()
                messages.info(request, u'Zmieniono kolejność')
    return HttpResponse(json.dumps({
        'success': True
    }))

def voters(request, rhyme_id):
    votes = models.VoteRhyme.objects.all().filter(rhyme__id=rhyme_id)
    data = []
    for vote in votes:
        model_items = model_to_dict(vote).items()
        external_items = {
            'author_name': vote.author.user.username
        }.items()
        data.append(dict(model_items + external_items))
    return HttpResponse(json.dumps({
        'success': True,
        'data': data
    }))

def comment_show(request, rhyme_id):
    comments = models.Comment.objects.filter(rhyme_id=rhyme_id).order_by('-date')[:5]
    data = []
    for comment in comments:
        model_items = model_to_dict(comment).items()
        external_items = {
            'author_name': comment.author.user.username,
            'date': str(comment.date)
        }.items()
        data.append(dict(model_items + external_items))
    return HttpResponse(json.dumps({
        'success': True,
        'data': data
    }))

@login_required
def comments_unread(request):
    user = request.user.profile
    comments = models.Comment.objects.all().filter(rhyme_author_saw=False)\
        .filter(rhyme__author=user).exclude(author=user)[:10]
    data = []
    for comment in comments:
        model_items = model_to_dict(comment).items()
        external_items = {
            'author_name': comment.author.user.username,
            'rhyme_url': reverse('frontsite:rhyme_view', kwargs={'id': comment.rhyme.id}),
            'rhyme_title': comment.rhyme.title,
            'date': str(comment.date)
        }.items()
        data.append(dict(model_items + external_items))
    return HttpResponse(json.dumps({
        'success': True,
        'data': data,
        'count': len(comments)
    }))
def comments_mark_as_read(request, rhyme_id):
    comments = []
    if (not hasattr(request.user, 'profile')):
        return HttpResponse(json.dumps({'success': True}))
    profile = request.user.profile
    rhyme = models.Rhyme.objects.get(pk=rhyme_id)
    if rhyme.author.pk == profile.pk:
        comments = models.Comment.objects.all().filter(rhyme__id=rhyme_id)
        for comment in comments:
            comment.rhyme_author_saw = True
            comment.save()
    return HttpResponse(json.dumps({
        'success': True,
        'count': len(comments)
    }))

def comments_mark_as_read_json(request):
    profile = request.user.profile
    comments = json.loads(request.body)
    for comment_data in comments:
        comment = models.Comment.objects.get(pk=comment_data[u'id'])
        if comment.rhyme.author.pk == profile.pk:
            comment.rhyme_author_saw = True
            comment.save()

    return HttpResponse(json.dumps({
        'success': True,
        'count': len(comments)
    }))

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
        comments_mark_as_read(request, rhyme_id=id)
        form = CommentForm()
    return render(request, 'frontsite/rhyme_view.html', {
        'rhyme': rhyme,
        'comments': find_comments(rhyme),
        'form': form
    })

class Rhyme(FormView):
    template_name = 'frontsite/rhyme.html'

    def find_data(self, category_id=None, search=None):
        if category_id is None:
            rhymes = models.Rhyme.objects.all()\
                .annotate(vote_strength=Sum('votes__strength'))\
                .order_by('-created')
        else:
            rhymes = models.Rhyme.objects.filter(category=category_id)\
                .annotate(vote_strength=Sum('votes__strength'))\
                .order_by('-created')
        if search is not None:
            rhymes = rhymes.filter(Q(title__icontains=search) | Q(content__icontains=search))
        if self.request.user.is_authenticated() and not self.request.user.is_staff:
            rhymes = rhymes.filter(Q(public=True) | Q(author=self.request.user.profile))
        if not self.request.user.is_authenticated():
            rhymes = rhymes.filter(public=True)
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
        data = self.request.POST
        if self.request.is_ajax():
            data = json.loads(self.request.body)
        form = RhymeForm(data)
        form_is_valid = form.is_valid()
        if form_is_valid:
            author = self.request.user.profile
            rhyme = form.save(commit=False)
            if self.kwargs.has_key('id'):
                rhyme.id = self.kwargs['id']
                existing_rhyme = models.Rhyme.objects.get(pk=self.kwargs['id'])
                rhyme.created = existing_rhyme.created
                author = existing_rhyme.author

            rhyme.author = author
            rhyme.save()
            if models.RhymeProfiles.objects.filter(owner=author, rhyme=rhyme).count() == 0:
                store = models.RhymeProfiles()
                (store.owner, store.rhyme) = (author, rhyme)
                store.save()
            if not self.request.is_ajax():
                return  redirect(reverse('frontsite:index'))
            if form_is_valid:
                messages.info(self.request, u'Dane zostały zaakceptowane')
        if self.request.is_ajax():
            return HttpResponse(json.dumps({
                'valid': form_is_valid,
                'errors': [(k, form.error_class.as_text(v)) for k, v in form.errors.items()]
            }))

        return render(self.request, self.template_name, {
            'form': form,
            'rhymes': self.find_data(),
            'stored': models.Rhyme.objects.filter(profiles__owner=self.request.user.profile),
        })

    def delete(self, *args, **kwargs):
        if self.kwargs.has_key('id'):
            rhyme = models.Rhyme.objects.get(pk=self.kwargs['id'])
            if self.kwargs.has_key('delete') and self.kwargs['delete'] == 'delete':
                rhyme.delete()
        return HttpResponse(json.dumps({'success': True}))

    def get(self, *args, **kwargs):
        rhyme, stored = (None, None)
        if hasattr(self.request.user, 'profile'):
            stored = models.Rhyme.objects.filter(profiles__owner=self.request.user.profile)
        if self.kwargs.has_key('id'):
            rhyme = models.Rhyme.objects.get(pk=self.kwargs['id'])
            if self.kwargs.has_key('delete') and self.kwargs['delete'] == 'delete':
                rhyme.delete()
                return redirect(reverse('frontsite:index'))
        by_category, search = (None, self.request.GET.get('search'))
        if self.kwargs.has_key('category_id'):
            by_category = self.kwargs['category_id']
        rhymes = self.find_data(by_category, search)
        for rhymeitem in rhymes:
            setattr(rhymeitem, 'comments_count', len(rhymeitem.comments.all()))
        if self.request.is_ajax():
            return HttpResponse(json.dumps({
                'data': [model_to_dict(item) for item in rhymes]
            }))
        return render(self.request, self.template_name, {
            'form': RhymeForm(instance=rhyme),
            'rhymes': rhymes,
            'stored': stored,
            'categories' : models.Category.objects.all(),
            'search': search if search is not None else ''
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
    def put(self, *args, **kwargs):
        user = json.loads(self.request.body)
        if not self.request.user.is_staff and self.request.user.id != user['id']:
            return HttpResponseForbidden()
        form = UserUpdateForm(user, instance=auth.models.User.objects.get(id=user['id']))
        if form.is_valid():
            form.save()
            messages.info(self.request, u'Dane zmienione')

        return HttpResponse(json.dumps({
           'valid': form.is_valid(),
            'errors': {k: form.error_class.as_text(v) for k, v in form.errors.items()},
            'id': user['id'],
            'username': user['username'],
            'email': user['email'],
            'last_name': user['last_name'],
            'first_name': user['first_name']
        }))

    @method_decorator(login_required)
    def get(self, *args, **kwargs):
        user = auth.models.User.objects.get(pk=self.kwargs.get('id'))
        if self.request.is_ajax():
            return HttpResponse(json.dumps({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'last_name': user.last_name,
                'first_name': user.first_name
            }))
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
        messages.info(self.request, u'Teraz możesz się zalogować')
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
        return HttpResponse(json.dumps({'strength': rhyme.vote_strength}))
    return redirect(reverse('frontsite:index'))

def rhyme_store(request, id):
    if not models.RhymeProfiles.objects.filter(owner__id=request.user.profile.id, rhyme__id=id).count() > 0:
        store = models.RhymeProfiles()
        (store.owner, store.rhyme) = (request.user.profile, models.Rhyme.objects.get(pk=id))
        store.save()
    if request.is_ajax():
        return HttpResponse(json.dumps({'success': True}))
    return redirect(reverse('frontsite:stored'))

def rhyme_unstore(request, id):
    if models.RhymeProfiles.objects.filter(owner__id=request.user.profile.id, rhyme__id=id).count() > 0:
        store = models.RhymeProfiles.objects.get(owner__id=request.user.profile.id, rhyme__id=id)
        store.delete()
    if request.is_ajax():
        return HttpResponse(json.dumps({'success': True}))
    return redirect(reverse('frontsite:stored'))

def stored(request):
    return render(request, 'frontsite/stored.html', {
        'storedRhymes': request.user.profile.stored_rhymes.all().order_by('position_no')
    })

def random(request):
    rhyme, last = (None, None)
    last = models.Rhyme.objects.all().filter(public=True).order_by('-id')
    if last:
        while rhyme is None:
            try:
                rhyme = models.Rhyme.objects.get(pk=randint(1, last[0].id), public=True)
            except:
                pass
    return render(request, 'frontsite/random.html', {
        'rhyme': rhyme
    })

def most_popular(request):
    mostLiked = models.Rhyme.objects.all().annotate(vote_strength=Sum('votes__strength')).filter(public=True).order_by('-vote_strength')[:5]
    mostSaved = models.Rhyme.objects.all().annotate(saved_count=Count('profiles')).filter(saved_count__gt=0, public=True).order_by('-saved_count')[:6]
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