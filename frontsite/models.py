from django.contrib import auth
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(auth.models.User, related_name='profile')

class Avatar(models.Model):
    name = models.CharField(max_length=50)
    path = models.CharField(max_length=255)
    profile = models.OneToOneField(UserProfile, related_name='avatar')

class VoteUserProfile(models.Model):
    user_profile = models.ForeignKey(UserProfile, related_name='votes')
    author = models.ForeignKey(UserProfile, related_name='voted')
    date = models.DateTimeField(auto_now_add=True, blank=True)
    strength = models.PositiveSmallIntegerField(default=1, blank=True)

class Category(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True, blank=True)
    def __unicode__(self):
        return self.title

class Rhyme(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(UserProfile, related_name='created_rhymes')
    profiles = models.ManyToManyField(UserProfile, related_name='stored_rhymes')
    category = models.ForeignKey(Category, null=True, blank=True, related_name='rhymes')

class VoteRhyme(models.Model):
    rhyme = models.ForeignKey(Rhyme, related_name='votes')
    author = models.ForeignKey(UserProfile, related_name='rhyme_voted')
    data = models.DateTimeField(auto_now=True, blank=True)
    strength = models.PositiveSmallIntegerField(default=1, blank=True)

class Comment(models.Model):
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True, blank=True)
    rhyme = models.ForeignKey(Rhyme, related_name='comments')
    rhyme_author_saw = models.BooleanField(default=False)
    author = models.ForeignKey(UserProfile, related_name='commented_rhymes')
