from django.contrib import auth
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(auth.models.User)