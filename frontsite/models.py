from django.contrib import auth
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(auth.models.User, related_name='profile')

class VoteUserProfile(models.Model):
    user_profile = models.ForeignKey(UserProfile, related_name='votes')
    author = models.ForeignKey(UserProfile, related_name='voted')
    date = models.DateTimeField(auto_now=True, blank=True)
    strength = models.PositiveSmallIntegerField(default=1, blank=True)

class Category(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now=True, blank=True)

# class Rhyme(models.Model):
#     pass
#
# class VoteRhyme(models.Model):
#     pass
#
# class SavedRhyme(models.Model):
#     pass
#
# class Comment(models.Model):
#     pass
#
# class VoteComment(models.Model):
#     pass